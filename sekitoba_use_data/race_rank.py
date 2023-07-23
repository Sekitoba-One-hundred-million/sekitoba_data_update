import sekitoba_library as lib
import sekitoba_data_manage as dm

def main():
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    race_rank_data = dm.pickle_load( "race_rank_data.pickle" )
    race_money_data = dm.pickle_load( "race_money_data.pickle" )

    for race_id in update_race_id_list:
        if race_id in race_rank_data:
            continue
        
        race_money = race_money_data[race_id]
        race_rank = 0
        
        if race_money <= 500:
            race_rank = 1
        elif race_money <= 1000:
            race_rank = 2
        elif race_money <= 1600:
            race_rank = 3
        else:
            race_rank = 4

        race_rank_data[race_id] = race_rank

    dm.pickle_upload( "race_rank_data.pickle", race_rank_data )

if __name__ == "__main__":
    main()
