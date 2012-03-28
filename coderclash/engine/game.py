class Goal(object):
    """
    A generic code golf goal.
    """
    def __init__(self, target):
        self.target = target

    def evaluate(self, code):
        """
        Run this code.
        """
        import requests
        import simplejson

        url = 'http://localhost:5000/v1/python/2.7.1'
        data = simplejson.dumps({'code': code})
        headers = {'content-type': 'application/json'}
        
        response = requests.post(
            url=url,
            data=data,
            headers=headers
        )
        data = simplejson.loads(response.content)

        return data  # or exceptions...

    def score(self, code):
        """
        Returns a tuple:
            (score 0-1000, results, error list) 

        Perfect score would be a length of 0.

        A score of 1 would be a len > 400.
        """
        code = code.strip()
        data = self.evaluate(code)

        results = data['results'].strip()
        if not self.target in results:
            return 0, results, data['errors']

        length = len(code)
        if length >= 400:
            return 1, results, data['errors']

        return 1000 - ((length * 10) / 4), results, data['errors']

    @property
    def dict(self):
        return dict(
            target=self.target
        )


class Rule(object):
    """
    A generic rule base class.
    """
    def __init__(self, must_contains=[], cannot_contains=[]):
        self.must_contains = must_contains
        self.cannot_contains = cannot_contains

    def check(self, code):
        """
        Given an input, check that it passes this rule.

        Returns a list of errors, which, if empty, means success.
        """
        errors = []

        for must_contain in self.must_contains:
            if must_contain not in code:
                errors.append(
                    'Must contain "{0}".'.format(must_contain)
                )

        for cannot_contain in self.cannot_contains:
            if cannot_contain in code:
                errors.append(
                    'Cannot contain "{0}".'.format(cannot_contain)
                )

        return errors

    @property
    def dict(self):
        return dict(
            must_contains=self.must_contains,
            cannot_contains=self.cannot_contains
        )


class Challenge(object):
    """
    A set of rules and a goal.
    """
    def __init__(self, goal, rules=[], time=60*10):
        self.goal = goal
        self.rules = rules
        self.time = time

    def tick(self):
        if self.time > 0:
            self.time -= 1

    def move(self, code):
        """
        Return a tuple: (score, errors)
        """
        errors = []

        for rule in self.rules:
            errors += rule.check(code)

        score, results, _errors = self.goal.score(code)

        errors += _errors

        return score, results, errors

    @property
    def dict(self):
        return dict(
            time=self.time,
            rules=[rule.dict for rule in self.rules],
            goal=self.goal.dict
        )



class Game(object):
    """
    A game may have many players (2+).

    A game will a current Challenge, which is a set of goals
    and rules.
    """

    def __init__(self, players, challenge=None):
        self.players = set(players)

        for player in self.players:
            player.join(self)

        # TODO: should not hardcode the challenge
        goal = Goal(target='1,2,3,4,5,6,7,8,9,10')
        rule = Rule(cannot_contains=['range', '1,2,3,4,5,6,7,8,9,10'])
        self.challenge = Challenge(goal=goal, rules=[rule])

        self.state = 'pregame'

    def tick(self):
        """
        Called every second by the loop.
        """
        self.challenge.tick()
        for player in set(self.players):
            pass

    def move(self, player, code):
        if self.challenge:
            score, results, errors = self.challenge.move(code)

            if score and not len(errors):
                if player.best:
                    old_score = player.best[0]
                    if score > old_score:
                        player.best = score, results, errors
                else:
                    player.best = score, results, errors

            return score, results, errors

        return 0, '', ['No challenge in progress.']

    def scores(self):
        """
        Returns a list of dicts with player names and their scores.
        """
        scores = []

        for player in self.players:
            score = 0

            if player.best:
                score = player.best[0]

            scores.append(dict(name=player.name, score=score))

        return scores


    def close(self):
        for player in set(self.players):
            player.leave()


    def get_state(self):
        # return a regular dictionary with the games's state
        return dict(
            state=self.state,
            players=[
                p.get_state() for p in self.players
            ],
            challenge=self.challenge.dict if self.challenge else None,
            scores=self.scores()
        )

    def __unicode__(self):
        return u'{0} players in game.'.format(len(self.players))