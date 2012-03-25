
def fsm(target, whence='*', attr='state'):
    """
    Ensure the states are good.

    `whence` should be a list of states that you can change from.

    `target` should be the target state
    """

    def function(method):
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
            setattr(self, attr, target) # set target
            return result
        return inner

    return function
