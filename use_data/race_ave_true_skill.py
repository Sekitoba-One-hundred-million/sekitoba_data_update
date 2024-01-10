import sekitoba_library as lib
import sekitoba_data_manage as dm

def main():
    result = {}
    race_data = dm.pickle_load( "race_data.pickle" )
    race_info = dm.pickle_load( "race_info_data.pickle" )
    race_day = dm.pickle_load( "race_day.pickle" )
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    true_skill_data = dm.pickle_load( "true_skill_data.pickle" )
    
    for k in race_data.keys():
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        key_place = str( race_info[race_id]["place"] )
        key_dist = str( race_info[race_id]["dist"] )
        key_kind = str( race_info[race_id]["kind"] )        
        key_baba = str( race_info[race_id]["baba"] )

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            continue

        if not race_id in true_skill_data["horce"]:
            continue

        current_true_skill = true_skill_data["horce"][race_id]
        count = 0
        true_skill_list = []
        
        for horce_id in race_data[k].keys():
            current_data, past_data = lib.race_check( horce_data[horce_id], race_day[race_id] )
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            true_skill = 25
            
            if horce_id in current_true_skill:
               true_skill = current_true_skill[horce_id] 

            true_skill_list.append( true_skill )

        if len( true_skill_list ) == 0:
            continue
            
        result[race_id] = sum( true_skill_list ) / len( true_skill_list )

    dm.pickle_upload( "race_ave_true_skill.pickle", result )

if __name__ == "__main__":
    main()
