from dashboard.api import *
from dashboard.utils import utils


def operatorview_helper(operator):
    client = Client()
    client.set_options(version="v1")
    users = client.all("users")
    return users.one(operator).all("assignments").get_list()
