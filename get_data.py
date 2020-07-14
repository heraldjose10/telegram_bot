import requests

url='https://api.covid19india.org/data.json'
r=requests.get(url)
data=r.json()
states=data.get('statewise')

def get_states_data():
    arr=[]
    d=dict()
    for i in states:
        arr.append(i.get('state'))
        d[i.get('state')]=[i.get('active'),i.get('confirmed'),i.get('deaths'),i.get('recovered')]
    return(d)

