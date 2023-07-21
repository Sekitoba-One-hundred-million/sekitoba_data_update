## !/bin/bash

version=`cat data/version`
version_manage='version-manage'
pickle_info='data/pickle_info.txt'
sekitoba_data_collect='sekitoba_data_collect'
sekitoba_use_data='sekitoba_use_data'

rm -rf ${version_manage}
#git clone -q git@github.com:Sekitoba-One-hundred-million/${version_manage}.git -b ${version}
#cp ${version_manage}/${pickle_info} ${pickle_info}
OLDIFS=${IFS}
IFS=$'\n'
status=0

for data in `cat ${pickle_info} | grep ${sekitoba_data_collect}`; do
    IFS=${OLDIFS}
    data_array=(${data})
    
    if [ ${#data_array[*]} -eq 2 ]; then
        pickle_name=${data_array[0]}
        file_name=${data_array[1]}
        ls ${sekitoba_data_collect} | grep -q ${file_name##*/}

        if [ $? -eq 1 ]; then
            status=1
            echo "not found ${file_name}"
        fi
     fi
done

IFS=$'\n'

for data in `cat ${pickle_info} | grep ${sekitoba_use_data}`; do
    IFS=${OLDIFS}
    data_array=(${data})
    
    if [ ${#data_array[*]} -eq 2 ]; then
        pickle_name=${data_array[0]}
        file_name=${data_array[1]}
        ls ${sekitoba_use_data} | grep -q ${file_name##*/}

        if [ $? -eq 1 ]; then
            status=1
            echo "not found ${file_name}"
        fi
     fi
done

for file_name in `ls ${sekitoba_data_collect}`; do
    grep -q ${file_name} ${pickle_info}

    if [ $? -eq 1 ]; then
        echo "not need ${sekitoba_data_collect}/${file_name}"
    fi
done

for file_name in `ls ${sekitoba_use_data}`; do
    grep -q ${file_name} ${pickle_info}

    if [ $? -eq 1 ]; then
        echo "not need ${sekitoba_use_data}/${file_name}"
    fi
done

exit ${status}
