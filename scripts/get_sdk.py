#!/usr/bin/env python3
"""Download and unpack the Epic Games EOS SDK."""

import hashlib
import json
import os
import shutil
from urllib import request
from zipfile import ZipFile

print('Initialize work directories')
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
out_dir = os.path.join(project_dir, 'libs')
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
    os.mkdir(out_dir)
tmp_dir = os.path.join(project_dir, '.tmpdir')
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

print('Extract target SDK information')
with open(os.path.join(project_dir, '.sdk_version.json'), 'r', encoding='utf8') as f:
    sdk_info = json.load(f)
SDK_VERSION = sdk_info['version']
SDK_URL = sdk_info['source_url']
SDK_CHECKSUM = sdk_info['checksum']['sha256']

sdk_path = os.path.join(tmp_dir, 'SDK.zip')

print('Downloading SDK zip file to', sdk_path)
# For some reason, epic blocks the urllib python agent
req = request.Request(SDK_URL, headers={'user-agent': 'curl/7.81.0'})
with open(sdk_path, 'wb') as out_file:
    with request.urlopen(req) as datastream:
        databuffer = datastream.read()
        out_file.write(databuffer)
        checksum = hashlib.sha256(databuffer).hexdigest()

print(f'Checking SDK zip file checksum (got {checksum})')
assert checksum == SDK_CHECKSUM

print('Unzipping SDK zip file')
with ZipFile(sdk_path, 'r') as zip_handle:
    memberlist = [f for f in zip_handle.filelist if f.filename.startswith('SDK/Bin/')]
    for m in memberlist:
        # Rewrite filename to remove SDK/Bin/ from output path
        m.filename = m.filename[8:]
    assert len(memberlist) > 0
    zip_handle.extractall(out_dir, memberlist)

print('Done')
