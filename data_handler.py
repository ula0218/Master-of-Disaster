import pandas as pd
from math import radians, sin, cos, sqrt, atan2

class DataHandler:
    def __init__(self):
        self.folder = 'data/'
        self.city_datafile = {
            'Taipei': '113年臺北市防空疏散避難設施資料集Q1_1130501.csv',
            'Hsinchu': '4325ac68-9ee1-43a3-97ad-c9d9ea6fdf60.csv',
        }
        self.columns = { # name : synonyms
            '類別': [],
            '建築物名稱': [],
            '電腦編號': [],
            '村里別': [],
            '地址': [],
            '緯經度': [],
            '地下樓層數': [],
            '可容納人數': [],
            '轄管分局': [],
            '備註': [],
        }
        self.city_df = {}
    def load_data(self):
        for city, file in self.city_datafile.items():
            self.city_df[city] = pd.read_csv(self.folder + file)#, index_col = 0)
        
        # print(self.city_df['Taipei'].iloc[4, :])
        # print(self.city_df['Hsinchu'].iloc[4, :])


    def find_closest(self, lat, lon):
        # 將座標字串轉換為數值
        df = pd.DataFrame(self.city_df['Taipei'])
        df['lat'] = df['緯經度'].apply(lambda x: eval(x)[0])
        df['lon'] = df['緯經度'].apply(lambda x: eval(x)[1])

        # Define Haversine distance calculation function
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth radius in kilometers
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            return distance

        # Calculate distances
        df['distance'] = df.apply(lambda row: haversine(row['lat'], row['lon'], lat, lon), axis=1)

        # Find the nearest coordinate
        nearest_coord = df.loc[df['distance'].idxmin()]

        # print("Type:", nearest_coord['類別'])
        # print("Nearest coordinate:", nearest_coord['緯經度'])
        # print("Address:", nearest_coord['地址'])
        # print("Floors:", nearest_coord['地下樓層數'])
        # print("Capacity:", nearest_coord['可容納人數'])
        # print("Authority:", nearest_coord['轄管分局'])
        # print("Distance:", nearest_coord['distance'], "km")

        return nearest_coord['類別'], nearest_coord['緯經度'], nearest_coord['地址'], \
            nearest_coord['地下樓層數'], nearest_coord['可容納人數'], nearest_coord['轄管分局'], \
                nearest_coord['distance']




# dh = DataHandler()
# dh.load_data()