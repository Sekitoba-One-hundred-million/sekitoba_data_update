import os
import glob
import datetime

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
    log_files = glob.glob( LOG_DIR + "*" )
    id_data = { RACE_ID: {}, JOCKEY_ID: {}, HORCE_ID: {}, TRAINER_ID: {} }
    max_timestamp = -1
    file_list = []

    for log_file in log_files:
        day = log_file.split( "/" )[-1].split( "-" )

        if not len( day ) == 3:
            continue
        
        check_day = datetime.datetime( int( day[0] ), int( day[1] ), int( day[2] ) )
        timestamp = int( datetime.datetime.timestamp( check_day ) )
        max_timestamp = max( timestamp, max_timestamp )
        file_list.append( { "timestamp": timestamp, "file": log_file } )

    limit_timestamp = 60 * 60 * 24 * 14 # 二週間
        
    for file_data in file_list:
        diff_timestamp = int( max_timestamp - file_data["timestamp"] )
        
        if diff_timestamp < limit_timestamp:
            print( file_data )
            add_id( file_data["file"], id_data )
    
    f = open( LOG_DIR + "update_id_data.txt", "w" )

    for kind in id_data.keys():
        for str_id in id_data[kind].keys():
            f.write( kind + " " + str_id + "\n" )

    f.close()

if __name__ == "__main__":
    main()
