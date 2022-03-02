import unittest
from nqdm import nqdm
from time import time
import pandas as pd
import numpy as np

class TestNqdm(unittest.TestCase):

    """
    Tests the initialization
    """
    def test_init_1(self):
        int_ex = nqdm(5).values
        self.assertListEqual(int_ex, [0, 1, 2, 3, 4])   
    def test_init_2(self): 
        list_ex = nqdm([1, 2]).values
        self.assertListEqual(list_ex, [1, 2])
    def test_init_3(self):
        float_ex = nqdm(1.0).values
        self.assertListEqual(float_ex, [0])
    def test_init_4(self):
        zero_ex = nqdm().values
        self.assertListEqual(zero_ex, [])
    def test_init_5(self):
        negative_ex = nqdm(-1.0).values
        self.assertListEqual(negative_ex, [])
    def test_init_6(self):
        dict_ex = nqdm({"a": 1, "b": 2, "c": 3}).values
        self.assertListEqual(dict_ex, [{"a": 1}, {"b": 2}, {"c": 3}])
    def test_init_7(self):
        range_ex = nqdm(range(6)).values
        self.assertListEqual(range_ex, list(range(6)))
    def test_init_8(self):
        numpy_ex = nqdm(np.arange(25)).values
        self.assertListEqual(numpy_ex, list(range(25)))
    def test_init_9(self):
        series_ex = nqdm(pd.Series({"a": 5, "b": 7})).values
        self.assertListEqual(series_ex, [{"a": 5}, {"b": 7}])
    def test_init_10(self):
        string_ex = nqdm("hello world").values
        self.assertListEqual(string_ex, list("hello world"))
    def test_init_11(self):
        tuple_ex = nqdm(tuple([1, 2])).values
        self.assertListEqual(tuple_ex, list([1, 2]))
    def test_init_12(self):
        set_ex = nqdm(set(list("abc"))).values
        self.assertSetEqual(set(set_ex), set(list("abc")))
    """
    Tests the effects of depth parameter
    """
    def test_depth_1(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        invalid_level_ex = nqdm(five_d_array, depth = -1).values
        for i in range(len(invalid_level_ex)):
            arr1 = invalid_level_ex[i]
            arr1_ = five_d_array[i]
            self.assertTrue(np.array_equal(arr1, arr1_))
    def test_depth_2(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        one_level_ex = nqdm(five_d_array, depth = 0).values
        for i in range(len(one_level_ex)):
            arr1 = one_level_ex[i]
            arr1_ = five_d_array[i]
            self.assertTrue(np.array_equal(arr1, arr1_))
    def test_depth_3(self):
        five_d_array = np.arange(2**5).reshape([2]*5)   
        two_level_ex = nqdm(five_d_array, depth = 1).values
        for i in range(len(two_level_ex)):
            arr1 = two_level_ex[i]
            arr1_ = five_d_array[i//2][i%2]
            self.assertTrue(np.array_equal(arr1, arr1_)) 
    def test_depth_4(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        three_level_ex = nqdm(five_d_array, depth = 2).values
        for i in range(len(three_level_ex)):
            arr1 = three_level_ex[i]
            arr1_ = five_d_array[i//4][i//2%2][i%2]
            self.assertTrue(np.array_equal(arr1, arr1_))
    def test_depth_5(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        four_level_ex = nqdm(five_d_array, depth = 3).values
        for i in range(len(four_level_ex)):
            arr1 = four_level_ex[i]
            arr1_ = five_d_array[i//8][i//4%2][i//2%2][i%2]
            self.assertTrue(np.array_equal(arr1, arr1_))
    def test_depth_6(self):
        five_d_array = np.arange(2**5).reshape([2]*5)    
        five_level_ex = nqdm(five_d_array, depth = 4).values
        for i in range(len(five_level_ex)):
            arr1 = five_level_ex[i]
            arr1_ = five_d_array[i//16][i//8%2][i//4%2][i//2%2][i%2]
            self.assertTrue(np.array_equal(arr1, arr1_))
    def test_depth_7(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        six_level_ex = nqdm(five_d_array, depth = 5).values
        for i in range(len(six_level_ex)):
            arr1 = six_level_ex[i]
            arr1_ = five_d_array[i//16][i//8%2][i//4%2][i//2%2][i%2]
            self.assertTrue(np.array_equal(arr1, arr1_))
    def test_depth_8(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        two_d_array = np.arange(4).reshape(2, 2)
        two_items_ex = nqdm(two_d_array, five_d_array, depth = [0, 0]).values
        for i in range(len(two_items_ex)):
            arr1 = two_items_ex[i]
            arr1_ = [two_d_array[i%2], five_d_array[i//2]]
            self.assertTrue(np.array_equal(arr1[0], arr1_[0]))
            self.assertTrue(np.array_equal(arr1[1], arr1_[1]))
    def test_depth_9(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        two_d_array = np.arange(4).reshape(2, 2)
        two_items_one_level_ex = nqdm(two_d_array, five_d_array, depth = [0, 1]).values
        for i in range(len(two_items_one_level_ex)):
            arr1 = two_items_one_level_ex[i]
            arr1_ = [two_d_array[i%2], five_d_array[i//4][i//2%2]]
            self.assertTrue(np.array_equal(arr1[0], arr1_[0]))
            self.assertTrue(np.array_equal(arr1[1], arr1_[1]))
    def test_depth_10(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        two_d_array = np.arange(4).reshape(2, 2)        
        two_items_two_level_ex = nqdm(two_d_array, five_d_array, depth = [0, 2]).values
        for i in range(len(two_items_two_level_ex)):
            arr1 = two_items_two_level_ex[i]
            arr1_ = [two_d_array[i%2], five_d_array[i//8][i//4%2][i//2%2]]
            self.assertTrue(np.array_equal(arr1[0], arr1_[0]))
            self.assertTrue(np.array_equal(arr1[1], arr1_[1]))
    def test_depth_11(self):
        five_d_array = np.arange(2**5).reshape([2]*5)
        two_d_array = np.arange(4).reshape(2, 2)
        two_items_one_level_both_ex = nqdm(two_d_array, five_d_array, depth = [1, 1]).values
        for i in range(len(two_items_one_level_both_ex)):
            arr1 = two_items_one_level_both_ex[i]
            arr1_ = [two_d_array[i//2%2][i%2], five_d_array[i//8][i//4%2]]
            self.assertTrue(np.array_equal(arr1[0], arr1_[0]))
            self.assertTrue(np.array_equal(arr1[1], arr1_[1]))
    def test_depth_12(self):
        three_d_dict = {str(k*4): {str(j*2+k*4): {str(i+j*2+k*4): i+j*2+k*4 
            for i in range(2)} 
            for j in range(2)} 
            for k in range(2)}
        dict_one_level = nqdm(three_d_dict, depth = 0).values
        for i in range(len(dict_one_level)):
            dict1 = dict_one_level[i]
            self.assertDictEqual(dict1, {str(i*4): 
            {str(i*4+j*2) : 
            {str(i*4+j*2+k) : i*4+j*2+k
            for k in range(2)} 
            for j in range(2)}})
    def test_depth_13(self):
        three_d_dict = {str(k*4): {str(j*2+k*4): {str(i+j*2+k*4): i+j*2+k*4 
            for i in range(2)} 
            for j in range(2)} 
            for k in range(2)}
        dict_two_level = nqdm(three_d_dict, depth = 1).values
        for i in range(len(dict_two_level)):
            dict1 = dict_two_level[i]
            self.assertDictEqual(dict1, {str(i*2): 
            {str(i*2+j): i*2+j 
            for j in range(2)}})
    def test_depth_14(self):
        three_d_dict = {str(k*4): {str(j*2+k*4): {str(i+j*2+k*4): i+j*2+k*4 
            for i in range(2)} 
            for j in range(2)} 
            for k in range(2)}
        dict_three_level = nqdm(three_d_dict, depth = 2).values
        for i in range(len(dict_three_level)):
            dict1 = dict_three_level[i]
            self.assertDictEqual(dict1, {str(i) : i})
    def test_depth_15(self):
        three_d_dict = {str(k*4): {str(j*2+k*4): {str(i+j*2+k*4): i+j*2+k*4 
            for i in range(2)} 
            for j in range(2)} 
            for k in range(2)}
        dict_four_level = nqdm(three_d_dict, depth = 3).values
        for i in range(len(dict_four_level)):
            dict1 = dict_four_level[i]
            self.assertEqual(dict1, i)
    """
    Tests the effects of order parameter
    """
    def test_order_1(self):
        five_arrays = [np.arange(2)]*5
        first_order = nqdm(*five_arrays, order = "first").values
        for i in range(len(first_order)):
            arr1 = first_order[i]
            arr1_ = [i%2, i//2%2, i//4%2, i//8%2, i//16]
            self.assertListEqual(arr1, arr1_)
    def test_order_2(self):
        five_arrays = [np.arange(2)]*5
        last_order = nqdm(*five_arrays, order = "last").values
        for i in range(len(last_order)):
            arr1 = last_order[i]
            arr1_ = [i%2, i//2%2, i//4%2, i//8%2, i//16][::-1]
            self.assertListEqual(arr1, arr1_)
    def test_order_3(self):
        five_arrays = [np.arange(2)]*5
        custom_order = nqdm(*five_arrays, order = [0, 2, 4, 3, 1]).values
        for i in range(len(custom_order)):
            arr1 = custom_order[i]
            arr1_ = [i%2, i//4%2, i//16, i//8%2, i//2%2]
            self.assertListEqual(arr1, arr1_)
    def test_order_4(self):
        five_arrays = [np.arange(2)]*5
        invalid_order = nqdm(*five_arrays, order = [0, 4, 4, 3, 1]).values
        for i in range(len(invalid_order)):
            arr1 = invalid_order[i]
            arr1_ = [i%2, i//2%2, i//4%2, i//8%2, i//16]
            self.assertListEqual(arr1, arr1_)
    """
    Tests the effects of enum parameter
    """
    def test_enum_1(self):
        custom_arr = np.array([1, 43, 32])
        custom_dict = {"a": 5, "x": 8}
        without_enum = nqdm(custom_arr, custom_dict)
        with_enum = nqdm(custom_arr, custom_dict, enum=True)
        for arr1, arr1_ in zip(enumerate(without_enum), with_enum):
            self.assertEqual(arr1[0], arr1_[0])
            self.assertListEqual(arr1[1], arr1_[1])
    """
    Stresses the whole algorithm
    """
    def test_stress_1(self):
        array = np.arange(7**6).reshape(*[7]*6)
        start = time()
        nqdm(array, depth = 3)
        self.assertGreaterEqual(0.15, time() - start)
    def test_stress_2(self):
        array = np.arange(7**6).reshape(*[7]*6)
        start = time()
        nqdm(array, depth = 4)
        self.assertGreaterEqual(0.30, time() - start)
    def test_stress_3(self):
        array = np.arange(7**6).reshape(*[7]*6)
        start = time()
        nqdm(array, depth = 5)
        self.assertGreaterEqual(1.00, time() - start)
    def test_stress_4(self):
        array = np.arange(7**6).reshape(*[7]*6)
        start = time()
        nqdm(array, depth = 6)
        self.assertGreaterEqual(3.00, time() - start)

if (__name__ == "__main__"):
    unittest.main()