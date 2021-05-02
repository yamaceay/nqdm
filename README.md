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

NQDM: 

100%|██████████| 6/6 [00:00<00:00, 18766.46it/s]

[(0, ()), (0, ())]
[(1, ()), (0, ())]
[(0, ()), (1, ())]
[(1, ()), (1, ())]
[(0, ()), (2, ())]
[(1, ()), (2, ())]

TQDM:

 0%|          | 0/2 [00:00<?, ?it/s]
100%|██████████| 3/3 [00:00<00:00, 18531.53it/s]

100%|██████████| 3/3 [00:00<00:00, 20729.67it/s]
100%|██████████| 2/2 [00:00<00:00, 262.59it/s][(0, ()), (0, ())]
[(0, ()), (1, ())]
[(0, ()), (2, ())]
[(1, ()), (0, ())]
[(1, ()), (1, ())]
[(1, ()), (2, ())]

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

NQDM:

100%|██████████| 9/9 [00:00<00:00, 18192.16it/s]

[(0, (None, 1)), (0, (None, 4))]
[(1, (None, 2)), (0, (None, 4))]
[(2, (None, 3)), (0, (None, 4))]
[(0, (None, 1)), (1, (None, 5))]
[(1, (None, 2)), (1, (None, 5))]
[(2, (None, 3)), (1, (None, 5))]
[(0, (None, 1)), (2, (None, 6))]
[(1, (None, 2)), (2, (None, 6))]
[(2, (None, 3)), (2, (None, 6))]

TQDM:

 0%|          | 0/3 [00:00<?, ?it/s]
100%|██████████| 3/3 [00:00<00:00, 3830.41it/s]

100%|██████████| 3/3 [00:00<00:00, 20593.96it/s]

100%|██████████| 3/3 [00:00<00:00, 20901.85it/s]
100%|██████████| 3/3 [00:00<00:00, 285.69it/s][(0, (None, 1)), (0, (None, 4))]
[(0, (None, 1)), (1, (None, 5))]
[(0, (None, 1)), (2, (None, 6))]
[(1, (None, 2)), (0, (None, 4))]
[(1, (None, 2)), (1, (None, 5))]
[(1, (None, 2)), (2, (None, 6))]
[(2, (None, 3)), (0, (None, 4))]
[(2, (None, 3)), (1, (None, 5))]
[(2, (None, 3)), (2, (None, 6))]

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

NQDM:

100%|██████████| 9/9 [00:00<00:00, 20460.02it/s]

[(0, (None, 'a')), (0, (None, 'c'))]
[(1, (None, 'b')), (0, (None, 'c'))]
[(2, (None, 'c')), (0, (None, 'c'))]
[(0, (None, 'a')), (1, (None, 'd'))]
[(1, (None, 'b')), (1, (None, 'd'))]
[(2, (None, 'c')), (1, (None, 'd'))]
[(0, (None, 'a')), (2, (None, 'e'))]
[(1, (None, 'b')), (2, (None, 'e'))]
[(2, (None, 'c')), (2, (None, 'e'))]

TQDM:

  0%|          | 0/3 [00:00<?, ?it/s]
100%|██████████| 3/3 [00:00<00:00, 10356.31it/s]

100%|██████████| 3/3 [00:00<00:00, 3929.70it/s]

100%|██████████| 3/3 [00:00<00:00, 17073.15it/s]
100%|██████████| 3/3 [00:00<00:00, 111.40it/s][(0, (None, 'a')), (0, (None, 'c'))]
[(0, (None, 'a')), (1, (None, 'c'))]
[(0, (None, 'a')), (2, (None, 'c'))]
[(1, (None, 'b')), (0, (None, 'd'))]
[(1, (None, 'b')), (1, (None, 'd'))]
[(1, (None, 'b')), (2, (None, 'd'))]
[(2, (None, 'c')), (0, (None, 'e'))]
[(2, (None, 'c')), (1, (None, 'e'))]
[(2, (None, 'c')), (2, (None, 'e'))]

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

NQDM:

100%|██████████| 6/6 [00:00<00:00, 13789.49it/s]

[(0, ('key1', 4)), (0, (978, 'horse'))]
[(1, ('key2', 5)), (0, (978, 'horse'))]
[(0, ('key1', 4)), (1, (979, 'cat'))]
[(1, ('key2', 5)), (1, (979, 'cat'))]
[(0, ('key1', 4)), (2, (980, 'mouse'))]
[(1, ('key2', 5)), (2, (980, 'mouse'))]

TQDM:

 0%|          | 0/2 [00:00<?, ?it/s]
100%|██████████| 3/3 [00:00<00:00, 11066.77it/s]

100%|██████████| 3/3 [00:00<00:00, 3534.53it/s]
100%|██████████| 2/2 [00:00<00:00, 61.71it/s][(0, ('key1', 4)), (0, 978, 'horse')]
[(0, ('key1', 4)), (1, 979, 'cat')]
[(0, ('key1', 4)), (2, 980, 'mouse')]
[(1, ('key2', 5)), (0, 978, 'horse')]
[(1, ('key2', 5)), (1, 979, 'cat')]
[(1, ('key2', 5)), (2, 980, 'mouse')]

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

NQDM:

0it [00:00, ?it/s]
0it [00:00, ?it/s]

100%|██████████| 1/1 [00:00<00:00, 1583.95it/s]
100%|██████████| 1/1 [00:00<00:00, 48.68it/s]

0it [00:00, ?it/s]

100%|██████████| 1/1 [00:00<00:00, 6797.90it/s]
100%|██████████| 1/1 [00:00<00:00, 131.54it/s]
100%|██████████| 2/2 [00:00<00:00, 48.77it/s]



[(0, (None, (0, (None, (0, (None, [[0, 1], [2, 3]]))))))]


[(0, (None, (0, (None, (1, (None, [[4, 5], [6, 7]]))))))]


TQDM:

0%|          | 0/2 [00:00<?, ?it/s]
  0%|          | 0/2 [00:00<?, ?it/s]

100%|██████████| 2/2 [00:00<00:00, 10866.07it/s]


100%|██████████| 2/2 [00:00<00:00, 12175.05it/s]
100%|██████████| 2/2 [00:00<00:00, 426.66it/s]

  0%|          | 0/2 [00:00<?, ?it/s]

100%|██████████| 2/2 [00:00<00:00, 17886.16it/s]


100%|██████████| 2/2 [00:00<00:00, 16844.59it/s]
100%|██████████| 2/2 [00:00<00:00, 214.28it/s]
100%|██████████| 2/2 [00:00<00:00, 56.65it/s]0
1
2
3
4
5
6
7

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


