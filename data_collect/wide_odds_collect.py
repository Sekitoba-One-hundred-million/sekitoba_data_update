import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_get( driver, url ):
    driver, _ = lib.driver_request( driver, url )
    time.sleep( 1 )
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup( html, "html.parser" )      
    table_tag = soup.findAll( "table" )
    odds_data = {}

    for table in table_tag:
        class_name = table.get( "class" )
        
        if class_name == None or len( class_name ) == 0 or not class_name[0] == "Odds_Table":
            continue

        instance_odds_data = {}
        td_tag = table.findAll( "td" )
        before_num = -1
        
        for td in td_tag:
            class_name = td.get( "class" )

            if class_name == None:
                continue

            if len( class_name ) == 1 and class_name[0] == "Waku_Normal":
                try:
                    before_num = int( lib.text_replace( td.text ) )
                except:
                    continue

            if len( class_name ) == 2 and class_name[0] == "Odds" and class_name[1] == "Popular":
                try:
                    odds_text = lib.text_replace( td.text )
                    min_odds = ""
                    max_odds = ""
                    max_flag = False

                    for i in range( 0, len( odds_text ) ):
                        if not max_flag:
                            min_odds += odds_text[i]

                            if not i == 0 and odds_text[i-1] == ".":
                                max_flag = True
                        else:
                            max_odds += odds_text[i]

                    min_odds = float( min_odds )
                    max_odds = float( max_odds )
                except:
                    before_num = -1
                    continue

                if not before_num == -1:
                    instance_odds_data[before_num] = { "min": min_odds, "max": max_odds }
                    before_num = -1

        if len( instance_odds_data ) == 0:
            continue

        base_num = min( instance_odds_data.keys() ) - 1
        odds_data[base_num] = instance_odds_data

    return odds_data

def main():
    driver = lib.driver_start()
    result = dm.pickle_load( "wide_odds_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )    

    for race_id in update_race_id_list:
        url = "https://race.netkeiba.com/odds/index.html?type=b5&race_id={}&housiki=c0".format( race_id )
        result[race_id] = data_get( driver, url )

    driver.quit()
    dm.pickle_upload( "wide_odds_data.pickle", result )

main()
    
