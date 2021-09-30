import json, os, sys
from pprint import pprint as print
from datetime import datetime
from datetime import date
from collections import Counter
from collections import OrderedDict

import pandas as pd
import lh3.api as lh3

try:
    from home.models import UnansweredChat
    from home.models import ReportMonthly
except:
    pass

client = lh3.Client()
chats = client.chats()

FRENCH_QUEUES = ['algoma-fr', 'clavardez', 'laurentian-fr', 'ottawa-fr',
        'saintpaul-fr', 'western-fr', 'york-glendon-fr']
SMS_QUEUES = ['carleton-txt', 'clavardez-txt', 'guelph-humber-txt',
            'mcmaster-txt', 'ottawa-fr-txt', 'ottawa-txt',
            'scholars-portal-txt', 'western-txt', 'york-txt']
PRACTICE_QUEUES = ['practice-webinars', 'practice-webinars-fr', 'practice-webinars-txt']

LIST_OF_HOURS = dict()
UNANSWERED_CHATS = list()
UNANSWERED_CHATS_HTML = ['<h1 align="center">UNANSWERED CHATS</h1><hr/><br/>']

def french_queues(chats):
    french = list()
    for chat in chats:
        if chat.get('queue') in FRENCH_QUEUES:
            french.append(chat)
    return french

def sms_queues(chats):
    sms = list()
    for chat in chats:
        if chat.get('queue') in SMS_QUEUES:
            sms.append(chat)
    return sms

def remove_practice_queues(chats_this_day):
    res = [chat for chat in chats_this_day if not "practice" in chat.get("queue")]
    return res

def get_chat_for_this_day(this_day):
    day = this_day.day
    year = this_day.year
    month = this_day.month

    all_chats = chats.list_day(year,month,day)
    return all_chats

def get_daily_stats(chats_this_day, chat_not_none, today):
    unanswered_chats = [chat for chat in chats_this_day if chat.get("accepted") is None]
    answered_chats_nbr = len(chats_this_day)- len(unanswered_chats)
    french_chats = french_queues(chat_not_none)
    sms_chats = sms_queues(chat_not_none)

    data = []
    data.append({
        # 'Date': today,
        'Day': today.strftime("%A, %b %d %Y"),
        'Total chats': len(chats_this_day),
        'Total Answered Chats': answered_chats_nbr,
        'Total UnAnswered Chats': len(unanswered_chats),
        'Total French Answered': len(french_chats),
        'Total SMS Answered': len(sms_chats)
    })
    return data

def get_chat_per_hour(chat_not_none):
    chat_per_hour_not_none = list()
    for chat in chat_not_none:
        d = datetime.strptime(chat.get('started'), "%Y-%m-%d %H:%M:%S")
        chat["hour"] = d.hour
        chat_per_hour_not_none.append(d.hour)

    nb_chat_per_hours = dict(Counter(chat_per_hour_not_none))

    sort_dic_hourly = {}
    for i in sorted(nb_chat_per_hours):
        sort_dic_hourly.update({i:nb_chat_per_hours[i]})

    return sort_dic_hourly


def list_of_un_answered_chats(all_chats, this_day, queues):
    chats_this_day = remove_practice_queues(all_chats)
    chat_is_none = [chat for chat in chats_this_day if chat.get("accepted") == None]
    for chat in chat_is_none:
        # breakpoint()
        try:
            queue = [q for q in queues if q['name'] == chat.get('queue')]
            url = "https://ca.libraryh3lp.com/dashboard/queues/" +str(queue[0].get('id')) +"/calls/"+ str(chat.get('guest')) + "/"+ str(chat.get('id'))
            chat.update({'transcript_url':url})
            UNANSWERED_CHATS.append(chat)
            UNANSWERED_CHATS_HTML.append("<p>"+"<a target='_blank' href='"+   url +"'>"+chat.get('started') + "--> " + chat.get('profile')  + " --> " + chat.get('protocol')   + "</a>"+ "'</p>")
            transcript = client.one('chats', chat.get('id')).get()['transcript'] or '<h3>No transcript found</h3>'
            UNANSWERED_CHATS_HTML.append(transcript+"<hr/>")
        except:
            pass
    return chat_is_none


