import sekitoba_library as lib
import sekitoba_data_manage as dm

def main():
    result = {}
    next_race_data = {}
    race_data = dm.pickle_load( "race_data.pickle" )
    race_day = dm.pickle_load( "race_day.pickle" )
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )

    for k in race_data.keys():
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        next_race_data[race_id] = {}
        ymd = { "y": int( year ), "m": race_day[race_id]["month"], "d": race_day[race_id]["day"] }

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            next_cd = lib.next_race( horce_data[horce_id], ymd )

            if not next_cd == None:
                next_race_data[race_id][horce_id] = next_cd

    dm.pickle_upload( "next_race_data.pickle", next_race_data )

if __name__ == "__main__":
    main()
