import sekitoba_library as lib
import sekitoba_data_manage as dm

import copy
import datetime
import trueskill

def main():
    horce_rating_data = {}
    jockey_rating_data = {}
    env = trueskill.TrueSkill( draw_probability = 0, beta = 12 )
    race_data = dm.pickle_load( "race_data.pickle" )
    horce_data = dm.pickle_load( "horce_data_storage.pickle", prod = True )
    race_day = dm.pickle_load( "race_day.pickle", prod = True )
    race_jockey_id_data = dm.pickle_load( "race_jockey_id_data.pickle" )
    
    sort_time_data = []

    for k in race_data.keys():
        race_id = lib.id_get( k )
        day = race_day[race_id]
        check_day = datetime.datetime( day["year"], day["month"], day["day"] )
        sort_time_data.append( { "k": k, "time": datetime.datetime.timestamp( check_day ) } )

    sort_time_data = sorted( sort_time_data, key=lambda x: x["time"] )
    
    for std in sort_time_data:
        k = std["k"]
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        jockey_id_list = race_jockey_id_data[race_id]
        rank_list = []
        rating_list = []
        use_jockey_id_list = []
        use_horce_id_list = []

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            try:
                jockey_id = jockey_id_list[horce_id]
            except:
                continue
            
            try:
                jockey_current_rating = jockey_rating_data[jockey_id]
            except:
                jockey_current_rating = env.create_rating()

            try:
                horce_current_rating = horce_rating_data[horce_id]
            except:
                horce_current_rating = env.create_rating()

            rank = cd.rank()

            if rank == 0:
                continue

            rank_list.append( int( rank - 1 ) )
            use_jockey_id_list.append( jockey_id )
            use_horce_id_list.append( horce_id )
            rating_list.append( ( copy.deepcopy( horce_current_rating ), copy.deepcopy( jockey_current_rating ) ) )

        if len( use_horce_id_list ) < 2:
            continue

        next_rating_list = env.rate( rating_list, ranks=rank_list )

        for i in range( 0, len( next_rating_list ) ):
            horce_rating_data[use_horce_id_list[i]] = copy.deepcopy( next_rating_list[i][0] )
            jockey_rating_data[use_jockey_id_list[i]] = copy.deepcopy( next_rating_list[i][1] )

    result = { "horce": {}, "jockey": {} }

    for horce_id in horce_rating_data.keys():
        result["horce"][horce_id] = horce_rating_data[horce_id].mu

    for jockey_id in jockey_rating_data.keys():
        result["jockey"][jockey_id] = jockey_rating_data[jockey_id].mu
        
    dm.pickle_upload( "true_skill_data.pickle", result, prod = True )
    dm.pickle_upload( "horce_jockey_true_skill_data.pickle", result )

if __name__ == "__main__":
    main()
