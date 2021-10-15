__version__ = "0.3.9"
__author__ = "Guinsly Mondésir"

sp_ask_school_dict = [
    {
        "school": {
            "id": 1,
            "queues": [
                "toronto",
                "toronto-mississauga",
                "toronto-scarborough",
                "toronto-st-george",
                "toronto-st-george-proactive",
            ],
            "suffix": ["_tor"],
            "short_name": "toronto",
            "full_name": "University of Toronto",
        }
    },
    {
        "school": {
            "id": 2,
            "queues": [],
            "suffix": ["_int", "_int.fr"],
            "short_name": "Scholars Portal - Mentees",
            "full_name": "Scholars Portal - Mentees",
        }
    },
    {
        "school": {
            "id": 3,
            "queues": [
                "western",
                "western-fr",
                "western-proactive",
                "western-txt",
            ],
            "suffix": ["_west", "_west.fr"],
            "short_name": "Western",
            "full_name": "University of Western Ontario",
        }
    },
    {
        "school": {
            "id": 4,
            "queues": [
                "carleton-txt",
                "carleton",
                "carleton-access-services-txt",
                "carleton-access-services",
            ],
            "suffix": ["_car"],
            "short_name": "Carleton",
            "full_name": "Carleton University",
        }
    },
    {
        "school": {
            "id": 5,
            "queues": ["ryerson", "ryerson-proactive"],
            "suffix": ["_rye"],
            "short_name": "Ryerson",
            "full_name": "Ryerson University",
        }
    },
    {
        "school": {
            "id": 6,
            "queues": ["laurentian", "laurentian-fr"],
            "suffix": ["_lan", "_lan.fr"],
            "short_name": "Laurentian",
            "full_name": "Laurentian University",
        }
    },
    {
        "school": {
            "id": 7,
            "queues": ["queens"],
            "suffix": ["_queens"],
            "short_name": "Queen's",
            "full_name": "Queen's university",
        }
    },
    {
        "school": {
            "id": 8,
            "queues": ["brock"],
            "suffix": ["_brk"],
            "short_name": "Brock",
            "full_name": "Brock University",
        }
    },
    {
        "school": {
            "id": 9,
            "queues": ["guelph-humber", "guelph-humber-txt"],
            "suffix": ["_guehum"],
            "short_name": "Guelph-Humber",
            "full_name": "University of Guelph-Humber",
        }
    },
    {
        "school": {
            "id": 10,
            "queues": ["guelph"],
            "suffix": ["_gue"],
            "short_name": "Guelph",
            "full_name": "University of Guelph",
        }
    },
    {
        "school": {
            "id": 12,
            "queues": ["ontario-tech"],
            "suffix": ["_ontech", "_uoit"],
            "short_name": "Ontario Tech",
            "full_name": "Ontario Tech University",
        }
    },
    {
        "school": {
            "id": 13,
            "queues": ["saintpaul", "saintpaul-fr"],
            "suffix": ["_stp", "_stp.fr"],
            "short_name": "Saint-Paul",
            "full_name": "Saint-Paul University",
        }
    },
    {
        "school": {
            "id": 14,
            "queues": ["ocad"],
            "suffix": ["_ocad"],
            "short_name": "OCAD",
            "full_name": "OCAD U",
        }
    },
    {
        "school": {
            "id": 15,
            "queues": ["lakehead", "lakehead-proactive"],
            "suffix": ["_lake"],
            "short_name": "Lakehead",
            "full_name": "Lakehead university",
        }
    },
    {
        "school": {
            "id": 16,
            "queues": ["algoma", "algoma-fr", "algoma-proactive"],
            "suffix": ["_alg"],
            "short_name": "Algoma",
            "full_name": "Algoma university",
        }
    },
    {
        "school": {
            "id": 17,
            "queues": ["mcmaster", "mcmaster-txt"],
            "suffix": ["_mac"],
            "short_name": "McMaster",
            "full_name": "McMaster university",
        }
    },
    {
        "school": {
            "id": 18,
            "queues": ["york", "york-glendon", "york-glendon-fr", "york-txt"],
            "suffix": ["_york", "_york.fr"],
            "short_name": "York",
            "full_name": "York university",
        }
    },
    {
        "school": {
            "id": 19,
            "queues": [
                "scholars-portal",
                "scholars-portal-txt",
                "scholars portal",
                "clavardez",
                "clavardez-txt",
            ],
            "suffix": ["_sp"],
            "short_name": "Scholars Portal",
            "full_name": "Scholars Portal",
        }
    },
    {
        "school": {
            "id": 20,
            "queues": ["ottawa", "ottawa-fr", "ottawa-fr-txt", "ottawa-txt"],
            "suffix": ["_ott"],
            "short_name": "Ottawa",
            "full_name": "Ottawa University",
        }
    },
    {
        "school": {
            "id": 21,
            "queues": [
                "practice-webinars",
                "practice-webinars-fr",
                "practice-webinars-txt",
            ],
            "suffix": [],
            "short_name": "Practice queue",
            "full_name": "SP Practice Queue",
        }
    },
    {
        "school": {
            "id": 22,
            "queues": ["sp-always-offline"],
            "suffix": [],
            "short_name": "LibraryH3lp",
            "full_name": "LibraryH3lp",
        }
    },
]


