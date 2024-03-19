import json
from bs4 import BeautifulSoup

import sekitoba_psql as ps
import sekitoba_library as lib
import sekitoba_data_manage as dm

def horse_data_collect( url ):
    horce_data = []

    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    tr_tag = soup.findAll( "tr" )

    for i in range( 0, len( tr_tag ) ):
        td_tag = tr_tag[i].findAll( "td" )
        
        if 2 < len( td_tag ) and td_tag[3].get( "class" ) != None \
           and td_tag[3].get( "class" )[0] == "txt_right":
            data_list = []
            for r in range( 0, len( td_tag ) ):
                #print( td_tag[r], r )
                if r != 5 and r != 16 and r != 19 and ( r == 27 or r < 24 ):
                    data = td_tag[r].text.replace( "\n", "" )

                    if not r == 27:
                        data_list.append( data )
                    else:
                        try:
                            data_list.append( float( data ) )
                        except:
                            data_list.append( 0 )

            if len( data_list ) == 22:
                horce_data.append( data_list )
                
    return horce_data
    
def parent_id_get( url ):
    result = {}
    result["father"] = ""
    result["mother"] = ""
    
    r, _ = lib.request( url )
    soup = BeautifulSoup( r.content, "html.parser" )
    td_tag = soup.findAll( "td" )

    for td in td_tag:
        rowspan = td.get( "rowspan" )

        if not rowspan == None \
          and rowspan == "2":
            a = td.find( "a" )
            p_id = a.get( "href" ).split( "/" )[3]
            
            if len( result["father"] ) == 0:
                result["father"] = p_id
            else:
                result["mother"] = p_id

    return result

def main():
    parent_id_data = dm.pickle_load( "parent_id_data.pickle" )

    update_horce_id_list = dm.pickle_load( "update_horce_id_list.pickle" )
    url_list = []
    key_list = []

    for horce_id in update_horce_id_list:
        #if not horce_id in parent_id_data:
        url_list.append( "https://db.netkeiba.com/horse/" + horce_id )
        key_list.append( horce_id )
        
    add_data = lib.thread_scraping( url_list, key_list ).data_get( parent_id_get )

    for horce_id in add_data.keys():
        parent_id_data[horce_id] = add_data[horce_id]
        ps.HorceData().update_data( "parent_id", json.dumps( add_data[horce_id] ), horce_id )
    
    dm.pickle_upload( "parent_id_data.pickle", parent_id_data )
    horce_data_storage = dm.pickle_load( "horce_data_storage.pickle" )
    url_list.clear()
    key_list.clear()
    
    for k in add_data.keys():
        f_id = parent_id_data[k]["father"]
        m_id = parent_id_data[k]["mother"]

        if not f_id in horce_data_storage:
            try:
                int( f_id )
                url_list.append( "https://db.netkeiba.com/horse/" + f_id )
                key_list.append( f_id )
            except:
                f_id = 0
                
            try:
                int( m_id )
                url_list.append( "https://db.netkeiba.com/horse/" + m_id )
                key_list.append( m_id )
            except:
                m_id = 0
                
    parent_data = lib.thread_scraping( url_list, key_list ).data_get( horse_data_collect )
    
    for horce_id in parent_data.keys():
        horce_data_storage[horce_id] = parent_data[horce_id]
    
    dm.pickle_upload( "horce_data_storage.pickle", horce_data_storage )
    
main()
