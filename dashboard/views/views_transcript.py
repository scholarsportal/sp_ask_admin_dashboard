from lh3.api import *
from dashboard.utils.utils import retrieve_transcript
from django.shortcuts import render
from pprint import pprint as print

from dateutil.parser import parse
from django.http import JsonResponse
from django.http import FileResponse
from django.http import HttpResponse
from django.core.files.base import ContentFile
from os import path
import pathlib
from sp_lh3_dashboard_config.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View


from dashboard.models import (
    chatReferenceQuestion
    )


from dashboard.utils.utils import (
    soft_anonimyzation,
    Chats,
    retrieve_transcript,
    search_chats,
)

def get_transcript(request, *args, **kwargs):
    client = Client()
    chat_id = int(kwargs.get("chat_id", None))
    transcript_metadata = client.one("chats", chat_id).get()
    transcript = retrieve_transcript(transcript_metadata, chat_id)
    queue_name = transcript_metadata.get("queue").get("name")
    started_date = parse(transcript_metadata.get("started")).strftime("%Y-%m-%d")

    if request.is_ajax():
        return JsonResponse(transcript, safe=False)
    return render(
        request,
        "transcript/transcript.html",
        {
            "object_list": transcript,
            "queue_name": queue_name,
            "started_date": started_date,
            "chat_id": chat_id,
        },
    )

def download_transcript_in_html(request, *args, **kwargs):
    client = Client()
    chat_id = int(kwargs.get("chat_id", None))
    transcript_metadata = client.one("chats", chat_id).get()
    transcript = retrieve_transcript(transcript_metadata, chat_id)

    url = "https://ca.libraryh3lp.com/dashboard/queues/"
    queue_id = str(transcript_metadata.get("queue").get("accunt_id")) + "/calls/"
    guest_id = (
        str(transcript_metadata.get("guest").get("jid"))
        + "/"
        + str(transcript_metadata.get("guest_id"))
    )
    url + queue_id + guest_id

    content = ["<html><body><h3 align='center'>Transcript</h3><hr/><br/><br>"]
    for msg in transcript:
        this_msg = msg.get("message")
        print(this_msg)
        content.append(this_msg)
    print(content)

    filename = "last-transcript-downloaded.html"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

    with open(filepath, "w") as file:
        file.write(" ".join(content))

    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)


@csrf_exempt
def search_transcript_with_this_keyword(request, *args, **kwargs):
    in_transcript = request.POST.get("in_transcript", None)
    chats = None
    if in_transcript:
        query = {
            "query": {
                "transcript": [in_transcript],
            },
            "sort": [{"started": "descending"}],
        }
        client = Client()
        chats, content_range = search_chats(
            client, query, chat_range=(0, 100)
        )
        chats = soft_anonimyzation(chats)
        chats = [Chats(chat) for chat in chats]
        return render(
            request,
            "results/search_in_transcript.html",
            {"object_list": chats, "guest_id": "fake GuestID"},
        )
    return render(request, "results/search_in_transcript.html", {"object_list": None})


@csrf_exempt
def search_transcript_that_was_transferred(request, *args, **kwargs):
    query = {
        "query": {
            "transcript": ['System message: transferring'],
        },
        "sort": [{"started": "descending"}],
    }
    client = Client()
    chats, content_range = search_chats(
            client, query, chat_range=(0, 100)
        )
    chats = soft_anonimyzation(chats)
    chats = [Chats(chat) for chat in chats]
    return render(
        request,
        "results/chat_transferred.html",
        {"object_list": chats, "guest_id": "fake GuestID"},
    )

@csrf_exempt
def search_transcript_that_contains_file_transfer(request, *args, **kwargs):
    query = {
        "query": {
            "transcript": ['System message: download from'],
        },
        "sort": [{"started": "descending"}],
    }
    client = Client()
    chats, content_range = search_chats(
            client, query, chat_range=(0, 100)
        )
    chats = soft_anonimyzation(chats)
    chats = [Chats(chat) for chat in chats]
    return render(
        request,
        "results/chat_with_file_transfer.html",
        {"object_list": chats, "guest_id": "fake GuestID"},
    )

class TranscriptRemoveReferenceQuestion(View):
    def get(self, request, *args, **kwargs):
        pass


def add_this_as_a_reference_question(request, *args, **kwargs):
    client = Client()
    chat_id = int(kwargs.get("chat_id", None)) 
    position = int(kwargs.get("message_position", None)) 
    transcript_metadata = client.one("chats", chat_id).get()
    transcript = retrieve_transcript(transcript_metadata, chat_id)
    queue_name = transcript_metadata.get("queue").get("name")
    started_date = parse(transcript_metadata.get("started")).strftime("%Y-%m-%d")
    breakpoint()

    chatReferenceQuestion.objects.create(
        lh3ChatID =chat_id,
        ref_question_found = True,
        ref_question_position = int(position) 
    )

    if request.is_ajax():
        return JsonResponse({"hello":'is working'}, safe=False)
    return JsonResponse({"hello":'is working'}, safe=False)