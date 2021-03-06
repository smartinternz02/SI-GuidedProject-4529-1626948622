# Python program to find current
# weather details of any city
# using openweathermap api

# import required modules
import requests, json
import wiotp.sdk.device
import time
import random


'''
# Enter your API key here
api_key = "560c4b69bb0a2c87ee3b704e9efed8e8"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
#complete_url = base_url  + "appid=" + api_key + "&q=" + city_name '''


complete_url = "https://api.openweathermap.org/data/2.5/weather?units=metric&appid=560c4b69bb0a2c87ee3b704e9efed8e8&q=Karnataka"
print(complete_url)

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":

	# store the value of "main"
	# key in variable y
	y = x["main"]

	# store the value corresponding
	# to the "temp" key of y
	current_temperature = y["temp"]

	# store the value corresponding
	# to the "pressure" key of y
	current_pressure = y["pressure"]

	# store the value corresponding
	# to the "humidity" key of y
	current_humidity = y["humidity"]

	

	# store the value of "weather"
	# key in variable z
	z = x["weather"]

	# store the value corresponding
	# to the "description" key at
	# the 0th index of z
	weather_description = z[0]["description"]

	current_visibility = x["visibility"]

	# print following values
	print(" Temperature (in Celcius unit) = " +
					str(current_temperature) +
		"\n atmospheric pressure (in hPa unit) = " +
					str(current_pressure) +
		"\n humidity (in percentage) = " +
					str(current_humidity) +
		"\n description = " +
					str(weather_description)+
                "\n Visibilty = " +
                                        str(current_visibility))
else:
	print(" City Not Found ")

if current_visibility < 200:
        speed = 10
elif current_visibility <= 3000 and current_visibility >=200:
        speed = 30
elif current_visibility <= 6000 and current_visibility >= 3000:
        speed = 40
else:
        speed = 60
print("Maitain Speed to: ",speed)
myConfig = { 
    "identity": {
        "orgId": "jt2v00",
        "typeId": "VITDevice",
        "deviceId":"12345"
    },
    "auth": {
        "token": "987654321"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    print()

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

tf_density = random.randint(0,100)
if tf_density > 80:
        tf_density = 'Pls take left diversion , Traffic ahead'
        divr = True
else:
        tf_density = 'No Traffic Ahead...Safe Journey'
        divr = False
print(tf_density)

myData={'temperature':current_temperature, 'humidity':current_humidity, 'des':weather_description,'visible':current_visibility,'Speed':speed,'density':tf_density,'div':divr}
client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
print("Published data Successfully: %s", myData)
while True:
    client.commandCallback = myCommandCallback
    time.sleep(2)
client.disconnect()

