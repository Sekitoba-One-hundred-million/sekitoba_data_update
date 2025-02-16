import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

import copy
import json
import datetime
import trueskill
from tqdm import tqdm

COLUM_NAME = "up3_true_skill"

def main():
    horce_rating_data = {}
    jockey_rating_data = {}
    trainer_rating_data = {}
    use_jockey_rateing = {}
    use_trainer_rateing = {}
    env = trueskill.TrueSkill( draw_probability = 0, beta = 12 )
    race_data = ps.RaceData()
    race_horce_data = ps.RaceHorceData()
    horce_data = ps.HorceData()
    jockey_data = ps.JockeyData()
    trainer_data = ps.TrainerData()
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    day_data = race_data.get_select_data( "year,month,day" )
    time_data = []

    for race_id in day_data.keys():
        if not race_id in update_race_id_list:
            continue
        
        check_day = datetime.datetime( day_data[race_id]["year"], day_data[race_id]["month"], + day_data[race_id]["day"] )        
        time_data.append( { "race_id": race_id, \
                           "time": datetime.datetime.timestamp( check_day ) } )

    line_timestamp = 60 * 60 * 24 * 2 - 100 # 2day race_numがあるので -100
    sort_time_data = sorted( time_data, key=lambda x: x["time"] )
    count = 0
    dev_result = { "horce": {}, "jockey": {}, "trainer": {} }

    horce_rating_data = horce_data.get_select_all_data( COLUM_NAME )
    jockey_rating_data = jockey_data.get_select_all_data( COLUM_NAME )
    trainer_rating_data = trainer_data.get_select_all_data( COLUM_NAME )

    for horce_id in horce_rating_data.keys():
        horce_rating_data[horce_id] = env.create_rating( mu = horce_rating_data[horce_id] )

    for jockey_id in jockey_rating_data.keys():
        jockey_rating_data[jockey_id] = env.create_rating( mu = jockey_rating_data[jockey_id] )
        use_jockey_rateing[jockey_id] = env.create_rating( mu = jockey_rating_data[jockey_id] )

    for trainer_id in trainer_rating_data.keys():
        trainer_rating_data[trainer_id] = env.create_rating( mu = trainer_rating_data[trainer_id] )
        use_trainer_rateing[trainer_id] = env.create_rating( mu = trainer_rating_data[trainer_id] )

    for std in tqdm( sort_time_data ):
        race_id = std["race_id"]
        race_data.get_all_data( race_id )
        race_horce_data.get_all_data( race_id )
        horce_data.get_multi_data( race_horce_data.horce_id_list )
        
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]
        ymd = { "year": race_data.data["year"], "month": race_data.data["month"], "day": race_data.data["day"] }
        
        dev_result["horce"][race_id] = {}
        dev_result["jockey"][race_id] = {}
        dev_result["trainer"][race_id] = {}
        rank_list = []
        rating_list = []
        use_jockey_id_list = []
        use_trainer_id_list = []
        use_horce_id_list = []

        if not count == 0:
            current_timestamp = std["time"]
            before_timestamp = sort_time_data[count-1]["time"]
            diff_timestamp = int( current_timestamp - before_timestamp )

            if line_timestamp < diff_timestamp:
                use_jockey_rateing = copy.deepcopy( jockey_rating_data )
                use_trainer_rateing = copy.deepcopy( trainer_rating_data )

        count += 1
        up3_data = {}

        for horce_id in race_horce_data.horce_id_list:
            current_data, past_data = lib.race_check( horce_data.data[horce_id]["past_data"], ymd )
            cd = lib.CurrentData( current_data )
            pd = lib.PastData( past_data, current_data, race_data )

            if not cd.race_check():
                continue

            up3_data[horce_id] = cd.up_time()

        sort_up3_list = sorted( up3_data.values() )

        for horce_id in race_horce_data.horce_id_list:
            current_data, past_data = lib.race_check( horce_data.data[horce_id]["past_data"], ymd )
            cd = lib.CurrentData( current_data )
            pd = lib.PastData( past_data, current_data, race_data )

            if not cd.race_check():
                continue

            jockey_id = race_horce_data.data[horce_id]["jockey_id"]
            trainer_id = race_horce_data.data[horce_id]["trainer_id"]

            if not horce_id in horce_rating_data:
                horce_rating_data[horce_id] = env.create_rating()

            if not jockey_id in jockey_rating_data:
                jockey_rating_data[jockey_id] = env.create_rating()
                use_jockey_rateing[jockey_id] = env.create_rating()
                
            if not trainer_id in trainer_rating_data:
                trainer_rating_data[trainer_id] = env.create_rating()
                use_trainer_rateing[trainer_id] = env.create_rating()

            horce_current_rating = horce_rating_data[horce_id]
            jockey_current_rating = jockey_rating_data[jockey_id]
            trainer_current_rating = trainer_rating_data[trainer_id]
            
            use_jockey_current_rateing = use_jockey_rateing[jockey_id]
            use_trainer_current_rateing = use_trainer_rateing[trainer_id]
            rank = sort_up3_list.index( up3_data[horce_id] )

            rank_list.append( int( rank - 1 ) )
            use_horce_id_list.append( horce_id )
            use_jockey_id_list.append( jockey_id )
            use_trainer_id_list.append( trainer_id )
            dev_result["horce"][race_id][horce_id] = horce_current_rating.mu
            dev_result["jockey"][race_id][jockey_id] = use_jockey_current_rateing.mu
            dev_result["trainer"][race_id][trainer_id] = use_trainer_current_rateing.mu
            rating_list.append( ( copy.deepcopy( horce_current_rating ), copy.deepcopy( jockey_current_rating ), copy.deepcopy( trainer_current_rating ) ) )

        if len( use_horce_id_list ) < 2:
            continue

        next_rating_list = env.rate( rating_list, ranks=rank_list )

        for i in range( 0, len( next_rating_list ) ):
            horce_rating_data[use_horce_id_list[i]] = copy.deepcopy( next_rating_list[i][0] )
            jockey_rating_data[use_jockey_id_list[i]] = copy.deepcopy( next_rating_list[i][1] )
            trainer_rating_data[use_trainer_id_list[i]] = copy.deepcopy( next_rating_list[i][2] )

    up3_true_skill_data = dm.pickle_load( "up3_true_skill_data.pickle" )
    up3_true_skill_prod_data = dm.pickle_load( "up3_true_skill_prod_data.pickle" )
    update_horce_id_list = dm.pickle_load( "update_horce_id_list.pickle" )

    for horce_id in horce_rating_data.keys():
        up3_true_skill_prod_data["horce"][horce_id] = horce_rating_data[horce_id].mu

        if horce_id in update_horce_id_list:
            horce_data.update_data( COLUM_NAME, up3_true_skill_prod_data["horce"][horce_id], horce_id )

    for jockey_id in jockey_rating_data.keys():
        up3_true_skill_prod_data["jockey"][jockey_id] = jockey_rating_data[jockey_id].mu
        ps.JockeyData().update_data( COLUM_NAME, up3_true_skill_prod_data["jockey"][jockey_id], jockey_id )

    for trainer_id in trainer_rating_data.keys():
        up3_true_skill_prod_data["trainer"][trainer_id] = trainer_rating_data[trainer_id].mu
        ps.TrainerData().update_data( COLUM_NAME, up3_true_skill_prod_data["trainer"][trainer_id], trainer_id )

    for race_id in update_race_id_list:
        for kind in dev_result.keys():
            if not race_id in dev_result[kind]:
                continue

            up3_true_skill_data[kind][race_id] = {}
            for kind_id in dev_result[kind][race_id].keys():
                race_horce_data.update_data( kind + "_" + COLUM_NAME, \
                                            dev_result[kind][race_id][kind_id], \
                                            race_id, kind_id, kind + "_id" )
                up3_true_skill_data[kind][race_id][kind_id] = dev_result[kind][race_id][kind_id]

    dm.pickle_upload( "up3_true_skill_data.pickle", up3_true_skill_data )
    dm.pickle_upload( "up3_true_skill_prod_data.pickle", up3_true_skill_prod_data )

if __name__ == "__main__":
    main()
