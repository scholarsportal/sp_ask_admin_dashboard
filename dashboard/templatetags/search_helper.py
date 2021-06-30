from django import template
from random import shuffle
import datetime
import time, secrets

# from .daily_report_range import create_report, get_chat_for_this_day
from dashboard.utils.ask_schools import (
    find_school_by_operator_suffix,
    find_school_abbr_by_queue_or_profile_name,
)

from dateutil.parser import parse

# from ..kiwoom import k_module

register = template.Library()
import random
from collections import Counter


@register.simple_tag
def get_new_tab_transcript_link(guest):
    return guest


@register.simple_tag
def get_duration_from_2_timestamps(started, ended):
    if not ended:
        return ""
    if not started:
        return ""
    started = started.strftime("%H:%M:%S")
    ended = ended.strftime("%H:%M:%S")
    total_time = datetime.datetime.strptime(
        ended, "%H:%M:%S"
    ) - datetime.datetime.strptime(started, "%H:%M:%S")
    return total_time


@register.simple_tag
def get_protocol(protocol):
    if "web":
        return '<i class="fas fa-comments"></i>'
    elif "twilio":
        return '<i class="fas fa-sms"></i>'
    else:
        return '<i class="fas fa-mobile-alt"></i>'


@register.simple_tag
def get_new_window_url_for_transcript(lh3id):
    return "https://ca.libraryh3lp.com/dashboard/queues/ANYTHING/calls/ANYTHING/" + str(
        lh3id
    )


@register.simple_tag
def random_operator_status():
    return secrets.choice(["busy", "available", "selecting queue"])


import time


@register.simple_tag
def print_timestamp():
    # specify format here
    return time.now.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.now))


@register.simple_tag
def find_school_from_username(operator_username):
    return find_school_by_operator_suffix(operator_username)


@register.simple_tag
def find_school_from_queue_name(queue_name):
    return find_school_abbr_by_queue_or_profile_name(queue_name)


@register.simple_tag
def get_duration_from_2_timestamps(started, ended):
    if not ended:
        return ""
    if not started:
        return ""
    started = started.strftime("%H:%M:%S")
    ended = ended.strftime("%H:%M:%S")
    total_time = datetime.datetime.strptime(
        ended, "%H:%M:%S"
    ) - datetime.datetime.strptime(started, "%H:%M:%S")
    return total_time


"""	 
@register.simple_tag
def find_avatar_for_school(operator_username):
	school =  find_school_by_operator_suffix(operator_username)

@register.simple_tag
def verify_if_this_chat_has_a_reference_question(chat_id):
	chat =  Chat.objects.filter(id__exact=chat_id).first()
	transcript =  Transcript.objects.filter(chat__exact=chat).first()
	if transcript:
		return True
	else:
		return False
"""
