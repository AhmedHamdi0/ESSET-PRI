#!/bin/bash

path="/home/esset/FTP/files/config/"

inotifywait -m -r -e close_write "$path" |
while read -r file; do
        echo "Run main algorithm"
        python main_alg.py
done