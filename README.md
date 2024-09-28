<div align="center">

<img width="65%" src="https://raw.githubusercontent.com/OLILHR/chonk/main/chonk.svg" alt="chonk.svg"><br>

<p>🧊 codebase consolidation.</p>

![PyPI status badge](https://img.shields.io/pypi/v/chonk?labelColor=30363D&color=fccccc)
![Unittests status badge](https://github.com/OLILHR/chonk/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/OLILHR/chonk/workflows/Coverage/badge.svg)
![Pylint status badge](https://github.com/OLILHR/chonk/workflows/Linting/badge.svg)
![Formatting status badge](https://github.com/OLILHR/chonk/workflows/Formatting/badge.svg)

</div>

## ℹ️ Installation

```sh
$ pip install chonk
```

> [!NOTE]
> It is generally recommended to add a `.chonkignore` file to the root directory of the codebase you wish to consolidate.
> Any files, folders, or file extensions specified in `.chonkignore` will be excluded from the output file.
> Refer to the `.chonkignore.example` for suggestions regarding what to include in `.chonkignore`.

To use this package outside of Python environments, install the package globally and ensure that the Python
executable is added to your system's `PATH`. Execute the script simply by running

```sh
$ chonk
```

and follow the prompts by providing an input directory, an output file destination and optional filters.

Alternatively, the script can be executed using a single command with the appropriate flags:  

```sh
$ chonk -i <input_path> -o <output_path> -f <optional filters>
```

For further information, run `$ chonk --help`.
