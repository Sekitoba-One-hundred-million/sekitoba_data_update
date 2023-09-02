from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def race_course_data_get( url ):
    result = {}
    r, _ = lib.request( url ) #requests.get( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
           and class_name[0] == "RaceData01":
            text_data = div.text.replace( "\n", "" ).split( "/" )[1].split( " " )

            if len( text_data ) == 4:
                result["out_side"] = True
            else:
                result["out_side"] = False

            if text_data[2][1] == "右":
                result["direction"] = 1
            else:
                result["direction"] = 2
                
            break

    return result 

def main():
    result = dm.pickle_load( "race_course_data.pickle" )
    
    if result == None:
        result = {}

    base_url = "https://race.netkeiba.com/race/result.html?race_id="
    update_race_id_data = dm.pickle_load( "update_race_id_list.pickle" )
    url_data = []
    key_data = []

    for race_id in update_race_id_data:
        if race_id in result:
            continue
        
        url = base_url + race_id
        url_data.append( url )
        key_data.append( race_id )
            
    add_data = lib.thread_scraping( url_data, key_data ).data_get( race_course_data_get )
    result.update( lib.thread_scraping( url_data, key_data ).data_get( race_course_data_get ) )    
    dm.pickle_upload( "race_course_data.pickle", result )

main()

