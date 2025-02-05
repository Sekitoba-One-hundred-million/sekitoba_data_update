import json
from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def wrap_get( url ):
    result = {}
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result

    soup = BeautifulSoup( r.content, "html.parser" )
    
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        summary = table.get( "summary" )

        if not summary == None \
           and summary == "ラップタイム":
            tr_tag = table.findAll( "tr" )
            dist_data = tr_tag[0].findAll( "th" )
            wrap_time = tr_tag[2].findAll( "td" )

            for i in range( 0, len( dist_data ) ):
                dist = dist_data[i].text.replace( "m", "" )
                wrap = float( wrap_time[i].text )
                result[dist] = wrap

    return result

def main():    
    wrap_data = dm.pickle_load( "wrap_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    base_url =  "https://race.netkeiba.com/race/result.html?race_id="
    url_list = []
    key_list = []

    for race_id in update_race_id_list:
        url = base_url + race_id
        url_list.append( url )
        key_list.append( race_id )

    add_data = lib.ThreadScraping( url_list, key_list ).data_get( wrap_get )
        
    for race_id in add_data.keys():
        wrap_data[race_id] = add_data[race_id]
        ps.RaceData().update_data( "wrap", json.dumps( wrap_data[race_id], ensure_ascii = False ), race_id )
    
    dm.pickle_upload( "wrap_data.pickle", wrap_data )

main()

