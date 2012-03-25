from coderclash.engine.utils import fsm


class Player(object):
    """
    Available states:

        not_ready (str)
            Player (by virtue of existing in memory) is defaulted to the
            not_ready state. The are not eligible for game selection.

        ready (str)
            A Player may move into the ready state where they are eligible
            for game selection.

        in_game (str)
            Once a player joins a game, they are no longer eligible for
            game selection

    """

    def __init__(self, connection):
        self.connection = connection
        self.state = 'not_ready'
        self.game = None


    @fsm('ready', whence=['not_ready'])
    def ready(self):
        pass

    @fsm('not_ready')
    def not_ready(self):
        pass


    @fsm('in_game', whence=['ready'])
    def join(self, game):
        self.game = game

    @fsm('not_ready', whence=['in_game'])
    def leave(self):
        self.game.players.remove(self)
        self.game = None


    def get_state(self):
        return dict(
            state=self.state,
        )

    def game_state(self):
        if self.game:
            return self.game.get_state()
        return None

    def __unicode__(self):
        return '<Player {0}>'.format(self.state)