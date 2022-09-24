import sekitoba_library as lib
import sekitoba_data_manage as dm

import copy
import trueskill

def main():
    result = {}
    horce_rating_data = {}
    env = trueskill.TrueSkill( draw_probability = 0 )
    race_data = dm.pickle_load( "race_data.pickle", prod = True )
    horce_data = dm.pickle_load( "horce_data_storage.pickle", prod = True )
    race_day = dm.pickle_load( "race_day.pickle", prod = True )

    sort_time_data = []

    for k in race_data.keys():
        race_id = lib.id_get( k )
        day = race_day[race_id]
        check_day = datetime.datetime( day["year"], day["month"], day["day"] )
        sort_time_data.append( { "k": k, "time": datetime.datetime.timestamp( check_day ) } )

    sort_time_data = sorted( sort_time_data, key=lambda x: x["time"] )
    
    for std in tqdm( sort_time_data ):
        k = std["k"]
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        rank_list = []
        rating_list = []
        horce_id_list = []
        lib.dic_append( result, race_id, {} )

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            try:
                current_rating = horce_rating_data[horce_id]
            except:
                current_rating = env.create_rating()

            rank = cd.rank()
            result[race_id][horce_id] = copy.deepcopy( current_rating.mu )

            if rank == 0:
                continue

            rank_list.append( int( rank - 1 ) )
            rating_list.append( ( copy.deepcopy( current_rating ), ) )
            horce_id_list.append( horce_id )

        if len( horce_id_list ) < 2:
            continue

        next_rating_list = env.rate( rating_list, ranks=rank_list )

        for i in range( 0, len( next_rating_list ) ):
            horce_rating_data[horce_id_list[i]] = copy.deepcopy( next_rating_list[i][0] )

    dm.pickle_upload( "true_skill_data.pickle", result, prod = True )

if __name__ == "__main__":
    main()
