
def fsm(target, whence='*', attr='state'):
    """
    Ensure the states are good.

    `whence` should be a list of states that you can change from.

    `target` should be the target state
    """

    def function(method):
        def inner(self, *args, **kwargs):
            # check that whence
            if whence == '*':
                pass
            elif getattr(self, attr) in whence:
                pass
            else:
                raise Exception('You shall not pass!')

            result = method(self, *args, **kwargs)
            setattr(self, attr, target) # set target
            return result
        return inner

    return function
