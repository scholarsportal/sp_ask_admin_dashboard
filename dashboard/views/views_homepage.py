from lh3.api import *
from lh3.utils import search_chats
from dashboard.utils.utils import soft_anonimyzation, Chats
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from dateutil.parser import parse
from django.contrib import messages
import requests
import json
from pprint import pprint as print
import pandas as pd
from django.http import FileResponse
import pathlib

from dotenv import dotenv_values
from sp_lh3_dashboard_config.settings import BASE_DIR



from dashboard.utils.ask_schools import (
    find_school_by_operator_suffix,
    find_queues_from_a_school_name,
    find_school_by_queue_or_profile_name,
)

import os
from tempfile import gettempdir
from pathlib import Path


def chat_usage_per_month_for_a_past_year(client, a_given_year):
    chats_report = client.chats()
    chats_for_that_time = chats_report.list_year(a_given_year)
    chats_for_that_time = [
        {
            "year": parse(chat.get("date")).year,
            "month": parse(chat.get("date")),
            "month_name": parse(chat.get("date")).strftime("%b"),
            "date": chat.get("date"),
            "count": chat.get("count"),
        }
        for chat in chats_for_that_time
    ]
    # stock last academic year in sessions (if session ACADEMIC do this... )

    given_year_usage_per_month = list()
    for element in range(1, 13):
        this_month = [
            item.get("count", 0)
            for item in chats_for_that_time
            if item.get("month").month == element
        ]
        given_year_usage_per_month.append(sum(this_month))
    return given_year_usage_per_month


def get_url(queue):
    url = (
        "https://ca.libraryh3lp.com/presence/jid/"
        + queue
        + "/chat.ca.libraryh3lp.com/text"
    )
    response = requests.get(url).content
    return response.decode("utf-8")

def get_homepage(request, *args, **kwargs):
    #my_env_file = Path(BASE_DIR, ".secrets")

    today = datetime.today()
    last2Days = today - timedelta(days=2)

    client = Client()
    chats = client.chats()
    to_date = (
        str(today.year) + "-" + "{:02d}".format(today.month) + "-" + str(today.day)
    )
    chats = chats.list_day(
        year=last2Days.year, month=last2Days.month, day=last2Days.day, to=to_date
    )

    chats = soft_anonimyzation(chats)
    chats = [Chats(chat) for chat in chats]

    """
    if request.session.get('last_year_chats_per_month'):
        chats_last_year_per_month=request.session['last_year_chats_per_month']
    else:
        chats_last_year_per_month = chat_usage_per_month_for_a_past_year(client, today.year-1)
        request.session['last_year_chats_per_month'] = chats_last_year_per_month
    """

    client.set_options(version="v1")
    users = client.all("users").get_list()
    users = [user for user in users if user.get("show") != "unavailable"]


    # Serivces opened
    queues = client.all('queues').get_list()

    #SMS
    all_sms = [qu for qu in queues if   '-txt' in qu['name']]
    sms_available = [ texto['name'] for texto in all_sms if texto['show']=='available']
    print("{0}/{1}".format(len(sms_available), len(all_sms)))
    sms_unavailable = [ texto['name'] for texto in all_sms if texto['show']=='unavailable']
    sms_service = "<em>SMS:</em> at least <i>{0} queues opened out of </i> <b> {1}</b>".format(len(all_sms) - len(sms_unavailable), len(all_sms))

    #WEB
    without_sms= [qu for qu in queues if   '-txt' not in qu['name']]
    web= [qu for qu in without_sms if   '-fr' not in qu['name']]
    web_unavailable = [ unavailable['name'] for unavailable in web if unavailable['show']=='unavailable']
    print("Web service  {0}/{1}".format(len(web) - len(web_unavailable), len(web)))
    web_service =  "<em>Web:</em> at least <i>{0} queues opened out of </i> <b> {1}</b>".format(len(web) - len(web_unavailable), len(web))

    #FR
    all_fr = [qu for qu in queues if   '-fr' in qu['name']]
    fr_available = [ fr_chat['name'] for fr_chat in all_fr if fr_chat['show']=='available']
    fr_unavailable = [ unavailable['name'] for unavailable in all_fr if unavailable['show']=='unavailable']
    fr_service = "<em>FR:</em> at least <i>{0} queues opened out of </i> <b> {1}</b>".format(len(all_fr) - len(fr_unavailable), len(all_fr))

    #Total vs total unavailable
    unavailable = [ unavailable['name'] for unavailable in queues if unavailable['show']=='unavailable']
    available = [ available['name'] for available in queues if available['show']=='available']
    #print("{0}/{1}".format(len(queues) - len(unavailable), len(queues)))




    if request.is_ajax():
        return JsonResponse(
            {
                "object_list": chats,
                "total_operator_online": users,
                "last_year": today.year - 1,
                "this_year": today.year,
                "sms_service": sms_service,
                "web_service": web_service,
                "fr_service": fr_service,
            },
            safe=False,
        )
    return render(
        request,
        "homepage.html",
        {
            "object_list": chats,
            "total_operator_online": users,
            "last_year": today.year - 1,
            "this_year": today.year,
            "sms_service": sms_service,
            "web_service": web_service,
            "fr_service": fr_service,
        },
    )


