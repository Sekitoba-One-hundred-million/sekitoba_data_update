import sekitoba_library as lib
import sekitoba_data_manage as dm

def main():
    result = dm.pickle_load( "race_rank_data.pickle", prod = True )

    if result == None:
        result = {}

    prod_race_data = dm.pickle_load( "race_data.pickle", prod = True )
    race_id_list = list( prod_race_data.keys() )        
    race_money_data = dm.pickle_load( "race_money_data.pickle", prod = True )

    for race_id in race_id_list:
        if race_id in result:
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

        result[race_id] = race_rank

    dm.pickle_upload( "race_rank_data.pickle", result, prod = True )

if __name__ == "__main__":
    main()
