import time, random, requests
import DAN
import threading, sys

#ServerURL = 'http://IP:9999'      #with non-secure connection
ServerURL = 'https://3.iottalk.tw' #with SSL connection
Reg_addr = 'C0:98:E5:00:00:97' #if None, Reg_addr = MAC address
url = 'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=46757'

DAN.profile['dm_name']='097dm'
DAN.profile['df_list']=['mes',]
DAN.profile['d_name']= 'IDF097' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line
print("dm_name is ", DAN.profile['dm_name'])
print("Server is ", ServerURL)
while True:
    try:
        import crawl_weather_V8
        data = crawl_weather_V8.table
        print(data['觀測時間'][0])
        # IDF_data = random.uniform(1, 10)
        # DAN.push ('Dummy_Sensor', IDF_data) #Push data to an input device feature "Dummy_Sensor"
        # data = requests.get(url)
        # print(data.text)
        DAN.push('AtPressure097', data['海平面氣壓(百帕)'][0])
        print(data['海平面氣壓(百帕)'][0])
        time.sleep(1)
        DAN.push('Humidity1_097', data['相對溼度(%)'][0])
        print(data['相對溼度(%)'][0])
        time.sleep(1)
        DAN.push('Temperature1_097', data['溫度(°C)'][0])
        print(data['溫度(°C)'][0])
        time.sleep(1)
        t = data['觀測時間'][0] 
        DAN.push('Time_097', t.strftime('%Y-%m-%d %H:%M'))
        print(data['觀測時間'][0])
        time.sleep(1)
        DAN.push('View_097', data['能見度(公里)'][0])
        print(data['能見度(公里)'][0])
        time.sleep(1)
        DAN.push('Weather_097', data['天氣'][0])
        print(data['天氣'][0])
        time.sleep(1)
        DAN.push('Wind1_097', data['風力 (m/s)'][0])
        print(data['風力 (m/s)'][0])
        time.sleep(1)
        DAN.push('Wind2_097', data['陣風 (m/s)'][0])
        print(data['陣風 (m/s)'][0])
        time.sleep(1)
        DAN.push('Winddr_097', data['風向'][0])
        print(data['風向'][0])
        time.sleep(1)



    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

