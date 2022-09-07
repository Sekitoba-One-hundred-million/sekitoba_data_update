from bs4 import BeautifulSoup

from name import *
import sekitoba_library as lib
import sekitoba_data_manage as dm

def race_money_get( url ):
    money = 0
    r, _ = lib.request( url ) #requests.get( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    div_tag = soup.findAll( "div" )

    for div in div_tag:
        class_name = div.get( "class" )

        if not class_name == None \
           and class_name[0] == "RaceData02":
            span_tag = div.findAll( "span" )

            for span in span_tag:
                text = span.text.replace( "\n", "" )
                split_text = text.split( "," )

                if len( split_text ) > 1 \
                   and "本賞金" in split_text[0]:
                    try:
                        money = float( split_text[0].split( ":" )[1] )
                    except:
                        money = 0
                    break
            break

    return money

def main():
    result = dm.pickle_load( "race_money_data.pickle" )

    if result == None:
        result = {}
    
    base_url = "https://race.netkeiba.com/race/result.html?race_id="
    race_id_list = dm.pickle_load( UPDATE_RACE_ID_LIST, prod = True )

    url_data = []
    key_data = []

    for race_id in race_id_list:
        url = base_url + race_id
        url_data.append( url )
        key_data.append( race_id )

    add_data = lib.thread_scraping( url_data, key_data ).data_get( race_money_get )

    for k in add_data.keys():
        result[k] = add_data[k]
    
    dm.pickle_upload( "race_money_data.pickle", result, prod = True )

main()

