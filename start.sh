while read line
do
    echo start $line
    process=`python $line`

    if [ ! $? -eq 0 ]; then
        echo $process
        exit 1
    fi
done < process.txt
