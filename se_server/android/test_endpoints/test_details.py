import requests
URL="http://127.0.0.1:8000/android/get_details"

#Run all possible tests

r=requests.post(URL,data={'user_name':'kai123456','password':'kai123456'})
print(r.text)
