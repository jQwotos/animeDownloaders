from __future__ import absolute_import

import argparse
import os
import logging
import glob
import re

from anime_scrapers.scraper_handler import scraper_handler
from anime_scrapers.download_handler import download_handler


parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', type=str, help='''
    Location where the show should be downloaded.
''')
parser.add_argument('-v', '--verbose', action="store_true", help='''
    Set logging level to verbose.
''')
parser.add_argument('-m', '--managed', action="store_true", help='''
    Moves new episode downloads into episode folders.
''')
parser.add_argument('link', type=str, help="Link to show", nargs="?")

args = vars(parser.parse_args())

file_pat = re.compile("([0-9]+).")


def _single_download(data):
    logging.info("Starting a single download.")
    download_handler.resolve(data)


def _multi_download(data):
    logging.info("Starting a multi download")
    [_single_download(x) for x in data['episodes']]


def _remove_temps(files):
    for x in files:
        os.remove(x)


def _remove_previous(data, alreadyDownloaded):
    return [x for x in data['episodes'] if x['epNum'] not in alreadyDownloaded]


def _get_already_downloaded():
    files = glob.glob("*")
    return [
        re.findall(file_pat, x)[0]
        for x in files
        if len(re.findall(file_pat, x)) > 0
    ]


def _managed_download(data):
    title = data['title']
    if not os.path.exists(title):
        logging.info("Folder for '%s' not found. Auto creating..." % (title,))
        os.makedirs(title)
    os.chdir(title)
    _remove_temps(glob.glob("*.tmp"))
    data['episodes'] = _remove_previous(data, _get_already_downloaded())

    _multi_download(data)


def _try_directory(directory):
    if not os.path.exists(directory):
        logging.info(
            "Directory '%s' was not found. Auto creating..."
            % (directory,)
        )
        os.makedirs(directory)
    os.chdir(directory)


def main(args):
    # Setting logging level based on parsed args
    loggingLevel = logging.INFO if args['verbose'] else logging.DEBUG
    logging.basicConfig(level=loggingLevel)

    if args['directory']:
        _try_directory(args['directory'])

    data = scraper_handler.resolve(args['link'])

    if 'episodes' in data:
        _managed_download(data) if args['managed'] else _multi_download(data)
    elif 'sources' in data:
        _single_download(data)
    else:
        logging.critical("'%s' did not match any resolver." % (args['link']))


if __name__ == "__main__":
    main(args)
