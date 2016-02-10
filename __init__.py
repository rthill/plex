#!/usr/bin/env python3
#########################################################################
#  Copyright 2016 Raoul Thill                       raoul.thill@gmail.com
#########################################################################
#  This file is part of SmartHome.py.    http://mknx.github.io/smarthome/
#
#  SmartHome.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHome.py. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
import json
import requests
import random

logger = logging.getLogger('')


class Plex:
    def __init__(self, smarthome, displaytime=6000):
        logger.info("Init Plex notifications")
        self._sh = smarthome
        self._displayTime = int(displaytime)
        self._images = ["info", "error", "warning"]
        self._clients = []

    def run(self):
        pass

    def stop(self):
        pass

    def _push(self, host, data):
        try:
            res = requests.post(host,
                                headers={
                                    "User-Agent": "sh.py",
                                    "Content-Type": "application/json"},
                                timeout=4,
                                data=json.dumps(data),
                                )
            logger.debug(res)
            response = res.text
            del res
            logger.info(response)
        except Exception as e:
            logger.exception(e)

    def notify(self, title, message, image="info"):
        if not image in self._images:
            logger.warn("Plex image must be: {}".format(", ".join(self._images)))
        else:
            data = {"jsonrpc": "2.0",
                    "id": random.randint(1, 99),
                    "method": "GUI.ShowNotification",
                    "params": {"title": title, "message": message, "displaytime": self._displayTime, "image": image}
                    }
            for host in self._clients:
                logger.debug("Plex sending push notification to host {}: {}".format(host, data))
                self._push(host, data)

    def parse_item(self, item):
        if 'plex_host' in item.conf:
            host = item.conf['plex_host']
            if 'plex_port' in item.conf:
                port = item.conf['plex_port']
            else:
                port = 3005
            logger.info("Plex found client {}".format(item))
            self._clients.append('http://' + host + ':' + str(port) + '/jsonrpc')
