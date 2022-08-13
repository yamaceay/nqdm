# NQDM

<img width="390" alt="logo1" src="https://user-images.githubusercontent.com/46201716/117867669-f2032e80-b298-11eb-89dc-9f57bd0affb5.png">

[A Gentle Introduction](https://yamaceay.medium.com/nqdm-modern-progress-bar-13a898a8f411)

A more generalised implementation to TQDM-progress bars, 
which simulates a single loop for multiple loops and returns 
multiple elements at the same time. It can iterate over the deeper levels. It is compatible with many data types, 
is customizable and beginner-friendly.

### Installing

Install it using the terminal

```
pip install nqdm
```

## Getting Started

First of all, you need to import nqdm.
```
from nqdm import nqdm
```

Let's explore some use cases of nqdm:

### Working With Different Data Types

There are three types of arguments: 
1. constant: returns `0, ..., constant-1`
2. iterable: returns `iterable[0], ..., iterable[-1]`
3. hashable: returns `{keys[0]: values[0]}, ..., {keys[-1]: values[-1]}`

A more detailled list of available arguments and return values:

| Argument | Type of Argument                | Returns                                                   |
|----------|---------------------------------|-----------------------------------------------------------|
| constant | int, float, double              | range(int(constant))                                      |
| iterable | numpy.ndarray, range, list, str | list(iterable)                                            |
| hashable | pandas.core.series.Series       | [{k: v} for k, v in zip(hashable.index, hashable.values)] |
| hashable | dict                            | [{k: v} for k, v in hashable.items()]                     |

#### **Length variables (int, float)**

Input:

```
len_1 = 2.0 
len_2 = 3 

for i in nqdm(len_1, len_2):
  print(i)
```

Output:

![NQDM_01](https://user-images.githubusercontent.com/46201716/116820687-87564280-ab76-11eb-9bcb-138aaba6e434.png)

#### **Lists and NumPy arrays**

Input:

```
arg_1 = [1, 2, 3]
arg_2 = np.array([4, 5, 6])

for i in nqdm(arg_1, arg_2):
  print(i)
```

Output:

![NQDM_02](https://user-images.githubusercontent.com/46201716/118552656-82d97e80-b75f-11eb-9250-f676844d76b6.png)


#### **Strings**

Input:

```
arg_1 = list("abc")
arg_2 = "cde"

for i in nqdm(arg_1, arg_2):
  print(i)
```

Output:

![NQDM_03](https://user-images.githubusercontent.com/46201716/118552551-60476580-b75f-11eb-809e-cc79b93f4fcc.png)


#### **Dictionaries and Pandas Series**

Input:

```
arg_1 = {"key1": 4, "key2": 5}
arg_2 = pd.Series(["horse", "cat", "mouse"], index=[978, 979, 980])

for i in nqdm(arg_1, arg_2):
  print(i)
```
Output:

![NQDM_04](https://user-images.githubusercontent.com/46201716/116821270-7fe46880-ab79-11eb-9727-875093e7d2c1.png)


### **NEW: Usage of Depth Feature**

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

### **NEW: Usage of Order Feature**

Input:

```
for i in nqdm(2, 2, 2, order = "last"):
    print(i)
```

Output:

![NQDM_9)](https://user-images.githubusercontent.com/46201716/118056798-dc6e3180-b38a-11eb-9924-600d80631b16.png)


Input:

```
for i in nqdm(2, 2, 2, order = "first"):
    print(i)
```

Output:

![NQDM_10](https://user-images.githubusercontent.com/46201716/118056822-e6903000-b38a-11eb-936d-55196bd60235.png)


Input:

```
for i in nqdm(2, 2, 2, order = [1, 2, 0]):
    print(i)
```

Output:

![NQDM_11](https://user-images.githubusercontent.com/46201716/118056744-bfd1f980-b38a-11eb-8284-02aee6a1dbfb.png)


### **NEW: Usage of Enum Feature**


Input:
```
data = pd.DataFrame({"x1": [2, 3, 5], "x2": [9, 8, 2], "x3": [0, 0, 2]})

for i in nqdm(data, enum=True, depth=1):
    print(i)
```

Output:

![NQDM_12](https://user-images.githubusercontent.com/46201716/118331627-1ebd7d00-b509-11eb-93a3-81ce1d09e59c.png)



## Built With

* [tqdm](https://github.com/tqdm/tqdm) - The progress bar

## Authors

* **Yamac Eren Ay** - *Initial work* - [yamaceay](https://github.com/yamaceay)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Special Thanks to:

* **Stanislav Kosorin** - [stano45](https://github.com/stano45) 
* **Ori Toledo** - *Logo design* - [oritoledo](https://github.com/oritoledo)

## Acknowledgments

It's worth mentioning that this module is built on top of [TQDM](https://tqdm.github.io/),  I would like to
thank them for making this process of creating progress bars easy and flexible. 
