import os
import glob

LOG_DIR = "/Volumes/Gilgamesh/sekitoba-log/"
RACE_ID = "race_id"
JOCKEY_ID = "jockey_id"
TRAINER_ID = "trainer_id"
HORCE_ID = "horce_id"

def get_id( str_data, key, id_data ):
    str_id = ""
    split_data = str_data.split( " " )

    for sd in split_data:
        if key in sd:
            str_id = sd.replace( key + ":", "" )
            break

    if not len( str_id ) == 0:
        id_data[key][str_id] = True

def add_id( file_name, id_data ):
    f = open( file_name, "r" )
    all_data = f.readlines()

    for str_data in all_data:
        str_data = str_data.replace( "\n", "" )

        if RACE_ID in str_data:
            get_id( str_data, RACE_ID, id_data )

        if JOCKEY_ID in str_data:
            get_id( str_data, JOCKEY_ID, id_data )

        if HORCE_ID in str_data:
            get_id( str_data, HORCE_ID, id_data )

        if TRAINER_ID in str_data:
            get_id( str_data, TRAINER_ID, id_data )

def main():
    analyze_check_file = LOG_DIR + "analyze_check.txt"
    checked_day = {}
    
    if os.path.isfile( analyze_check_file ):
        f = open( LOG_DIR + "analyze_check.txt", "r" )
        all_data = f.readlines()
        f.close()

        for str_data in all_data:
            day = str_data.replace( "\n", "" )
            checked_day[day] = True

    log_files = glob.glob( LOG_DIR + "*" )
    id_data = { RACE_ID: {}, JOCKEY_ID: {}, HORCE_ID: {}, TRAINER_ID: {} }

    for log_file in log_files:
        day = log_file.split( "/" )[-1]

        if day in checked_day:
            continue

        checked_day[day] = True
        add_id( log_file, id_data )

    f = open( analyze_check_file, "w" )

    for day in checked_day.keys():
        f.write( day + "\n" )
    
    f.close()
    
    f = open( LOG_DIR + "update_id_data.txt", "w" )

    for kind in id_data.keys():
        for str_id in id_data[kind].keys():
            f.write( kind + " " + str_id + "\n" )

    f.close()

if __name__ == "__main__":
    main()
