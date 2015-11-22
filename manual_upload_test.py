#!/usr/bin/python3
# -*- coding: utf-8 -*-

""""
Author:  Jan Harasym <jharasym@linux.com>
Website: dijit.sh

Creation Date: 2015-10-22
Last Modified: Thu 22 Oct 22:52:49 2015

Description:
Expected Use: ./backend_handler.py {filename}
"""

from sys import argv
from hashlib import sha256
from functools import partial
import redis

filename = argv[1]
image = open(filename,'rb').read()

def sha256sum_old(filename):
    d = sha256()
    with filename as f:
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

def sha256sum(image):
    d = sha256()
    d.update(image)
    return d.hexdigest()

def redis_set(hash,image):
    try:
        db = redis.Redis()
        db.setex(hash,image,1000)
        db.setex(hash + '_mime','image/jpeg',1000)
        print(hash)
    except:
        print("Failed to submit to server")

hash = sha256sum(image)
redis_set(hash,image)
