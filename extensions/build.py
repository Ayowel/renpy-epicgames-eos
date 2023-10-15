#!/usr/bin/python

import glob
import os
import pyparsing
import zipfile

def hide_py_file(file_content):
    if file_content.strip():
        # Remove all comments and docstrings
        filters = [
            pyparsing.pythonStyleComment.suppress(),
            pyparsing.QuotedString('"""', multiline=True).suppress()
            ]
        for f in filters:
            file_content = f.transformString(file_content)

    return file_content

def package_dir(base_dir, target_file):
    dir_list = [''] # local path in base_dir
    with zipfile.ZipFile(target_file, 'w') as zip:
        for name in ('LICENSE', 'CREDITS'):
            if os.path.exists(f'../{name}'):
                with open(f'../{name}', 'r') as f:
                    zip.writestr(zipfile.ZipInfo(f'{name}.txt'), f.read())
        while len(dir_list) > 0:
            local_dir_path = dir_list.pop(0)
            dir_path = os.path.join(base_dir, local_dir_path)
            for p in os.listdir(dir_path):
                p_path = os.path.join(dir_path, p)
                p_local_path = os.path.join(local_dir_path, p)
                if os.path.isfile(p_path):
                    with open(p_path, 'rb') as f:
                        content = f.read()
                    if p_path.endswith(".py"):
                        content = hide_py_file(content.decode('utf-8'))
                    zip.writestr(zipfile.ZipInfo(p_local_path), content)
                elif os.path.isdir(p_path):
                    dir_list.append(p_local_path)
                else:
                    print('Ignoring {} in {}'.format(p_local_path, base_dir))

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for p in glob.glob('./*/autorun.py'):
        dir_path = os.path.dirname(p)
        print("Creating new archive {}.rpe for extension in {}".format(dir_path, dir_path))
        package_dir(dir_path, os.path.join('..', 'game', "{}.rpe".format(dir_path)))
