from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def money_get( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    td_tag = soup.findAll( "td" )
    count = 0

    for td in td_tag:
        class_name = td.get( "class" )

        if not class_name == None \
           and class_name[0] == "Payout":
            count += 1
            m_data = td.text.split( "円" )
            
            if count == 1:
                result["単勝"] = int( m_data[0].replace( ",", "" ) )
            elif count == 2:
                result["複勝"] = []
                for i in range( 0, len( m_data ) - 1 ):
                    result["複勝"].append( int( m_data[i].replace( ",", "" ) ) )
            elif count == 4:
                result["馬連"] = int( m_data[0].replace( ",", "" ) )
            elif count == 5:
                result["ワイド"] = []
                for i in range( 0, len( m_data ) - 1 ):
                    result["ワイド"].append( int( m_data[i].replace( ",", "" ) ) )
            elif count == 6:
                result["馬単"] = int( m_data[0].replace( ",", "" ) )
            elif count == 7:
                result["三連複"] = int( m_data[0].replace( ",", "" ) )
            elif count == 8:
                result["三連単"] = int( m_data[0].replace( ",", "" ) )

    return result
        
                    

def main():
    odds_data = dm.pickle_load( "odds_data.pickle" )
    base_url = "https://race.netkeiba.com/race/result.html?race_id="
    id_data = lib.update_id_list_create()
    url_data = []
    key_data = []
    
    for race_id in id_data["race_id"].keys():
        if not race_id in odds_data:
            url = base_url + race_id + "&rf=race_list"
            url_data.append( url )
            key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( money_get )

    for k in add_data.keys():
        odds_data[k] = add_data[k]
    
    dm.pickle_upload( "odds_data.pickle", odds_data )
    
main()

