from django.http.response import JsonResponse
from lh3.api import *
from dashboard.utils.utils import soft_anonimyzation, Chats
from datetime import datetime, timedelta
from django.shortcuts import render
from dateutil.parser import parse

from dashboard.utils.daily_report import real_report
from dashboard.utils.utils import helper_for_operator_assignments

import pathlib
from project_config.settings import BASE_DIR
from django.http import FileResponse
import pandas as pd
import json
from datetime import timezone, datetime
import json
from os import path
from pprint import pprint as print

from datetime import datetime, timedelta
import lh3.api
from dashboard.utils.ask_schools import (
    find_school_by_queue_or_profile_name,
)

def download_in_xslx_report__for_queues_for_this_year(request):
    # https://gitlab.com/libraryh3lp/libraryh3lp-sdk-python/-/blob/master/examples/scheduled-reports.py
    today = datetime.today()

    client = lh3.api.Client()
    chats_per_operator = client.reports().chats_per_queue(
        start="2021-01-01", end="2021-12-31"
    )

    print(chats_per_operator)


def download_in_xslx_report_for_this_year(request):
    # https://gitlab.com/libraryh3lp/libraryh3lp-sdk-python/-/blob/master/examples/scheduled-reports.py
    today = datetime.today()

    client = lh3.api.Client()
    this_year = str(today.year)
    chats_per_operator = client.reports().chats_per_operator(
       start=this_year+"-01-01", end=this_year+"-12-31"
    )

    chats_per_operator = chats_per_operator.split("\r\n")
    chats_per_operator = chats_per_operator[1::]
    report = list()
    for data in chats_per_operator:
        if len(data) > 0:
            data = data.split(",")
            report.append(
                {
                    "operator": data[0],
                    "Total chat answered": data[1],
                    "Mean - of wait time (sec.)": data[2],
                    "Median - of wait time (sec.)": data[3],
                    "Min - of wait time (sec.)": data[4],
                    "Max - of wait time (sec.)": data[5],
                }
            )

    today = datetime.today().strftime("%Y-%m-%d")
    filename = "report-" + today + ".xlsx"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

    df = pd.DataFrame(report)
    # Create file using the UTILS functions
    df.to_excel(filepath, index=False, sheet_name=this_year+"_report_for_operator")

    # TODO: Create this report using a cronjob
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)



def chord_diagram(request):
    """
    client = Client()
    today = datetime.today()
    chats = client.chats()
    chats = chats.list_day(year=2021, month=1, day=1, to="2021-04-11")
    df = pd.DataFrame(chats)
    """

    return render(request, "chord_diagram.html")


def daily_report(request):
    today = datetime.today().strftime("%Y-%m-%d")

    filename = "daily-" + today + ".xlsx"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

    df = real_report()
    # Create file using the UTILS functions
    df.to_excel(filepath, index=False)

    # TODO: Create this report using a cronjob
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)


def pivotTableOperatorAssignment(request):
    assignments = helper_for_operator_assignments()

    context = {"schools": assignments}

    df = pd.DataFrame(assignments)
    df["operator_copy"] = df["operator"]

    filename = "operator.xlsx"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

    writer = pd.ExcelWriter(filepath, engine="xlsxwriter")
    df.to_excel(writer, index=False)
    writer.save()

    # return JsonResponse(context, safe=False)
    return render(request, "pivot.html", context)


def download_excel_file_Operator_Assignment(request):

    filename = "operator.xlsx"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

    from os import path

    if path.exists(filepath):
        print("file exist in : " + filepath)
        return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
    else:
        assignments = helper_for_operator_assignments()

        df = pd.DataFrame(assignments)
        df["operator_copy"] = df["operator"]

        filename = "operator.xlsx"
        filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

        writer = pd.ExcelWriter(filepath, engine="xlsxwriter")
        df.to_excel(writer, index=False)
        writer.save()

    # TODO: Create this report using a cronjob
    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)


def get_unanswered_chats(request, *args, **kwargs):
    client = Client()
    today = datetime.today()
    chats = client.chats()
    last10days = today - timedelta(days=10)

    to_date = (
        str(last10days.year)
        + "-"
        + "{:02d}".format(last10days.month)
        + "-"
        + str(last10days.day)
    )
    all_chats = chats.list_day(
        year=today.year, month=today.month, day=today.day, to=to_date
    )
    unanswered = list()
    for chat in all_chats:
        if chat.get("operator") == None:
            unanswered.append(chat)

    # return JsonResponse(chats, safe=False)
    heatmap = [
        parse(chat.get("started")).replace(tzinfo=timezone.utc).timestamp()
        for chat in unanswered
    ]
    counter = {x: heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)
    username = "Unanswered"
    current_year = "Last 10 days"

    unanswered = [Chats(chat) for chat in unanswered]
    return render(
        request,
        "results/chats.html",
        {
            "object_list": unanswered,
            "heatmap_chats": heatmap_chats,
            "username": username,
            "current_year": current_year,
        },
    )


def pivotTableChatAnsweredByOperator(request):
    client = Client()
    chats = client.chats()

    today = datetime.today()
    yesterday = today - timedelta(days=3)

    chats = client.chats().list_day(year=2021, month=4, day=1, to="2021-05-18")[0:200]
    chats_initital = [Chats(chat) for chat in chats]

    chats_initital = [
        {
            "queue": s.queue,
            "school": s.school,
            "year": parse(s.started).year,
            "month": parse(s.started).strftime("%B"),
            "operator": s.operator,
        }
        for s in chats_initital
    ]

    breakpoint()
    operators = [chat.get("operator") for chat in chats_initital]
    queues = [chat.get("queue") for chat in chats]
    context = {"schools": chats_initital}
    return render(request, "pivot.html", context)


def pivot_table_chats_per_schools(request):
    today = datetime.today()
    query = {
    "query": {
        "from": str(today.year)+"-06-19", 
        "to": str(today.year)+"-06-21"
        },
        "sort": [{"started": "descending"}],
    }
    client = Client()
    chats = client.api().post("v4", "/chat/_search", json=query)

    my_list = list()

    for chat in chats:
        accepted ='not answered'
        this_date = 'None'
        school = 'None'
        operator = 'None'
        if chat.get('accepted'):
            accepted = 'answered'
        if chat.get('queue'):
            school = find_school_by_queue_or_profile_name(chat.get('queue'))
        if chat.get('operator'):
            operator = chat.get('operator')
        try:
            if chat.get('started', 'None'):
                this_date = chat.get('started').split('T')[0]
        except:
            pass
        my_list.append({'accepted':accepted, 'this_date':this_date, 
                        'school':school, 'operator':operator, 'date':this_date,
                        'queue':chat.get('queue')})
    my_second_list = list()
    print(my_list)
    
    return render(request, "pivot/chats_per_school.html", {"object_list": my_list})