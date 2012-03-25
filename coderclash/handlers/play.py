import tornadio2
import tornado.ioloop
from datetime import datetime

from coderclash.handlers.base import BaseHandler

from coderclash.engine import Player, Game


class Play(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.write(self.render('play/play.html', user=user))


callback = None

players = set()
games = set()

COUNTDOWN = 10
countdown = int(COUNTDOWN)


class PlaySocket(tornadio2.SocketConnection):
    """
    This is the interface for speaking to the client through websockets. Game
    and Player state are constantly given to the client. The client sends
    commands that update both their and the games state.
    """
    def __init__(self, *args, **kwargs):
        super(PlaySocket, self).__init__(*args, **kwargs)

        global callback
        if callback is None:
            callback = tornado.ioloop.PeriodicCallback(self.tick, 1000)
            callback.start()

    def tick(self):

        print datetime.now()
        print ' ', 'players', [unicode(p) for p in players]
        print ' ', 'games', [unicode(g) for g in games]

        # tick or remove current games
        for game in games:
            if len(game.players) > 1:
                game.tick()
            else:
                game.close()
                games.remove(game)

        self.start_matches()

        for player in players:
            player.connection.emit('state',
                player=player.get_state(),
                game=player.game_state()
            )

    def on_open(self, message):
        player = Player(connection=self)
        players.add(player)

    def get_connected_player(self):
        for player in players:
            if player.connection == self:
                return player

    def on_close(self):
        player = self.get_connected_player()

        if player.state == 'in_game':
            player.leave()

        players.remove(player)

    def on_message(self, message):
        pass


    def start_matches(self):
        """
        Decrement the countdown, if 0, start the match & reset countdown.
        """
        global countdown

        if countdown == 0:
            players_to_game = set([p for p in players if p.state == 'ready'])

            # might be wise to collect groups of... say 2 or 4 instead
            # of all players who are ready
            if len(players_to_game) > 1:
                games.add(Game(players_to_game))

            countdown = int(COUNTDOWN)
        else:
            countdown -= 1

        for player in players:
            if player.state == 'ready':
                player.connection.send(
                    'Match starts in {0} seconds.'.format(countdown)
                )

    @tornadio2.event
    def command(self, command):  # target state...
        player = self.get_connected_player()

        commands = ['ready', 'not_ready', 'leave']
        if command in commands:
            getattr(player, command)(silent=True)
