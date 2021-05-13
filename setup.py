from distutils.core import setup

setup(
    name = 'nqdm',
    packages = ['nqdm'],
    version = '0.1.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'NQDM -- An extension of TQDM which enables you to loop over multiple objects simultaneously, and specify the depth of iteration for each object. It is just pure Python magic, no extra libraries needed. It is customizable, minimal and open source.',
    author = 'Yamac Eren Ay',
    author_email = 'yamacerenay2001@gmail.com',
    url = 'https://github.com/yamaceay/nqdm',
    download_url = "https://github.com/yamaceay/nqdm/archive/refs/tags/v0.1.0.tar.gz",
    keywords = ['nqdm', 'NQDM', "progress bar", "tqdm"],
    classifiers = [],
)