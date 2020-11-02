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
`docker build -t reversi .`

Play  
`docker run --rm -it reversi python -m reversi`
