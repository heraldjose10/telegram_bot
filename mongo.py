from pymongo import MongoClient

client=MongoClient("mongodb://heraldjose10:9400840572@covid-shard-00-00-9pl1n.mongodb.net:27017,covid-shard-00-01-9pl1n.mongodb.net:27017,covid-shard-00-02-9pl1n.mongodb.net:27017/covid?ssl=true&replicaSet=Covid-shard-0&authSource=admin&retryWrites=true&w=majority")
db=client.covid

def get_states_data():
    arr=[]
    res=db.covid_india_test.find({})
    for doc in res:
        arr.append([doc.get('name')])
    return(arr)

def make_dict(name):
    res=db.covid_india_test.find({})
    for i in res:
        if (i.get('name')==name):
            return(i.get('data'))
# print(get_states_data())
print(make_dict('Assam'))

# if __name__=='__main__':
#     main()
