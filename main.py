import requests
import datetime
# importing environment variables from env_variables file
from env_variables import username, password, app_id, api_key, endpoint


# Hard coded username, password, id, and key. Would use these if I didn't set as env variables
# sheety_auth_username = "AuthorizedUser"
# sheety_auth_password = "100daysofcode"
# nutritionix_app_id = '5bf0bfcf'
# nutritionix_api_key = '31be71fa2c4599c8d0f084617b460d02'


# headers for nutritionix app_id and api_key to authenticate post request
headers = {
    "x-app-id": app_id,
    "x-app-key": api_key,
}

user_input = input("What exercises did you do?\n")

# parameters for request with fake data, will use whatever I type in for user_input
exercise_params = {
    "query": user_input,
    "gender": "male",
    "weight_kg": 100,
    "height_cm": 167.64,
    "age": 30
}

# feeds the inputs into the nutritionix exercise endpoint
# params for are for get requests and json is for post/put
exercise_response = requests.post(url='https://trackapi.nutritionix.com/v2/natural/exercise', json=exercise_params, headers=headers)
exercise_response.raise_for_status()
exercise_data = exercise_response.json()

# gets the current date & time
time_now = datetime.datetime.now()

# parses the date & time into designated formart and assigns to variables
Date = time_now.strftime("%m/%d/%Y")
Time = time_now.strftime("%H:%M:%S")

# endpoint for google sheet, input as an environment variable
sheety_endpoint = endpoint


# the response from the nutritionix exercise data goes dictionary -> list (of each individual exercise) -> dictionary.
# this for loop iterates through each of the workouts (segments of the list) and grabs exercise name, duration, and calories
# It takes these variables, along with the pre-assigned date & time, and adds them into a nested dictionary called "workout".
# It is called "workout" because it will go into the sheet called "workouts". To finish out the loop, it will then
# add that workout data to the google sheet as a new row. The loop will then continue to iterate, and add new rows if there
# were multiple workouts completed.
for exercise in exercise_data["exercises"]:
    add = {
        "workout":{
            "date": Date,
            "time": Time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheety_post = requests.post(url=sheety_endpoint, json=add, auth=(username,password))
    sheety_post.raise_for_status()




