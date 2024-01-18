import time
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

            lib.dic_append( result, horce_num, {} )
            ul_tag = dl.findAll( "ul" )

            for ul in ul_tag:
                ul_class_name = ul.get( "class" )

                if ul_class_name == None or len( ul_class_name ) == 0 or not ul_class_name[0] == "Past_Direction":
                    continue

                li_tag = ul.findAll( "li" )

                for li in li_tag:
                    past_div_tag = li.findAll( "div" )

                    try:
                        race_id = past_div_tag[2].find( "a" ).get( "href" ).split( "/" )[-2]
                        first_up3 = float( past_div_tag[6].text.split( " " )[1].replace( "前", "" ) )
                    except:
                        continue

                    result[horce_num][race_id] = first_up3

    return result

def main():
    result = dm.pickle_load( "first_up3_halon.pickle" )
    base_url = "https://race.netkeiba.com/race/newspaper.html?race_id="
    race_data = dm.pickle_load( "race_data.pickle" )
    horce_data = dm.pickle_load( "horce_data_storage.pickle" )
    race_day = dm.pickle_load( "race_day.pickle" )
    driver = lib.driver_start()
    driver = lib.login( driver )
    count = 0

    collect_race_id_list = []

    for k in race_data.keys():
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        if not race_id in result:
            collect_race_id_list.append( race_id )
        else:
            horce_id = list( race_data[k].keys() )[0]
            current_data, _ = lib.race_check( horce_data[horce_id], race_day[race_id] )
            cd = lib.current_data( current_data )

            if not cd.race_check() or cd.new_check():
                continue

            if len( result[race_id] ) == 0:
                collect_race_id_list.append( race_id )
            else:
                zero_count = 0
                for key_horce_num in result[race_id].keys():
                    if not type( result[race_id][key_horce_num] ) is dict:
                        collect_race_id_list.append( race_id )
                        break
                    elif len( result[race_id][key_horce_num] ) == 0:
                        zero_count += 1

                if zero_count == len( result[race_id] ):
                    collect_race_id_list.append( race_id )

    for race_id in collect_race_id_list:
        url = base_url + race_id
        driver, _ = lib.driver_request( driver, url )
        time.sleep( 2 )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        result[race_id] = first_time_get( soup )
            
        count += 1

        if count % 100 == 0:
            dm.pickle_upload( "first_up3_halon.pickle", result )

    driver.close()
    dm.pickle_upload( "first_up3_halon.pickle", result )

if __name__ == "__main__":
    while 1:
        try:
            main()
            break
        except:
            pass
