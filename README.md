# NQDM

A more generalised implementation to TQDM-progress bars, 
which simulates a single loop for multiple loops and returns multiple indices at the same time. 

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

Then it is ready to use!
Let's explore some use cases of nqdm:

### Working With Different Data Types

**Length variables (int, float)**

NQDM:

```
len_1 = 2.0 
len_2 = 3 

for i in nqdm(len_1, len_2):
  print(i)
```
TQDM:

```
len_1 = 2.0 
len_2 = 3

for i in tqdm(range(int(len_1))):
  for j in tqdm(range(len_2)):
    print([(i, ()), (j, ())])
```

![NQDM_01](https://user-images.githubusercontent.com/46201716/116811201-49422a00-ab48-11eb-8463-7aac66c51bdf.png)

![TQDM_01](https://user-images.githubusercontent.com/46201716/116811230-70006080-ab48-11eb-96e4-83f9214bdf1f.png)


**RESULT:** There are almost no fundamental differences between these approaches. 
However, NQDM is more readable, has a better output format and is simpler.  


**Lists and NumPy arrays**

NQDM:

```
arg_1 = [1, 2, 3]
arg_2 = numpy.array([4, 5, 6])

for i in nqdm(arg_1, arg_2):
  print(i)
```

TQDM:

```
arg_1 = [1, 2, 3]
arg_2 = np.array([4, 5, 6])

for i in tqdm(range(len(arg_1))):
  for j in tqdm(range(len(arg_2))):
    print([(i, (None, arg_1[i])), (j, (None, arg_2[j]))])
```

![NQDM_02](https://user-images.githubusercontent.com/46201716/116811241-85758a80-ab48-11eb-83ff-7f0d37a3662f.png)

![TQDM_02](https://user-images.githubusercontent.com/46201716/116811242-8c9c9880-ab48-11eb-8544-f3808107b89b.png)


**RESULT:** The output of TQDM is hard to interpret. 
NQDM seems to be more beginner-friendly for iterating over multiple arrays at the same time.

**Strings**

NQDM:

```
arg_1 = list("abc")
arg_2 = "cde"

for i in nqdm(arg_1, arg_2):
  print(i)
```

TQDM:

```
arg_1 = list("abc")
arg_2 = "cde"

for i in tqdm(range(len(arg_2))):
  for j in tqdm(range(len(arg_2))):
    print([(i, (None, arg_1[i])), (j, (None, arg_2[i]))])
```

![NQDM_03](https://user-images.githubusercontent.com/46201716/116811247-9b834b00-ab48-11eb-927d-bc6d2ea60fcd.png)

![TQDM_03](https://user-images.githubusercontent.com/46201716/116811250-a50cb300-ab48-11eb-8a40-3f114a9c6e18.png)


**RESULT:** NQDM has many important advantages. It is more readable 
and has just one loop, and you don't really need to deal with converting string
into character array.

**Dictionaries and Pandas Series**

NQDM:

```
arg_1 = {"key1": 4, "key2": 5}
arg_2 = pd.Series(["horse", "cat", "mouse"], index=[978, 979, 980])

for i in nqdm(arg_1, arg_2):
  print(i)
```

TQDM: 

```
arg_1 = {"key1": 4, "key2": 5}
arg_2 = pd.Series(["horse", "cat", "mouse"], index=[978, 979, 980])

for i in tqdm(range(len(arg_1))):
  for j in tqdm(range(len(arg_2))):
    print([(i, list(arg_1.items())[i]),
    (j, list(arg_2.index)[j], list(arg_2.values)[j])
    ])
```

![NQDM_04](https://user-images.githubusercontent.com/46201716/116811259-b05fde80-ab48-11eb-8370-000017f70bf2.png)

![TQDM_04](https://user-images.githubusercontent.com/46201716/116811260-b2c23880-ab48-11eb-8149-43bf92d7e214.png)


**RESULT:** NQDM seems to be better integrated for dicts and Pandas.Series.
That means you may experience a boost in your data science projects switching from TQDM to NQDM!


### A Quick Comparison Of NQDM with TQDM

**3D-Lists:**

NQDM:

```
list_of_list_of_lists = [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
for outer in nqdm(list_of_list_of_lists):
  for middle in nqdm(outer):
    for inner in nqdm(middle):
      print(inner)
```

TQDM:

```
list_of_list_of_lists = [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
for outer in tqdm(list_of_list_of_lists):
  for middle in tqdm(outer):
    for inner in tqdm(middle):
      print(inner)
```

![NQDM_05](https://user-images.githubusercontent.com/46201716/116811272-c4a3db80-ab48-11eb-912a-9c4322ff1ac2.png)

![TQDM_05](https://user-images.githubusercontent.com/46201716/116811276-cf5e7080-ab48-11eb-8841-398d0045672b.png)


**RESULT:** NQDM is having trouble converting any outer NQDM loop's output to input.
It is better using TQDM in the case of multi-level lists for now. It is still an open issue and 
I would like to see your contribution :)

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
* This module still has issues and I would be more than happy to see your contribution :)


