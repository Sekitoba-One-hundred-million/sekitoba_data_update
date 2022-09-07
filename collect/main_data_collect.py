import datetime
from bs4 import BeautifulSoup

from name import *
import sekitoba_library as lib
import sekitoba_data_manage as dm

def num_check( num ):
    if len( num ) == 1:
        return "0" + num
    else:
        return num

def horse_data_collect( url ):
    horce_data = []

    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            data_list = []
            for r in range( 0, len( td_tag ) ):
                if r != 5 and r != 16 and r != 19 and ( r == 27 or r < 24 ):
                    data = td_tag[r].text.replace( "\n", "" )

                    if not r == 27:
                        data_list.append( data )
                    else:
                        try:
                            data_list.append( float( data ) )
                        except:
                            data_list.append( 0 )

            if len( data_list ) == 22:
                horce_data.append( data_list )
    
    return horce_data

def race_data_search( url ):
    current_race_data = {}
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    span_tag = soup.findAll( "span" )
    
    for span in span_tag:
        class_name = span.get( "class" )

        if class_name != None\
           and class_name[0] == "HorseName":
            a_tag = span.find( "a" )

            if not a_tag == None:
                horce_name = a_tag.get( "title" )
                h_url = a_tag.get( "href" )
                horce_id = h_url.split( "/" )[-1]
                current_race_data[horce_id] = None

    return current_race_data

def main():
    url_list = []
    race_data_storage = dm.pickle_load( "race_data.pickle", prod = True )

    if race_data_storage == None:
        race_data_storage = {}

    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id="
    current_year = int( datetime.datetime.today().year )

    for y in range( current_year, current_year + 1 ):
        for p in range( 1, 11 ):
            for m in range( 1, 11 ):
                for d in range( 1, 13 ):
                    for r in range( 1, 13 ):
                        race_id = str( y ) + num_check( str( p ) ) + num_check( str( m ) ) + num_check( str( d ) ) + num_check( str( r ) )
                        url = base_url + race_id

                        try:
                            race_data_storage[url]
                        except:
                            url_list.append( url )

    update_horce_url = {}
    add_race_data = lib.thread_scraping( url_list, url_list ).data_get( race_data_search )
    need_update_race_id_list = []
    need_update_horce_id_list = []

    for k in add_race_data.keys():
        if len( add_race_data[k] ) == 0:
            continue

        race_data_storage[k] = add_race_data[k]
        need_update_race_id_list.append( lib.dic_append( k ) )

        for horce_id in add_race_data[k].keys():
            update_horce_url[horce_id] = "https://db.netkeiba.com/horse/" + horce_id
            need_update_horce_id_list.append( horce_id )

    horce_url_list = []
    horce_id_list = []

    for k in update_horce_url.keys():
        horce_id_list.append( k )
        horce_url_list.append( update_horce_url[k] )

    horce_data_storage = dm.pickle_load( "horce_data_storage.pickle", prod = True )
    add_horce_data = lib.thread_scraping( horce_url_list, horce_id_list ).data_get( race_data_search )

    for k in add_horce_data.keys():
        horce_data_storage[k] = add_horce_data[k]

    dm.pickle_upload( "race_data.pickle", race_data_storage, prod = True )
    dm.pickle_upload( "horce_data_storage.pickle", horce_data_storage, prod = True )
    dm.pickle_upload( UPDATE_RACE_ID_LIST, need_update_race_id_list, prod = True )
    dm.pickle_upload( UPDATE_HORCE_ID_LIST, need_update_horce_id_list, prod = True )
    
main()
