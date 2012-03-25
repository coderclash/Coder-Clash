
def fsm(target, whence='*', attr='state'):
    """
    `target` should be the target state
    `whence` should be a list of states that you can change from.

    Example:

        class Car(object):
            state = 'off'

            @fsm('on', whence=['off'])
            def turn_on(self):
                pass

            @fsm('off', whence=['on'])
            def turn_off(self):
                pass

        car = Car()
        # state is 'off'

        car.turn_off()  # raise Exception
        car.turn_off(silent=True)  # fails silently
        # state is still 'off'

        car.turn_on()
        # state is 'on

    """

    def dec(method):
        def inner(self, *args, **kwargs):
            silent = kwargs.pop('silent', False)

            # check that whence
            if whence == '*':
                pass
            elif getattr(self, attr) in whence:
                pass
            else:
                if not silent:
                    raise Exception('You shall not pass!')
                else:
                    return None

            result = method(self, *args, **kwargs)
            setattr(self, attr, target) # set state to target

            return result
        return inner

    return dec

