"""NQDM progress bar
        - Compresses nested loops into a single loop
        - Can work with different types of data
        - Is implemented using TQDM"""
import tqdm
def __typeof__(arg):
    are = lambda feature : isinstance(arg,feature)
    has = lambda feature : hasattr(type(arg),feature)
    got = lambda feature : has('__dict__') and feature in type(arg).__dict__
    is_constant = got("as_integer_ratio")
    is_hashable = got("fromkeys") or got("items")
    is_iterable = got("sort") or are(range) or are(str)
    unique = int(is_constant + is_hashable + is_iterable) == 1
    if unique and is_hashable:
        result = "dict"
    elif unique and is_constant:
        result = "int"
    elif unique or has("__len__") or has("__iter__"):
        result = "list"
    else:
        result = "any"
    return result
def __apply__(arg, kind = "any"):
    typeof = __typeof__(arg)
    if typeof == "dict":
        if kind == "flat":
            result = list(dict(arg).values())
        elif kind == "iter":
            result = [{k : v} for k, v in dict(arg).items()]
        else:
            result = dict(arg)
    elif typeof == "int":
        if kind == "flat":
            result = []
        elif kind == "iter":
            result = list(range(arg))
        else:
            result = int(arg)
    elif typeof == "list":
        result = list(arg)
    else:
        if kind == "flat":
            result = []
        else:
            result = arg
    return result
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

        disable : bool = False

            Progress bar is not displayed if set to True


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
        get_elem = lambda point : [arg[offset] for arg, offset in zip(args, self.__offset__(point))]
        args = list(map(get_elem, self.iterable))
        if self.number == 0:
            args = []
        if self.number == 1:
            args = list(map(lambda x : x[0], args))
        if enum:
            args = list(enumerate(args))
        self.values = args
    def __iter__(self):
        if self.disable:
            yield self.values
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
        if isinstance(order, list):
            if len(order) != self.number:
                order = "first"
            if any((i not in order for i in range(self.number))):
                order = "first"
        if order == "first":
            order = list(range(self.number))
        if order == "last":
            order = list(range(self.number-1, -1, -1))
        self.order = order
    def __offset__(self, point):
        indices = []
        for length in self.lengths:
            indices.append(point % length)
            point //= length
        indices = [indices[order_i] for order_i in self.order]
        return indices
