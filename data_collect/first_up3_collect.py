import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

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
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    driver = lib.driver_start()
    driver = lib.login( driver )
    count = 0

    for race_id in update_race_id_list:
        url = base_url + race_id
        driver, _ = lib.driver_request( driver, url )
        print( race_id )
        time.sleep( 2 )
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup( html, "html.parser" )
        result[race_id] = first_time_get( soup )
        ps.RaceData().update_data( "first_up3_halon", json.dumps( result[race_id], ensure_ascii = False ), race_id )

    driver.close()
    dm.pickle_upload( "first_up3_halon.pickle", result )

if __name__ == "__main__":
    main()
