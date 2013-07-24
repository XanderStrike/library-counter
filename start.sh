#!/bin/bash

sudo screen -d -m -L python /srv/library-counter/counter.py
sudo screen -d -m -L python /srv/library-counter/server.py
