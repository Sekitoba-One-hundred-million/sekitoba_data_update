import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import sekitoba_library as lib
import sekitoba_data_manage as dm


def data_get( driver, url ):
    driver, _ = lib.driver_request( driver, url )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )        

    td_tag = soup.findAll( "td" )
    instance = []
    
    for td in td_tag:
        class_name = td.get( "class" )

        if not class_name == None \
           and len( class_name ) == 2 \
           and class_name[0] == "tC" \
           and "cyaku" in class_name[1]:
            try:
                instance.append( float( td.text ) )
            except:
                instance.append( 0 )
            
    if len( instance ) == 0:
        return "", []
    
    p_tag = soup.findAll( "p" )
    r_day = ""
    r_count = ""
                
    for p in p_tag:
        itemprop_name = p.get( "itemprop" )
        class_name = p.get( "class" )
        
        if not itemprop_name == None \
           and not class_name == None \
           and itemprop_name == "about" \
           and class_name[0] == "bold":
            num_data = p.text.split( "\n" )

            count = 0

            for i in range( 0, len( num_data[1] ) ):
                try:
                    r_count += str( int( num_data[1][i] ) )
                except:
                    count = i
                    break

            finish = False
            
            for i in range( count, len( num_data[1] ) ):
                try:
                    r_day += str( int( num_data[1][i] ) )
                    finish = True
                except:
                    if finish:
                        break

    return instance

def url_connect( url, str_data ):
    if len( str_data ) == 1:
        url += "0"

    url += str_data
    return url

def main():
    base_url = "https://www.keibalab.jp/db/race/"
    driver = webdriver.Chrome()
    omega_index_data = dm.pickle_load( "omega_index_data.pickle" )
    race_day_data = dm.pickle_load( "race_day.pickle" )
    race_info_data = dm.pickle_load( "race_info_data.pickle" )
    test_year = int( lib.test_years[-1] )
    month = 13

    id_data = lib.update_id_list_create()

    for race_id in id_data["race_id"].keys():
        if race_id in omega_index_data:
            continue
        
        year = int( race_day_data[race_id]["year"] )
        month = int( race_day_data[race_id]["month"] )
        day = int( race_day_data[race_id]["day"] )
        race_num = race_id[10:12]
        place_num = str( race_info_data[race_id]["place"] )
        url = base_url + str( year )
        url = url_connect( url, str( month ) )
        url = url_connect( url, str( day ) )
        url = url_connect( url, place_num )
        url += race_num
        url += "/syutsuba.html"
        data = data_get( driver, url )
        time.sleep( 1 )
        
        if len( data ) == 0:
            continue

        omega_index_data[race_id] = data

    dm.pickle_upload( "omega_index_data.pickle", omega_index_data )
                        
main()
    
