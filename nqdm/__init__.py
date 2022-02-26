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
            depth = [depth]*len(args)

        self.depth = depth

        # if order has an inconsistent length, then set order to first

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

        self.enum = enum

        # arguments are saved in self.arguments attribute
        args = list(map(self.__transform__, args, depth))
        self.arguments = list(map(self.__flatten__, args, depth))


        # self.total is set to the __limit__(*args) 
        # which returns the total number of expected iterations over all loops
        self.total = self.__limit__()

        # self.iterable is the iterable data shown in the progress bar
        # in this case, it returns the range of all iterations 
        self.iterable = range(self.total) 

        # self.values contains all iteration values
        self.values = list(map(self.__getelems__, self.iterable))       

        # self.delay is set to 0
        self.delay = 0

    def __iter__(self):
        if self.disable:
            return self.values
        mininterval = self.mininterval
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        min_start_t = self.start_t+self.delay
        n = self.n
        time = self._time
        
        # the bar is not disabled and it works well
        try:
            print("\n")
            for ind in self.iterable:
                # returns an informations list (see __getelems__())
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

    def __convert__(self, y_i):
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
        
        y_type = type(y_i)

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
        
        is_iterable = is_sortable or is_range
        is_hashable = has_keys or has_items
        is_countable = has_len or has_iter

        unique = sum([is_iterable, is_hashable, is_constant, is_string]) == 1
        if unique:
            
            if is_iterable or is_string:
                result = list(y_i), "string" if is_string else "list"
        
            elif is_hashable:
                result = dict(y_i), "dict"
        
            else:
                result = int(y_i), "int"
        
        else:
            result = list(y_i) if is_countable else y_i, y_type
        
        return result 
        
    def __limit__(self):
        """
        Calculates the total number of iterations over every loops.
        
        Parameters
        ----------
       
        Returns
        ----------
        product : int
        
            Total number of iterations expected over all arguments
        """
        product = 1
        for arg in self.arguments:

            is_iterable = hasattr(arg, "__len__")
            leng = len(arg) if is_iterable else int(arg)
            product *= leng

        return product

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
        arg, typ = self.__convert__(arg)

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

        command = "arg_ = arg.values() if type(arg) == dict else arg if hasattr(arg, '__len__') else []\nfor arg0 in arg_:\n"
        for i in range(1, depth+1):
            command += "  "*(2*i-1) + f"arg_{i-1} = arg{i-1}.values() if type(arg{i-1}) == dict else arg{i-1} if hasattr(arg{i-1}, '__len__') else []\n"
            command += "  "*(2*i-1) + f"if not len(arg_{i-1}):\n"
            command += "  "*(2*i) + f"args.append(arg{i-1})\n"
            command += "  "*(2*i-1) + f"else:\n"
            command += "  "*(2*i) + f"for arg{i} in arg_{i-1}:\n"
        command += "  "*(2*i+1) + f"args.append(arg{i})\n"

        exec(command)
        return args

    def __getelems__(self, point):
        """
        Finds out the offsets of each argument and saves the current element if needed
        
        Parameters
        ----------
        point : int
        
            The current offset of the main progress bar
        
        Returns
        ----------
        elems : list
            
            Contains current offset of each arguments 
            (and if given: their corresponding key-value pairs)
        """

        elems = []

        args = [self.arguments[order_i] for order_i in self.order]

        for i in range(len(args)):
            data, typ = self.__convert__(args[i])

            if typ == "float":
                data = int(data)

            leng = data if type(data) == int else len(data)

            offset = point%leng
            point = point//leng
            
            if typ == "dict":
                data = [{k : v} 
                for k, v in data.items()][offset]
            elif typ == "list":
                data = data[offset]
            else:
                data = offset
            
            elems.append(data)

        elems = [elems[order_i] for order_i in self.reverse_order]
        if len(elems) == 1 :
            elems = elems[0] 

        if self.enum:
            elems = (point, elems)

        return elems

if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    from time import time

    arg1 = {k: v for k,v in zip(list("abcde"), list("fghij"))}
    arg2 = [v**2 for v in range(10)]
    arg3 = 4.0

    start = time()
    for data in nqdm(arg1):
        print(data)
    print(time() - start)

    start = time()
    for data in nqdm(arg1, arg2, arg3):
        print(data)
    print(time() - start)

    arg1_deep = np.arange(80000).reshape(200, 20, 20)
    arg2_deep = {str(i): {k+str(i): v+str(i) for k,v in zip(list("abcde"), list("fghij"))} for i in range(20)}  

    start = time()
    for data in nqdm(arg1_deep, depth=0):
        pass
    print(time() - start)

    start = time()
    for data in nqdm(arg1_deep, depth=1):
        pass
    print(time() - start)

    start = time()
    for data in nqdm(arg1_deep, depth=2):
        pass
    print(time() - start)

    start = time()
    for data in nqdm(arg2_deep, depth=0):
        pass
    print(time() - start)

    start = time()
    for data in nqdm(arg2_deep, depth=1):
        pass
    print(time() - start)