def find_school_by_operator_suffix(username):
    """from an username suffix find the short name of that School

    Arguments:
        username {str} -- suffix of the schoo i.e. nalini_tor

    Returns:
        str -- The short name of the school i.e. Toronto
    """
    # print("This username :{0}".format(username))

    if username is None:
        return username

    if "_" in username:
        # print("_ found in {0}".format(username))
        suffix = username.split("_")
        try:
            suffix = "_" + suffix[1]
        except:
            # print(username)
            # breakpoint()
            pass
        # print("suffix:{0}".format(suffix))
        for item in sp_ask_school_dict:
            if suffix in item.get("school").get("suffix"):
                # print(item.get('school').get('short_name') )
                return item.get("school").get("short_name")
    elif "admin" in username:
        school = username.split("-")[0]
        return school
    else:
        return "Unknown"


def find_queues_from_a_school_name(school):
    if school is None:
        return school
    school = school.lower()

    for item in sp_ask_school_dict:
        if school == item.get("school").get("short_name").lower():
            return item.get("school").get("queues")
    return "Unknown"


def get_shortname_by_full_school_name(school):
    """from a University Full name find the shortname of that School

    Arguments:
        school {str} -- school (i.e. Full name)

    Returns:
        str -- The short name of the school i.e. Toronto
    """
    if school is None:
        return school
    school = school.lower()

    for item in sp_ask_school_dict:
        if school == item.get("school").get("full_name"):
            return item.get("school").get("short_name")


def find_school_by_queue_or_profile_name(queue):
    """from the name of a queue find the full  name of that School

    Arguments:
        queue {str} -- queue/service i.e. western-proactive

    Returns:
        str -- The full name of the school i.e. Toronto
    """
    if queue is None:
        return queue

    for item in sp_ask_school_dict:
        if queue in item.get("school").get("queues"):
            return item.get("school").get("short_name")
    return "Unknown"


def find_school_abbr_by_queue_or_profile_name(queue):
    """from a queue name or the name of a Queue Profile find the short name of that School

    Arguments:
        queue {str} -- queue/service i.e. ryerson-proactive

    Returns:
        str -- The short name of the school i.e. Toronto
    """
    if queue is None:
        return queue

    for item in sp_ask_school_dict:
        if queue in item.get("school").get("queues"):
            return item.get("school").get("short_name")
    return "Unknown"


HTF_schools = [
    "Brock University",
    "Carleton University",
    "Laurentian University",
    "University of Toronto",
    "Ontario Tech University",
    "Western Ontario University",
    "Queens University",
    "Ryerson University",
]


def find_queue_by_criteria(criteria=None):
    """[summary]

    Args:
        criteria ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    queue_list = list()
    for item in sp_ask_school_dict:
        for element in item.get("queues"):
            if criteria in element:
                queue_list.append(element)

    return queue_list


FRENCH_QUEUES = [
    "algoma-fr",
    "clavardez",
    "laurentian-fr",
    "ottawa-fr",
    "saintpaul-fr",
    "western-fr",
    "york-glendon-fr",
]

SMS_QUEUES = [
    "carleton-txt",
    "clavardez-txt",
    "guelph-humber-txt",
    "mcmaster-txt",
    "ottawa-fr-txt",
    "ottawa-txt",
    "scholars-portal-txt",
    "western-txt",
    "york-txt",
    "york-fr-txt",
    "txt-carleton-access-services",
    "carleton-access-services-txt",
]

PRACTICE_QUEUES = ["practice-webinars", "practice-webinars-fr", "practice-webinars-txt"]


def find_routing_model_by_profile_name(university_name):
    """[summary]

    Args:
        university_name ([type]): [description]

    Returns:
        [type]: [description]
    """
    if university_name is None:
        return university_name
    if university_name in HTF_schools:
        return "HTF"
    else:
        return "FLAT"


if __name__ == "__main__":
    FRENCH_QUEUES = find_queue_by_criteria(criteria="-fr")
    SMS_QUEUES = find_queue_by_criteria(criteria="-txt")
    PRACTICE_QUEUES = find_queue_by_criteria(criteria="practice")
