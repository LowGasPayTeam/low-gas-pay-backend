#!/bin/sh

# usage:
# 1. change data file
# 2. ./cmd.sh

http POST https://lowgaspay.com/api/v1/nfts < ./data.json --debug
