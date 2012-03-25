import unittest

from coderclash.engine.utils import fsm


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

        # already on
        self.assertRaises(car.turn_on)
        self.assertEquals('on', car.state)

        car.turn_off()
        car.turn_off() # can do it twice!
        self.assertEquals('off', car.state)
