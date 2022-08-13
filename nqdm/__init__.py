"""NQDM progress bar
        - Compresses nested loops into a single loop
        - Can work with different types of data
        - Is implemented using TQDM"""
import tqdm
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


        Attributes
        -----------

        values : list

            List of iterable objects and single variables

        iterable : list

            List of indices ranging from 0 to # of total iterations - 1

        lengths : list

            Lengths of each argument passed into"""
    def __init__(self, *args, depth = 0, order = "first", enum = False, **kwargs):
        super().__init__(**kwargs)
        self.number = len(args)
        self.__set_depth__(depth)
        self.__set_order__(order)
        reverse_order = list(map(lambda kv : kv[1], sorted(zip(self.order, range(self.number)))))
        args = list(map(__process__, args, self.depth))
        lengths = list(map(len, args))
        self.lengths = [lengths[order_i] for order_i in reverse_order]
        total = 1
        for length in self.lengths:
            total *= length
        self.iterable = range(total)
        args = self.__values__(args)
        if enum:
            args = list(enumerate(args))
        self.values = args
    def v(self):
        return self.values
    def __iter__(self):
        mininterval = self.mininterval
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        min_start_t = self.start_t+self.delay
        time = self._time
        n_copy = self.n
        try:
            print("\n")
            for ind in self.iterable:
                yield self.values[ind]
                n_copy += 1
                if n_copy - last_print_n >= self.miniters:
                    cur_t = time()
                    dif_t = cur_t - last_print_t
                    if dif_t >= mininterval and cur_t >= min_start_t:
                        self.update(n_copy - last_print_n)
                        last_print_n = self.last_print_n
                        last_print_t = self.last_print_t
        finally:
            self.n = n_copy
            self.close()
    def __set_depth__(self, depth):
        if isinstance(depth, list):
            if len(depth) != self.number:
                depth = 0
        if isinstance(depth, int):
            depth = [depth]*self.number
        self.depth = depth
    def __set_order__(self, order):
        if order == "first":
            order = list(range(self.number))
        if order == "last":
            order = list(range(self.number-1, -1, -1))
        order = self.__check_order__(order)
        self.order = order
    def __check_order__(self, order):
        if isinstance(order, list):
            mismatch = len(order) != self.number
            failed = any((i not in order for i in range(self.number)))
            if mismatch or failed:
                order = list(range(self.number))
        return order
    def __offset__(self, point):
        indices = []
        for length in self.lengths:
            indices.append(point % length)
            point //= length
        indices = [indices[order_i] for order_i in self.order]
        return indices
    def __values__(self, args):
        get_elem = lambda point : [arg[offset] for arg, offset in zip(args, self.__offset__(point))]
        args = list(map(get_elem, self.iterable))
        if self.number == 0:
            args = []
        if self.number == 1:
            args = list(map(lambda x : x[0], args))
        return args
