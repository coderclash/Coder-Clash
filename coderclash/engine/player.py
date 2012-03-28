from coderclash.engine.utils import fsm, make_name


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

    state = 'not_ready'
    game = None
    best = None

    def __init__(self, socket):
        self.socket = socket
        self.name = make_name()


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
        self.socket.give_state(self)


    def get_state(self):
        if self.best:
            best = dict(
                score=self.best[0],
                results=self.best[1],
                errors=self.best[2]
            )
        return dict(
            state=self.state,
            best=best if self.best else None
        )

    def game_state(self):
        if self.game:
            return self.game.get_state()
        return None

    def __unicode__(self):
        return '<{0} {1}>'.format(self.name, self.state)