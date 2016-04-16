import requests
URL="http://127.0.0.1:8000/android/chatbot_details"

r=requests.post(URL,data={'user_name':'kai123456android','password':'kai123456android',
'age':20,'gender':'M','dob':'1996-01-01','address':'home','phone_number':'9741091140','first_name':'kaiAndroid','last_name':'AndroidKai'})
print(r.text,r.status_code)