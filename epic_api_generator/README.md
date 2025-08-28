# Epic API generator

This python module takes a [JSON API spec](https://github.com/Ayowel/eos-sdk-json) for Epic Game's EOS SDK and generates python-to-c API bindings..

Use this module by moving to its parent directory and invoke it with the directory's name:

```sh
python3 -m epic_api_generator spec/EOS_SDK-*.json -o "extensions/epic_eos/epic_eos/cdefs.py"
```

To debug, call with the logging level set to 0:

```sh
LOGGING_LEVEL=0 python3 -m epic_api_generator spec/EOS_SDK-*.json -o "extensions/epic_eos/epic_eos/cdefs.py"
```
