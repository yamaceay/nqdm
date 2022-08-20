"""NQDM progress bar
        - Compresses nested loops into a single loop
        - Can work with different types of data
        - Is implemented using TQDM"""
import tqdm
import numpy
import plotly_express
def __has__(arg, feature):
    return hasattr(type(arg),feature)
def __got__(arg, feature):
    return __has__(arg, '__dict__') and feature in type(arg).__dict__
def __typeof_calc__(arg):
    is_constant = __got__(arg, "as_integer_ratio")
    is_hashable = __got__(arg, "fromkeys") or __got__(arg, "items")
    is_iterable = __got__(arg, "sort") or isinstance(arg, (range, str))
    is_countable = __has__(arg, "__len__") or __has__(arg, "__iter__")
    return [is_hashable, is_constant, is_iterable, is_countable]
def __typeof_result__(types):
    if types[0]:
        result = "dict"
    elif types[1]:
        result = "int"
    elif types[2]:
        result = "list"
    return result
def __typeof__(arg):
    types = __typeof_calc__(arg)
    result = "list" if types[3] else "any"
    if sum(types[:3]) == 1:
        result = __typeof_result__(types)
    return result
def __handle_dict__(kind, arg):
    if kind == "flat":
        arg = list(dict(arg).values())
    elif kind == "iter":
        arg = [{k : v} for k, v in dict(arg).items()]
    else:
        arg = dict(arg)
    return arg
def __handle_int__(kind, arg):
    if kind == "flat":
        arg = []
    elif kind == "iter":
        arg = list(range(arg))
    else:
        arg = int(arg)
    return arg
def __apply__(arg, kind = "any"):
    typeof = __typeof__(arg)
    if typeof == "dict":
        arg = __handle_dict__(kind, arg)
    elif typeof == "int":
        arg = __handle_int__(kind, arg)
    elif typeof == "list":
        arg = list(arg)
    elif kind == "flat":
        arg = []
    return arg
def __process__(arg, depth):
    arg = __apply__(arg)
    if __typeof__(arg) in ["list", "dict"] and depth >= 1:
        arg = __flatten__(arg, depth)
    arg = __apply__(arg, 'iter')
    return arg
def __flatten__(arg, depth):
    if depth < 1:
        return arg
    arg = __apply__(arg, 'flat')
    args = []
    for arg_i in arg:
        arg_i = __flatten__(arg_i, depth-1)
        if __typeof__(arg_i) not in ["list", "dict"]:
            args.append(arg_i)
        else:
            args.extend(__apply__(arg_i, 'iter'))
    return args
class nqdm(tqdm.tqdm):
    """NQDM progress bar
        - Compresses nested loops into a single loop
        - Can work with different types of data
        - Is implemented using TQDM

        Arguments
        ----------

        args : list

            List of positional arguments to be iterated

        depth : int | list = 0

            How many dimensions deep it will be iterated

        order : str | list = "first"

            Order defining the hierarchy of nested loops

        enum : bool = False

            Whether data is enumerated or not

        maxiter : int = 0

            The number of iterated variables (all if set to 0)

        random : bool = False

            Whether tuples are yielded in random order or not

        Methods
        -----------

        values() -> list

            List of iterable objects and single variables

        shape() -> list

            Lengths of each iterable object

        history() -> list

            Number of iterations over seconds

        plot_history() -> None

            Plots the history
        """
    def __init__(self, *args, depth = 0, order = "first", enum = False, random = False, maxiter = 0, **kwargs):
        super().__init__(**kwargs)
        self._number = len(args)
        self.__set_depth__(depth)
        self.__set_order__(order)
        reverse_order = list(map(lambda kv : kv[1], sorted(zip(self._order, range(self._number)))))
        args = list(map(__process__, args, self._depth))
        lengths = list(map(len, args))
        self._lengths = [lengths[order_i] for order_i in reverse_order]
        self.total = 1
        for length in self._lengths:
            self.total *= length
        self._iterable = range(self.total)
        self.maxiter = min(maxiter, self.total) if maxiter > 0 else self.total
        args = self.__values__(args)
        if enum:
            args = list(enumerate(args))
        self._values = args
        self._random = random
        self._history = dict()
    def values(self):
        return self._values
    def shape(self):
        return self._lengths
    def history(self, second=False):
        times = list(self._history.keys())
        freqs = list(self._history.values())
        if len(times):
            times = [t - times[0] for t in times]
            if second:
                int_times = [int(t) for t in times]
                new_freqs = {i: 0 for i in range(int_times[0], int_times[len(int_times) - 1] + 1)}
                for int_t in int_times:
                    for t, f in zip(times, freqs):
                        if int(t) == int_t:
                            new_freqs[int_t] += f
                times = list(sorted(new_freqs))
                freqs = [new_freqs[t] for t in times]
        return times, freqs
    def plot_history(self, second=False):
        timeline, history = self.history(second=second)
        plot = plotly_express.line(
            x=timeline,
            y=history,
            title="Benchmark",
            labels={"x": "# Seconds", "y": "# Iterations"}
        )
        plot.show()
    def __getitem__(self, subscript):
        if isinstance(subscript, slice):
            return self.__getslice__(subscript)
        else:
            return self._values[subscript]
    def __getslice__(self, subscript):
        start = subscript.start
        stop = subscript.stop
        step = subscript.step
        if start is None:
            start = 0
        if stop is None:
            stop = self.__len__()
        if step is None:
            step = 1
        return nqdm(
            self._values[start:stop:step], 
            random=self._random,
            desc=self.desc,
            leave=self.leave,
            colour=self.colour
        )
    def __len__(self):
        return self.total
    def __iter__(self):
        mininterval = self.mininterval
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        min_start_t = self.start_t+self.delay
        time = self._time
        n_copy = self.n
        try:
            print("\n")
            iterable = self._iterable
            if self._random:
                iterable = numpy.random.permutation(iterable)
            for i in range(self.maxiter):
                ind = iterable[i]
                yield self._values[ind]
                n_copy += 1
                n_left = n_copy - last_print_n
                if n_left >= self.miniters:
                    cur_t = time()
                    dif_t = cur_t - last_print_t
                    if dif_t >= mininterval and cur_t >= min_start_t:
                        self.update(n_left)  
                        last_print_n = self.last_print_n
                        last_print_t = self.last_print_t
        finally:
            self.n = n_copy
            self.close()
    def update(self, n):
        super().update(n)
        self._history.update({self._time(): n})
    def __set_depth__(self, depth):
        if isinstance(depth, list):
            if len(depth) != self._number:
                depth = 0
        if isinstance(depth, int):
            depth = [depth]*self._number
        self._depth = depth
    def __set_order__(self, order):
        if order == "first":
            order = list(range(self._number))
        if order == "last":
            order = list(range(self._number-1, -1, -1))
        order = self.__check_order__(order)
        self._order = order
    def __check_order__(self, order):
        if isinstance(order, list):
            mismatch = len(order) != self._number
            failed = any((i not in order for i in range(self._number)))
            if mismatch or failed:
                order = list(range(self._number))
        return order
    def __offset__(self, point):
        indices = []
        for length in self._lengths:
            indices.append(point % length)
            point //= length
        indices = [indices[order_i] for order_i in self._order]
        return indices
    def __values__(self, args):
        get_elem = lambda point : [arg[offset] for arg, offset in zip(args, self.__offset__(point))]
        args = list(map(get_elem, self._iterable))
        if self._number == 0:
            args = []
        if self._number == 1:
            args = list(map(lambda x : x[0], args))
        return args
