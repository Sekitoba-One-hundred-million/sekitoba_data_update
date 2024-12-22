from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( url ):
    result = ''
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result

    soup = BeautifulSoup( r.content, 'html.parser' )
    dl_tag = soup.findAll( 'dl' )

    for dl in dl_tag:
        class_name = dl.get( 'class' )

        if not class_name == None and \
          class_name[0] == 'RacePace':
            try:
                dd = dl.find( 'dd' )
                result = lib.textReplace( dd.text )
                break
            except:
                continue

    return result

def main():
    result = dm.pickle_load( 'predict_netkeiba_pace_data.pickle' )
    
    if result == None:
        result = {}

    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    base_url = 'https://race.netkeiba.com/race/shutuba.html?race_id='
    url_data = []
    key_data = []
    
    for race_id in update_race_id_list:
        url = base_url + race_id
        url_data.append( url )
        key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( data_get )

    for race_id in add_data.keys():
        result[race_id] = add_data[race_id]
        ps.RaceData().update_data( "predict_netkeiba_pace", add_data[race_id], race_id )
    
    dm.pickle_upload( 'predict_netkeiba_pace_data.pickle', result )

if __name__ == '__main__':
    main()
