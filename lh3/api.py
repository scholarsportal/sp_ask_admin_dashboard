from __future__ import absolute_import, unicode_literals
from builtins import map, object
from contextlib import closing
import configparser
import hashlib
import os
from pathlib import Path
from colorama import Fore, init, Style

__authors__ = "libraryh3lp.com; nubgames"
# Scholars Portal add some modifications
__description__="This is a slightly modify version of the LH3 API"

from collections import OrderedDict

if os.name == "nt":
    # pip install python-dotenv
    from dotenv import dotenv_values

# pip install requests
import requests
import requests.utils


class LH3JSONError(Exception):
    """Exists only to distinguish LibraryH3lp errors from other generated errors."""
    pass

class LH3AuthError(Exception):
    """Exists only to distinguish LibraryH3lp errors from other generated errors."""

    def __init__(self):
        self.message = (
                ('\n\n')
                +("*" * 40)
                + "\n\nPlease add your LibraryH3lp credentials in the " + Style.BRIGHT +  Fore.RED + ".secrets" + Fore.RESET + " found in the current directory:\n\t\t {0}to authenticate on the libraryh3lp servers\n".format( os.path.join(os.path.realpath('.'), ".secrets"))
                +("Please visit https://github.com/scholarsportal/sp_ask_admin_dashboard \n\n")
                + ("*" * 40)
        )
        super().__init__(self.message)



class DashboardEnvFileNotFound(Exception):
    """raise when there is no configuration file found"""

    def __init__(self):
        self.message = (
                ('\n\n')
                +("*" * 40)
                + "\n\nYou need to create a " + Style.BRIGHT +  Fore.RED + ".secrets" + Fore.RESET + " file in the current directory:\n\t\t {0}\n".format( os.path.join(os.path.realpath('.'), ".secrets"))
                +("Please visit https://github.com/scholarsportal/sp_ask_admin_dashboard/issues/1 \n\n")
                + ("*" * 40)
        )
        super().__init__(self.message)


class Client(object):
    default_config = {
        "salt": "you should probably change this",
        "scheme": "https",
        "server": "libraryh3lp.com",
        "timezone": "UTC",
        "version": "v2",
    }

    def __init__(self, profile=None):
        self._config = None
        self._api = None
        self._queues = {}
        self._users = {}
        self.load_config(profile)

    def load_config(self, profile=None):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        my_env_file = Path(BASE_DIR, ".secrets")
        if os.path.isfile(my_env_file):
            config = dotenv_values(my_env_file)
            self._config = OrderedDict(config)
        else:
            raise DashboardEnvFileNotFound

    def set_credentials(self, username, password=None):
        self.set_options(username=username, password=password)

    def set_options(self, **options):
        self._config.update(options)
        if self._api is not None:
            self._api = _API(self._config)

    def api(self, config=None):
        if self._api is None:
            options = self._config.copy()
            if config:
                options.update(config)
            self._api = _API(options)

        return self._api

    # Returns a reference to an element.
    def one(self, route, id):
        return self.one_url(self.url(route, id))

    # Returns a reference to a collection.
    def all(self, route):
        return self.all_url(self.url(route))

    def one_url(self, url):
        return _Element(self.api(), url)

    def all_url(self, url):
        return _Collection(self.api(), url)

    def url(self, *args):
        return "/".join([""] + list(map(str, args)))

    def account(self):
        if self.is_admin():
            return self.one("accounts", self.account_id())
        else:
            return None

    def is_admin(self):
        return self.account_id() is not None

    def account_id(self):
        return self.api().account_id

    def chats(self):
        return _Chats(self.api())

    def reports(self):
        return _Reports(self.api())

    def find_queue_by_name(self, queue):
        if queue not in self._queues:
            for q in self.all("queues").get_list():
                self._queues[q["name"]] = q["id"]

        if queue not in self._queues:
            return None

        return self.one("queues", self._queues[queue])

    def find_user_by_name(self, user):
        if user not in self._users:
            for u in self.all("users").get_list():
                self._users[u["name"]] = u["id"]

        if user not in self._users:
            return None

        return self.one("users", self._users[user])


# Represents a connection to the server.
class _API(object):
    versions = {
        # version: path, X-Api-Version
        "v1": ["2011-12-03", "2011-12-03"],
        "v2": ["2013-07-21", "2013-07-21"],
        "v3": ["2016-02-10", "2016-02-10"],
        "v4": ["api", "2017-01-20"],
    }

    def __init__(self, config):
        self._config = config
        if not self.username:
            raise LH3AuthError

        self.session = requests.Session()
        requests.utils.add_dict_to_cookiejar(
            self.session.cookies, {"libraryh3lp-timezone": self.timezone}
        )

        self.login()

    def __getattr__(self, name):
        return self._config.get(name)

    def login(self):
        result = self.session.post(
            self._api("/auth/login"),
            data={"username": self.username, "password": self._get_password()},
        )
        if not result.ok:
            raise LH3AuthError

        json = result.json()
        if not json.get("success", False):
            raise LH3JSONError(json.get("error", "unknown authentication failure"))

        self.account_id = json.get("account_id")

        if not self.session.cookies.get("libraryh3lp-session"):
            session_uuid = result.headers["Set-Cookie"].split("=")[1].split(";")[0]
            requests.utils.add_dict_to_cookiejar(
                self.session.cookies, {"libraryh3lp-session": session_uuid}
            )

    def _get_password(self):
        return self.password or hashlib.sha256(self.salt + self.username).hexdigest()

    def delete(self, version, path=None, **kwargs):
        return self._request("delete", version, path, **kwargs)

    def get(self, version, path=None, **kwargs):
        return self._request("get", version, path, **kwargs)

    def patch(self, version, path=None, **kwargs):
        return self._request("patch", version, path, **kwargs)

    def post(self, version, path=None, **kwargs):
        return self._request("post", version, path, **kwargs)

    def put(self, version, path=None, **kwargs):
        return self._request("put", version, path, **kwargs)

    def _request(self, method, version, path=None, **kwargs):
        result = self.raw_request(method, version, path, **kwargs)
        return self._maybe_json(result)

    def raw_request(self, method, version, path=None, **kwargs):
        request = getattr(self.session, method)
        _, x_api_version = _API.versions.get(version) or _API.versions.get(self.version)
        headers = {"Content-Type": "application/json", "X-Api-Version": x_api_version}
        return request(self._api(version, path), headers=headers, **kwargs)

    def _maybe_json(self, result):
        try:
            return result.json()
        except ValueError as e:
            return result.text

    def _api(self, version, path=None):
        if not path:
            path = version
            version = self.version

        version, _ = _API.versions.get(version, version)
        return "{}://{}/{}{}".format(self.scheme, self.server, version, path)


