#!/bin/sh

# usage:
# ./cmd.sh order_id
# ./cmd.sh 10

http DELETE http://127.0.0.1:9999/api/v1/tokens/$1
