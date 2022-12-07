# Development guideline

## Pre-requisites

The following instructions require a Windows environment to work as intended.
If you run Linux, use a Virtual Machine to perform the documented steps.

* This repository
* The latest supported Ren'Py version
* The Epic Games EOS SDK dev Authentication tool (Available in the EOS SDK archive)
* Python 3

Hereafter, instructions assume that Ren'Py is in the `PATH` and that the
terminal is in this repository's directory.

## Environment setup

* Follow the Epic Games Setup instructions in the README
* Create new `game/epic.rpy` and `game/01epic_dev.rpy` files (see instructions in README)
* Install extension build requirements

```sh
pip3 install -r extensions/build-requirements.txt
```

## Development

* Ensure that the Dev auth tool from the EOS SDK is running and configured according to the content of `game/01epic_dev.rpy`
* Build the `epic_eos` extension

```sh
python3 extensions/build.py
```

* Run the Ren'Py game

```sh
renpy . run
```
