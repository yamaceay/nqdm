# NQDM

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
    print([i, j])
```
NQDM:

![NQDM_01](https://user-images.githubusercontent.com/46201716/116820687-87564280-ab76-11eb-9bcb-138aaba6e434.png)

TQDM:

![TQDM_01](https://user-images.githubusercontent.com/46201716/116820698-91784100-ab76-11eb-8a3b-a06c20a3585e.png)


**RESULT:** As it is clear, NQDM is more readable, has a 
better output format, reducing the dimensionality by 1 and is simpler. 


**Lists and NumPy arrays**

NQDM:

```
arg_1 = [1, 2, 3]
arg_2 = np.array([4, 5, 6])

for i in nqdm(arg_1, arg_2):
  print(i)
```

TQDM:

```
arg_1 = [1, 2, 3]
arg_2 = np.array([4, 5, 6])

for i in tqdm(range(len(arg_1))):
  for j in tqdm(arg_2):
    print([arg_1[i], j)
```

NQDM:

![NQDM_02](https://user-images.githubusercontent.com/46201716/116820837-5591ab80-ab77-11eb-9954-f9f9d60d24c9.png)

TQDM:

![TQDM_02](https://user-images.githubusercontent.com/46201716/116820849-68a47b80-ab77-11eb-80a5-27757a1ad5a9.png)



**RESULT:** The output of TQDM is slightly harder to interpret. NQDM seems to be 
more beginner-friendly for iterating over multiple arrays at the same time.

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

for i in tqdm(arg_1):
  for j in tqdm(range(len(arg_2))):
    print([i, arg_2[j]])
```

NQDM:

![NQDM_03](https://user-images.githubusercontent.com/46201716/116821097-c6859300-ab78-11eb-95e9-0a7ec46a4631.png)

QDM:

![TQDM_03](https://user-images.githubusercontent.com/46201716/116821904-43fed280-ab7c-11eb-9532-0e086b0a2c01.png)


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
    print([list(arg_1.items())[i], {arg_2.index[j]: arg_2.values[j]}])
```

NQDM:

![NQDM_04](https://user-images.githubusercontent.com/46201716/116821270-7fe46880-ab79-11eb-9727-875093e7d2c1.png)

TQDM:

![TQDM_04](https://user-images.githubusercontent.com/46201716/116821277-88d53a00-ab79-11eb-9ffa-ef5b6969dfdd.png)


**RESULT:** NQDM seems to be better integrated for dicts and Pandas.Series.
That means you may experience a boost in your data science projects switching from TQDM to NQDM.

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

NQDM:

![NQDM_05](https://user-images.githubusercontent.com/46201716/116821688-29782980-ab7b-11eb-9ca1-4f9ed816daba.png)

TQDM:

![TQDM_05](https://user-images.githubusercontent.com/46201716/116821692-2da44700-ab7b-11eb-84a4-9782ee9312af.png)


**RESULT:** They both have inconsistencies about unfinished progress bars and
newline openings. It is open for discussion, which one would outperform in many
more levels, but still NQDM might be better implemented because of multi-indexing cdapability.

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
