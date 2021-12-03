from lh3.api import *
from pprint import pprint as print
import pandas as pd


client = Client()
client.set_options(version = 'v1')
users = client.all('users').get_list()
total_number_of_operators = len(users)
report = list()

for user in users[45:50]:
    possible_buddies = client.one('contacts', user.get('name')).get_list('users')
    # LH3 support => If subscription is N, then there's no subscription and the users are not buddied.
    buddies = [b for b in possible_buddies if b['subscription'] != 'N']

    print(user.get('name'))
    if len(users) != len(buddies):
        print("This is user:{0} has not been buddied with some operators".format(user.get('name')))
    
    new_entry = {
        "operator x":user.get('name'),
        "Total number of operator": total_number_of_operators,
        "Total buddies of operator x":len(buddies),
        "discrepancy": total_number_of_operators == len(buddies),
        "difference": total_number_of_operators - len(buddies)
    }
    print(new_entry)
    report.append(new_entry)
    
df = pd.DataFrame(report)
df.to_excel("operator_buddies2.xlsx")