def download_list_of_chats_on_homepage(request):

    today = datetime.today()
    last2Days = today - timedelta(days=2)

    client = Client()
    chats = client.chats()
    to_date = (
        str(today.year) + "-" + "{:02d}".format(today.month) + "-" + str(today.day)
    )
    chats = chats.list_day(
        year=last2Days.year, month=last2Days.month, day=last2Days.day, to=to_date
    )

    chats = soft_anonimyzation(chats)
    df = pd.DataFrame(chats)
    del df['tags']
    del df['referrer']
    del df['id']
    del df['profile']
    df['school_from_operator_username'] = df['operator'].apply(lambda x: find_school_by_operator_suffix(x))
    df['school_from_queue_name'] = df['queue'].apply(lambda x: find_school_by_queue_or_profile_name(x))
    df['guest'] = df['guest'].apply(lambda x: x.split('@')[0][0:8])
    
    today = datetime.today().strftime("%Y-%m-%d-%H:%M")

    tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
    os.makedirs(tmp)

    filename = "list_of_chats_from_homepage_" + today +".xlsx"
    filepath = str(pathlib.PurePath(tmp, filename))

    writer = pd.ExcelWriter(filepath, engine="xlsxwriter")
    df.to_excel(writer, index=False)
    writer.save()

    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)


def service_web(request):
    service = get_url("scholars-portal")
    return JsonResponse({"service": service}, safe=False)


def service_sms(request):
    service = get_url("scholars-portal-txt")
    return JsonResponse({"service": service}, safe=False)


def service_fr(request):
    service = get_url("clavardez")
    return JsonResponse({"service": service}, safe=False)


def get_total_chats_per_month_for_this_year(request):
    client = Client()
    today = datetime.today()
    chats_report = client.chats()
    chats_for_this_year = chats_report.list_year(today.year)

    this_year_usage_per_month = list()
    for element in range(1, 13):
        holder_for_this_month = list()
        for item in chats_for_this_year:
            if parse(item.get("date")).month == element:
                if item.get("count") > 0:
                    holder_for_this_month.append(item.get("count"))
        if holder_for_this_month:
            this_year_usage_per_month.append(sum(holder_for_this_month))
    return JsonResponse(
        {"this_year_usage_per_month": this_year_usage_per_month}, safe=False
    )


def service_availability(request):
    service = request.GET.get("service", None)
    if service:
        service = get_url("scholars-portal")
        # sms = get_url("scholars-portal-txt")
        # fr = get_url("clavardez")
        return JsonResponse({"service": service}, safe=False)
    return JsonResponse({"service": None}, safe=False)


def get_operators_currently_online(request):
    client = Client()
    client.set_options(version="v1")
    users = client.all("users").get_list()
    users = [user for user in users if user.get("show") == "available"]
    return JsonResponse(users, safe=False)


def get_total_for_this_day(request):
    client = Client()
    today = datetime.today()
    total_chat_today = client.chats().list_day(
        year=today.year, month=today.month, day=today.day
    )

    return JsonResponse({"total_chats": len(total_chat_today)}, safe=False)


def get_total_for_this_month(request):
    client = Client()
    today = datetime.today()
    chats = client.chats().list_month(year=today.year, month=today.month)
    chats = [chat.get("day").get("count") for chat in chats]

    return JsonResponse({"total_chats": sum(chats)}, safe=False)


def get_total_for_this_year(request):
    client = Client()
    chats = client.chats().list_year(year=2021)
    chats = [chat.get("day").get("count") for chat in chats]

    return JsonResponse({"total_chats": sum(chats)}, safe=False)


def get_list_of_last_400_chats(request):
    client = Client()
    chats = client.chats().list_day(year=2021, month=4, day=1, to="2021-05-18")[0:200]

    return JsonResponse({"chats": chats}, safe=False)


def get_data_for_chart(request):
    client = Client()
    today = datetime.today()
    chats_last_year_per_month = chat_usage_per_month_for_a_past_year(
        client, today.year - 1
    )
    chats_this_year_per_month = chat_usage_per_month_for_a_past_year(client, today.year)

    return JsonResponse(
        {
            "last_year": chats_last_year_per_month,
            "this_year": chats_this_year_per_month,
        },
        safe=False,
    )


def get_data_for_users_currently_online_table(request, *args, **kwargs):
    client = Client()
    client.set_options(version="v1")
    users = client.all("users").get_list()
    users = [user for user in users if user.get("show") != "unavailable"]
    counter = 1
    user_list = list()
    for user in users:
        user_list.append([str(counter), user.get("name"), user.get("show")])
        counter += 1
    return JsonResponse({"users": user_list}, safe=False)

