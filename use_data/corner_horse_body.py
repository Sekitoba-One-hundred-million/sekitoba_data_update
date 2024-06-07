import sekitoba_psql as ps
import sekitoba_library as lib
import sekitoba_data_manage as dm

import json

COLUM_NAME = "corner_horce_body"

def main():
    result = {}
    test = {}
    corner_rank = dm.pickle_load( "corner_rank_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    
    for race_id in corner_rank.keys():
        for corner in corner_rank[race_id].keys():
            if len( corner_rank[race_id][corner] ) == 0:
                continue

            lib.dic_append( result, race_id, {} )
            result[race_id][corner] = {}
            hb = 0
            box = False
            skip = False
            cr = corner_rank[race_id][corner]

            for i in range( 0, len( cr ) ):
                if skip:
                    skip = False
                    continue
                
                if cr[i] == "(":
                    box = True
                    
                    if not i == 0:
                        hb += 1
                    
                elif cr[i] == ")":
                    box = False
                    hb += 1
                elif not box and cr[i] == ",":
                    hb += 1.5
                elif cr[i] == "-":
                    hb += 3.5
                elif cr[i] == "=":
                    hb += 6

                if str.isdecimal( cr[i] ):
                    c = cr[i]

                    if not i == len( cr ) - 1 and str.isdecimal( cr[i+1] ):
                        c += cr[i+1]
                        skip = True
                        
                    result[race_id][corner][c] = hb

                    if 100 < hb:
                        test[race_id] = 0

    for k in test.keys():
        result.pop( k )

    for race_id in update_race_id_list:
        ps.RaceData().update_data( COLUM_NAME,
                                  json.dumps( result[race_id], ensure_ascii = False ),
                                  race_id )
    
    dm.pickle_upload( "corner_horce_body.pickle", result )
                    
main()        
            

