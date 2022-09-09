from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( url ):
    result = {}
    r, _ = lib.request( url )
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
    base_url = "https://db.netkeiba.com/jockey/result/"
    jockey_id_data = dm.pickle_load( "jockey_id_data.pickle", prod = True )
    url_list = []
    key_list = []
    
    for k in jockey_id_data.keys():
        jockey_id = k
        url = base_url + jockey_id
        url_list.append( url )
        key_list.append( jockey_id )

    result = lib.thread_scraping( url_list, key_list ).data_get( data_collect )
    dm.pickle_upload( "jockey_year_rank_data.pickle", result, prod = True )

if __name__ == "__main__":
    main()
