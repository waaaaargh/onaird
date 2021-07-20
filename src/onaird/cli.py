"""
Command Line Interface Module.
"""

import os
import sys
import logging
import time
import json
import select

from configparser import SafeConfigParser

import requests
import fire

def onaird_service(config_path: str = "onaird.ini", verbose=False):
    """
    Launch OnAir Host Service.
    """

    logging.basicConfig()
    logging.root.setLevel(logging.INFO)

    # Read Configuration
    logging.info("onaird launching...")

    config = SafeConfigParser(os.environ)
    result = config.read(filenames=[config_path])
    if not result:
        logging.error("error reading config file")
        sys.exit(1)

    from pprint import pprint; pprint(config['onair'])

    if 'onair' not in config:
        sys.exit(1)

    for value in ['ApiBaseUrl', 'ApiKey', 'StateFile', 'Interval', 'DeviceId']:
        if value not in config['onair']:
            logging.error(f"required value {value} not in config file")
            sys.exit(1)

    http_sesn = requests.Session()

    watcher = select.epoll()

    f = open(config['onair']['StateFile'], 'r')
    content = None

    try:
        while(True):
            new_content = f.read()
            if content != new_content:
                webcam_on = ( new_content != "0\n")
                logging.info(f"webcam_on: {webcam_on}")

                res = requests.put(
                    url=f"{config['onair']['ApiBaseUrl']}/devices/{config['onair']['DeviceId']}/status",
                    headers={'x-api-key': config['onair']['ApiKey']},
                    data=json.dumps({'on': webcam_on})
                )

                logging.info(res)

            content = new_content

            f.seek(0)
            time.sleep(float(config['onair']['Interval']))
    except KeyboardInterrupt:
        logging.info("caught KeyboardInterrupt, exiting")
        sys.exit(0)

    

def main():
    fire.Fire(onaird_service)