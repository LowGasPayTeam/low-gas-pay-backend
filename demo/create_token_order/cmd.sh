#!/bin/sh

# usage:
# 1. change data file
# 2. ./cmd.sh

http POST http://127.0.0.1:9999/api/v1/tokens < ./data.json --debug
