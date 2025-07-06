#!/usr/bin/env python3
"""
CLI entrypoint for python file generation from EOS SDK spec
"""

import argparse
import json
import logging
import os
import sys
from . import SpecManager

logger = logging.getLogger()

def main():
    """Cli main"""
    logging_level = int(os.environ.get('LOGGING_LEVEL', logging.INFO) or logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging_level)
    logger.setLevel(logging_level)
    logger.addHandler(handler)

    ap = argparse.ArgumentParser()
    ap.add_argument("api_json", default="-", nargs='?', help='Path to the JSON spec file for the EOS API')
    ap.add_argument("-o", "--output", default="-", help='Path to the output dll load file')
    args = ap.parse_args()

    if args.api_json == '-':
        logger.info('Reading from standard input.')
        input_stream = sys.stdin
    else:
        logger.info('Reading from %s.', args.api_json)
        input_stream = open(args.api_json, "r", encoding = 'utf8')
    with input_stream as f:
        api = json.load(f)

    spec = SpecManager()
    spec.ingest_spec(api)

    if args.output == '-':
        logger.info('Writing to standard output.')
        writer = sys.stdout
    else:
        logger.info('Writing to %s.', args.output)
        writer = open(args.output, "w", encoding = 'utf8')

    with writer as out:
        spec.render(out)

if __name__ == "__main__":
    main()
