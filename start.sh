file_check_log=`./file_check.sh`

if [ ! $? -eq 0 ]; then
    echo ${file_check_log}
   exit 1
fi
