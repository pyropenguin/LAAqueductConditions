'''
Created on Jun 17, 2017

@author: pyropenguin
'''
from AqueductConditionsReports import District, DISTRICTS, DataSource
from ExportData import DataExporter

exp = DataExporter()
for district in DISTRICTS.keys():
    d = District(DISTRICTS[district])
    d.fetchIds()
    
    print('===== ' + district + ' =====')
    for _id in d.DataSourceIDs:
        #print(_id)
        d = DataSource(_id)
        d.fetchData()
        
        print(d.title)
        print(d.data[0:5])
        
        exp.add(district, d.title, d.data)
    
exp.export()
