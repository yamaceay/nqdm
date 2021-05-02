import numpy as np
import pandas as pd
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
        total number of expected iterations over all loops
    iterable : range
        range object storing indices ranging from 0 to total-1
    arguments : list
        list of iterable objects and single variables
    delay : int
        total delay (is set to 0)
    """
    def __init__(self, *args, **kwargs):
        
        # all features of tqdm are implemented
        # NOTE: the parameters of tqdm have to be in keyword arguments format
        super().__init__(**kwargs)

        # self.total is set to the __limit__(*args) 
        # which returns the total number of expected iterations over all loops
        self.total = self.__limit__(*args)

        # self.iterable is the iterable data shown in the progress bar
        # in this case, it returns the range of all iterations 
        self.iterable = range(self.total)

        # self.delay is set to 0
        self.delay = 0

        # arguments are saved in self.arguments attribute
        self.arguments = self.__preprocess__(args) 

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

                # returns an informations list (see __ndrate__())
                obj = self.__ndrate__(ind, *self.arguments)
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
                # returns an informations list (see __ndrate__())
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

    def __checkit__(self, data):
        """
        Identifies the type of data. If the data is the output
        of an outer nqdm loop, then it extracts the information.
        """
        if not isinstance(data, tuple):
            return data

        if not(isinstance(data[0], int)):
            return data

        if not (isinstance(data[1], tuple)):
            return data

        if len(data[1]) == 0:

            #scalar
            return data[0]
        if data[1][0] is None:

            #array
            return data[1][1]
        else:

            #hash
            return dict(data[1])
    def __transformate__(self):
        """
        Transformates the following data types into suitable input format:
         - pandas.Series() -> list of index, list of values
         - numpy.array() -> list of values
         - str -> list of characters
         - dict -> list of keys and list of values
         - float -> int
         - list and int are unmodified 
        """
        return {
            "<class 'pandas.core.series.Series'>": (lambda data: (list(data.index), list(data.values))),
            "<class 'numpy.ndarray'>": (lambda data: (None, data.tolist())),
            "<class 'str'>": (lambda data: (None, list(data))),
            "<class 'dict'>": (lambda data: (list(data.keys()), list(data.values()))),
            "<class 'list'>": (lambda data: (None, data)),
            "<class 'int'>": (lambda data: (None, data)),
            "<class 'float'>": (lambda data: (None, int(data)))
        }
    def __limit__(self, *args):
        """
        Calculates the total number of iterations over every loops.
        
        Parameters
        ----------
        *args 
            unpacked list of arguments of any iterable object type or int/float
        
        Returns
        ----------
        product : int
            total number of iterations expected over all arguments
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
    
    def __preprocess__(self, *args):
        """
        Checks if any of the arguments are outputs of an outer nqdm loop
        
        Parameters
        ----------
        *args:
            Unpacked list of arguments ready to be processed

        Returns
        ----------
        new_args:
            Preprocessed arguments
        """

        new_args = []
        for arg_hidden in args:
            for arg in arg_hidden:
                arg = self.__checkit__(arg)
                new_args.append(arg)
        
        return new_args
            
            

    def __ndrate__(self, point, *args):
        """
        Finds out the offsets of each argument and saves the current element if needed
        
        Parameters
        ----------
        point: int
            the current offset of the main progress bar
        *args: list
            unpacked list of arguments containing iterable objects or int/float variables
        
        Returns
        ----------
        informations: list
            contains current offset of each arguments 
            (and if given: their corresponding key-value pairs)
        """

        # informations list to be returned
        informations = []

        for i in range(len(args)):
            arg = args[i]

            # the following operations depends on the type of argument
            typ = type(arg)

            # the respective transformating function is selected
            tr_func = self.__transformate__()[str(typ)]

            # the content is extracted to a more useful format
            # as keys and values
            keys, vals = tr_func(arg)

            # checks if the argument has a key or not
            is_key = keys is not None

            # checks if the argument is an iterable object or not
            is_iterable = hasattr(vals, "__len__")

            # if the argument an iterable object, then save its length
            # otherwise it is already a length variable
            leng = len(vals) if is_iterable else vals

            # the index/offset of given argument
            offset = point%leng

            # keys and values are saved 
            key = keys[offset] if is_key else None
            val = vals[offset] if is_iterable else None

            # if both of them are set to none
            # then return a empty tuple object
            # otherwise save them as a (key, value) pair
            pair = () if key is None and val is None else (key, val)

            # save the information about current argument
            informations.append((offset, pair))

            # continue with new arguments
            point = point//leng
        return informations