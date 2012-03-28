
def fsm(target, whence='*', attr='state'):
    """
    `target` -> (str): REQUIRED
        should be the target state.

    `whence` -> (list): '*'
        should be a *list* of states that you can change from.

    `attr` -> (str): 'state'
        is the that of the attribute that represents state.


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

        car.turn_off()              # raise Exception
        car.turn_off(silent=True)   # fails silently
        # state is still 'off'

        car.turn_on()
        # state is 'on

    """

    def dec(method):
        def inner(self, *args, **kwargs):
            silent = kwargs.pop('silent', False)

            # check that whence == curent state
            if whence == '*':
                pass
            elif getattr(self, attr) in whence:
                pass
            else:
                if not silent:
                    raise Exception('You shall not pass!')  #LOTR
                else:
                    return None

            result = method(self, *args, **kwargs)
            setattr(self, attr, target) # set state to target

            return result
        return inner

    return dec


adjectives = ['agreeable', 'amused', 'brave', 'calm', 'charming', 'cheerful', 'comfortable', 'cooperative', 'courageous', 'delightful', 'determined', 'eager', 'elated', 'enchanting', 'encouraging', 'energetic', 'enthusiastic', 'excited', 'exuberant', 'fair', 'faithful', 'fantastic', 'fine', 'friendly', 'funny', 'gentle', 'glorious', 'good', 'happy', 'healthy', 'helpful', 'hilarious', 'jolly', 'joyous', 'kind', 'lively', 'lovely', 'lucky', 'nice', 'obedient', 'perfect', 'pleasant', 'proud', 'relieved', 'silly', 'smiling', 'splendid', 'successful', 'thankful', 'thoughtful', 'victorious', 'vivacious', 'witty', 'wonderful', 'zealous', 'zany']
animals = ['aardvark', 'albatross', 'alligator', 'alpaca', 'bison', 'ant', 'anteater', 'antelope', 'ape', 'armadillo', 'donkey', 'baboon', 'badger', 'barracuda', 'bat', 'bear', 'beaver', 'bee', 'bison', 'boar', 'buffalo', 'bush baby', 'butterfly', 'camel', 'caribou', 'cat', 'caterpillar', 'cattle', 'chamois', 'cheetah', 'chicken', 'chimpanzee', 'chinchilla', 'clam', 'cobra', 'cockroach', 'cod', 'cormorant', 'coyote', 'crab', 'crane', 'crocodile', 'crow', 'deer', 'dinosaur', 'dog', 'dogfish', 'dolphin', 'donkey', 'dove', 'dragonfly', 'duck', 'dugong', 'eagle', 'echidna', 'eel', 'eland', 'elephant', 'elephant seal', 'elk', 'emu', 'falcon', 'ferret', 'finch', 'fish', 'fly', 'fox', 'frog', 'gaur', 'gazelle', 'gerbil', 'giant panda', 'giraffe', 'gnat', 'gnu', 'goat', 'goose', 'gopher', 'gorilla', 'grasshopper', 'grouse', 'guanaco', 'guinea fowl', 'guinea pig', 'gull', 'hamster', 'hare', 'hawk', 'hedgehog', 'heron', 'hippopotamus', 'hornet', 'horse', 'human', 'hummingbird', 'hyena', 'iguana', 'jackal', 'jaguar', 'jay, blue', 'jellyfish', 'kangaroo', 'koala', 'komodo dragon', 'kouprey', 'kudu', 'lark', 'lemur', 'leopard', 'lion', 'llama', 'lobster', 'locust', 'loris', 'louse', 'lyrebird', 'magpie', 'mallard', 'manatee', 'meerkat', 'mink', 'mole', 'monkey', 'moose', 'mouse', 'mosquito', 'mule', 'narwhal', 'newt', 'nightingale', 'okapi', 'opossum', 'oryx', 'ostrich', 'otter', 'owl', 'ox', 'oyster', 'panda - see bear', 'panther', 'parrot', 'partridge', 'peafowl', 'pelican', 'penguin', 'pig', 'pigeon', 'platypus', 'pony', 'porcupine', 'porpoise', 'prairie dog', 'quelea', 'rabbit', 'raccoon', 'rail', 'ram', 'rat', 'raven', 'red deer', 'red panda', 'reindeer', 'rhinoceros', 'rook', 'salamander', 'sand dollar', 'sea lion', 'sea urchin', 'seahorse', 'seal', 'seastar', 'serval', 'shark', 'sheep', 'shrew', 'skunk', 'snail', 'snake', 'spider', 'squid', 'squirrel', 'stinkbug', 'swallow', 'swan', 'tapir', 'tarsier', 'termite', 'tiger', 'toad', 'trout', 'turkey', 'turtle', 'wallaby', 'walrus', 'wasp', 'weasel', 'whale', 'wolf', 'wombat', 'woodpecker', 'worm', 'wren', 'yak', 'zebra']

def make_name():
    import random
    adj = random.choice(adjectives)
    ani = random.choice(animals)
    return '{0} {1}'.format(adj.capitalize(), ani.capitalize())