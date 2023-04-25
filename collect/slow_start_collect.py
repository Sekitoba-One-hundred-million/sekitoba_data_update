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
            try:
                day_key = td_tag[0].text.replace( "\n", "" ).replace( " ", "" )
                slow_start_str = td_tag[25].text.replace( "\n", "" ).replace( " ", "" )
            except:
                continue

            slow_start = False
            
            if slow_start_str == "出遅れ":
                slow_start = True

            result[day_key] = slow_start

    return result

def main():
    cookie = lib.netkeiba_login()
    prod_slow_start_data = dm.pickle_load( "slow_start_data.pickle", prod = True )
    dev_slow_start_data = dm.pickle_load( "slow_start_data.pickle" )
    slow_start_data = lib.link_prod_dev_data( prod_slow_start_data, dev_slow_start_data, method = "value_length" )
    id_data = lib.update_id_list_create()
    key_list = []
    url_list = []

    for horce_id in id_data["horce_id"].keys():
        key_list.append( horce_id )
        url = "https://db.netkeiba.com/horse/" + horce_id
        url_list.append( { "url": url, "cookie": cookie } )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for k in add_data.keys():
        slow_start_data[k] = add_data[k]

    dm.pickle_upload( "slow_start_data.pickle", slow_start_data, prod = True )
    dm.pickle_upload( "slow_start_data.pickle", slow_start_data )

if __name__ == "__main__":
    main()