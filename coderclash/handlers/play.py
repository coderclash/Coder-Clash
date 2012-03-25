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
    def __init__(self, *args, **kwargs):
        super(PlaySocket, self).__init__(*args, **kwargs)

        global callback
        if callback is None:
            callback = tornado.ioloop.PeriodicCallback(self.tick, 1000)
            callback.start()

    def tick(self):
        global countdown

        print 'players', [unicode(p) for p in players]
        print 'games', [unicode(g) for g in games]

        for player in players:
            if player.state == 'ready':
                player.connection.send(
                    'Match starts in {0} seconds.'.format(countdown)
                )

        for game in games:
            if len(game.players) > 1:
                game.tick()
            else:
                game.close()
                games.remove(game)

        if countdown == 0:
            self.start_matches()
            countdown = int(COUNTDOWN)
        else:
            countdown -= 1

        # TODO: send state to client


    def on_open(self, message):
        player = Player(connection=self)
        players.add(player)

    def get_player(self):
        for player in players:
            if player.connection == self:
                return player

    def on_close(self):
        player = self.get_player()

        if player.state == 'in_game':
            player.leave()

        players.remove(player)

    def on_message(self, message):
        pass


    def start_matches(self):
        players_to_game = set([p for p in players if p.state == 'ready'])

        # might be wise to collect groups of... say 2 or 4 instead
        # of all players who are ready
        if len(players_to_game) > 1:
            games.add(Game(players_to_game))

    @tornadio2.event
    def player_state(self, state):
        player = self.get_player()

        if state == 'ready':
            player.ready()
