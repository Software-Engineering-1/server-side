import requests

data={}
r=requests.post("127.0.0.1:8000/android/login",data,data)
print(r)