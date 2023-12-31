## !/bin/bash

. ./shell/func.sh

if [ ! -f ${process} ]; then
    touch ${process}
fi

status=0

# スタートする前に抜けがないかを確認
for data in `find ${data_collect_path}/*.py | awk -F '/' '{ print $NF }'`; do
    grep -q ${data} ${start_list}
    
    if [ ! $? -eq 0 ]; then
        status=1
        echo not found start_list ${data_collect}/${data}
    fi
done

for data in `find ${use_data_path}/*.py | awk -F '/' '{ print $NF }'`; do
    grep -q ${data} ${start_list}

    if [ ! $? -eq 0 ]; then
        status=1
        echo not found start_list ${use_data}/${data}
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
