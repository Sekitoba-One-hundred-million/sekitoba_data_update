## !/bin/bash

OLDIFS=$IFS
sekitoba_update_home=`pwd`
version=`cat ${sekitoba_update_home}/version`
version_manage='version-manage'
data_collect='data_collect'
use_data='use_data'
version_manage_path="${sekitoba_update_home}/${version_manage}"
#sekitoba_data_collect_path="${sekitoba_update_home}/sekitoba_data_collect"
#sekitoba_use_data_path="${sekitoba_update_home}/sekitoba_use_data"
data_collect_path="${sekitoba_update_home}/data_collect"
use_data_path="${sekitoba_update_home}/use_data"

pickle_info="${version_manage_path}/data/pickle_info.txt"
git_commit="${version_manage_path}/data/git-commit.txt"

function git_clone {
    repogitory=$1
    commit=$2
    git_url="ssh://git@github.com/Sekitoba-One-hundred-million/${repogitory}.git"
    git clone -q ${git_url}
    cd ${repogitory}; git checkout -q ${commit}; cd ..
}

function commit_get {
    repogitory=$1
    cat ${git_commit}| grep ${repogitory} | awk -F ' ' '{ print $2 }'
}
