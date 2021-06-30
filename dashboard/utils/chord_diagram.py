from lh3.api import *
from datetime import date
from datetime import datetime
from pprint import pprint as print
import pandas as pd
import numpy as np


from dashboard.utils.ask_schools import (
    find_school_by_queue_or_profile_name,
    find_school_by_operator_suffix,
    get_shortname_by_full_school_name,
)


def remove_columns_from_df(df, columns):
    df.drop(columns, axis=1, inplace=True)
    return df


def chord_diagram(year, month, day, to=None):
    client = Client()
    chats = client.chats().list_day(year, month, day, to=to)
    chats_this_day = [chat for chat in chats if "practice" not in chat.get("queue")]
    chats_answered = [chat for chat in chats_this_day if chat.get("accepted") != None]
    return chats_answered


def prepare_to_dataframe(chats_answered):
    df = pd.DataFrame(chats_answered)
    df["guest"] = df["guest"].apply(lambda x: x[0:7])

    df["from"] = df["queue"].apply(lambda x: find_school_by_queue_or_profile_name(x))
    df["to"] = df["operator"].apply(lambda x: find_school_by_operator_suffix(x))
    df["school"] = df["operator"].apply(lambda x: find_school_by_operator_suffix(x))

    breakpoint()

    

    df["short"] = df["from"].apply(lambda x: find_school_by_queue_or_profile_name(x))

    columns = [
        "duration",
        "reftracker_id",
        "started",
        "operator",
        "reftracker_url",
        "desktracker_id",
        "ended",
        "desktracker_url",
        "wait",
        "profile",
        "id",
        "referrer",
        "ip",
        "accepted",
        "protocol",
    ]
    df = remove_columns_from_df(df, columns)
    

    
    del df["from"]

    df.rename({"short": "from"}, axis=1, inplace=True)
    columns = ["guest", "from", "to"]
    df = df[columns]
    df.sort_values(by=["from"])
    df = df.groupby("from")["to"].value_counts().reset_index(name="value")
    # df.to_excel("for_chordiagram.xlsx", index=False)
    # df.to_csv("for_chordiagram.csv", index=False)
    return df


def gephi_data(df):
    schools = list(set(list(df["from"].unique()) + list(df["to"].unique())))
    node = pd.DataFrame({"id": np.arange(1, len(schools) + 1), "label": schools})

    gephi = df.merge(node, left_on="from", right_on="label")
    gephi = gephi.merge(node, left_on="to", right_on="label")
    edges = gephi[["id_x", "id_y"]]
    edges["source"] = gephi["id_x"]
    edges["target"] = gephi["id_y"]
    edges["weight"] = gephi["value"]

    del edges["id_x"]
    del edges["id_y"]

    return [node, edges]


if __name__ == "__main__":
    chats_answered = chord_diagram(2020, 9, 1, to="2020-11-11")
    df = prepare_to_dataframe(chats_answered)
    # print(df.head(50))
    nodes, edges = gephi_data(df)
    nodes.to_csv("nodes.csv", index=False)
    edges.to_csv("edges.csv", index=False)

    df.columns = ["source", "target", "value"]
    # breakpoint()
    df["label"] = df["source"]
    df.to_csv("test.csv", index=False)
    del df["label"]
    df.columns = ["from", "to", "value"]
    df.to_excel("data_for_chord_diagram_or_network_graph.xlsx", index=False)
    df.to_json("for_chordiagramNov2020.json", orient="records")
    # breakpoint()

    print(df.head())

    # df.rename({'to':"target"}, axis=1, inplace=True)
    # df.rename({'from': 'source'}, axis=1, inplace=True)

    # Gephi
    # Nodes
    schools = set(list(df["from"].unique()) + list(df["to"].unique()))
    # print(schools)
