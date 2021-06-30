import lh3.api
from lh3.api import *
from typing import List
from dateutil.parser import parse
from dashboard.utils.ask_schools import find_school_by_operator_suffix
from datetime import datetime
from bs4 import BeautifulSoup
from dashboard.utils.ask_schools import find_school_by_queue_or_profile_name

from datetime import datetime, time
from dateutil import tz, parser

default_date = datetime.combine(
    datetime.now(), time(0, tzinfo=tz.gettz("America/New_York"))
)


import re

content_range_pattern = re.compile(r"chats (\d+)-(\d+)\/(\d+)")


def extract_content_range(content_range):
    matches = content_range_pattern.match(content_range)
    begin = matches.group(1)
    end = matches.group(2)
    total = matches.group(3)
    return (begin, end, total)


def search_chats(client, query, chat_range):
    begin, end = chat_range
    _, x_api_version = lh3.api._API.versions.get("v4")
    headers = {
        "Content-Type": "application/json",
        "Range": "chats {begin}-{end}".format(begin=begin, end=end),
        "X-Api-Version": x_api_version,
    }

    request = getattr(client.api().session, "post")
    response = request(
        client.api()._api("v4", "/chat/_search"), headers=headers, json=query
    )
    chats = client.api()._maybe_json(response)
    content_range = extract_content_range(response.headers["Content-Range"])
    return chats, content_range


class Chats(object):
    def __init__(self, chat):
        self.operator = chat.get("operator", "")
        self.guest = chat.get("guest")
        self.started = None
        self.ended = None
        if chat.get("started"):
            # self.started = parser.parse(chat.get('started'), default=default_date).strftime("%Y-%m-%d %H:%M:%S")
            self.started = parser.parse(
                chat.get("started"),
                default=datetime(2017, 10, 13, tzinfo=tz.gettz("America/New_York")),
            ).strftime("%Y-%m-%d %H:%M:%S")
        if chat.get("ended"):
            # self.ended = parser.parse(chat.get('ended'), default=default_date).strftime("%Y-%m-%d %H:%M:%S")
            self.ended = parser.parse(
                chat.get("ended"),
                default=datetime(2017, 10, 13, tzinfo=tz.gettz("America/New_York")),
            ).strftime("%Y-%m-%d %H:%M:%S")
        self.protocol = chat.get("protocol")
        self.school = None
        if chat.get("accepted"):
            self.school = find_school_by_operator_suffix(chat.get("operator"))
        if self.started and self.ended:
            self.duration = parse(chat.get("ended")) - parse(chat.get("started"))
            minutes = divmod(self.duration.seconds, 60)
            if minutes[0] == 0:
                self.duration = "{0} secs".format(minutes[1])
            else:
                self.duration = "{0} min {1} secs".format(minutes[0], minutes[1])
        if self.started and chat.get("accepted"):
            self.wait = parse(chat.get("accepted")) - parse(chat.get("started"))
            minutes = divmod(self.wait.seconds, 60)
            if minutes[0] == 0:
                self.wait = "{0} secs".format(minutes[1])
            else:
                self.wait = "{0} min. {1} secs".format(minutes[0], minutes[1])
        self.queue_id = chat.get("queue_id")
        self.queue = chat.get("queue")
        self.chat_id = chat.get("id")
        self.chat_standalone_url = (
            "https://ca.libraryh3lp.com/dashboard/queues/{0}/calls/REDACTED/{1}".format(
                self.queue_id, self.chat_id
            )
        )


def retrieve_transcript(transcript_metadata, chat_id):
    queue_id = transcript_metadata["queue_id"]
    guest = transcript_metadata["guest"].get("jid")
    get_transcript = (
        transcript_metadata["transcript"] or "<div>No transcript found</div>"
    )
    soup = BeautifulSoup(get_transcript, "html.parser")
    divs = soup.find_all("div")
    transcript = list()
    counter = 1
    for div in divs[1::]:
        try:
            transcript.append(
                {
                    "chat_id": chat_id,
                    "message": str(div),
                    "counter": counter,
                    "chat_standalone_url": "https://ca.libraryh3lp.com/dashboard/queues/{0}/calls/REDACTED/{1}".format(
                        queue_id, chat_id
                    ),
                    "guest": guest,
                }
            )
            counter += 1
        except:
            pass
    return transcript


def soft_anonimyzation(list_of_chat: List[dict]) -> List[dict]:
    chats = list()
    for chat in list_of_chat:
        chat.pop("desktracker_url", None)
        chat.pop("reftracker_id", None)
        chat.pop("ip", None)
        chat.pop("reftracker_url", None)
        chat.pop("desktracker_id", None)
        chats.append(chat)
    return chats


def operatorview_helper(operator: str) -> List[dict]:
    client = Client()
    client.set_options(version="v1")
    users = client.all("users")
    operator = [user for user in users.get_list() if user.get("name") == operator]
    operator_id = operator[0].get("id")
    return users.one(operator_id).all("assignments").get_list()


def helper_for_operator_assignments():
    client = Client()
    client.set_options(version="v1")
    users = client.all("users")

    num_users = 0
    operator_report = list()
    for user in users.get_list():
        # Is that user staffing any queue?
        staffing = False
        assignments = users.one(user["id"]).all("assignments").get_list()[0:3]
        for assignment in assignments[0:5]:
            assignment["school"] = find_school_by_queue_or_profile_name(
                assignment.get("queue")
            )
            operator_report.append(assignment)

    assignments = [
        {
            "queue": assign.get("queue"),
            "operator": assign.get("user"),
            "school": assign.get("school"),
        }
        for assign in operator_report
    ]
    return assignments
