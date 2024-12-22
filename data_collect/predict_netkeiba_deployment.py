import copy
import json
from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( url ):
    result = []
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result

    soup = BeautifulSoup( r.content, 'html.parser' )
    div_tag = soup.findAll( 'div' )

    for div in div_tag:
        class_name = div.get( 'class' )
        data_slick_index_name = div.get( 'data-slick-index' )
        
        if not class_name == None and \
          class_name[0] == 'DeployRace_SlideBoxItem':
            li_tag = div.findAll( "li" )
            count = 0
            key = ''
            instance_list = []

            for li in li_tag:
                dt = li.find( "dt" )

                if not dt == None:
                    if not len( key ) == 0:
                        result.append( copy.deepcopy( instance_list ) )
                        instance_list = []

                    key = lib.textReplace( dt.text )
                    continue

                try:
                    instance_list.append( int( lib.textReplace( li.find( "span" ).text ) ) )
                except:
                    continue
                
            break

    try:
        result.append( copy.deepcopy( instance_list ) )
    except:
        pass
        
    return result

def main():
    result = dm.pickle_load( 'predict_netkeiba_deployment_data.pickle' )
    
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
        ps.RaceData().update_data( "predict_netkeiba_deployment", json.dumps( add_data[race_id], ensure_ascii = False ), race_id )
    
    dm.pickle_upload( 'predict_netkeiba_deployment_data.pickle', result )

if __name__ == '__main__':
    main()
