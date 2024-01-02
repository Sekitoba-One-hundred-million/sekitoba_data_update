## !/bin/bash

./shell/file_check.sh

error_log "fail file_check"

./shell/start.sh

error_log "fail data update"

./shell/version_data_update.sh

error_log "fail version data update"

not_need_data_remove
