

class Game(object):
    """
    A game may have many players (2+).

    A game will have a goal and rules.
    """

    def __init__(self, players):
        self.players = set(players)

        for player in self.players:
            player.join(self)

        self.state = 'pregame'

    def tick(self):
        """
        Called every second by the loop.
        """

        for player in self.players:
            pass

    def close(self):
        for player in self.players:
            player.leave()


    def get_state(self):
        # return a regular dictionary with the games's state
        return dict(
            state=self.state,
            players=[
                p.get_state() for p in self.players
            ]
        )

    def __unicode__(self):
        return u'{0} players in game.'.format(len(self.players))