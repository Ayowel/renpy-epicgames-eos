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
* Create a new `game/epic.rpy` file (see usage instructions in README)
* Create a new `game/01epic_dev.rpy` with the following content:

```py
define config.epic_log_console = True # Enable console logging
define config.epic_userlogin = 'localhost:6547' # Dev auth tool address:port
define config.epic_userpassword = 'username_key' # The username key configured in the dev auth tool
define config.epic_authtype = 'developer' # Enable dev auth tool usage

init python:
    # Remove dev file from release
    build.classify('game/01epic_dev.rpy', None)
    build.classify('game/01epic_dev.rpyc', None)
```

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
