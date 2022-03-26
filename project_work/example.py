from time import time
import fastf1 as ff1
import pandas as pd

ff1.Cache.enable_cache('C:/Users/vikyb/Desktop/project_dir/project_work/cached_data')

# ----------------------------------------------------------------------------------------------------

# Testing Track Data
def testing_track_data(race_session):
    track_data = ff1.api.track_status_data(race_session.api_path)
    status_data = track_data['Status']
    print ('status_data type', type(status_data))

    red_flag_count = 0
    safety_car_count = 0
    count = 0
            
    for status in status_data:
        print('Status = ', status)
        count += 1
        if status == '5':
            red_flag_count += 1
        if status == '4':
            safety_car_count += 1

    print('Generic Count = ', count)
    print('Number of red flags = ', red_flag_count)
    print('Number of safety cars = ', safety_car_count)

# ----------------------------------------------------------------------------------------------------

# Testing Weather Data
def testing_weather_data(race_session):
    weather_data = ff1.api.weather_data(race_session.api_path)
    print(weather_data['Rainfall'])
    
    ambient_air_pressure = weather_data['Pressure']
    humidity = weather_data['Humidity']
    track_temp = weather_data['TrackTemp']
    wind_speed = weather_data['WindSpeed']
    
    pressure_average = round(sum(ambient_air_pressure) / len(ambient_air_pressure), 3)
    humdity_average = round(sum(humidity) / len(humidity), 3)
    track_temp_average = round(sum(track_temp) / len(track_temp), 3)
    wind_speed_average = round(sum(wind_speed) / len(wind_speed), 3)
    
    if True in weather_data['Rainfall']:
        rain_fall = 1
    else:
        rain_fall = 0
    
    weather_frame = pd.DataFrame(data = [[1002, 2018, 3, pressure_average, humdity_average, track_temp_average, wind_speed_average, rain_fall]], 
                                 columns = ['Race Id', 'Year', 'GP', 'Pressure', 'Humidity', 'TrackTemp', 'WindSpeed', 'Rainfall'])
    weather_frame.to_csv('project_work/weather_data/weather_data_2.csv')

# ----------------------------------------------------------------------------------------------------


# Calling the methods above
race = ff1.get_session(2018, 3, 'R')
#testing_track_data(race)
testing_weather_data(race)