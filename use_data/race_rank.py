import SekitobaLibrary as lib
import SekitobaDataManage as dm

def main():
    race_rank_data = dm.pickle_load( "race_rank_data.pickle" )
    race_money_data = dm.pickle_load( "race_money_data.pickle" )

    for race_id in race_money_data.keys():
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
