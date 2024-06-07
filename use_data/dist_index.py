import json
from tqdm import tqdm

import sekitoba_data_manage as dm
import sekitoba_psql as ps

COLUM_NAME = "dist_index"

def main():
    dist_index_data = dm.pickle_load( "dist_index.pickle" )
    race_data = ps.RaceData()
    race_id_list = dm.pickle_load( "update_race_id_list.pickle" )

    for race_id in tqdm( race_id_list ):
        race_data.update_data( COLUM_NAME, json.dumps( dist_index_data, ensure_ascii = False ), race_id )

if __name__ == "__main__":
    main()
