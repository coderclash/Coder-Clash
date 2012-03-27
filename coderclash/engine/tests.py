import unittest

from coderclash.engine.utils import fsm
from coderclash.engine.game import Challenge, Rule, Goal


class Car(object):
    state = 'off'

    @fsm('on', whence=['off'])
    def turn_on(self):
        pass

    @fsm('off')
    def turn_off(self):
        pass


class FMSTest(unittest.TestCase):

    def test_simple(self):
        car = Car()
        self.assertEquals('off', car.state)

        car.turn_on()
        self.assertEquals('on', car.state)

        # already on, raise error
        self.assertRaises(car.turn_on)
        self.assertEquals('on', car.state)

        car.turn_off()
        car.turn_off() # can do it twice!
        self.assertEquals('off', car.state)

    def test_silent(self):
        car = Car()
        self.assertEquals('off', car.state)

        car.turn_on(silent=True)
        self.assertEquals('on', car.state)

        # silent fail
        car.turn_on(silent=True)
        self.assertEquals('on', car.state)

        car.turn_off(silent=True)
        car.turn_off(silent=True) # can do it twice!
        self.assertEquals('off', car.state)


class BasicGameTest(unittest.TestCase):
    def setUp(self):
        goal = Goal(target='1,2,3,4,5,6,7,8,9,10')
        rule = Rule(cannot_contains=['range', '1,2,3,4,5,6,7,8,9,10'])
        self.challenge = Challenge(goal=goal, rules=[rule])
        self.code = """l,c=[],1
while c<11:l+=[str(c)];c+=1
print ','.join(l)"""

    def test_load(self):
        self.assertEquals(
            {'rules': [{'must_contains': [], 'cannot_contains': ['range', '1,2,3,4,5,6,7,8,9,10']}], 'goal': {'target': '1,2,3,4,5,6,7,8,9,10'}, 'time': 60},
            self.challenge.dict
        )

    def test_tick(self):
        self.assertEquals(60, self.challenge.dict['time'])
        self.challenge.tick()
        self.assertEquals(59, self.challenge.dict['time'])

    def test_failed_move(self):
        code = '",".join([x for x in range(1, 10)'
        score, errors = self.challenge.move(code)

        print score, errors


