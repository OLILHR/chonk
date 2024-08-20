<div align="center">

<img width="85%" src="https://raw.githubusercontent.com/OLILHR/epitaxy/main/epitaxy.svg" alt="epitaxy.svg"><br>

<p>🧊 codebase consolidation.</p>

![PyPI status badge](https://img.shields.io/pypi/v/epitaxy?labelColor=30363D&color=fccccc)
![Unittests status badge](https://github.com/OLILHR/epitaxy/workflows/Unittests/badge.svg)
![Coverage status badge](https://github.com/OLILHR/epitaxy/workflows/Coverage/badge.svg)
![Pylint status badge](https://github.com/OLILHR/epitaxy/workflows/Linting/badge.svg)
![Formatting status badge](https://github.com/OLILHR/epitaxy/workflows/Formatting/badge.svg)

</div>

## ℹ️ Installation

```sh
$ pip install epitaxy
```

> [!NOTE]
> It is generally recommended to add an `.epitaxyignore` file to the root directory of the codebase you'd like to consolidate.
> All files, folders and file extensions specified in `.epitaxyignore` will be excluded from the output file.
> Please refer to the `.epitaxyignore.example` for suggestions regarding what to include in `.epitaxyignore`.

To execute the script, simply run

```sh
$ epitaxy
```

and follow the prompts by providing an input directory, an output file destination and optional filters.

Alternatively, the script can be executed using a single command with the appropriate flags:  

```sh
$ epitaxy -i <input_path> -o <output_path> -f <(optional) filters>
```

For further information, run `$ epitaxy --help`.
