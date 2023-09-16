'''
Created on Jun 17, 2017

@author: pyropenguin
'''
import datetime
import os

DATA_PATH = os.path.join('data')

class DataExporter:
    def __init__(self):
        self.data = []
    
    def add(self, district, source, date_val_data):
        #self.data += [(date, district, source, val, retrieved) for date, val in date_val_data]
        self.data += [(date, district, source, val) for date, val in date_val_data]
    
    def sort_by_datetime(self, data):
        return sorted(data, key=lambda tup: tup[0]) # date
        
    def sort_by_district_datetime(self, data):
        data = sorted(data, key=lambda tup: tup[0]) # date
        data = sorted(data, key=lambda tup: tup[1]) # district

    def sort_by_district_source_datetime(self, data):
        data = sorted(data, key=lambda tup: tup[0]) # date
        data = sorted(data, key=lambda tup: tup[1]) # district
        data = sorted(data, key=lambda tup: tup[2]) # source
        return data
    
    def get_district_set(self, data):
        return set(item[1] for item in data)
    
    def export(self):
        date_sets = self.build_date_sets(self.data)
        
        for date in date_sets.keys():
            data = date_sets[date]
            filename = self.get_data_filename(date)
            filepath = os.path.join(DATA_PATH,filename)
            
            if os.path.exists(filepath):
                data = self.merge_data_with_file(data, filepath)
            else:
                pass
            
            data = self.sort_by_datetime(data)
            
            with open(filepath, 'w') as f:
                f.write('date,district,source,value\n')
                for entry in data:
                    line = ','.join(str(item) for item in entry)
                    f.write(line)
                    f.write('\n')
    
    def build_date_sets(self, data):
        date_sets = {}
        for entry in data:
            date = entry[0].date()
            try:
                date_sets[date].append(entry)
            except KeyError:
                date_sets[date] = [entry]
        return date_sets

    def get_data_filename(self, date):
        return 'AqueductConditions_' + \
            str(date.year) + '-' + \
            str(date.month) + '-' + \
            str(date.day) + '.csv'
                
    def merge_data_with_file(self, data, filepath):
        file_data = self.get_data_from_file(filepath)
        
        for entry in file_data:
            if entry not in data:
                data.append(entry)
                #print('Added data: ' + str(entry))
            else:
                #print('Data already present: ' + str(entry))
                pass #do not add
            
        return data
        
    def get_data_from_file(self, filepath):
        header = True
        file_data = []
        with open(filepath, 'r') as f:
            for line in f:
                if header == True:
                    header = False
                    continue
                split_line = line.strip().split(',')
                entry = (datetime.datetime.strptime(split_line[0], '%Y-%m-%d %H:%M:%S'), # date
                         split_line[1], # district
                         split_line[2], # source
                         float(split_line[3])) # value
                         #datetime.datetime.strptime(split_line[4], '%Y-%m-%d %H:%M:%S.%f')) # retrieved
                file_data.append(entry)
        return file_data
        

if __name__ == '__main__':
    TestData=[(datetime.datetime(2017, 6, 17, 9, 9, 56), 14.3), (datetime.datetime(2017, 6, 17, 8, 54, 56), 14.3), (datetime.datetime(2017, 6, 17, 8, 39, 56), 12.7), (datetime.datetime(2017, 6, 17, 8, 24, 56), 12.7), (datetime.datetime(2017, 6, 17, 8, 9, 56), 12.7)]
    TestDistrict='Long Valley'
    TestDataSource='Upper Gorge at TRS'
    
    d = DataExporter()
    d.add(TestDistrict, TestDataSource, TestData)
    d.export()
    
    