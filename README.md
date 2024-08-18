<div align="center">

<img width="65%" src="" alt="codebase">

**codebase consolidation tool.**

![PyPI status badge](https://img.shields.io/pypi/v/codebase?labelColor=fff8e7&color=fccccc)
![Unittests status badge](https://github.com/OLILHR/codebase/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/OLILHR/codebase/workflows/Coverage/badge.svg)
![Pylint status badge](https://github.com/OLILHR/codebase/workflows/Linting/badge.svg)
![Formatting status badge](https://github.com/OLILHR/codebase/workflows/Formatting/badge.svg)

</div>


## ℹ️ Installation

```sh
pip install git+https://github.com/OLILHR/codebase.git
```

> [!NOTE]
> It is generally recommended to add a `.codebaseignore` file to the root directory of the projects you'd like to consolidate.
> All files, folders and file extensions specified in `.codebaseignore` will be excluded from the output file.
> Please refer to the `.codebaseignore.example` for suggestions regarding what to include in `.codebaseignore`.

To execute the script, simply run

```sh
codebase
```

and follow the prompts by providing an input directory, an output file destination and optional filters.

Alternatively, the script can also be executed using a single command with the appropriate flags:  

```sh
codebase -i <input_path> -o <output_path> -f <(optional) filters>
```

For further information, run `$ codebase --help`.
