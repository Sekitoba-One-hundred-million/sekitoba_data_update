import datetime
from bs4 import BeautifulSoup

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def data_collect( base_url, result ):
    count = 1
    finish = False

    while 1:
        if finish:
            break

        url = base_url + str( count )
        r, requestSucess = lib.request( url )

        if not requestSucess:
            print( "Error: {}".format( data["url"] ) )
            return result

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

                if key_day in result and key_race_num in result[key_day]:
                    finish = True
                    break

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
                result[key_day][key_race_num]["weight"] = td_tag[13].text
                result[key_day][key_race_num]["dist"] = td_tag[14].text
                result[key_day][key_race_num]["baba"] = td_tag[15].text
                result[key_day][key_race_num]["time"] = td_tag[16].text
                result[key_day][key_race_num]["diff"] = td_tag[17].text
                result[key_day][key_race_num]["passing"] = td_tag[18].text
                result[key_day][key_race_num]["pace"] = td_tag[19].text
                result[key_day][key_race_num]["up"] = td_tag[20].text
                
        count += 1
    
    return result

def main():
    result = dm.pickle_load( "jockey_full_data.pickle" )
    base_url = "https://db.netkeiba.com/?pid=jockey_detail&id="

    c = 0
    url_list = []
    key_list = []
    update_jockey_id_list = dm.pickle_load( "update_jockey_id_list.pickle" )

    for jockey_id in update_jockey_id_list:
        url = base_url + jockey_id + "&page="
        print( len( update_jockey_id_list ) - c )
        c += 1
        url_list.append( url )
        key_list.append( jockey_id )
        lib.dic_append( result, jockey_id, {} )
        result[jockey_id] = data_collect( url, result[jockey_id] )

    dm.pickle_upload( "jockey_full_data.pickle", result )

if __name__ == "__main__":
    main()
