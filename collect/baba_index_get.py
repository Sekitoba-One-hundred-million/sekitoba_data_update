
from bs4 import BeautifulSoup
import requests

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
            baba_index = td_tag[16].text.replace( "\n", "" ).replace( " ", "" )
            day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )

            try:
                result[day_key] = float( baba_index )
            except:
                result[day_key] = 0

    return result

def main():
    baba_index_data = dm.pickle_load( "baba_index_data.pickle" )
    cookie = lib.netkeiba_login()
    id_data = lib.update_id_list_create()
    key_list = []
    url_list = []

    for horce_id in id_data["horce_id"].keys():
        key_list.append( horce_id )
        url = "https://db.netkeiba.com/horse/" + horce_id
        url_list.append( { "url": url, "cookie": cookie } )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for k in add_data.keys():
        baba_index_data[k] = add_data[k]    
    
    dm.pickle_upload( "baba_index_data.pickle", baba_index_data )

if __name__ == "__main__":
    main()
    
