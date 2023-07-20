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
    prod_race_day_data = dm.pickle_load( "race_day.pickle", prod = True )
    dev_race_day_data = dm.pickle_load( "race_day.pickle" )
    race_day_data = lib.link_prod_dev_data( prod_race_day_data, dev_race_day_data )
    
    id_data = lib.update_id_list_create()
    key_list = []

    for race_id in id_data["race_id"].keys():
        if not race_id in race_day_data:
            key_list.append( race_id )
    
    add_data = lib.thread_scraping( key_list, key_list ).data_get( day_get )

    for k in add_data.keys():
        race_day_data[k] = add_data[k]

    dm.pickle_upload( "race_day.pickle", race_day_data, prod = True )
    dm.pickle_upload( "race_day.pickle", race_day_data )
    
main()
    
