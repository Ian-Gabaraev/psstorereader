import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psstore-ru",
    version="2.0.0",
    author="Ian Gabaraev",
    author_email="hrattisianees@gmail.com",
    description="Play Station Store Russian Python Interface",
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
       'requests', 'bs4', 'pyyaml', 'asyncio', 'aiohttp'
    ],
    python_requires='>=3.6',
)
