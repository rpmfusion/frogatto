#!/bin/sh

DATA_DIRECTORY=/usr/share/frogatto
BINARY_FILE=/usr/libexec/frogatto/game

cd $DATA_DIRECTORY
exec $BINARY_FILE "$@"

