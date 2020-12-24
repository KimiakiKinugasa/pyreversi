# Reversi

## Setup

### Clone this repository

```sh
git clone https://github.com/KimiakiKinugasa/reversi.git
poetry install
```

### Install with poetry

```sh
poetry add git+https://github.com/KimiakiKinugasa/reversi.git
```

### Install with pip

```sh
pip install git+https://github.com/KimiakiKinugasa/reversi.git
```

## Play

`python -m reversi`

## Docker

Build  
`docker build -t pyreversi .`

Play  
`docker run --rm -it pyreversi python -m pyreversi`

## Build documentation

```sh
sphinx-apidoc -f -o ./docs ./pyreversi
sphinx-build -b singlehtml ./docs ./docs/_build
```
