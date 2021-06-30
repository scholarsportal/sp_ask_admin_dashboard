from django.http import Http404

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render

from datetime import datetime

from lh3.api import *
from dashboard.utils import utils
import pandas as pd
from os import path
import pathlib
from project_config.settings import BASE_DIR
from django.http import FileResponse
from dashboard.utils.ask_schools import (
    find_school_by_operator_suffix,
    find_queues_from_a_school_name,
    find_school_by_queue_or_profile_name,
)
from uuid import uuid4
import os
from tempfile import gettempdir

def get_users(request):
    client = Client()
    client.set_options(version="v1")
    users = client.all("users").get_list()
    if request.is_ajax():
        return JsonResponse(users, safe=False)
    return render(request, "results/operators.html", {"object_list": users})

def download_get_users(request):
    client = Client()
    client.set_options(version="v1")
    users = client.all("users").get_list()
    df = pd.DataFrame(users)
    df['school'] = df['name'].apply(lambda x: find_school_by_operator_suffix(x))
    del df['id']
    del df['type']
    del df['email']
    del df['show']
    del df['status']

    today = datetime.today().strftime("%Y-%m-%d-%H:%M")

    tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
    os.makedirs(tmp)

    filename = "operators_" + today +".xlsx"
    filepath = str(pathlib.PurePath(tmp, filename))

    writer = pd.ExcelWriter(filepath, engine="xlsxwriter")
    df.to_excel(writer, index=False)
    writer.save()

    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)


def get_queues(request):
    client = Client()
    client.set_options(version="v1")
    queues = client.all("queues").get_list()
    if request.is_ajax():
        return JsonResponse(queues, safe=False)
    return render(request, "results/queues.html", {"object_list": queues})
    # path('queues/', GetListOfQueues.as_view(), name='Get list of Queues'),

def download_get_queues(request):
    client = Client()
    client.set_options(version="v1")
    queues = client.all("queues").get_list()
    df = pd.DataFrame(queues)
    df['school'] = df['name'].apply(lambda x: find_school_by_queue_or_profile_name(x))
    del df['transcripts']
    del df['type']
    del df['email']
    del df['avatar']
    #del df['id']
    del df['show']
    del df['status']

    today = datetime.today().strftime("%Y-%m-%d-%H:%M")

    tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
    os.makedirs(tmp)

    filename = "queues_" + today +".xlsx"
    filepath = str(pathlib.PurePath(tmp, filename))

    writer = pd.ExcelWriter(filepath, engine="xlsxwriter")
    df.to_excel(writer, index=False)
    writer.save()

    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)




def get_profiles(request, *args, **kwargs):
    queue_id = kwargs.get("queue_id", None)
    client = Client()
    queues = client.all("queues").get_list()
    title = "Profile"
    profile = None
    if request.method == "GET":
        if request.is_ajax():
            return JsonResponse(profile, safe=False)
        return render(
            request,
            "results/profile.html",
            {"queues": queues, "title": title, "profile": profile},
        )
    if queue_id:
        profile = client.one("profiles", int(queue_id)).get()
        profile = profile["content"]
        title = profile["name"]
        standalone_link = (
            "https://ca.libraryh3lp.com/dashboard/profiles/"
            + str(int(queue_id))
            + "?standalone=true"
        )

        if request.is_ajax():
            return JsonResponse(profile, safe=False)
        return render(
            request,
            "results/profile.html",
            {"profile": profile, "title": title, "standalone_link": standalone_link},
        )
    if request.is_ajax():
        return JsonResponse(queues, safe=False)
    return render(
        request,
        "results/profile.html",
        {"queues": queues, "title": title, "profile": profile},
    )



def get_faqs(request, *args, **kwargs):
    faq_id = kwargs.get("faq_id", None)
    client = Client()
    faqs = client.all("faqs").get_list()
    title = "FAQ"
    faq = None
    if request.method == "GET":
        if request.is_ajax():
            return JsonResponse(faq, safe=False)
        return render(
            request,
            "results/faq.html",
            {"faqs": faqs, "title": title, "faq": faq},
        )
    if faq_id:
        faq = client.one("faqs", int(faq_id)).get()
        faq = faq["content"]
        title = faq["name"]
        standalone_link = (
            "https://ca.libraryh3lp.com/dashboard/faqs/"
            + str(int(faq_id))
            + "?standalone=true"
        )

        if request.is_ajax():
            return JsonResponse(faq, safe=False)
        return render(
            request,
            "results/faq.html",
            {"faq": faq, "title": title, "standalone_link": standalone_link},
        )
    if request.is_ajax():
        return JsonResponse(faqs, safe=False)
    return render(
        request,
        "results/faq.html",
        {"faqs": faqs, "title": title, "faq": faq},
    )
# TODO clean template html remove console error.
