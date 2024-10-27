import openmeteo_requests
import numpy as np
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
import json
def get_weather(x):

	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)


	url = "https://archive-api.open-meteo.com/v1/archive"
	params = {
		"latitude": float(x.split(',')[0]),
		"longitude": float(x.split(',')[1].removeprefix(' ')),
		"start_date": "2023-09-28",
		"end_date": "2024-09-30",
		"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "et0_fao_evapotranspiration", "wind_speed_10m", "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm", "soil_temperature_28_to_100cm", "soil_temperature_100_to_255cm", "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm", "soil_moisture_28_to_100cm", "soil_moisture_100_to_255cm"]
	}
	responses = openmeteo.weather_api(url, params=params)

	response = responses[0]

	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
	hourly_rain = hourly.Variables(3).ValuesAsNumpy()
	hourly_et0_fao_evapotranspiration = hourly.Variables(4).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy()
	hourly_soil_temperature_0_to_7cm = hourly.Variables(6).ValuesAsNumpy()
	hourly_soil_temperature_7_to_28cm = hourly.Variables(7).ValuesAsNumpy()
	hourly_soil_temperature_28_to_100cm = hourly.Variables(8).ValuesAsNumpy()
	hourly_soil_temperature_100_to_255cm = hourly.Variables(9).ValuesAsNumpy()
	hourly_soil_moisture_0_to_7cm = hourly.Variables(10).ValuesAsNumpy()
	hourly_soil_moisture_7_to_28cm = hourly.Variables(11).ValuesAsNumpy()
	hourly_soil_moisture_28_to_100cm = hourly.Variables(12).ValuesAsNumpy()
	hourly_soil_moisture_100_to_255cm = hourly.Variables(13).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["temperature_2m"] = np.average(hourly_temperature_2m.tolist())
	hourly_data["relative_humidity_2m"] = np.average(hourly_relative_humidity_2m.tolist())
	hourly_data["dew_point_2m"] = np.average(hourly_dew_point_2m.tolist())
	hourly_data["rain"] = np.average(hourly_rain.tolist())
	hourly_data["et0_fao_evapotranspiration"] = np.average(hourly_et0_fao_evapotranspiration.tolist())
	hourly_data["wind_speed_10m"] = np.average(hourly_wind_speed_10m.tolist())
	st1 = np.average(hourly_soil_temperature_0_to_7cm.tolist())
	st2 = np.average(hourly_soil_temperature_7_to_28cm.tolist())
	st3 = np.average(hourly_soil_temperature_28_to_100cm.tolist())
	st4 = np.average(hourly_soil_temperature_100_to_255cm.tolist())
	sm1 = np.average(hourly_soil_moisture_0_to_7cm.tolist())
	sm2 = np.average(hourly_soil_moisture_7_to_28cm.tolist())
	sm3 = np.average(hourly_soil_moisture_28_to_100cm.tolist())
	sm4 = np.average(hourly_soil_moisture_100_to_255cm.tolist())
	soilt = (st1 + st2 + st3 + st4) / 4
	soilm = (sm1 + sm2 + sm3 + sm4) / 4
	entry = [hourly_data["temperature_2m"], hourly_data["relative_humidity_2m"], hourly_data["dew_point_2m"], hourly_data["rain"], hourly_data["et0_fao_evapotranspiration"],
			 hourly_data["wind_speed_10m"], soilt, soilm]

	return entry



def get_air(x):
	params = {
	  "period": {
		  "startTime":"2024-09-23T08:00:00Z",
		  "endTime":"2024-10-13T08:00:00Z"
	  },
	  "pageSize": 24,
	  "location": {
		"latitude": float(x.split(',')[0]),
		"longitude": float(x.split(',')[1].removeprefix(' '))
	  },
	  "extraComputations": [
		"POLLUTANT_CONCENTRATION"
	  ],
	}

	link = requests.post('https://airquality.googleapis.com/v1/history:lookup?key=AIzaSyDxGsCeJRDMAgqfTVJBpnHpVQ-vE_7K1cI', json=params)
	i = link.json()


	pollutants = i['hoursInfo'][0]['pollutants']
	co = pollutants[0]['concentration']['value']
	no = pollutants[1]['concentration']['value']
	o3 = pollutants[2]['concentration']['value']
	pm10=pollutants[3]['concentration']['value']
	pm25=pollutants[4]['concentration']['value']
	so2 =pollutants[5]['concentration']['value']

	return [co, no, o3, pm10, pm25, so2]




