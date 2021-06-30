from lh3.api import *
from django.views.generic import TemplateView
from dashboard.utils.utils import (
    soft_anonimyzation,
    operatorview_helper,
    Chats,
    retrieve_transcript,
    search_chats,
)
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from pprint import pprint as print
from dateutil.parser import parse
from operator import itemgetter

class SearchProfileResultsView(TemplateView):
    """[summary]

    Args:
        TemplateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    template_name = "results/profile.html"

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(SearchProfileResultsView, self).get_context_data(**kwargs)
        context["title"] = "Profile"
        search_value = self.request.GET.get("queue_id")

        client = Client()
        profile = client.one("profiles", int(search_value)).get()
        context["profile"] = profile["content"]
        context["title"] = profile["name"]
        context["queues"] = client.all("queues").get_list()
        context["standalone_link"] = (
            "https://ca.libraryh3lp.com/dashboard/profiles/"
            + str(int(search_value))
            + "?standalone=true"
        )

        return context


def get_this_profile(request, *args, **kwargs):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    queue_id = kwargs.get("queue_id", None)
    queue_id = int(queue_id)
    client = Client()
    queues = client.all("queues").get_list()
    title = "Profile"
    profile = None
    if queue_id:
        profile_api = client.one("profiles", int(queue_id)).get()
        profile = profile_api["content"]
        title = profile_api.get("name", None)
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
            {
                "profile": profile,
                "title": title,
                "standalone_link": standalone_link,
                "queues": queues,
            },
        )
    if request.is_ajax():
        return JsonResponse(queues, safe=False)
    return render(
        request,
        "results/profile.html",
        {"queues": queues, "title": title, "profile": profile},
    )

class SearchFAQResultsView(TemplateView):
    """[summary]

    Args:
        TemplateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    template_name = "results/faq.html"

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(SearchFAQResultsView, self).get_context_data(**kwargs)
        context["title"] = "FAQ"
        search_value = self.request.GET.get("faq_id")

        client = Client()
        context["faqs"] = client.all("faqs").get_list()
        info = client.one('faqs', search_value).all('questions')
        try:
            context['response'] = info.get_list()
            question_response = list()
            for question in info.get_list():
                this_id = question.get('id')
                #TODO order question by Date
                if question.get("question", None):
                    likes = question.get('likes')
                    dislikes = question.get('dislikes')
                    views = question.get('views')
                    published = str(question.get('published'))
                    updated = parse(question.get('updatedAt'))

                    question = question.get('question')
                    answer = client.one('faqs', search_value).one('questions', id=this_id).get().get('answer')
                    question_response.append(
                        {"question":question, "answer":answer, 
                        "likes":likes, "dislikes":dislikes, "views":views,
                        "updated":updated, "published":published
                        }
                    )
            context['title'] = client.one('faqs', search_value).get().get('name')
            context['question'] = client.one('faqs', search_value).one('questions', id=591).get().get('answer')
            question_response.sort(key=itemgetter('updated'), reverse=True)
            context['results']=   question_response
            if len(question_response) ==0:
                messages.add_message(self.request, messages.WARNING, "This FAQ doesn't contain any questions")
            return context
        except:
            messages.add_message(self.request, messages.WARNING, 'An error occured. Please verify the FAQ ID')
            context["faqs"] = client.all("faqs").get_list()
            return context