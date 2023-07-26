## !/bin/bash

start_list='data/start_list.txt'
process='process.txt'

file_check_log=`./file_check.sh`

if [ ! $? -eq 0 ]; then
    echo ${file_check_log}
    exit 1
fi

if [ ! -f ${process} ]; then
    touch ${process}
fi

status=0

# スタートする前に抜けがないかを確認
for data in `find sekitoba_data_collect/*.py`; do
    grep -q ${data} ${start_list}

    if [ ! $? -eq 0 ]; then
        status=1
        echo not found start_list ${data}
    fi
done

for data in `find sekitoba_use_data/*.py`; do
    grep -q ${data} ${start_list}

    if [ ! $? -eq 0 ]; then
        status=1
        echo not found start_list ${data}
    fi
done

for data in `cat ${start_list}`; do
    find ./ | grep -q ${data}

    if [ ! $? -eq 0 ]; then
        status=1
        echo not found file ${data}
    fi
done

if [ ! ${status} -eq 0 ]; then
    exit ${status}
fi

# pythonファイルの実行
for data in `cat ${start_list}`; do
    grep -q ${data} ${process}

    if [ $? -eq 0 ]; then
        continue
    fi

    echo ${data}
    log=`python ${data}`

    if [ ! $? -eq 0 ]; then
        echo ${log}
        exit 1
    fi
    
    echo ${data} >> ${process}
done

rm process.txt
