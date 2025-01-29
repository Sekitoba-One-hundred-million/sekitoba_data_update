## !/bin/bash

OLDIFS=$IFS
sekitoba_update_home=`pwd`
version=`cat ${sekitoba_update_home}/version`
version_manage='version-manage'
data_collect='data_collect'
use_data='use_data'
config_path="${sekitoba_update_home}/config"
version_manage_path="${sekitoba_update_home}/${version_manage}"
data_collect_path="${sekitoba_update_home}/data_collect"
use_data_path="${sekitoba_update_home}/use_data"
start_list="${config_path}/start_list.txt"
process="${sekitoba_update_home}/process.txt"

pickle_info="${version_manage_path}/data/pickle_info.txt"
git_commit="${version_manage_path}/data/git-commit.txt"
exclusion="${config_path}/exclusion.txt"

ATHENA_HOST='Athena'
predictServerName='predict-server'
proxyServerName='proxy-server'

function startPredictServer {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  cd /home/athena/ghq/github.com/Sekitoba-One-hundred-million/predict-server
  tmux new-session -d -s "${predictServerName}" 'python main.py'
EOC
}

function stopPredictServer {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  pgrep -f "${predictServerName}" | xargs kill
EOC
}

function startSekitobaProxy {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  cd /home/athena/ghq/github.com/Sekitoba-One-hundred-million/proxy-manage
  go build
  tmux new-session -d -s "${proxyServerName}" './sekitoba-proxy-manage'
EOC
}

function stopServer {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  pgrep sekitoba-proxy | xargs kill
  sleep 20
  pgrep -f "${predictServerName}" | xargs kill
EOC
  echo "Stop Server"
}

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

function not_need_data_remove {
    rm -rf ${version_manage_path}
}

function error_log {
    if [ ! $? -eq 0 ]; then
        echo $1
        not_need_data_remove
        exit 1
    fi
}
