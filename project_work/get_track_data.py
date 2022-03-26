from time import time
import fastf1 as ff1
import pandas as pd

ff1.Cache.enable_cache('C:/Users/vikyb/Desktop/project_dir/project_work/cached_data')

def get_track_status_data():
    """ 
    This function creates sessions for all races in all Grand Prix's from 2018 to 2021. 
    For each session, the function calls the API to GET the track_status_data.
    Once the track status data is in, it loops through the status counting the # of red flags 
    and # of safety cars for each race.
    Once all numbers are calculated for each race, the data to a Pandas DataFrame to be outputted 
    to a .csv file in 'project_work/track_data/track_data.csv'
    """
    actual_race_id = 989
    
    for year in (2018, 2019, 2020, 2021):
        for race_id in range(1, 23, 1):
            if (year == 2018 and race_id <= 21) or (year == 2019 and race_id <= 21) or (year == 2020 and race_id <= 17) or (year == 2021):
                
                race = ff1.get_session(year, race_id, 'R')
                track_data = ff1.api.track_status_data(race.api_path)
        
                time_data = track_data['Time']
                status_data = track_data['Status']
                message_data = track_data['Message']
        
                colated_list = []
                
                if year == 2020 or year == 2021:
                    for i in range(len(time_data)):
                        colated_list.append([time_data[i], status_data[i], message_data[i]])
                    
                    collected_data = pd.DataFrame(data = colated_list, columns = ['Time', 'Status', 'Message'])
                else:
                    for i in range(len(time_data)):
                        colated_list.append([actual_race_id, time_data[i], status_data[i], message_data[i]])
                    
                    collected_data = pd.DataFrame(data= colated_list, columns = ['race_id', 'Time', 'Status', 'Message'])
            
                collected_data.to_csv("project_work/track_data/track_{}_{}.csv".format(year, race_id))
            
                actual_race_id = actual_race_id + 1

# -----------------------------------------------------------------------------------------------------------------------------------

def get_weather_data():
    """ 
    This function creates sessions for all races in all Grand Prix's from 2018 to 2021. 
    For each session, the function calls the API to GET the track_status_data.
    Once the track status data is in, it loops through the status counting the # of red flags 
    and # of safety cars for each race.
    Once all numbers are calculated for each race, the data to a Pandas DataFrame to be outputted 
    to a .csv file in 'project_work/track_data/track_data.csv'
    """
    actual_race_id = 989
    
    for year in (2018, 2019, 2020, 2021):
        for race_id in range(1, 23, 1):
            if (year == 2018 and race_id <= 21) or (year == 2019 and race_id <= 21) or (year == 2020 and race_id <= 17) or (year == 2021):
                
                race = ff1.get_session(year, race_id, 'R')
                weather_data = ff1.api.weather_data(race.api_path)
                
                ambient_air_pressure = weather_data['Pressure']   
                humdity = weather_data['Humidity']
                track_temp = weather_data['TrackTemp']
                wind_speed = weather_data['WindSpeed']
                rain_fall = weather_data['Rainfall']
        
                colated_list = []
                
                if year == 2020 or year == 2021:
                    for i in range(len(ambient_air_pressure)):
                        colated_list.append([ambient_air_pressure[i], humdity[i], track_temp[i], wind_speed[i], rain_fall[i]])
                    
                    collected_data = pd.DataFrame(data = colated_list, columns = ['Pressure', 'Humidity', 'TrackTemp', 'WindSpeed', 'Rainfall'])
                else:
                    for i in range(len(ambient_air_pressure)):
                        colated_list.append([actual_race_id, ambient_air_pressure[i], humdity[i], track_temp[i], wind_speed[i], rain_fall[i]])
                    
                    collected_data = pd.DataFrame(data= colated_list, columns = ['race_id', 'Pressure', 'Humidity', 'TrackTemp', 'WindSpeed', 'Rainfall'])
            
                collected_data.to_csv("project_work/weather_data/weather_for_{}_{}.csv".format(year, race_id))
            
                actual_race_id = actual_race_id + 1

# -----------------------------------------------------------------------------------------------------------------------------------

def get_weather_and_track_data():
    """ 
    This function creates sessions for all races in all Grand Prix's from 2018 to 2021. 
    For each session, the function calls the API to GET the track_status_data.
    Once the track status data is in, it loops through the status counting the # of red flags 
    and # of safety cars for each race.
    Once all numbers are calculated for each race, the data to a Pandas DataFrame to be outputted 
    to a .csv file in 'project_work/track_data/track_data.csv'
    """
    
    track_data_finalized = pd.DataFrame(columns=['Race Id', 'Year', 'GP', 'Pressure', 'Humidity', 
                                                 'TrackTemp', 'WindSpeed', 'Rainfall', 'Number of Red Flags', 
                                                 'Number of Safety cars deployed'])
    actual_race_id = 989
    rain_percentage_during_race = 0.6
    
    for year in (2018, 2019, 2020, 2021):
        for race_id in range(1, 23, 1):
            if (year == 2018 and race_id <= 21) or (year == 2019 and race_id <= 21) or (year == 2020 and race_id <= 17) or (year == 2021):
                
                race = ff1.get_session(year, race_id, 'R')
                track_data = ff1.api.track_status_data(race.api_path)
                weather_data = ff1.api.weather_data(race.api_path)
                
                ambient_air_pressure = round(sum(weather_data['Pressure']) / len(weather_data['Pressure']), 3)    
                humdity = round(sum(weather_data['Humidity']) / len(weather_data['Humidity']), 3)
                track_temp = round(sum(weather_data['TrackTemp']) / len(weather_data['TrackTemp']), 3)
                wind_speed = round(sum(weather_data['WindSpeed']) / len(weather_data['WindSpeed']), 3)

                rain_true_counts = weather_data['Rainfall'].count(True)
                
                if (rain_true_counts / len(weather_data['Rainfall']) >= rain_percentage_during_race):
                    rain_fall = 1
                else:
                    rain_fall = 0
        
                status_data = track_data['Status']
                red_flag_count = 0
                safety_car_count = 0
            
                for status in status_data:
                    if status == '5':
                        red_flag_count += 1
                    elif status == '4':
                        safety_car_count += 1
        
                track_data_frame = pd.DataFrame(data = [[actual_race_id, year, race_id, ambient_air_pressure, humdity, track_temp, wind_speed, rain_fall, red_flag_count, safety_car_count]], 
                                                columns = ['Race Id', 'Year', 'GP', 'Pressure', 'Humidity', 'TrackTemp', 'WindSpeed', 'Rainfall', 'Number of Red Flags', 'Number of Safety cars deployed'])
                track_data_finalized = pd.concat([track_data_finalized, track_data_frame], sort=False)
            
                actual_race_id = actual_race_id + 1
                
    track_data_finalized.to_csv("project_work/finalized_data/track_and_weather_data_version2.csv")


get_weather_and_track_data()