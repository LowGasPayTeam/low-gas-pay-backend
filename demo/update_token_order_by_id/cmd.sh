#!/bin/sh

# usage:
# 1. update data file
# 2. ./cmd.sh 6

http PUT http://127.0.0.1:9999/api/v1/tokens/$1 < ./data.json
