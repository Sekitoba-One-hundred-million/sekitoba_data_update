import json
import requests
from bs4 import BeautifulSoup

import sekitoba_psql as ps
import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( data ):
    result = {}
    r, _ = lib.request( data["url"], cookie = data["cookie"] )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            time_index = td_tag[19].text.replace( "\n", "" ).replace( " ", "" )
            day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )

            try:
                result[day_key] = float( time_index )
            except:
                result[day_key] = 0

    return result

def main():
    time_index_data = dm.pickle_load( "time_index_data.pickle" )
    update_horce_id_list = dm.pickle_load( "update_horce_id_list.pickle" )
    cookie = lib.netkeiba_login()

    key_list = []
    url_list = []

    for horce_id in update_horce_id_list:
        key_list.append( horce_id )
        url = "https://db.netkeiba.com/horse/" + horce_id
        url_list.append( { "url": url, "cookie": cookie } )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )    

    for horce_id in add_data.keys():
        time_index_data[horce_id] = add_data[horce_id]
        ps.HorceData().update_data( "time_index", json.dumps( add_data[horce_id], ensure_ascii = False ), horce_id )
        
    dm.pickle_upload( "time_index_data.pickle", time_index_data )

if __name__ == "__main__":
    main()
    
