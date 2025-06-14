from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_collect( url ):
    result = {}
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result

    soup = BeautifulSoup( r.content, "html.parser" )
    table_tag = soup.findAll( "table" )

    for table in table_tag:
        class_name = table.get( "class" )

        if not class_name == None \
           and len( class_name ) > 1 \
           and class_name[0] == "RaceCommon_Table" \
           and class_name[1] == "Corner_Num":
            tr_tag = table.findAll( "tr" )

            for tr in tr_tag:
                th = tr.find( "th" )
                td = tr.find( "td" )
                corner_num = th.text[0]
                result[corner_num] = td.text

    return result

def main():
    result = dm.pickle_load( "corner_rank_data.pickle" )

    if result == None:
        result = {}    
    
    race_data = dm.pickle_load( "race_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    url_list = []
    key_list = []

    for race_id in update_race_id_list:
        url = "https://race.netkeiba.com/race/result.html?race_id=" + race_id
        key_list.append( race_id )
        url_list.append( url )

    add_data = lib.ThreadScraping( url_list, key_list ).data_get( data_collect )

    for k in add_data.keys():
        result[k] = add_data[k]

    dm.pickle_upload( "corner_rank_data.pickle", result )    
    
main()
