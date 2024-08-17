<div align="center">

<img width="65%" src="alloy.svg" alt="alloy">

**codebase consolidation tool.**

![PyPi Status Badge](https://img.shields.io/pypi/v/alloy)
![Unittests status badge](https://github.com/OLILHR/alloy/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/OLILHR/alloy/workflows/Coverage/badge.svg)
![Pylint status badge](https://github.com/OLILHR/alloy/workflows/Linting/badge.svg)
![Formatting status badge](https://github.com/OLILHR/alloy/workflows/Formatting/badge.svg)

</div>


## ℹ️ Installation

```sh
$ pip install git+https://github.com/OLILHR/alloy.git
```

> [!NOTE]
> It is generally recommended to add an `.alloyignore` file to the root directory of the projects you'd like to consolidate.
> All files, folders and file extensions specified in `.alloyignore` will be excluded from the output file.
> Please refer to the `.alloyignore.example` for suggestions regarding what to include in `.alloyignore`.

To execute the script, simply run

```sh
$ alloy
```

and follow the prompts by providing an input directory, an output file destination and optional filters.

Alternatively, the script can also be executed using a single command with the appropriate flags:  

```sh
$ alloy -i <input_path> -o <output_path> -f <(optional) filters>
```

For further information, run `$ alloy --help`.
