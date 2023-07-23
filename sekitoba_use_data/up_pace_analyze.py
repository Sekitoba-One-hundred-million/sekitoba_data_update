import math
from tqdm import tqdm
import matplotlib.pyplot as plt

import sekitoba_library as lib
import sekitoba_data_manage as dm

horce_data = dm.pickle_load( "horce_data_storage.pickle" )

def analyze( race_data ):    
    result = {}
    finish_horce = {}

    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]
        
        for kk in race_data[k].keys():
            horce_name = kk.replace( " ", "" )

            try:
                a = finish_horce[horce_name]
            except:
                finish_horce[horce_name] = True
                str_data = horce_data[horce_name]

                for i in range( 0, len( str_data ) ):
                    cd = lib.current_data( str_data[i] )

                    if not cd.race_check():
                        continue

                    k_dist = int( cd.dist() * 1000 )
                    race_kind = cd.race_kind()

                    if not k_dist == 0 \
                    and not race_kind == 0:
                        key_dist = str( k_dist )
                        key_kind = str( int( race_kind ) )
                        lib.dic_append( result, key_kind, {} )
                        lib.dic_append( result[key_kind], key_dist, { "pace": [], "up_time": [] } )
                    
                        pace1, pace2 = cd.pace()
                        up_time = cd.up_time()
                        result[key_kind][key_dist]["pace"].append( pace1 - pace2 )
                        result[key_kind][key_dist]["up_time"].append( up_time )
                    
    return result

def main():
    regressin_data = {}
    
    race_data = dm.pickle_load( "race_data.pickle" )
    analyze_data = analyze( race_data )

    for k in analyze_data.keys():
        for kk in analyze_data[k].keys():
            lib.dic_append( regressin_data, k, {} )
            lib.dic_append( regressin_data[k], kk, { "a": 0, "b": 0 } )
            a, b = lib.xy_regression_line( analyze_data[k][kk]["pace"], analyze_data[k][kk]["up_time"] )
            regressin_data[k][kk]["a"] = a
            regressin_data[k][kk]["b"] = b

    dm.pickle_upload( "up_pace_regressin.pickle", regressin_data )

if __name__ == "__main__":
    main()
