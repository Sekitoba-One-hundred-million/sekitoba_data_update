from bs4 import BeautifulSoup

import SekitobaPsql as ps
import SekitobaLibrary as lib
import SekitobaDataManage as dm

def race_money_get( url ):
    money = 0
    r, requestSucess = lib.request( url )

    if not requestSucess:
        print( "Error: {}".format( data["url"] ) )
        return result

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
    race_money_data = dm.pickle_load( "race_money_data.pickle" )
    update_race_id_list = dm.pickle_load( "update_race_id_list.pickle" )
    base_url = "https://race.netkeiba.com/race/result.html?race_id="

    url_data = []
    key_data = []

    for race_id in update_race_id_list:
        url = base_url + race_id
        url_data.append( url )
        key_data.append( race_id )

    add_data = lib.ThreadScraping( url_data, key_data ).data_get( race_money_get )

    for race_id in add_data.keys():
        race_money_data[race_id] = add_data[race_id]
        ps.RaceData().update_data( "money", add_data[race_id], race_id )
    
    dm.pickle_upload( "race_money_data.pickle", race_money_data )

main()

