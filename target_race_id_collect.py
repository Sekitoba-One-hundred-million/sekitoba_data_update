import time
import datetime
import jpholiday
from bs4 import BeautifulSoup
from selenium import webdriver

import sekitoba_library as lib
import sekitoba_data_manage as dm

def is_biz_day( date ):    
    if date.weekday() >= 5 or jpholiday.is_holiday( date ):
        return True

    return False

def race_id_get( driver, url ):
    race_id_list = []
    year = url.split( "kaisai_date=" )[-1][0:4]
    driver = lib.driver_start()
    driver, _ = lib.driver_request( driver, url )
    time.sleep( 5 )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )
    p_tag = soup.findAll( "p" )

    for p in p_tag:
        class_name = p.get( "class" )

        if not class_name == None \
          and class_name[0] == "RaceList_DataTitle":

            try:
                split_data = p.text.split( " " )
                str_count = split_data[0].replace( "回", "" )
                place_num = str( int( lib.place_num( split_data[1] ) ) )
                str_day = split_data[2].replace( "日目", "" )
            except:
                continue

            base_id = year + lib.padding_str_math( place_num ) + lib.padding_str_math( str_count ) + lib.padding_str_math( str_day )

            for i in range( 1, 13 ):
                race_id_list.append( base_id + lib.padding_str_math( str( i ) ) )

    return race_id_list

def main():
    result = []
    race_data = dm.pickle_load( "race_data.pickle" )
    driver = lib.driver_start()
    today_date = datetime.datetime.today()
    day_count = 0

    while 1:
        check_date = today_date - datetime.timedelta( days = day_count )
        day_count += 1

        if not is_biz_day( check_date ):
            continue

        str_date = str( check_date.year ) + lib.padding_str_math( str( check_date.month ) ) + lib.padding_str_math( str( check_date.day ) )
        url = "https://race.netkeiba.com/top/?kaisai_date={}".format( str_date )
        driver, _ = lib.driver_request( driver, url )
        race_id_list = race_id_get( driver, url )

        if not len( race_id_list ) == 0:
            check_key = "https://race.netkeiba.com/race/shutuba.html?race_id={}".format( race_id_list[0] )
            
            if check_key in race_data:
                break

            result.extend( race_id_list )
            
    dm.pickle_upload( "update_race_id_list.pickle", result )
    driver.quit()

if __name__ == "__main__":
    main()
