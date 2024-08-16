<div align="center">

<img width="65%" src="alloy.svg" alt="alloy">

**CLI tool to consolidate codebases into single markdown files.**

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
> It is generally recommended to add an `.alloyignore` file to the root directory of the project you'd like to consolidate.
> All extensions, files and directories listed in the `.alloyignore` file will be excluded from the output file.
> Please refer to the `.alloyignore.example` for suggestions on what to include in `.alloyignore`.

To execute the script, either run

```sh
$ alloy
```

to be prompted for an input directory, an output destination for the markdown file as well as optional filters; 
or directly run

```sh
$ alloy -i <input_path> -o <output_path> -f <(optional) filters>
```

For further information, run `$ alloy --help`.