def get_farm(county):
	farm_dict = {'Alamance County':[271353,720], 'Alexander County':[166122,544],'Alleghany County':[150398,448],'Anson County':[340216,412],'Ashe County':[272778,864], 'Avery County':[158108,351],'Beaufort County':[529908,310],'Bertie County':[447601,323],'Bladen County':[559592,512],'Brunswick County':[542033,231],'Buncombe County':[419779,1073],'Burke County':[324276,508],'Cabarrus County':[231524,629],'Caldwell County':[301819,411],'Camden County':[153958,81],'Carteret County':[323655,158],'Caswell County':[271679,493],'Catawba County':[255179,638],'Chatham County':[436696,1116],'Cherokee County':[291367,277],'Chowan County':[110460,97],'Clay County':[137425,164],'Cleveland County':[297120,1005],'Columbus County':[599880,514],'Craven County': [453695,245],'Cumberland County':[417211,336],'Currituck County': [167608,89],'Dare County':[245424,32],'Davidson County':[353417,1003],'Davie County': [168993,591],'Duplin County':[521886,820],'Durham County':[183022,241],
			  'Edgecombe County': [323276,249],'Forsyth County':[261220,557],'Franklin County':[314701,538],'Gaston County':[227856,522],'Gates County':[217884,141],'Graham County':[186915,123],'Granville County':[339838,557],'Greene County':[170201,207],'Guilford County':[413565,854],'Halifax County':[463414,336],'Harnett County': [380757,643],'Haywood County':[354344,541],'Henderson County':[238691,455],'Hertford County':[226028,126],'Hoke County':[250076,189],'Hyde County':[392146,138],'Iredell County':[367488,1055],'Jackson County':[314055,215],'Johnston County':[506377,1063],'Jones County':[301576,177],'Lee County':[163168,250],'Lenoir County':[255858,386],'Lincoln County':[190683,614],'McDowell County':[282219,333],'Macon County':[329964,340],'Madison County':[287629,639],'Martin County':[295152,332],'Mecklenburg County':[335216,216],'Mitchell County':[141718,250],'Montgomery County':[314730,240],'Moore County':[446491,733],'Nash County':[345751,425],'New Hanover':[122569,59],'Northampton County':[343409,272],'Onslow County':[489752,340],'Orange County':[254461,686],'Pamlico County':[215643,100],'Pasquotank County':[145203,126],'Pender County':[556656,336],
			  'Perquimans County':[158159,149],'Person County':[251069,393],'Pitt County':[417012,478],'Polk County':[152222,281],'Randolph County':[503162,1368],'Richmond County':[302998,237],'Robeson County':[607208,722],'Rockingham County':[361953,844],'Rowan County':[327141,925],'Rutherford County':[361034,620],'Sampson County':[604599,960],'Scotland County':[204293,108],'Stanly County':[252836,672],'Stokes County':[287269,856],'Surry County':[340586,1064],'Swain County':[337978,99],
			  'Transylvania County':[242162,215],'Tyrrell County':[248980,68],'Union County':[404160,957],'Vance County':[162248,238],'Wake County':[532415,691],'Warren County':[274207,267],'Washington County':[222843,141],'Watauga County':[199388,520],'Wayne County':[353730,551],
			  'Wilkes County':[483420,932],'Wilson County':[235633,276],'Yadkin County':[214289,818],'Yancey County':[199974,369]}
	return farm_dict[county]

import pandas as pd
import requests
import urllib
import geopy.distance
import pickle
import catboost
dfi = pd.read_excel("C:/Users/johns/OneDrive/Documents/databook.xlsx")
df = pd.read_excel("C:/Users/johns/OneDrive/Documents/pfas.xlsx")
def get_coords(x):
    

    ex = urllib.parse.quote_plus(x)
    req = requests.post(f'https://maps.googleapis.com/maps/api/geocode/json?address={ex}&key=AIzaSyDxGsCeJRDMAgqfTVJBpnHpVQ-vE_7K1cI')
    resp = req.json()


    lat , lng = resp['results'][0]['geometry']['location']['lat'], resp['results'][0]['geometry']['location']['lng']
    county = resp['results'][0]['address_components'][3]['long_name']
    return (str(lat) + ',' + str(lng)), county


def pollutors(x):
    num12 = 0
    num4 = 0
    num1 = 0
    for i in dfi['Add'].tolist():
        c = geopy.distance.distance(x, (i)).km
        if c < 12:
            num12 += 1
            if c < 4:
                num4 += 1
                if c < 1:
                    num1 += 1
    return (num12, num4, num1)


def known(x):
    knum = 0
    known_dic = {}
    
    for i in dfi['Address'].tolist()[:43]:
       
        c = geopy.distance.distance((x), (i)).km
        if c < 50:
            knum += 1
            l = dfi.loc[dfi['Address']==i]['Num'].item()
            
            known_dic[l] = c
    closest = min(known_dic, key=known_dic.get)
    closest_dict = known_dic[closest] 
    return (knum, closest, closest_dict)

def basin(x):
    dist = {}
    for n,l in zip(df['lat'].tolist(), df['lng'].tolist()):
        i = str(n) + ',' + str(l)
        c = geopy.distance.distance(x, (i)).km
        dist[i] = c
    closest = min(dist, key=dist.get)
    lat = float(closest.split(',')[0])  
    get_basin = df.loc[df['lat']==lat]['Basin'].item()
    return get_basin


def final(x, y):
    coords, county = get_coords(x)
    p12, p4, p1 = pollutors(coords)
    knowna, dist, name = known(coords)
    w = get_weather(coords)
    a = get_air(coords)
    farm, land = get_farm(county)
    entry = [float(coords.split(',')[0]), float(coords.split(',')[1].removeprefix(' ')),farm, land,p1,p4,p12,knowna, dist, name, basin(coords), w[0], w[1], w[2], w[3], w[4],w[5],w[6],w[7],a[0], a[1],a[2],a[3],a[4],a[5], y]

    return entry

def predict(address, well_depth):
    predictors = final(address, well_depth)
    with open("C:/Users/johns/Downloads/model.pkl", 'rb') as f:
        model = pickle.load(f)
    y_pred = model.predict(predictors)
    return (y_pred)
