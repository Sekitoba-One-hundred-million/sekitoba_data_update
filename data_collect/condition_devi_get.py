from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( url ):
    result = {}
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result
    
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )

        if not class_name == None and \
          len( class_name ) == 2 and \
          class_name[0] == "HorseList":
            td_tag = tr.findAll( "td" )
            try:
                a_tag = td_tag[2].find( "a" )
                horce_id = a_tag.get( "href" ).split( "&" )[0].split( "horse_id=" )[-1]
                span_tag = td_tag[3].findAll( "span" )
                condition_devi = float( lib.text_replace( span_tag[0].text ) )
                result[horce_id] = condition_devi
            except:
                continue

    return result

def main():
    condition_devi_data = dm.pickle_load( "condition_devi_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )    
        
    base_url = "https://race.sp.netkeiba.com/barometer/score.html?race_id="
    race_data = dm.pickle_load( "race_data.pickle" )
    url_data = []
    key_data = []
    
    for race_id in update_race_id_list:
        url = base_url + race_id
        url_data.append( url )
        key_data.append( race_id )

    add_data = lib.ThreadScraping( url_data, key_data ).data_get( data_get )

    for k in add_data.keys():
        condition_devi_data[k] = add_data[k]
    
    dm.pickle_upload( "condition_devi_data.pickle", condition_devi_data )

if __name__ == "__main__":
    main()
