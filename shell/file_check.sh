## !/bin/bash

. ./shell/func.sh

git_clone ${version_manage} ${version}

#sekitoba_data_collect_commit=`git_commit ${sekitoba_data_collect}`
#sekitoba_use_data_commit=`git_commit ${sekitoba_use_data}`

#git_clone ${sekitoba_data_collect} ${sekitoba_data_collect_commit}
#git_clone ${sekitoba_use_data} ${sekitoba_use_data_commit}

OLDIFS=${IFS}
IFS=$'\n'
status=0

for data in `cat ${pickle_info} | grep ${data_collect}`; do
    IFS=${OLDIFS}
    data_array=(${data})
    
    if [ ${#data_array[*]} -eq 2 ]; then
        pickle_name=${data_array[0]}
        file_name=${data_array[1]}
        cat ${exclusion} | grep -q ${file_name##*/}

        if [ $? -eq 0 ]; then
            continue
        fi
        
        ls ${data_collect} | grep -q ${file_name##*/}

        if [ $? -eq 1 ]; then
            status=1
            echo "not found ${file_name}"
        fi
     fi
done

IFS=$'\n'

for data in `cat ${pickle_info} | grep ${use_data}`; do
    IFS=${OLDIFS}
    data_array=(${data})
    
    if [ ${#data_array[*]} -eq 2 ]; then
        pickle_name=${data_array[0]}
        file_name=${data_array[1]}

        cat ${exclusion} | grep -q ${file_name##*/}

        if [ $? -eq 0 ]; then
            continue
        fi

        ls ${use_data} | grep -q ${file_name##*/}

        if [ $? -eq 1 ]; then
            status=1
            echo "not found ${file_name}"
        fi
     fi
done

for file_name in `ls ${data_collect}`; do
    grep -q ${file_name} ${pickle_info}

    if [ $? -eq 1 ]; then
        status=1
        echo "not need ${data_collect}/${file_name}"
    fi
done

for file_name in `ls ${use_data}`; do
    grep -q ${file_name} ${pickle_info}

    if [ $? -eq 1 ]; then
        status=1
        echo "not need ${use_data}/${file_name}"
    fi
done

rm -rf ${version_manage_path}

exit ${status}
