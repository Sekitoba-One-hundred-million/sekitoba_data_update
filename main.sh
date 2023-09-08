## !/bin/bash

./shell/file_check.sh

if [ ! $? -eq 0 ]; then
    exit 1
fi

./shell/start.sh
