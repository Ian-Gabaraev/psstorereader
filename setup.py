import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psstore4-ru",
    version="0.0.4",
    author="Ian Gabaraev",
    author_email="hrattisianees@gmail.com",
    description="Play Station 4 Store Russian Python Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ian-Gabaraev/psstorereader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'requests',
       'bs4',
    ],
    python_requires='>=3.6',
)
