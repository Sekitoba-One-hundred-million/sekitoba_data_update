## !/bin/bash

./shell/file_check.sh

if [ ! $? -eq 0 ]; then
    echo "fail update"
    exit 1
fi

./shell/start.sh
