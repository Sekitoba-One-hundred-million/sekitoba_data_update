from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_get( url ):
    result = {}
    result["kind"] = 0
    result["dist"] = 0
    result["baba"] = 0
    result["place"] = 0
    
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None:
            if class_name[0] == "RaceData01":
                span_tag = div.findAll( "span" )
                str_dist = span_tag[0].text.replace( " ", "" )
                _, kind = lib.dist( str_dist )
                dist = int( lib.k_dist( str_dist ) * 1000 )
                baba = lib.baba( span_tag[2].text.split( ":" )[1] )
                result["kind"] = kind
                result["dist"] = dist
                result["baba"] = baba
                
            elif class_name[0] == "RaceData02":
                span_tag = div.findAll( "span" )
                place = lib.place_num( span_tag[1].text )
                result["place"] = place

    return result

def main():
    race_info_data = dm.pickle_load( "race_info_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    url_list = []
    key_list = []

    for race_id in update_race_id_list:
        if not race_id in race_info_data:
            url_list.append( "https://race.netkeiba.com/race/result.html?race_id=" + race_id )
            key_list.append( race_id )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_get )
    rd = dm.pickle_load( "race_course_data.pickle" )
    
    for k in add_data.keys():
        race_info_data[k] = add_data[k]

    for k in race_info_data.keys():
        race_info_data[k]["out_side"] = False
        
        try:
            race_info_data[k]["out_side"] = rd[k]["out_side"]
        except:
            try:
                race_info_data[k]["out_side"] = rd[k]["外"]
            except:
                continue
            
        race_info_data[k]["direction"] = rd[k]["direction"]
    
    dm.pickle_upload( "race_info_data.pickle", race_info_data )

main()
