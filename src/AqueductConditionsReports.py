'''
Created on Jun 10, 2017

@author: pyropenguin
'''
import requests
from html.parser import HTMLParser
import re
from datetime import datetime


DISTRICTS = {'Mono Basin':                  'monorealtime',
             'Long Valley':                 'lvrealtime',
             'Northern Owens Valley':       'norealtime',
             'Southern Owens Valley':       'sorealtime',
             'Lower Owens River Project':   'owensrealtime',
             'Southern District':           'sdrealtime'}

class District:
    URL_BASE = 'http://wsoweb.ladwp.com/Aqueduct/realtime/'
    def __init__(self, DistrictExtension):
        self.URL = self.URL_BASE + DistrictExtension + '.htm'
        self.DataSourceIDs = None
    
    def _request(self):
        self.r = requests.get(self.URL)
    
    def fetchIds(self):
        self._request()
        
        p = self.DistrictHTMLParser()
        p.feed(self.r.text)
        
        self.DataSourceIDs = p.DataSourceIDs

    class DistrictHTMLParser(HTMLParser):
        def __init__(self):
            self.DataSourceIDs = []
            HTMLParser.__init__(self)

        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                # Try to get dataID from lastfive javascript function parameter
                for _attr in [x[1] for x in attrs if 'lastfive' in x[1]]:
                    try:
                        r = re.search("lastfive\('([0-9]*)'\)",_attr)
                        _id = r.group(1)
                        self.DataSourceIDs.append(_id)
                    except:
                        pass # Ignore if the regex fails        

class DataSource:
    URL_BASE = 'http://wsoweb.ladwp.com/Aqueduct/realtime/'
    def __init__(self, DataSourceID):
        self.URL = self.URL_BASE + DataSourceID + '.htm'
        self.title = None
        self.data = None

    def _request(self):
        self.r = requests.get(self.URL)
    
    def fetchData(self):
        self._request()
        
        p = self.DataSourceHTMLParser()
        p.feed(self.r.text)
        
        self.title = p.title
        self.data = p.data
        self.retrieved = datetime.utcnow()

    class DataSourceHTMLParser(HTMLParser):
        def __init__(self):
            self.isTitle = False
            self.isData = False
            self.title = None
            self.date = None
            self.data = []
            HTMLParser.__init__(self)
            
        def handle_starttag(self, tag, attrs):
            if tag == 'form':
                self.isTitle = True
                
        def handle_data(self, data):
            if self.isTitle and len(data.strip()) > 0:
                self.title = data
                self.isTitle = False
            elif data == 'Reading':
                self.isData = True
            elif self.isData and len(data.strip()) > 0:
                if self.date is None:
                    # Save the date because the next thing will be the value
                    try:
                        self.date = datetime.strptime(data.strip(), 
'%m/%d/%y %I:%M:%S %p')
                    except:
                        print('Could not convert date: ', data.strip())
                else:
                    # Write the date and value to the data, then clear the saved date
                    self.data.append((self.date, 
float(data.replace(' ','').strip())))
                    self.date = None # 


if __name__ == '__main__':
    for district in DISTRICTS.keys():
    #for district in ['Southern District']:
        d = District(DISTRICTS[district])
        d.fetchIds()
        
        print('===== ' + district + ' =====')
        for _id in d.DataSourceIDs:
            #print(_id)
            d = DataSource(_id)
            d.fetchData()
            
            print(d.title)
            print(d.data[0:5])
