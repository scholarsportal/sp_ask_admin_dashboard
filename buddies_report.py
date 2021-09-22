from lh3.api import *
from pprint import pprint as print


client = Client()
client.set_options(version = 'v1')
users = client.all('users').get_list()

for user in users:
    print(user.get('name'))
    buddies = client.one('contacts', user.get('name')).get_list('users')

    if len(users) != len(buddies):
        print("This is user:{0} has not been buddied with some operators".format(user.get('name')))
    
