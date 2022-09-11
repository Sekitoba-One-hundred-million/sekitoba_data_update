echo \nstart collect/main_data_collect.py
python collect/main_data_collect.py

echo \nstart collect/race_day_get.py
python collect/race_day_get.py

echo \nstart collect/race_money.py
python collect/race_money.py

echo \nstart collect/train_data_collect.py
python collect/train_data_collect.py

echo \nstart collect/wrap_data_collect.py
python collect/wrap_data_collect.py

echo \nstart collect/jockey_id_collect.py
python collect/jockey_id_collect.py

echo \nstart collect/jockey_year_rank_collect.py
python collect/jockey_year_rank_collect.py

echo \nstart collect/jockey_data_collect.py
python collect/jockey_data_collect.py

echo \nstart collect/trainer_id_collect.py
python collect/trainer_id_collect.py

echo \nstart collect/trainer_data_collect.py
python collect/trainer_data_collect.py

echo \nstart create/race_rank.py
python create/race_rank.py

echo \nstart create/race_level.py
python create/race_level.py

echo \nstart create/train_ave_data_create.py
python create/train_ave_data_create.py

echo \nstart create/true_skill_create.py
python create/true_skill_create.py

echo \nfinish sekitoba data update
