from bs4 import BeautifulSoup
import requests

import sekitoba_library as lib
import sekitoba_data_manage as dm

def data_collect( data ):
    result = {}
    count = 1
    r, _ = lib.request( data["url"], cookie = data["cookie"] )
    soup = BeautifulSoup( r.content, "html.parser" )
    ul_tag = soup.findAll( "ul" )
    tr_tag = soup.findAll( "tr" )    

    for tr in tr_tag:
        class_name = tr.get( "class" )

        if not class_name == None \
          and "OikiriDataHead" in class_name[0]:
            td_tag = tr.findAll( "td" )
            
            if not len( td_tag ) == 13:
                continue

            key = td_tag[1].text
            lib.dic_append( result, key, { "time": [], "wrap": [], "load": "", "critic": "", "rank": "", "cource": ""  } )
            li_tag = td_tag[8].findAll( "li" )
            result[key]["cource"] = td_tag[5].text            
            result[key]["load"] = td_tag[10].text
            result[key]["critic"] = td_tag[11].text
            result[key]["rank"] = td_tag[12].text

            for li in li_tag:
                text_list = li.text.replace( ")", "" ).split( "(" )

                if not len( text_list ) == 2:
                    continue

                train_time = text_list[0]
                wrap_time = text_list[1]

                try:
                    result[key]["time"].append( float( train_time ) )
                    result[key]["wrap"].append( float( wrap_time ) )
                except:
                    continue

    return result

def main():
    prod_train_time_data = dm.pickle_load( "train_time_data.pickle", prod = True )
    dev_train_time_data = dm.pickle_load( "train_time_data.pickle", prod = True )
    train_time_data = lib.link_prod_dev_data( prod_train_time_data, dev_train_time_data )

    id_data = lib.update_id_list_create()
    cookie = lib.netkeiba_login()
    key_list = []
    url_list = []

    for race_id in id_data["race_id"].keys():
        if not race_id in train_time_data:
            url = "https://race.netkeiba.com/race/oikiri.html?race_id=" + race_id
            key_list.append( race_id )
            url_list.append( { "url": url, "cookie": cookie } )

    add_data = lib.thread_scraping( url_list, key_list ).data_get( data_collect )

    for k in add_data.keys():
        train_time_data[k] = add_data[k]
        
    dm.pickle_upload( "train_time_data.pickle", train_time_data, prod = True )
    dm.pickle_upload( "train_time_data.pickle", train_time_data )

if __name__ == "__main__":
    main()
