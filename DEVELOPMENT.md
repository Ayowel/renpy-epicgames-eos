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

## Environment preparation

* Follow the Epic Games Setup instructions in the README
* Create new `game/epic.rpy` and `game/01epic_dev.rpy` files (see instructions in README)
* Install extension build requirements

```sh
pip3 install -r extensions/build-requirements.txt
```

### Download the SDK

The SDK must be present in the `libs` subdirectory for the extension to work. To get the version for which the extension is made, run the following command:

```sh
python3 scripts/get_sdk.py
```

### Running the Authentication tool on Linux

On Linux, you will need a Windows VM to run the Authentication tool and make tests.

Once the tool is running, open your firewall's port `6548` and expose the local auth tool port's externally by running the following command in an administrator terminal:

```sh
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=6548 connectaddress=127.0.0.1 connectport=6547
```

Once this is done, you may run the app from your linux host by setting `config.epic_userlogin` to `'YOUR_VM_IP:6548'`.
`

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

## SDK version update

When updating the SDK:

* Get a new EOS SDK spec file from https://github.com/Ayowel/eos-sdk-json/releases: `wget https://github.com/Ayowel/eos-sdk-json/releases/latest/download/eos-sdk-spec.zip`
* Unzip the downloaded archive: `unzip eos-sdk-spec.zip`
* Update the sdk version json with jq: `jq .metadata -c  < spec/EOS_SDK-*.json > .sdk_version.json`
* Rebuild the c definitions file: `python3 -m epic_api_generator spec/EOS_SDK-*.json -o extensions/epic_eos/epic_eos/cdefs.py`
* Re-download the SDK: `python3 scripts/get_sdk.py`

Note that the `epic_api_generator` module will output a list of functions that could not be associated to a class object. If you do not expect one of the displayed functions to be part of a class, this should be fine.

Once the update is tested:

* Update the README's shield text to match the SDK version
