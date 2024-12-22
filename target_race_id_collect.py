import time
import datetime
import jpholiday
from bs4 import BeautifulSoup
from selenium import webdriver

import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

def is_biz_day( date ):    
    if date.weekday() >= 5 or jpholiday.is_holiday( date ):
        return True

    return False

def race_idGet( driver, url ):
    race_id_list = []
    year = url.split( "kaisai_date=" )[-1][0:4]
    #driver = lib.driverStart()
    driver, _ = lib.driverRequest( driver, url )
    time.sleep( 10 )
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
                place_num = str( int( lib.placeNum( split_data[1] ) ) )
                str_day = split_data[2].replace( "日目", "" )
            except:
                continue

            base_id = year + lib.paddingStrMath( place_num ) + lib.paddingStrMath( str_count ) + lib.paddingStrMath( str_day )

            for i in range( 1, 13 ):
                race_id_list.append( base_id + lib.paddingStrMath( str( i ) ) )

    return race_id_list

def main():
    result = []
    race_data = ps.RaceData()
    all_race_id_list = race_data.get_all_race_id()
    driver = lib.driverStart()
    today_date = datetime.datetime.now() - datetime.timedelta(1)
    day_count = 0

    while 1:
        check_date = today_date - datetime.timedelta( days = day_count )
        day_count += 1

        if not is_biz_day( check_date ):
            continue

        print( check_date )
        str_date = str( check_date.year ) + lib.paddingStrMath( str( check_date.month ) ) + lib.paddingStrMath( str( check_date.day ) )
        url = "https://race.netkeiba.com/top/?kaisai_date={}".format( str_date )
        race_id_list = []
        
        for i in range( 0, 10 ):
            try:
                race_id_list = race_idGet( driver, url )
                break
            except Exception as e:
                print( e )
                continue

        if not len( race_id_list ) == 0:
            if race_id_list[0] in all_race_id_list:
                break

            result.extend( race_id_list )
            
    dm.pickle_upload( "update_race_id_list.pickle", result )
    driver.quit()

if __name__ == "__main__":
    main()
