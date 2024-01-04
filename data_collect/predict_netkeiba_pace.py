from tqdm import tqdm
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_get( url ):
    result = ''
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, 'html.parser' )
    dl_tag = soup.findAll( 'dl' )

    for dl in dl_tag:
        class_name = dl.get( 'class' )

        if not class_name == None and \
          class_name[0] == 'RacePace':
            try:
                dd = dl.find( 'dd' )
                result = lib.text_replace( dd.text )
                break
            except:
                continue

    return result

def main():
    result = dm.pickle_load( 'predict_netkeiba_pace_data.pickle' )
    
    if result == None:
        result = {}
        
    base_url = 'https://race.netkeiba.com/race/shutuba.html?race_id='
    race_data = dm.pickle_load( 'race_data.pickle' )
    url_data = []
    key_data = []
    
    for k in race_data.keys():
        race_id = lib.id_get(k)
        url = base_url + race_id

        if not race_id in result:
            url_data.append( url )
            key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( data_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( 'predict_netkeiba_pace_data.pickle', result )

if __name__ == '__main__':
    main()
