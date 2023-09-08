import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import sekitoba_library as lib
import sekitoba_data_manage as dm

def first_time_get( soup ):
    result = {}
    count = 0
    div_tag = soup.find( "body" ).findAll( "div" )

    for div in div_tag:
        div_class_name = div.get( "class" )

        if div_class_name == None or len( div_class_name ) == 0 or not div_class_name[0] == "HorseList_Wrapper":
            continue
        
        dl_tag = div.findAll( "dl" )

        for dl in dl_tag:
            dl_class_name = dl.get( "class" )

            if dl_class_name == None or len( dl_class_name ) == 0 or not dl_class_name[0] == "HorseList":
                continue

            dt_tag = dl.findAll( "dt" )

            try:
                horce_num = int( dt_tag[1].text )
            except:
                continue

            lib.dic_append( result, horce_num, [] )
            ul_tag = dl.findAll( "ul" )

            for ul in ul_tag:
                ul_class_name = ul.get( "class" )

                if ul_class_name == None or len( ul_class_name ) == 0 or not ul_class_name[0] == "Past_Direction":
                    continue

                li_tag = ul.findAll( "li" )

                for li in li_tag:
                    past_div_tag = li.findAll( "div" )

                    try:
                        first_up3 = float( past_div_tag[6].text.split( " " )[1].replace( "前", "" ) )
                    except:
                        continue

                    result[horce_num].append( first_up3 )
    return result

def main():
    result = dm.pickle_load( "first_up3_halon.pickle" )
    base_url = "https://race.netkeiba.com/race/newspaper.html?race_id="
    race_data = dm.pickle_load( "race_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    
    driver = lib.driver_start()
    driver = lib.login( driver )

    for race_id in update_race_id_list:
        if race_id in result:
            continue

        url = base_url + race_id
        driver, _ = lib.driver_request( driver, url )
        time.sleep( 3 )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )        
        result[race_id] = first_time_get( soup )

    driver.close()
    dm.pickle_upload( "first_up3_halon.pickle", result )
    
main()
