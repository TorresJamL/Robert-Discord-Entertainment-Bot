from collections.abc import MutableMapping 
import random

class extras:
    class WeightedDict(MutableMapping): 
        """ Specialized Dictionary for weighted chances. 
            dict values must be type INT
        """
        def __init__(self, *args, **kwargs):
            for arg in args[0]:
                if type(arg[1]) != int:
                    raise TypeError(f"Values of WeightedDict must be type 'int', {arg[1]} is of type {type(arg[1])}")
            self.store = dict()
            self.update(dict(*args, **kwargs))  # use the free update to set keys

        def __getitem__(self, key):
            return self.store[self._keytransform(key)]

        def __setitem__(self, key, value):
            self.store[self._keytransform(key)] = value

        def __delitem__(self, key):
            del self.store[self._keytransform(key)]

        def __iter__(self):
            return iter(self.store)
        
        def __len__(self):
            return len(self.store)

        def _keytransform(self, key):
            return key
        
        def random(self):
            """
            Returns a random key based on the weights of the keys. So theoretically, 
            having a weightedDict of {a : 10, b : 20, c: 30} would mean your chances of getting 'a' as an output is 
            10 / 60, 'b' is 20 / 60, and 'c' is 30 / 60. 60 being the total of all weights.

            Examples:\n
                wDict = WeightedDict([("a", 1), ("b", 3), ("c", 6)]) // {"a" : 1, "b" : 3, "c" : 6}
                for _ in range(10):
                    print(wDict.random())     

                Possible Outputs: 
                    b c c c b b b c c b
                    c b a a b a c c c b
                    c b b b b a c a b c
            """
            cumulative_weights = []
            total_weight = 0
            for weight in list(self.values()):
                total_weight += weight
                cumulative_weights.append(total_weight)

            rand_num = random.randint(0, total_weight)

            for i, cumulative_weight in enumerate(cumulative_weights):
                if rand_num <= cumulative_weight:
                    return list(self.keys())[i]
            return
        
        def __str__(self):
            return self.store.__str__()
        
        def __repr__(self):
            return super().__repr__()
        
        def tst(self):
            print(self.store)
