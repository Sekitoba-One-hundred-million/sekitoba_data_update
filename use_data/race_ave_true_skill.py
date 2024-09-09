import sekitoba_psql as ps
import sekitoba_library as lib
import sekitoba_data_manage as dm

COLUM_NAME = "race_ave_true_skill"

def main():
    race_ave_true_skill = dm.pickle_load( "race_ave_true_skill.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    race_data = ps.RaceData()
    race_horce_data = ps.RaceHorceData()
    
    for race_id in update_race_id_list:
        race_data.get_all_data( race_id )
        race_horce_data.get_all_data( race_id )

        if race_data.error:
            continue

        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        key_kind = str( race_data.data["kind"] )        

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            continue

        count = 0
        true_skill_list = []
        
        for horce_id in race_horce_data.horce_id_list:
            true_skill_list.append( race_horce_data.data[horce_id]["horce_true_skill"] )

        if len( true_skill_list ) == 0:
            continue
            
        race_ave_true_skill[race_id] = sum( true_skill_list ) / len( true_skill_list )
        race_data.update_data( COLUM_NAME, race_ave_true_skill[race_id], race_id )

    dm.pickle_upload( "race_ave_true_skill.pickle", race_ave_true_skill )

if __name__ == "__main__":
    main()
