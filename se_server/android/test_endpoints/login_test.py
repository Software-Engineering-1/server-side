import requests
URL="http://127.0.0.1:8000/android"

#Run all possible tests

r=requests.post(URL+"/login",data={'user_name':'kai123456','password':'kai123456'})
print(r.text)

r=requests.post(URL+"/login",data={'user_name':'','password':''})
print(r.text)

r=requests.post(URL+"/login",data={'user_name':'kai123456','password':'kai1456'})
print(r.text)

r=requests.post(URL+"/login",data={'user_name':'kai123456'})
print(r.text)

