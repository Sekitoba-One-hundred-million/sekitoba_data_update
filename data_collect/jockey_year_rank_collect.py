import json
from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_collect( url ):
    result = {}
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result
    
    soup = BeautifulSoup( r.content, "html.parser" )
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        table_class = table.get( "class" )

        if not table_class == None and table_class[0] == "nk_tb_common":
            tr_tag = table.findAll( "tr" )

            for tr in tr_tag:
                td_tag = tr.findAll( "td" )

                if len( td_tag ) == 21:
                    year = 0

                    try:
                        year = int( lib.text_replace( td_tag[0].text ) )
                        rank = int( lib.text_replace( td_tag[1].text ) )
                    except:
                        continue

                    key_year = str( year )
                    result[key_year] = rank

    return result
        
def main():
    jockey_year_rank_data = dm.pickle_load( "jockey_year_rank_data.pickle" )
    update_jockey_id_list = dm.pickle_load( "update_jockey_id_list.pickle" )
    base_url = "https://db.netkeiba.com/jockey/result/"

    url_list = []
    key_list = []
    
    for jockey_id in update_jockey_id_list:
        url = base_url + jockey_id
        url_list.append( url )
        key_list.append( jockey_id )

    add_data = lib.ThreadScraping( url_list, key_list ).data_get( data_collect )

    for jockey_id in add_data.keys():
        jockey_year_rank_data[jockey_id] = add_data[jockey_id]
        ps.JockeyData().update_data( "jockey_year_rank", json.dumps( add_data[jockey_id], ensure_ascii = False ), jockey_id )
    
    dm.pickle_upload( "jockey_year_rank_data.pickle", jockey_year_rank_data )

if __name__ == "__main__":
    main()
