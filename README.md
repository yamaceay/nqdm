# NQDM

![Logo](https://user-images.githubusercontent.com/46201716/116823016-4d8b3900-ab82-11eb-9661-ea9dc75d93e3.png)

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
1. length: returns 0, ..., length-1
2. array: returns array[0], ..., array[length-1]
3. hashable: returns {keys[0]: values[0]}, ..., {keys[length-1]: values[length-1]}

A more detailled list of available arguments and return values:

| Argument | Type of Argument          | Returns                                                   |
|----------|---------------------------|-----------------------------------------------------------|
| length   | int                       | range(length)                                             |
| length   | float                     | range(int(length))                                        |
| array    | numpy.ndarray             | list(array)                                               |
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


**3D-Lists:**

Input:

```
list_of_list_of_lists = [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
for outer in nqdm(list_of_list_of_lists):
  for middle in nqdm(outer):
    for inner in nqdm(middle):
      print(inner)
```

Output:

![NQDM_05](https://user-images.githubusercontent.com/46201716/116821688-29782980-ab7b-11eb-9ca1-4f9ed816daba.png)



## Built With

* [tqdm](https://github.com/tqdm/tqdm) - The progress bar
* [numpy](https://github.com/numpy/numpy) - Data type conversion 
* [pandas](https://pandas.pydata.org/) - Data type conversion

## Authors

* **Yamac Eren Ay** - *Initial work* - [yamaceay](https://github.com/yamaceay)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* It's worth mentioning that this module is built on top of [TQDM](https://tqdm.github.io/),  I would like to
* thank them for doing the real hard job and making this process of creating progress bars easy and flexible. 
