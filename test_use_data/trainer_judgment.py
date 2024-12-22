import SekitobaLibrary as lib
import SekitobaDataManage as dm

import copy
import datetime
import trueskill

def main():
    trainer_judgment = {}
    use_trainer_judgment = {}
    race_data = dm.pickle_load( "race_data.pickle" )
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    race_day = dm.pickle_load( "race_day.pickle" )
    race_trainer_id_data = dm.pickle_load( "race_trainer_id_data.pickle" )
    sort_time_data = []
    param_list = [ "limb", "popular", "flame_num", "dist", "kind", "baba", "place" ]

    for k in race_data.keys():
        race_id = lib.idGet( k )
        day = race_day[race_id]
        check_day = datetime.datetime( day["year"], day["month"], day["day"] )
        race_num = int( race_id[-2:] )
        timestamp = int( datetime.datetime.timestamp( check_day ) + race_num )
        sort_time_data.append( { "k": k, "time": timestamp } )

    line_timestamp = 60 * 60 * 24 * 2 - 100 # 2day race_numがあるので -100
    sort_time_data = sorted( sort_time_data, key=lambda x: x["time"] )
    dev_result = {}
    
    for i, std in enumerate( sort_time_data ):
        k = std["k"]
        race_id = lib.idGet( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        dev_result[race_id] = {}
        trainer_id_list = race_trainer_id_data[race_id]

        if not i == 0:
            current_timestamp = std["time"]
            before_timestamp = sort_time_data[i-1]["time"]
            diff_timestamp = int( current_timestamp - before_timestamp )

            if line_timestamp < diff_timestamp:
                use_trainer_judgment = copy.deepcopy( trainer_judgment )

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.raceCheck( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.CurrentData( current_data )
            pd = lib.PastData( past_data, current_data )

            if not cd.raceCheck():
                continue

            if not horce_id in trainer_id_list:
                continue

            first_passing_rank = -1

            try:
                first_passing_rank = int( cd.passingRank().split( "-" )[0] )
            except:
                continue

            trainer_id = trainer_id_list[horce_id]
            limb_math = lib.limbSearch( pd )

            key_data = {}
            key_data["limb"] = str( int( limb_math ) )
            key_data["popular"] = str( int( cd.popular() ) )
            key_data["flame_num"] = str( int( cd.flameNumber() ) )
            key_data["dist"] = str( int( cd.distKind() ) )
            key_data["kind"] = str( int( cd.raceKind() ) )
            key_data["baba"] = str( int( cd.babaStatus() ) )
            key_data["place"] = str( int( cd.place()) )

            if not trainer_id in trainer_judgment:
                trainer_judgment[trainer_id] = {}

            dev_result[race_id][horce_id] = {}
            
            for param in param_list:
                lib.dicAppend( trainer_judgment[trainer_id], param, {} )                
                lib.dicAppend( trainer_judgment[trainer_id][param], key_data[param], { "count": 0, "score" : 0 } )
                trainer_judgment[trainer_id][param][key_data[param]]["score"] += first_passing_rank
                trainer_judgment[trainer_id][param][key_data[param]]["count"] += 1
                
                score = -1000

                if trainer_id in use_trainer_judgment and \
                param in use_trainer_judgment[trainer_id] and \
                key_data[param] in use_trainer_judgment[trainer_id][param] and \
                not use_trainer_judgment[trainer_id][param][key_data[param]]["count"] == 0:
                    score = use_trainer_judgment[trainer_id][param][key_data[param]]["score"] / use_trainer_judgment[trainer_id][param][key_data[param]]["count"]
                    
                dev_result[race_id][horce_id][param] = score

                trainer_judgment[trainer_id][param][key_data[param]]["count"] += 1
                trainer_judgment[trainer_id][param][key_data[param]]["score"] += first_passing_rank

        if race_id == "202306040508":
            break

    for trainer_id in use_trainer_judgment.keys():
        for param in use_trainer_judgment[trainer_id].keys():
            for data in use_trainer_judgment[trainer_id][param].keys():
                use_trainer_judgment[trainer_id][param][data] = use_trainer_judgment[trainer_id][param][data]["score"] / use_trainer_judgment[trainer_id][param][data]["count"]

    dm.pickle_upload( "trainer_judgment_prod_data.pickle", use_trainer_judgment )

if __name__ == "__main__":
    main()
