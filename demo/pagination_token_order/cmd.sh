#!/bin/sh

# usage:
# ./cmd.sh page size address
# ./cmd.sh 1 10 0x123456789

http http://127.0.0.1:9999/api/v1/tokens\?page=$1\&size=$2\&address=$3
