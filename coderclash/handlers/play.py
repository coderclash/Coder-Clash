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
        """
        Dispatch all the ticks and handle player state, etc...
        """
        self.print_info()

        self.tick_games()
        self.start_games()

        self.update_players()

    def print_info(self):
        print datetime.now()
        print ' ', 'players', [unicode(p) for p in players]
        print ' ', 'games', [unicode(g) for g in games]

    def on_message(self, message):
        pass


    ##################
    ## HANDLE GAMES ##
    ##################

    def tick_games(self):
        """
        Ticks each live game, or, closes the game if fewer than
        2 players remain.
        """
        for game in set(games):
            if len(game.players) > 1:
                game.tick()
            else:
                game.close()
                games.remove(game)

    def start_games(self):
        """
        Decrement the countdown, if 0, start the match & reset countdown.
        """
        global countdown

        if countdown is 0:
            players_to_game = set(
                [p for p in players if p.state == 'ready']
            )

            # might be wise to collect groups of... say 2 or 4 instead
            # of all players who are ready
            if len(players_to_game) > 1:
                games.add(Game(players_to_game))
                message = 'Game starting!'
            else:
                message = 'Not enough players to start game.'

            # reset
            countdown = int(COUNTDOWN)
        else:
            message = 'Next game starts in {0} seconds.'.format(countdown)
            countdown -= 1

        # send info to players...
        for player in players:
            if player.state == 'ready':
                player.socket.send(message)


    ####################
    ## HANDLE PLAYERS ##
    ####################

    def on_open(self, message):
        """
        Add a player to the pool.
        """
        player = Player(socket=self)
        players.add(player)

    def on_close(self):
        """
        Remove a player from the pool.
        """
        player = self.get_current_player()

        if player.state == 'in_game':
            player.leave()

        players.remove(player)

    def get_current_player(self):
        """
        Locate and return the current player.
        """
        for player in players:
            if player.socket == self:
                return player

    def give_state(self, player):
        player.socket.emit(
            'state',
            player=player.get_state(),
            game=player.game_state()
        )

    def update_players(self):
        """
        Give each connected player their state.
        """
        for player in players:
            self.give_state(player)

    @tornadio2.event
    def command(self, command):
        """
        Allow the client to send commands. Only permit certain
        commands, block others. Try to run the command without
        raising any errors (silently).
        """
        player = self.get_current_player()

        commands = ['ready', 'not_ready', 'leave']
        if command in commands:
            getattr(player, command)(silent=True)
