import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nqdm",
    version="0.1.9",
    author="Yamac Eren Ay",
    author_email="yamacerenay2001@gmail.com",
    description="NQDM -- An extension of TQDM which enables you to loop over multiple objects simultaneously, and specify the depth of iteration for each object. It is just pure Python magic, no extra libraries needed. It is customizable, minimal and open source.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yamaceay/nqdm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
          'tqdm==4.6.0'
      ],
    python_requires='>=3.6'
)