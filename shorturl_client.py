'''Shorturl is pythonscript module for tinyfying urls
    Copyright (C) 2019  Luis Miguel Santos
    email: luismigue1234@hotmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
'''
Name: shorturl
Author: Luis Miguel Santos
Purpose: This small python module provides functionality for a url shortening infrastructure.
Basically, a program using this library can process a larger url and produce a smaller version 
that can always be regenerated. The generated url contains a the base domain name and an 
alias. Both the alias and original url are saved in a SQL database which gets garbage collected
routinely for unused aliases. A server implementation was included for reference purposes.
The server listens for urls encapsulated by <url> for url that need to be converted to a tinier
version and [url] for aliases used to extract the real/original url. All functions in the library attempt
to be sane (check for a valid connection or statement compiler object).

Example:
Client -> <www.gshdjkgh.com> : Server -> new_url
Client-> [new_url] : Server -> www.gshdjkgh.com

Internally:
Server takes www.gshdjkgh.com and generates a alias/fingerprint/digest and stores it in the
sqlite database. When Client requests the url by providing the alias, the server retrieves www.gshdjkgh.com from database entry with alias = new_url

List of symbols defined:
shorturl_init
shorturl_exists
shorturl_generateAlias
shorturl_getAlias
shorturl_getRealURL
shorturl_new
shorturl_parse_alias
shorturl_purgeURL
shorturl_close

Access API:
shorturl_init
shorturl_new(url)
shorturl_getAlias(url)
shorturl_getRealURL(alias)
shorturl_close
'''
'''Needed modules'''
import sqlite3, socket, base64, zlib

db_location = "shorturl.db"
db_connection = None
db_statement_compiler = None
'''Server globals'''
shorturl_server_socket = None
shorturl_HOST = 'localhost'
shorturl_PORT = 5555


'''Library initializing function'''
def shorturl_init():
    global db_connection 
    global db_statement_compiler
    db_connection = sqlite3.connect(db_location)
    if db_connection is None:
        print "Error making a database connection!"
        return
    else:
        db_statement_compiler = db_connection.cursor()
        if db_statement_compiler is None:
            print "Error grabbing an instance of a SQLite cursor/statement compiler!"
            return
        else:
            print "shorturl initialized successfully!"

'''Clean library for a clean shutdown. Make sure to flush contents ijn memory back to database'''
def shorturl_close():
    global db_connection 
    global db_statement_compiler
    if db_connection != None:
        db_connection.commit()
        db_connection.close()

''' Main function of this library. Provide a url and it will return its digest. The function will store the
url:digest mapping in a SQL database'''
def shorturl_new(url):
    global db_connection 
    global db_statement_compiler
    alias_entry = None
    if db_connection != None or db_statement_compiler != None:
        alias_entry = shorturl_generateAlias(url)
        if shorturl_exists(alias_entry):
            db_statement_compiler.execute("UPDATE shorturl SET alias=?, url=? WHERE alias=?", (alias_entry, url,alias_entry))
            db_connection.commit()
        else:
            db_statement_compiler.execute("INSERT INTO shorturl(alias,url) VALUES(?,?)", (alias_entry, url))
            db_connection.commit()
        return alias_entry
    else:
        print "Error: no connection or statement compiler available!"
    
'''Returns the url mapped by alias'''    
def shorturl_getRealURL(alias):
    global db_connection 
    global db_statement_compiler
    url = None
    row = None
    print alias
    if db_connection != None or db_statement_compiler != None:
        db_statement_compiler.execute("SELECT * FROM shorturl WHERE alias=?", (alias,))
        row = db_statement_compiler.fetchone()
        print row
        if row is not None:
            return row[2]
        else:
            print "Error: No results available or SQLite failed to generate row object"
            return None
    else:
        print "Error: no connection or statement compiler available!"

'''Returns alias mapped by url'''            
def shorturl_getAlias(url):
    global db_connection 
    global db_statement_compiler
    alias = None
    row = None
    if db_connection != None or db_statement_compiler != None:
        db_statement_compiler.execute("SELECT * FROM shorturl WHERE url=?", (url,))
        row = db_statement_compiler.fetchone()
        if row is not None:
            return row[1]
        else:
            print "Error: No results available or SQLite failed to generate row object"
            return None
    else:
        print "Error: no connection or statement compiler available!"
        
'''Check if record already exists'''
def shorturl_exists(alias):
    global db_connection 
    global db_statement_compiler
    if db_connection != None or db_statement_compiler != None:
        print alias
        db_statement_compiler.execute("SELECT * FROM shorturl WHERE alias=?", (alias,))
        row = db_statement_compiler.fetchone()
        if row is not None:
            return True
    else:
        print "Error: no connection or statement compiler available!"
    return False

'''Simple alias generation from a string'''        
def shorturl_generateAlias(url):
    #return base64.b64encode(url) is too long, so we run it on a crc digest first
    return base64.b64encode(str(zlib.crc32(url)))
    
def shorturl_parse_alias(url):
    return url.rfind("/")

'''Unit test for shorturl'''
def shorturl_unittest():
    url = "https://github.com/kiseitai2/Engine_Eureka/blob/master/Dependencies/Python27/include/bufferobject.h"
    print "Old url: ", url
    shorturl_init()
    print "New url: ", shorturl_new(url)
    print "Original url: ", shorturl_getRealURL(shorturl_new(url))
    shorturl_close()

def shorturl_client():
    shorturl_init()
    shorturl_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    shorturl_server_socket.connect((shorturl_HOST, shorturl_PORT))
    shorturl_server_socket.send("<https://github.com/kiseitai2/Engine_Eureka/blob/master/Dependencies/Python27/include/bufferobject.h>")
    data = shorturl_server_socket.recv(1024)
    print data
    shorturl_server_socket.send("[" + "http://test.nothing/" + data + "]")
    data = shorturl_server_socket.recv(1024)
    print data
    
    shorturl_close()
    

if __name__=="__main__":
    #Unit test
    shorturl_unittest()
	#main()
    shorturl_client()
	
