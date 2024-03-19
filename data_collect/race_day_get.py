from bs4 import BeautifulSoup

import sekitoba_psql as ps
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
    race_day_data = dm.pickle_load( "race_day.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    
    key_list = []

    for race_id in update_race_id_list:
        if not race_id in race_day_data:
            key_list.append( race_id )
    
    add_data = lib.thread_scraping( key_list, key_list ).data_get( day_get )

    for race_id in add_data.keys():
        race_day_data[race_id] = add_data[race_id]

        for kind in add_data[race_id].keys():
            ps.RaceData().update_race_data( kind, add_data[race_id][kind], race_id )

    dm.pickle_upload( "race_day.pickle", race_day_data )
    
main()
    
