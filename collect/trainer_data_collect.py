import datetime
from bs4 import BeautifulSoup

import sekitoba_library as lib
import sekitoba_data_manage as dm

def trainer_data_collect( trainer_id ):
    base_url = "https://db.netkeiba.com/?pid=trainer_detail&id=" + trainer_id + "&page="
    result = {}
    count = 1
    before_year = int( datetime.date.today().year ) - 1
    
    while 1:
        url = base_url + str( count )
        r,_  = lib.request( url )
        soup = BeautifulSoup( r.content, "html.parser" )
        tbody = soup.find( "tbody" )
        if tbody == None:
            break
        
        tr_tag = tbody.findAll( "tr" )

        if len( tr_tag ) == 0:
            break
        else:
            for tr in tr_tag:
                td_tag = tr.findAll( "td" )
                key_day = td_tag[0].text
                key_race_num = td_tag[3].text
                try:
                    horce_id = td_tag[12].find( "a" ).get( "href" ).replace( "horse", "" ).replace( "/", "" )
                except:
                    horce_id = ""

                ymd = key_day.split( "/" )

                if not len( ymd ) == 3:
                    continue

                year = int( ymd[0] )
                
                if year < before_year:
                    return result
                elif before_year < year:
                    continue

                lib.dic_append( result, key_day, {} )
                lib.dic_append( result[key_day], key_race_num, {} )
                result[key_day][key_race_num]["place"] = td_tag[1].text
                result[key_day][key_race_num]["weather"] = td_tag[2].text
                result[key_day][key_race_num]["all_horce_num"] = td_tag[6].text
                result[key_day][key_race_num]["flame_num"] = td_tag[7].text
                result[key_day][key_race_num]["horce_num"] = td_tag[8].text
                result[key_day][key_race_num]["odds"] = td_tag[9].text
                result[key_day][key_race_num]["popular"] = td_tag[10].text
                result[key_day][key_race_num]["rank"] = td_tag[11].text
                result[key_day][key_race_num]["horce_id"] = horce_id
                result[key_day][key_race_num]["weight"] = td_tag[14].text
                result[key_day][key_race_num]["dist"] = td_tag[15].text
                result[key_day][key_race_num]["baba"] = td_tag[16].text
                result[key_day][key_race_num]["time"] = td_tag[17].text
                result[key_day][key_race_num]["diff"] = td_tag[18].text
                result[key_day][key_race_num]["passing"] = td_tag[19].text
                result[key_day][key_race_num]["pace"] = td_tag[20].text
                result[key_day][key_race_num]["up"] = td_tag[21].text
                
        count += 1
    
    return result

def main():
    trainer_data = dm.pickle_load( "prod_trainer_data.pickle", prod = True )

    if trainer_data == None:
        trainer_data = {}
    
    key_list = []
    url_list = []
    base_url = "https://db.netkeiba.com/?pid=trainer_detail&id="
    trainer_id_data = dm.pickle_load( "trainer_id_data.pickle", prod = True )
    
    for trainer_id in trainer_id_data.keys():
        url = base_url + trainer_id
        key_list.append( trainer_id )
        url_list.append( url )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( joceky_data_collect )

    for k in add_data.keys():
        trainer_data[k] = add_data[k]

    dm.pickle_upload( "prod_trainer_data.pickle", trainer_data, prod = True )

if __name__ == "__main__":
    main()
