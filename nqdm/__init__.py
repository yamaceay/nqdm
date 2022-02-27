import tqdm 

class nqdm(tqdm.tqdm):
    """
    NQDM progress bar
     - Compresses nested loops into a single loop 
     - Can work with different types of data
     - Is implemented by TQDM 
    Attributes
    ----------
    total : int

        Total number of expected iterations over all loops

    iterable : range
        
        Range object storing indices ranging from 0 to total-1
    
    arguments : list
        
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
        super().__init__(**kwargs)

        # Depth is set
        if type(depth) == list:
            if len(depth) != len(args):
                depth = 0

        if type(depth) == int:
            depth = [depth]*len(args)

        self.depth = depth

        # Order is set
        if type(order) == list:
            if len(order) != len(args):
                order = "first"

        if order == "first":
            order = list(range(len(args)))
        if order == "last":
            order = list(range(len(args)-1, -1, -1))

        self.order = order 
        map_order = sorted(zip(order, range(len(order))))
        self.reverse_order = list(map(lambda kv : kv[1], map_order))

        # Other variables are set
        self.enum = enum
        self.delay = 0
        self.disable = disable

        # Arguments are transformed
        args = list(map(self.__transform__, args, depth))
        args = list(map(self.__flatten__, args, depth))
        types = list(map(self.__typeof__, args))
        args = list(map(self.__getfunctions__("iter"), types, args))
        
        # Length features are set
        lens = list(map(len, args))
        self.lens = [lens[order_i] for order_i in self.reverse_order]
        self.total = 1
        for ln in self.lens:
            self.total *= ln
        self.iterable = range(self.total) 

        # Items are ready to yield
        get_elem = lambda point : [arg[offset] for arg, offset in zip(args, self.__ndindex__(point))]
        args = list(map(get_elem, self.iterable))
        if len(self.lens) == 1: args = list(map(lambda x : x[0], args))
        if enum: args = list(enumerate(args))
        self.values = args

    def __iter__(self):
        if self.disable:
            return self.values
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

    def __getfunctions__(self, kind = None):
        """
        Context-specific type-handling happens here
        
        Parameters
        ----------
        kind : String = None
        
            'iter': for yielding the data
            'flat': for flattening the data
            otherwise for transforming the data
        
        Returns
        ----------
        arg
        
            New argument

        """

        if kind == "iter":
            functions = {
                "dict" : lambda arg : [{k : v} 
                for k, v in arg.items()],
                "list" : lambda arg : arg,
                "int" : lambda arg : list(range(arg))*arg,
                "any" : lambda arg : arg
            }   
        elif kind == "flat":
            functions = {
                "list": lambda arg : arg,
                "dict": lambda arg : arg.values(),
                "int": lambda arg : [],
                "any": lambda arg : []
            }
        else:
            functions = {
                "list": lambda arg : list(arg),
                "dict": lambda arg : dict(arg),
                "int": lambda arg : int(arg),
                "any": lambda arg : arg
            }        
        return lambda typ, arg : functions[typ](arg)
    
    def __typeof__(self, arg):
        """
        Returns the type that the argument will be casted
        
        Parameters
        ----------
        arg
        
            Argument to be casted
        
        Returns
        ----------
        typ
        
            New type of argument
        """

        y_type = type(arg)

        are = lambda feature : y_type == feature
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

    def __ndindex__(self, point):
        """
        Finds the offsets of given iteration step
        
        Parameters
        ----------
        point
        
            The iteration step
        
        Returns
        ----------
        indices
        
            Indices of arguments

        """

        indices = []
        for ln in self.lens:
            indices.append(point % ln)
            point //= ln

        indices = [indices[order_i] for order_i in self.order]
        return indices        

    def __transform__(self, arg, depth):
        """
        Transforms the deeper levels of argument if needed
        
        Parameters
        ----------
        arg
        
            Argument to be transformed deeply
        
        depth : int
        
            Depth of transformation
        
        Returns
        ----------
        arg
        
            Transformed argument
        """
        
        typ = self.__typeof__(arg)
        arg = self.__getfunctions__()(typ, arg)

        if depth < 1:
            return arg

        if typ == "dict":
            arg = dict(map(lambda kv: (kv[0], self.__transform__(kv[1], depth-1)), arg.items()))

        if typ == "list":
            arg = list(map(lambda v: self.__transform__(v, depth-1), arg))

        return arg

    def __flatten__(self, arg, depth):
        """
        Very flexible function allowing to create an arbitrary 
        number of loops and flatten the given argument
        Parameters
        ----------
        arg
        
            Argument to be flattened
        
        depth : int
        
            Depth of argument
        
        Returns
        ----------
        args
        
            Flattened argument
        """

        if depth < 1:
            return arg

        
        args = []
        command = ""
        build = lambda idt, string : command + "  "*idt + string

        command = build(0, "typ = self.__typeof__(arg)\n")
        command = build(0, "arg_ = self.__getfunctions__('flat')(typ, arg)\n")
        command = build(0, "for arg0 in arg_:\n")
        for i in range(depth):
            command = build(2*i+1, f"typ{i} = self.__typeof__(arg{i})\n")
            command = build(2*i+1, f"arg_{i} = self.__getfunctions__('flat')(typ{i}, arg{i})\n")
            command = build(2*i+1, f"if typ{i} in ['any', 'int']:\n")
            command = build(2*i+2, f"args.append(arg{i})\n")
            command = build(2*i+1, f"else:\n")
            command = build(2*i+2, f"for arg{i+1} in arg_{i}:\n")
        command = build(2*i+3, f"args.append(arg{i+1})\n")

        exec(command)
        return args
