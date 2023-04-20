import sekitoba_library as lib
import sekitoba_data_manage as dm

def main():
    prod_race_data_storage = dm.pickle_load( "race_data.pickle", prod = True )
    dev_race_data_storage = dm.pickle_load( "race_data.pickle" )
    race_data = lib.link_prod_dev_data( prod_race_data_storage, dev_race_data_storage )

    prod_race_rank_data = dm.pickle_load( "race_rank_data.pickle", prod = True )
    dev_race_rank_data = dm.pickle_load( "race_rank_data.pickle" )
    race_rank_data = lib.link_prod_dev_data( prod_race_rank_data, dev_race_rank_data )
    
    race_money_data = dm.pickle_load( "race_money_data.pickle", prod = True )

    for k in race_data.keys():
        race_id = lib.id_get( k )

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

    dm.pickle_upload( "race_rank_data.pickle", race_rank_data, prod = True )
    dm.pickle_upload( "race_rank_data.pickle", race_rank_data )

if __name__ == "__main__":
    main()
