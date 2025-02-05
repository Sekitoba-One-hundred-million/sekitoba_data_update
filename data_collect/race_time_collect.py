from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def time_get( soup ):
    race_time = 0
    span_tag = soup.findAll( "span" )

    for span in span_tag:
        class_name = span.get( "class" )

        if not class_name == None \
          and class_name[0] == "RaceTime":
            try:
                race_time = lib.time( span.text )
                break
            except:
                continue
            
        
    return race_time

def dist_get( soup ):
    dist = 0
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
          and class_name[0] == "RaceData01":
            span = div.find( "span" )
            dist = int( lib.k_dist( span.text ) * 1000 )

            if not dist == 0:
                break

    return dist

def data_get( url ):
    result = {}
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result

    soup = BeautifulSoup( r.content, "html.parser" )

    result["time"] = time_get( soup )
    result["dist"] = dist_get( soup )

def main():
    result = dm.pickle_load( "race_time_data.pickle" )

    if result == None:
        result = {}
        
    update_race_id_data = dm.pickle_load( "update_race_id_list.pickle" )
    url_data = []
    key_data = []

    for race_id in update_race_id_data:
        year = race_id[0:4]

        if race_id in result:
            continue
        
        url = "https://race.netkeiba.com/race/result.html?race_id=" + race_id
        url_data.append( url )
        key_data.append( race_id )

    result.update( lib.ThreadScraping( url_data, key_data ).data_get( data_get ) )    
    dm.pickle_upload( "race_time_data.pickle", result )
           
main()
