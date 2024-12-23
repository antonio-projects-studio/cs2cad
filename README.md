# cs2cad

## Requirements

```sh
conda create -n cs2cad python=3.10
conda activate cs2cad
conda install -c conda-forge pythonocc-core=7.8.1
pip install git+https://github.com/antonio-projects-studio/cs2cad
```

## Usage

```python
from cs2cad import cs2cad

cs2cad(json_file: Path | str | dict, save_path: Path | str, name: str | None = None)
```