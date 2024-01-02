## !/bin/bash

. ./shell/func.sh

sekitoba_data_dir='/Volumes/Gilgamesh/sekitoba-data'
version_path="${sekitoba_data_dir}/${version}"

if [ ! -d "${version_path}" ]; then
    exit 1
fi

IFS=$'\n'

for data in `cat "${pickle_info}"`; do
    IFS=$OLDIFS
    data_array=(${data})
    pickle_name=${data_array[0]}
    file_name=${data_array[1]}

    if [ ${file_name} == "None" ]; then
        continue
    fi
    
    cp "${sekitoba_data_dir}/${pickle_name}" "${version_path}/${pickle_name}"
done
