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
    
    delay : int = 0
        
        Total delay

    enum : bool = False

        Whether data is enumerated or not
    """
    def __init__(self, *args, depth = 0, order = "first", enum = False, **kwargs):

        # all features of tqdm are implemented
        # NOTE: the parameters of tqdm have to be in keyword arguments format
        super().__init__(**kwargs)

        # if depth is an integer, then every depth is the same
        # if depth has an inconsistent length, then set depth to 0
        if type(depth) == list:
            if len(depth) != len(args):
                depth = 0

        if type(depth) == int:
            depth = [depth for i in range(len(args))]

        self.depth = depth

        # if order has an inconsistent length, then set order to first
        if type(order) == list:
            if len(order) != len(args):
                order = "first"
            
        self.order = order

        self.enum = enum

        # arguments are saved in self.arguments attribute
        args = [self.__transformdeep__(arg, depth_i) for arg, depth_i in zip(args, depth)]
        self.arguments = [self.__flatten__(arg, depth_i) for arg, depth_i in zip(args, depth)]

        # self.total is set to the __limit__(*args) 
        # which returns the total number of expected iterations over all loops
        self.total = self.__limit__()

        # self.iterable is the iterable data shown in the progress bar
        # in this case, it returns the range of all iterations 
        self.iterable = range(self.total)

        # self.delay is set to 0
        self.delay = 0

    def __neworder__(self, data):
        """
        Reorders the arguments
        Parameters
        ----------
        data : list

            List of arguments to be reordered
        
        Returns
        ----------
        sorted_values : list
        
            Reordered list of arguments
        """

        # if first, then do not change anything
        if self.order == "first":
            sorted_values = data
        
        # if last, then reverse it
        elif self.order == "last":
            sorted_values = data[::-1]

        # if any arbitrary order, then reorder accordingly
        else:
            indices = list(range(len(data)))
            mapper = {order_i: data[index_i] for order_i, index_i in zip(self.order, indices)}
            sorted_mapper = {key: mapper[key] for key in sorted(mapper.keys())}
            sorted_values = list(sorted_mapper.values())
        
        return sorted_values
    
    def __oldorder__(self, data):

        # if first, do not change anything
        if self.order == "first":
            old_data = data
        
        # if last, reverse it
        elif self.order == "last":
            old_data = data[::-1]

        # if any arbitrary order, reorder to the old structure
        else:
            old_data = [data[order_i] for order_i in self.order]
        return old_data
    

    def __iter__(self):
        """
        Built-in iter function. Some parts of the 
        __iter__() function of TQDM is reimplemented
        """
        iterable = self.iterable

        # no display in the case the bar is disabled
        if self.disable:
            print("\n")
            for ind in iterable:

                # returns an informations list (see __getelems__())
                obj = self.__getelems__(ind, *self.arguments)

                # if data needs to be enumerated, then add index
                if self.enum:
                    obj = (ind, obj)
                    
                yield obj
            return
        mininterval = self.mininterval
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        min_start_t = self.start_t+self.delay
        n = self.n
        time = self._time
        
        # the bar is not disabled and it works well
        try:
            print("\n")
            for ind in iterable:
                # returns an informations list (see __getelems__())
                obj = self.__getelems__(ind, *self.arguments)

                # if data is to be enumerated, then add index
                if self.enum:
                    obj = (ind, obj)

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

    def __transform__(self, y_i):
        """
        Converts the given object to its respective built-in equivalent
        Parameters
        ----------
        y_i
        
            Argument to transform
        
        Returns
        ----------
        arg
        
            Transformed argument
        
        typ : str
        
            Type of argument
        """

        # Functions to extract features from given object
        is_iterable = lambda y: True if y == range else any([x == "sort" for x in y.__dict__]) if hasattr(y, '__dict__') else False
        is_hashable = lambda y: any([x in ["fromkeys", "items"] for x in y.__dict__]) if hasattr(y, '__dict__') else False
        is_constant = lambda y: any([x == "as_integer_ratio" for x in y.__dict__]) if hasattr(y, '__dict__') else False
        is_string = lambda y: y == str

        argmax = lambda x: max(zip(x, range(len(x))))[1]

        # List of functions
        functions = [is_iterable, is_hashable, is_constant, is_string]

        # Iterate over functions and get results
        y = [fn(type(y_i))*1 for fn in functions]

        # No overlapping allowed due to the simplicity reasons
        # If possible try to convert to list
        if sum(y) != 1:
            try:
                if hasattr(y_i, "__len__") or hasattr(y_i, "__iter__"):
                    y_i = list(y_i)
            except:
                pass
            return y_i, type(y_i)

        # Convert to list
        if argmax(y) == 0:
            return list(y_i), "list" 
        
        # Conversion to dict
        if argmax(y) == 1:
            return dict(y_i), "dict"
        
        # Check if int or not given that it is a constant
        if argmax(y) == 2:
            if type(y_i) == int:
                return y_i, "int"
            else:
                # Note: float here means it is not int
                return y_i, "float"
        
        # Conversion of string to list
        if argmax(y) == 3:
            return list(y_i), "string"
        
    def __limit__(self):
        args = self.arguments
        """
        Calculates the total number of iterations over every loops.
        
        Parameters
        ----------
        *args 
        
            Unpacked list of arguments of any iterable object type or int/float
        
        Returns
        ----------
        product : int
        
            Total number of iterations expected over all arguments
        """
        product = 1
        for i in range(len(args)):
            arg = args[i]

            # if the argument an iterable object
            # then multiply the product with the length of argument
            # otherwise multiply the product with the argument itself
            # (it is already a length variable)
            is_iterable = hasattr(arg, "__len__")
            leng = len(arg) if is_iterable else int(arg)
            product *= leng

        return product

    def __transformdeep__(self, arg, depth):
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

        # Initial transformation of data
        arg, typ = self.__transform__(arg)

        # If depth is 0 or less, than end the transformation
        if depth < 1:
            return arg

        # If it is a dict, transform each value
        if typ == "dict":
            arg = {k: self.__transformdeep__(v, depth-1) for k,v in arg.items()}

        # If it is a list, transform each element
        if typ == "list":
            arg = [self.__transformdeep__(v, depth-1) for v in arg]

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

        # If depth is 0 or less, then flattening is not possible
        if depth < 1:
            return arg
        
        # Dynamically create the code for iteration
        args = []
        command = "arg_ = arg.values() if type(arg) == dict else arg if hasattr(arg, '__len__') else []\nfor arg0 in arg_:\n"
        for i in range(1, depth+1):
            
            # If dict then iterate over values
            # If list then iterate over itself
            # If constant then don't iterate
            command += "  "*(2*i-1) + f"arg_{i-1} = arg{i-1}.values() if type(arg{i-1}) == dict else arg{i-1} if hasattr(arg{i-1}, '__len__') else []\n"
            
            # If constant, then save data directly
            command += "  "*(2*i-1) + f"if not len(arg_{i-1}):\n"
            command += "  "*(2*i) + f"args.append(arg{i-1})\n"

            # Otherwise iterate further
            command += "  "*(2*i-1) + f"else:\n"
            command += "  "*(2*i) + f"for arg{i} in arg_{i-1}:\n"
        
        # Append each item flatly
        command += "  "*(2*i+1) + f"args.append(arg{i})\n"

        # Execute the command
        exec(command)
        return args

    def __getelems__(self, point, *args):
        """
        Finds out the offsets of each argument and saves the current element if needed
        
        Parameters
        ----------
        point : int
        
            The current offset of the main progress bar
        
        *args : list
        
            Unpacked list of arguments containing iterable objects or int/float variables
        
        Returns
        ----------
        informations : list
            
            Contains current offset of each arguments 
            (and if given: their corresponding key-value pairs)
        """

        # informations list to be returned
        informations = []

        # other datas
        offsets = []
        datas = []
        types = []

        args = self.__neworder__(args)

        for i in range(len(args)):

            arg = args[i]

            # the following operations depends on the type of argument
            data, typ = self.__transform__(arg)

            # if data is float then convert it to int
            if typ == "float":
                data = int(data)

            # calculate length
            leng = data if type(data) == int else len(data)

            # the index/offset of given argument
            offset = point%leng

            # continue with new arguments
            point = point//leng
        
            # add indices
            offsets.append(offset)
            datas.append(data)
            types.append(typ)
        
        for i in range(len(args)):

            # get current index
            offset = offsets[i]
            data = datas[i]
            typ = types[i]

            # store variables as either dict item or list value or offset
            if typ == "dict":
                data = {list(data.keys())[offset]: list(data.values())[offset]}
            elif typ == "list":
                data = data[offset]
            else:
                data = offset
            
            informations.append(data)

        # reduce dimension if just one element
        elems = informations[0] if len(informations) == 1 else self.__oldorder__(informations)

        return elems