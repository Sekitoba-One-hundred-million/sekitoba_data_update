echo start collect/main_data_collect.py
python collect/main_data_collect.py

echo start collect/race_day_get.py
python collect/race_day_get.py

echo start collect/race_money.py
python collect/race_money.py

echo start collect/train_data_collect.py
python collect/train_data_collect.py

echo start collect/wrap_data_collect.py
python collect/wrap_data_collect.py

echo start create/race_rank.py
python create/race_rank.py

echo start create/race_level.py
python create/race_level.py

echo start create/train_ave_data_create.py
python create/train_ave_data_create.py

echo start create/true_skill_create.py
python create/true_skill_create.py

echo finish sekitoba data update
