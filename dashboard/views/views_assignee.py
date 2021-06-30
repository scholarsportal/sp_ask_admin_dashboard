from lh3.api import *
from dashboard.utils import utils

from django.http import JsonResponse
from django.shortcuts import render


def get_assignee_for_this_queue(request, *args, **kwargs):
    client = Client()
    queue = kwargs.get("queue_name", None)
    assignments = client.find_queue_by_name(queue).all("operators").get_list()

    # return JsonResponse(assignments, safe=False)
    return render(request, "index.html", {"object_list": assignments})
