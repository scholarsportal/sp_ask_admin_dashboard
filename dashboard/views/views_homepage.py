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

    if request.is_ajax():
        return JsonResponse(
            {
                "object_list": chats,
                "total_operator_online": users,
                "last_year": today.year - 1,
                "this_year": today.year,
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


def get_data_for_users_currently_online_table(request):
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
