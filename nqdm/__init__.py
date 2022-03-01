import tqdm 

class nqdm(tqdm.tqdm):
    """
    NQDM progress bar
     - Compresses nested loops into a single loop 
     - Can work with different types of data
     - Is implemented using TQDM
    Attributes
    ----------

    iterable : range
        
        Range object storing indices ranging from 0 to total-1
    
    values : list
        
        List of iterable objects and single variables
    
    depth : int | list = 0
        
        How many dimensions deep it will be iterated 
    
    order : str | list = "first"
        
        Order defining the hierarchy of nested loops

    enum : bool = False

        Whether data is enumerated or not

    disable : bool = False

        Progress bar is not displayed if set to True

    
    """

    def __init__(self, *args, depth = 0, order = "first", enum = False, disable = False, **kwargs):
        super().__init__(disable = disable, **kwargs)

        self.number = len(args)
        self.__set_depth__(depth)
        self.__set_order__(order)

        self.enum = enum
        self.delay = 0
        self.disable = disable

        args = list(map(self.__process__, args, self.depth))
        
        lens = list(map(len, args))
        self.lens = [lens[order_i] for order_i in self.reverse_order]
        total = 1
        for ln in self.lens:
            total *= ln
        self.iterable = range(total) 

        args = list(map(
            lambda point : [arg[offset] 
            for arg, offset in zip(args, self.__offset__(point))
            ], self.iterable))

        if self.number == 0: args = []
        if self.number == 1: args = list(map(lambda x : x[0], args))
        if enum: args = list(enumerate(args))
        self.values = args

    def __iter__(self):
        if self.disable: yield self.values
        mininterval = self.mininterval
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        min_start_t = self.start_t+self.delay
        n = self.n
        time = self._time
        
        try:
            print("\n")
            for ind in self.iterable:
                yield self.values[ind]
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

    def __set_depth__(self, depth):
        # Depth is set
        if type(depth) == list:
            if len(depth) != self.number:
                depth = 0

        if type(depth) == int:
            depth = [depth]*self.number

        self.depth = depth

    def __set_order__(self, order):
        # Order is set
        if type(order) == list:
            if len(order) != self.number:
                order = "first"
            if any([i not in order for i in range(self.number)]):
                order = "first"

        if order == "first":
            order = list(range(self.number))
        if order == "last":
            order = list(range(self.number-1, -1, -1))

        self.order = order 
        self.reverse_order = list(map(
            lambda kv : kv[1], 
            sorted(zip(order, range(self.number)))
            ))


    def __apply__(self, kind = "any"):
        functions = {
            "any" : {
                "list": lambda arg : list(arg),
                "dict": lambda arg : dict(arg),
                "int": lambda arg : int(arg),
                "any": lambda arg : arg
            },      
            "flat" : {
                "list": lambda arg : list(arg),
                "dict": lambda arg : list(dict(arg).values()),
                "int": lambda arg : [],
                "any": lambda arg : []
            },
            "iter" : {
                "dict" : lambda arg : [{k : v} 
                for k, v in arg.items()],
                "list" : lambda arg : arg,
                "int" : lambda arg : list(range(arg)),
                "any" : lambda arg : arg
            }
        }
        return lambda arg : functions[kind][self.__typeof__(arg)](arg)
    
    def __typeof__(self, arg):
        y_type = type(arg)

        are = lambda feature : y_type is feature
        has = lambda feature : hasattr(y_type, feature)
        got = lambda feature : feature in y_type.__dict__

        has_len = has("__len__")
        has_iter = has("__iter__")
        has_dict = has('__dict__')

        is_range = are(range)
        is_string = are(str)

        is_sortable, has_keys, has_items, is_constant = False, False, False, False
        if has_dict:
            is_sortable = got("sort")
            has_keys = got("fromkeys") 
            has_items = got("items") 
            is_constant = got("as_integer_ratio") 
        
        is_iterable = is_sortable or is_range or is_string
        is_hashable = has_keys or has_items
        is_countable = has_len or has_iter

        unique = sum([is_iterable, is_hashable, is_constant]) == 1
        if unique and is_hashable:
            result = "dict" 
        elif unique and is_constant:
            result = "int"
        elif unique or is_countable:
            result = "list"
        else:
            result = "any"

        return result

    def __offset__(self, point):
        indices = []
        for ln in self.lens:
            indices.append(point % ln)
            point //= ln
            
        indices = [indices[order_i] for order_i in self.order]
        return indices        

  
    def __process__(self, arg, depth):
        arg = self.__apply__()(arg)

        if type(arg) in [list, dict] and depth >= 1:
            arg = self.__flatten__(arg, depth)
        
        arg = self.__apply__('iter')(arg)

        return arg
    
    def __flatten__(self, arg, depth):
        if depth < 1: return arg
        
        arg = self.__apply__('flat')(arg)

        args = []
        for arg_i in arg:
            arg_i = self.__flatten__(arg_i, depth-1)
            if not hasattr(arg_i, "__len__"):
                args.append(arg_i)
            else:
                args.extend(self.__apply__('iter')(arg_i))
        return args