def get_list_of_operators_currently_online(request, *args, **kwargs):
    client = Client()
    client.set_options(version="v1")
    users = client.all("users").get_list()
    users = [user for user in users if user.get("show") != "unavailable"]
    response = {"data":[]}
    counter = 0
    for user in users:
        counter += 1
        response.get('data').append({
            "id": counter,
            "username": user.get('name'),
            "status": user.get('show')
        })
    if request.is_ajax():
        return JsonResponse(
            response,
            safe=False,
        )
    else:
        return JsonResponse(
            response,
            safe=False,
        )

def operator_is_not_none(url, info):
    if info:
        return '<a href='+url+info +' ">'+ info + ' </a>',
    return None

def check_if_Waited_is_none(info):
    if info:
        return info,
    return " "

def check_if_Ended_is_none(info):
    if info:
        return info.split(" ")[1],
    return " "

from dateutil.parser import parse
from dashboard.utils.ask_schools import find_school_by_operator_suffix

def get_duration(chat):
    started=chat.get("started")
    ended= chat.get("ended")
    duration = " "
    if started and ended:
        duration = parse(chat.get("ended")) - parse(chat.get("started"))
        minutes = divmod(duration.seconds, 60)
        if minutes[0] == 0:
            duration = "{0} secs".format(minutes[1])
        else:
            duration = "{0} min {1} secs".format(minutes[0], minutes[1])
    return 7

def get_wait(chat):
    started=chat.get("started")
    ended= chat.get("ended")
    wait= chat.get("wait")
    if chat.get("accepted"):
        school = find_school_by_operator_suffix(chat.get("operator"))
    if started and ended:
        duration = parse(chat.get("ended")) - parse(chat.get("started"))
        minutes = divmod(duration.seconds, 60)
        if minutes[0] == 0:
            duration = "{0} secs".format(minutes[1])
        else:
            duration = "{0} min {1} secs".format(minutes[0], minutes[1])
    if started and chat.get("accepted"):
        wait = parse(chat.get("accepted")) - parse(chat.get("started"))
        minutes = divmod(wait.seconds, 60)
        if minutes[0] == 0:
            wait = "{0} secs".format(minutes[1])
        else:
            wait = "{0} min. {1} secs".format(minutes[0], minutes[1])


def get_duration(chat):
    started=chat.started
    ended= chat.ended
    duration = " "
    if started and ended:
        duration = parse(ended) - parse(chat.get("started"))
        minutes = divmod(duration.seconds, 60)
        if minutes[0] == 0:
            duration = "{0} secs".format(minutes[1])
        else:
            duration = "{0} min {1} secs".format(minutes[0], minutes[1])
    return 7


def get_chat_wait(chat):
    try:
        if chat.wait:
            return chat.wait
    except:
        return " "

def get_chat_duration(chat):
    try:
        if chat.duration:
            return chat.duration
    except:
        return " "

def get_protocol_icon(chat):
    if chat.protocol == "web":
        return ' <i class="fas fa-2x  fa-comments"></i>'
    elif chat.protocol == "sms":
        return '<i class="fas fa-2x fa-sms"></i>'
    elif chat.protocol == "twillio":
        return '<i class="fas fa-2x fa-sms"></i>'
    else:
        return '<i class="fas fa-2x  fa-comments"></i>'


def last_chats(request, *args, **kwargs):
    #my_env_file = Path(BASE_DIR, ".secrets")

    today = datetime.today()
    last2Days = today - timedelta(days=2)

    client = Client()
    chats = client.chats()
    to_date = (
        str(today.year) + "-" + "{:02d}".format(today.month) + "-" + str(today.day)
    )
    chats = chats.list_day(
        year=last2Days.year, month=last2Days.month, day=last2Days.day, to=to_date
    )

    chats = soft_anonimyzation(chats)
    chats = [Chats(chat) for chat in chats]

    print(dir(chats[0]))
    response = {"data":[]}
    counter = 0
    for chat in chats:
        counter += 1
        response.get('data').append({
            "id": counter,
            "Guest": '<a href='+chat.chat_standalone_url+' target="_blank">'+ chat.guest[0:7] + ' </a>',
            "Started": chat.started,
            "From Queue": '<a href="/search/chats/from/this/queue/for/this/year/using/only/the/queue_name/'+chat.queue+' ">'+ chat.queue + ' </a>',
            "Operator": operator_is_not_none('/search/chats/answered/by/this/users/', chat.operator),
            "Ended": check_if_Ended_is_none(chat.ended),
            "Transcript":'<a href="/search/chat/transcript/'+str(chat.chat_id)+' "> Transcript</a>',
            "Wait":get_chat_wait(chat),
            "Duration":get_chat_duration(chat),
            "Protocol": get_protocol_icon(chat),
        })
    if request.is_ajax():
        return JsonResponse(
            response,
            safe=False,
        )
    else:
        return JsonResponse(
            response,
            safe=False,
        )