# NQDM

<img width="870" alt="logo1" src="https://user-images.githubusercontent.com/46201716/117867669-f2032e80-b298-11eb-89dc-9f57bd0affb5.png">

A more generalised implementation to TQDM-progress bars, 
which simulates a single loop for multiple loops and returns 
multiple indices at the same time. It is compatible with many data types, 
is customizable and beginner-friendly.

### Installing

Install it using the terminal
```
git clone https://github.com/yamaceay/nqdm.git
```
or install it on a .ipynb notebook.
```
!git clone https://github.com/yamaceay/nqdm.git
```

## Getting Started

First of all, you need to import nqdm.
```
from nqdm import nqdm
```

Let's explore some use cases of nqdm:

### Working With Different Data Types

There are three types of arguments: 
1. length: returns `0, ..., length-1`
2. array: returns `array[0], ..., array[length-1]`
3. hashable: returns `{keys[0]: values[0]}, ..., {keys[length-1]: values[length-1]}`

A more detailled list of available arguments and return values:

| Argument | Type of Argument          | Returns                                                   |
|----------|---------------------------|-----------------------------------------------------------|
| length   | int                       | range(length)                                             |
| length   | float                     | range(int(length))                                        |
| array    | numpy.ndarray             | list(array)                                               |
| array    | range                     | list(array)                                               |
| array    | list                      | array                                                     |
| array    | str                       | list(array)                                               |
| hashable | pandas.core.series.Series | [{k: v} for k, v in zip(hashable.index, hashable.values)] |
| hashable | dict                      | [{k: v} for k, v in hashable.items()]                     |

**Length variables (int, float)**

Input:

```
len_1 = 2.0 
len_2 = 3 

for i in nqdm(len_1, len_2):
  print(i)
```

Output:

![NQDM_01](https://user-images.githubusercontent.com/46201716/116820687-87564280-ab76-11eb-9bcb-138aaba6e434.png)

**Lists and NumPy arrays**

Input:

```
arg_1 = [1, 2, 3]
arg_2 = np.array([4, 5, 6])

for i in nqdm(arg_1, arg_2):
  print(i)
```

Output:

![NQDM_02](https://user-images.githubusercontent.com/46201716/116820837-5591ab80-ab77-11eb-9954-f9f9d60d24c9.png)


**Strings**

Input:

```
arg_1 = list("abc")
arg_2 = "cde"

for i in nqdm(arg_1, arg_2):
  print(i)
```

Output:

![NQDM_03](https://user-images.githubusercontent.com/46201716/116821097-c6859300-ab78-11eb-95e9-0a7ec46a4631.png)


**Dictionaries and Pandas Series**

Input:

```
arg_1 = {"key1": 4, "key2": 5}
arg_2 = pd.Series(["horse", "cat", "mouse"], index=[978, 979, 980])

for i in nqdm(arg_1, arg_2):
  print(i)
```
Output:

![NQDM_04](https://user-images.githubusercontent.com/46201716/116821270-7fe46880-ab79-11eb-9727-875093e7d2c1.png)


**NEW: Usage of Depth Feature**

Input:

```
list_of_list_of_lists = [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
for list_of_list in nqdm(list_of_list_of_lists, depth=0):
  print(list_of_list)
```

Output:

![NQDM_05](https://user-images.githubusercontent.com/46201716/117814400-8bfcb400-b264-11eb-9dfc-7cfad4071a35.png)


Input:

```
list_of_list_of_lists = np.arange(8).reshape(2, 2, 2)
for arr in nqdm(list_of_list_of_lists, depth=1):
  print(arr)
```

Output:

![NQDM_06](https://user-images.githubusercontent.com/46201716/117814430-961eb280-b264-11eb-9efc-429c9e8ef89d.png)

Input:

```
list_of_dict_of_lists = [{"a": [0, 1], "b": [2, 3]}, {"a": [4, 5], "b": [6, 7]}]
for elem in nqdm(list_of_dict_of_lists, depth=2):
  print(elem)
```

Output:

![NQDM_07](https://user-images.githubusercontent.com/46201716/117814463-a0d94780-b264-11eb-8e67-c663e9b10f57.png)


Input:

```
list_of_list_of_lists = np.arange(8).reshape(2, 2, 2)
list_of_list_of_dicts = [[{"a": 1, "b": 2}, {"c": 3, "d": 4}], [{"e": 5, "f": 6}, {"g": 7, "h": 8}]]
for elems in nqdm(list_of_list_of_lists, list_of_list_of_dicts, depth=[0, 1]):
  print(elems)
```

Output:

![NQDM_08](https://user-images.githubusercontent.com/46201716/117816662-0b8b8280-b267-11eb-8015-89a872044ca5.png)


## Built With

* [tqdm](https://github.com/tqdm/tqdm) - The progress bar
* [numpy](https://github.com/numpy/numpy) - Data type conversion 
* [pandas](https://pandas.pydata.org/) - Data type conversion

## Authors

* **Yamac Eren Ay** - *Initial work* - [yamaceay](https://github.com/yamaceay)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Collaborators

* **Stanislav Kosorin** - [stano45](https://github.com/stano45) 

Special Thanks to:

* **Ori Toledo** - *Logo design* - [oritoledo](https://github.com/oritoledo)

## Acknowledgments

It's worth mentioning that this module is built on top of [TQDM](https://tqdm.github.io/),  I would like to
thank them for doing the real hard job and making this process of creating progress bars easy and flexible. 