def main(all_chats, this_day):
    chats_this_day = remove_practice_queues(all_chats)
    chat_not_none = [chat for chat in chats_this_day if chat.get("accepted") != None]

    data = get_daily_stats(chats_this_day, chat_not_none, this_day)
    data = data[-1]

    sort_dic_hourly = get_chat_per_hour(chat_not_none)
    print(data)
    report = data.update(sort_dic_hourly)
    LIST_OF_HOURS.update(sort_dic_hourly)
    return data
    #update_excel_file(data, sort_dic_hourly)


def unanswered_chats():
    #print(UNANSWERED_CHATS)
    df = pd.DataFrame(UNANSWERED_CHATS)
    try:
        del df['duration']
        del df['reftracker_id']
        del df['reftracker_url']
        del df['desktracker_id']
        del df['desktracker_url']
        del df['wait']
        del df['referrer']
        del df['ip']
        del df['accepted']
    except:
        print("error on deleting columns")

    df['started'] = pd.to_datetime(df['started'])
    df['ended'] = pd.to_datetime(df['ended'])
    df["started_time"] = df['started'].apply(lambda x:x.time())
    df["ended_time"] = None#df['ended'].apply(lambda x:x.time())
    del df['ended']
    df["guest"] = df['guest'].apply(lambda x:x[0:7])
    df['shift'] =df['started'].dt.hour

    cols = ['id', 'guest', 'protocol', 'started',  "started_time" ,'shift' ,
    'queue','operator', "ended_time", 'profile',  'transcript_url']
    df = df[cols]
    df.sort_values(by=['id'])
    return df


def save_un_into_file(df):
    df.to_excel("UNANSWERED_CHATS.xlsx", index=False)

    try:
        os.remove("unanswered_chats.html")
    except:
        pass

    for val in UNANSWERED_CHATS_HTML:
        with open("unanswered_chats.html", "a", encoding="utf-8") as f:
            f.write(val)

def find_data_for_report(today=datetime.now()):
    queues = client.all('queues').get_list()

    month = today.month
    year = today.year
    day = today.day
    report = list()
    for loop_day in range(1, day + 1):
        all_chats = get_chat_for_this_day(date(year, month, loop_day))
        report.append(main(all_chats, date(year, month, loop_day)))
        list_of_un_answered_chats(all_chats, date(year, month, loop_day), queues)
    
    return report

def save_unanswered_chat_into_db():
    today = datetime.now()
    found_object = UnansweredChat.objects.filter(started__month=today.month, started_year=today.year)
    if found_object:
        found_object.content = UNANSWERED_CHATS_HTML
        found_object.save()
    else:
        UnansweredChat.objects.create(content=UNANSWERED_CHATS_HTML)

def save_daily_report_into_db(df):
    today = datetime.now()
    found_object = ReportMonthly.objects.filter(started__month=today.month, started_year=today.year)
    if found_object:
        found_object.content = df.astype(str)
        found_object.save()
    else:
        ReportMonthly.objects.create(content= df.astype(str))

def real_report():
    report = find_data_for_report()
    print(str(report))
    df = pd.DataFrame(report)

    sorted_hours = sorted(LIST_OF_HOURS.keys())
    cols = ['Day',
    'Total chats',
    'Total Answered Chats',
    'Total UnAnswered Chats',
    'Total French Answered',
    'Total SMS Answered',
    ]
    cols = cols + (sorted_hours)
    # print(cols)
    df = df[cols]
    df.fillna(0, inplace=True)

    
    filename = "daily.xlsx"

    df.to_excel(filename, index=False)

    try:
        #save unanswered Chats into DB  with timestamps
        save_unanswered_chat_into_db()
        #Save Report DF into DB with timestamps
        save_daily_report_into_db(df)
    except:
        pass

if __name__ == '__main__':
    real_report()

    """
    Saved to Django Database
    # https://stackoverflow.com/questions/37688054/saving-a-pandas-dataframe-to-a-django-model

    
    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))

    for dic in json_list:
        HistoricalPrices.objects.get_or_create(**dic)
    """
