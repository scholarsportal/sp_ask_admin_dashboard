#!/usr/bin/env python

# check-service.py
# ----------------
# Look to see if your services are online
#chats Open
import lh3.api
import requests
client = lh3.api.Client()
queues = client.all('queues').get_list()

#SMS
all_sms = [qu for qu in queues if   '-txt' in qu['name']]
sms_available = [ texto['name'] for texto in all_sms if texto['show']=='available']
print("{0}/{1}".format(len(sms_available), len(all_sms)))
sms_unavailable = [ texto['name'] for texto in all_sms if texto['show']=='unavailable']
print(sms_unavailable)

#WEB
without_sms= [qu for qu in queues if   '-txt' not in qu['name']]
web= [qu for qu in without_sms if   '-fr' not in qu['name']]

#Total vs total unavailable
unavailable = [ unavailable['name'] for unavailable in queues if unavailable['show']=='unavailable']
available = [ available['name'] for available in queues if available['show']=='available']
print("{0}/{1}".format(len(queues) - len(unavailable), len(queues)))


def main():
    client = lh3.api.Client()
    for queue in QUEUES:
        check_queue(client, queue)

if __name__ == '__main__':
    main()


