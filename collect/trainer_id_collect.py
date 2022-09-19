import copy
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( url ):
    result = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for tr in tr_tag:
        class_name = tr.get( "class" )
        
        if not class_name == None and class_name[0] == "HorseList":
            horce_id = ""
            trainer_id = ""
            td_tag = tr.findAll( "td" )
            for td in td_tag:
                td_class_name = td.get( "class" )
                
                if not td_class_name == None:
                    if td_class_name[0] == "Horse_Info":
                        a = td.find( "a" )
                        try:
                            href = a.get( "href" )
                            horce_id = href.split( "/" )[-1]
                        except:
                            continue
                        
                    elif td_class_name[0] == "Trainer":
                        a = td.find( "a" )
                        try:
                            href = a.get( "href" )
                            trainer_id = href.split( "/" )[-2]
                        except:
                            continue

            if not len( horce_id ) == 0 and not len( trainer_id ) == 0:
                result[horce_id] = trainer_id

    return result

def main():
    prod_race_data = dm.pickle_load( "race_data.pickle", prod = True )
    race_trainer_id_data = dm.pickle_load( "race_trainer_id_data.pickle", prod = True )
    trainer_id_data = dm.pickle_load( "trainer_id_data.pickle", prod = True )
    race_id_list = list( prod_race_data.keys() )
    key_list = []
    url_list = []

    for race_id in race_id_list:
        if not race_id in trainer_id_data:
            url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id
            key_list.append( race_id )
            url_list.append( url )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for k in add_data.keys():
        race_trainer_id_data[k] = copy.deepcopy( add_data[k] )

        for kk in add_data[k].keys():
            trainer_id = copy.copy( add_data[k][kk] )
            trainer_id_data[trainer_id] = True

    dm.pickle_upload( "race_trainer_id_data.pickle", race_trainer_id_data, prod = True )
    dm.pickle_upload( "trainer_id_data.pickle", trainer_id_data, prod = True )

if __name__ == "__main__":
    main()
