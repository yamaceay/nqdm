import numpy as np
import pandas as pd
import tqdm 

class nqdm(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.total = self.__limit__(*args)
        self.iterable = range(self.total)
        self.delay = 0
        self.arguments = args
    def __iter__(self):
        iterable = self.iterable
        if self.disable:
            print("\n")
            for ind in iterable:
                obj = self.__ndrate__(ind, *self.arguments)
                yield obj
            return
        mininterval = self.mininterval
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        min_start_t = self.start_t+self.delay
        n = self.n
        time = self._time
        try:
            print("\n")
            for ind in iterable:
                obj = self.__ndrate__(ind, *self.arguments)
                yield obj
                n += 1
                if n - last_print_n >= self.miniters:
                    cur_t = time()
                    dt = cur_t - last_print_t
                    if dt >= mininterval and cur_t >= min_start_t:
                        self.update(n - last_print_n)
                        last_print_n = self.last_print_n
                        last_print_t = self.last_print_t
        finally:
            self.n = n
            self.close()
    def __transformate__(self):
        return {
            "<class 'pandas.core.series.Series'>": (lambda data: (list(data.index), list(data.values))),
            "<class 'numpy.ndarray'>": (lambda data: (None, data.tolist())),
            "<class 'str'>": (lambda data: (None, list(data))),
            "<class 'dict'>": (lambda data: (list(data.keys()), list(data.values()))),
            "<class 'list'>": (lambda data: (None, list(data))),
            "<class 'int'>": (lambda data: (None, data)),
            "<class 'float'>": (lambda data: (None, int(data)))
        }
    def __limit__(self, *args):
        product = 1
        for i in range(len(args)):
            arg = args[i]
            is_iterable = hasattr(arg, "__len__")
            leng = len(arg) if is_iterable else int(arg)
            product *= leng
        return product
    def __ndrate__(self, point, *args):
        informations = []
        for i in range(len(args)):
            arg = args[i]
            typ = type(arg)
            tr_func = self.__transformate__()[str(typ)]
            keys, vals = tr_func(arg)
            is_key = keys is not None
            is_iterable = hasattr(vals, "__len__")
            leng = len(vals) if is_iterable else vals
            offset = point%leng
            key = keys[offset] if is_key else None
            val = vals[offset] if is_iterable else None
            pair = () if key is None and val is None else (key, val)
            informations.append((offset, pair))
            point = point//leng
        return informations