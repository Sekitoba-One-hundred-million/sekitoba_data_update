from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def day_get( race_id ):
    result = {}
    result["year"] = int( race_id[0:4] )
    result["month"] = 0
    result["day"] = 0
    r, _ = lib.request( "https://race.netkeiba.com/race/result.html?race_id=" + race_id + "&rf=race_list" )
    soup = BeautifulSoup( r.content, "html.parser" )
    dd_tag = soup.findAll( "dd" )

    for dd in dd_tag:
        class_name = dd.get( "class" )

        if not class_name == None \
           and class_name[0] == "Active":
            try:
                text = dd.find( "a" ).get( "title" )
                m_split = text.split( "月" )
                d_split = m_split[1].split( "日" )
                result["month"] = int( m_split[0] )
                result["day"] = int( d_split[0] )
            except:
                break
            
            break

    return result

def main():    
    result = dm.pickle_load( "race_day.pickle", prod = True )

    if result == None:
        result = {}

    prod_race_data = dm.pickle_load( "race_data.pickle", prod = True )
    key_list = list( prod_race_data.keys() )
    
    url_list = []
    key_list = []

    base_url = "https://race.netkeiba.com/race/result.html?race_id="

    for k in key_list:
        race_id = lib.id_get( k )

        if not race_id in result:
            key_list.append( race_id )
            url_list.append( race_id )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( day_get )

    for k in add_data.keys():
        result[k] = add_data[k]

    dm.pickle_upload( "race_day.pickle", result, prod = True )
    
main()
    