# A Collection is a reference to a group of items on the server.  It
# does not contain any actual data.  Call `get_list` to fetch the
# referenced data from the server.
class _Collection(object):
    def __init__(self, api, path):
        self._api = api
        self._path = path

    def delete(self):
        return self._api.delete(self.url())

    def get(self, id, params=None):
        return self._api.get(self.url(id), params=params)

    def get_list(self, params=None):
        return self._api.get(self.url(), params=params)

    def patch(self, id, json):
        return self._api.patch(self.url(id), json=json)

    def post(self, json):
        return self._api.post(self.url(), json=json)

    def put(self, json):
        return self._api.put(self.url(data["id"]), json=json)

    def custom_get(self, path, **kwargs):
        return self._api.get(self.url(path), **kwargs)

    def custom_get_list(self, path, **kwargs):
        return self._api.get(self.url(path), **kwargs)

    def custom_post(self, path, json):
        return self._api.post(self.url(path), json=json)

    # Returns a reference to a child element.  Call `get` to fetch the
    # data instead.
    def one(self, id):
        return self.one_url(self.url(id))

    # Returns a reference to a child collection.
    def all(self, route):
        return self.all_url(self.url(route))

    def one_url(self, url):
        return _Element(self._api, url)

    def all_url(self, url):
        return _Collection(self._api, url)

    def url(self, *args):
        return "/".join([self._path or ""] + list(map(str, args)))


# An Element is a reference to an item on the server.  It does not
# contain any actual data.  Call `get` to fetch the referenced data
# from the server.
class _Element(object):
    def __init__(self, api, path):
        self._api = api
        self._path = path

    def delete(self):
        return self._api.delete(self.url())

    def get(self, **kwargs):
        return self._api.get(self.url(), **kwargs)

    def get_list(self, route, **kwargs):
        return self._api.get(self.url(route), **kwargs)

    def patch(self, json):
        return self._api.patch(self.url(), json=json)

    def post(self, route, json):
        return self._api.post(self.url(route), json=json)

    def put(self, json):
        return self._api.put(self.url(), json=json)

    # Returns a reference to a child element.
    def one(self, route, id):
        return self.one_url(self.url(route, id))

    # Returns a reference to a child collection.  Call `get_list` to
    # fetch the contents of that collection.
    def all(self, route):
        return self.all_url(self.url(route))

    def one_url(self, url):
        return _Element(self._api, url)

    def all_url(self, url):
        return _Collection(self._api, url)

    def url(self, *args):
        return "/".join([self._path] + list(map(str, [arg for arg in args if arg])))


class _Chats(_Collection):
    def __init__(self, api):
        super(_Chats, self).__init__(api, None)

    def list_year(self, year):
        return self.all("activity").custom_get_list(year)

    def list_month(self, year, month):
        return self.all("activity").custom_get_list("{}/{}".format(year, month))

    def list_day(self, year, month, day, to=None):
        path = "{}/{}/{}".format(year, month, day)
        return self.all("activity").custom_get_list(
            path, params={"to": to, "format": "json"}
        )

    def anonymize(self, ids):
        return self._api.raw_request("get", "/chats/anonymize", params={"id[]": ids})

    def download_xml(self, ids, out=None):
        if not out:
            return self._api.raw_request(
                "get", "/chats/download_xml", params={"id[]": ids}
            )

        response = self._api.raw_request(
            "get", "/chats/download_xml", params={"id[]": ids}, stream=True
        )
        with closing(response) as r:
            for chunk in r.iter_content(chunk_size=1024):
                out.write(chunk)

    def delete_chats(self, ids):
        return self._api.raw_request("get", "/chats/delete_chats", params={"id[]": ids})

    def delete_transcripts(self, ids):
        return self._api.raw_request(
            "get", "/chats/delete_transcripts", params={"id[]": ids}
        )


class _Reports(_Collection):
    def __init__(self, api):
        super(_Reports, self).__init__(api, None)

    def chats_per_hour(self, **kwargs):
        return self._api.get("v1", "/reports/chats-per-hour", params=kwargs)

    def chats_per_month(self, **kwargs):
        return self._api.get("v1", "/reports/chats-per-month", params=kwargs)

    def chats_per_operator(self, **kwargs):
        return self._api.get("v1", "/reports/chats-per-operator", params=kwargs)

    def chats_per_profile(self, **kwargs):
        return self._api.get("v1", "/reports/chats-per-profile", params=kwargs)

    def chats_per_protocol(self, **kwargs):
        return self._api.get("v1", "/reports/chats-per-protocol", params=kwargs)

    def chats_per_queue(self, **kwargs):
        return self._api.get("v1", "/reports/chats-per-queue", params=kwargs)
