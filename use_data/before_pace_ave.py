import json
import copy
import datetime
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
import sekitoba_psql as ps

COLUM_NAME = "before_pace"

def analyze( data ):
    result = {}

    for key in data.keys():
        result[key] = data[key]["data"] / data[key]["count"]

    return result

def main():
    prod_result = {}
    dev_result = {}
    analyze_data = {}
    race_data = ps.RaceData()
    prod_data = ps.ProdData()
    race_id_list = race_data.get_all_race_id()
    day_data = race_data.get_select_data( "year,month,day" )
    race_data.add_colum( COLUM_NAME, "{}" )
    prod_data.add_colum( COLUM_NAME, "{}" )
    time_data = []

    for race_id in day_data.keys():
        check_day = datetime.datetime( day_data[race_id]["year"], day_data[race_id]["month"], + day_data[race_id]["day"] )        
        time_data.append( { "race_id": race_id, \
                           "time": datetime.datetime.timestamp( check_day ) } )

    line_timestamp = 60 * 60 * 24 * 2 - 100 # 2day race_numがあるので -100
    sort_time_data = sorted( time_data, key=lambda x: x["time"] )
    count = 0

    for std in tqdm( sort_time_data ):
        race_id = std["race_id"]
        race_data.get_all_data( race_id )

        if not count == 0:
            current_timestamp = std["time"]
            before_timestamp = sort_time_data[count-1]["time"]
            diff_timestamp = int( current_timestamp - before_timestamp )

            if line_timestamp < diff_timestamp:
                prod_result = analyze( analyze_data )

        count += 1
        dev_result[race_id] = copy.deepcopy( prod_result )

        if len( race_data.data["wrap"] ) == 0:
            continue

        key_dist = str( race_data.data["dist"] )
        lib.dic_append( analyze_data, key_dist, { "count": 0, "data": 0 } )        
        before_pace, after_pace = lib.before_after_pace( race_data.data["wrap"] )
        analyze_data[key_dist]["count"] += 1
        analyze_data[key_dist]["data"] += before_pace

    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )

    for race_id in update_race_id_list:
        if race_id in dev_result:
            race_data.update_data( COLUM_NAME, json.dumps( dev_result[race_id], ensure_ascii = False ), race_id )
    
    prod_result = analyze( analyze_data )
    prod_data.update_data( COLUM_NAME, json.dumps( prod_result, ensure_ascii = False ) )
    dm.pickle_upload( "before_pace_ave_data.pickle", dev_result )
    dm.pickle_upload( "prod_before_pace_ave_data.pickle", prod_result )

if __name__ == "__main__":
    main()
