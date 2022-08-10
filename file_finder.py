from pathlib import Path
import time
import csv
import itertools
import re
import pandas as pd
import numpy as np

start = time.time()


def file_exists():
    """check if file exists in directory"""

    mydir = Path("../HiRunnerExtended/Example")
    filenames = [
        file.name
        for file in mydir.iterdir()
        if file.name.startswith("HiTrack") and not file.name.endswith("json")
    ]
    file_paths = [
        file
        for file in mydir.iterdir()
        if file.name.startswith("HiTrack") and not file.name.endswith("json")
    ]

    if not filenames:
        print(
            "There are no huawei files in folder. Place HiTrack files into folder : ..\\HiRunnerExtended\\Example \n"
            "or check if they have not been renamed or removed. \n"
            "File name should be like this HiTrack_20190924_192535 "
        )

    # print(str(len(filenames)) + " Hitrack files found.")
    return (filenames, file_paths)


filenames, file_paths = file_exists()

with open(file_paths[0], "r", newline="") as csv_file:
    csv_reader = csv.reader(csv_file)
    tpe = []
    dfr = []
    dict_hitr = {}
    for i in itertools.islice(csv_reader, 0, None):
        dfr.append(i)

dict_list = []
dict_hitr["name"] = ""
dict_hitr["timestamp"] = ""
dict_hitr["value"] = ""
for j in itertools.islice(dfr, 0, None):

    if (
        j[0].startswith("tp=p-m")
        or j[0].startswith("tp=s-r")
        or j[0].startswith("tp=rs")
        or j[0].startswith("tp=rp")
    ):
        x = re.split(";|=", j[0])
        tpe.append(x)
start_date_timestamp = None
pacef = []

for j in itertools.islice(tpe, 0, None):
    if j[1] == "p-m":
        j[1] = "pace"
        j[2] = "timestamp"
        j[4] = "paceval"
        del j[0]

    if j[1] == "s-r":
        j[1] = "cadence"
        j[2] = "timestamp"
        j[3] = int(j[3])
        j[4] = "cadval"
        del j[0]
        if start_date_timestamp is None:
            start_date_timestamp = j[2]
    if j[1] == "rs":
        j[1] = "speed"
        j[2] = "timestamp"
        j[4] = "speedval"
        del j[0]
    if j[1] == "rp":
        j[1] = "extended"
        j[2] = "timestamp"
        del j[0]


keys_gen = []
for j in itertools.islice(tpe, 0, None):
    if j[0] == "pace":
        timestamp2 = int(j[2]) / 1000 * 6
        j[2] = int(timestamp2) + int(start_date_timestamp)
    if j[0] == "speed" or j[0] == "extended":
        timestamp2 = int(j[2]) * 1000
        j[2] = int(timestamp2) + int(start_date_timestamp)
    keys_gen.append((j[2]))

end = time.time()
""""generate keys for dict based on timestamp"""
d = dict.fromkeys(keys_gen, [])
lst = []


def val_parser():
    """parses values from extracted Huawei file and creates dictionaries"""
    footstrike1_16 = 0
    """OOP pre ukladanie dict"""

    for j in itertools.islice(tpe, 0, None):

        dictt = {
            "timestamp": [],
            #     "timestampunits": "s",
            "pace": [],
            "cadence": [],
            "speed": [],
            "stance_time": [],
            "pronation_excursion": [],
            "pitch_excursion": [],
            "impact_gs": [],
            "footstrike_type": [],
        }
        dictt.clear()
        if j[0] == "pace":
            dictt["timestamp"] = int(j[2] / 1000)
            # dictt["timestampunits"] = "s"
            dictt["pace"] = j[4]

        if j[0] == "cadence":
            dictt["timestamp"] = int(j[2] / 1000)
            # dictt["timestampunits"] = "s"
            dictt["cadence"] = j[4]

        if j[0] == "speed":
            dictt["timestamp"] = int(j[2] / 1000)
            #  dictt["timestampunits"] = "s"
            dictt["speed"] = j[4]

        if j[0] == "extended":
            dictt["timestamp"] = int(j[2] / 1000)
            #  dictt["timestampunits"] = "s"
            dictt["stance_time"] = j[4]
            dictt["pronation_excursion"] = j[6]
            dictt["pitch_excursion"] = j[8]
            dictt["impact_gs"] = j[10]
            # preratat na hodnoty medzi 1 az 16 pre footstrike type
            print(j[12], j[14], j[16], type(j[16]))
            if int(j[12]) > int(j[14]) > int(j[16]):
                # od 1 do 5
                footstrike1_16 = int(np.ceil((int(j[12]) / 10 * 5)))
            elif j[12] <= j[14] > j[16]:
                # od 6 do 10
                footstrike1_16 = int(np.ceil((int(j[14]) / 10 * 5) + 5))
            elif (
                int(j[12]) == 0
                and int(j[14]) < int(j[16])
                or int(j[14]) == int(j[16] != 0)
            ):
                # od 11 do 16
                footstrike1_16 = int(np.ceil((int(j[16]) / 10 * 5) + 10))
            elif j[12] == j[14] == j[16] == "0":
                footstrike1_16 = None
            dictt["footstrike_type"] = footstrike1_16

        lst.append(dictt)


val_parser()

print("sort", lst[1]["timestamp"])
"""Zoradenie podla timestampu v dictionaries stale s dualnymi hodnotami"""
newlist = sorted(lst, key=lambda d: d["timestamp"])

indextodelete = []
for j in range(len(newlist), 1, -1):
    if newlist[j - 1]["timestamp"] == newlist[j - 2]["timestamp"]:
        newlist[j - 2].update(newlist[j - 1])
        indextodelete.append(j)

result = []
dvt = []
for d in newlist:
    if d["timestamp"] not in dvt:
        dvt.append(d["timestamp"])  # note it down for further iterations
        result.append(d)
df2 = pd.DataFrame(result)

for j in itertools.islice(result, 0, None):
    print(j)


def val_appender():
    """VALUES APPENDER"""
    pass
    # checks if values can be added to timestamp, if timestanp is not in dictionary, then create it


df2.to_csv("newfile_h.csv", index=False)

# header creator

df3 = pd.DataFrame(
    columns=[
        "Type",
        "Local Number",
        "Message",
        "Field 1",
        "Value 1",
        "Units 1",
        "Field 2",
        "Value 2",
        "Units 2",
        "Field 3",
        "Value 3",
        "Units 3",
        "Field 4",
        "Value 4",
        "Units 4",
        "Field 5",
        "Value 5",
        "Units 5",
        "Field 6",
        "Value 6",
        "Units 6",
        "Field 7",
        "Value 7",
        "Units 7",
        "Field 8",
        "Value 8",
        "Units 8",
        "Field 9",
        "Value 9",
        "Units 9",
        "Field 10",
        "Value 10",
        "Units 10",
    ]
)
valuedf2 = [
    "Definition",
    "0",
    "file_id",
    "type",
    "1",
    "",
    "manufacturer",
    "1",
    "",
    "product",
    "1",
    "",
    "time_created",
    "",
    "",
    "serial_number",
    "1",
    "",
    "number",
    "1",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf3 = [
    "Data",
    "0",
    "file_id",
    "type",
    "4",
    "",
    "manufacturer",
    "0",
    "",
    "product",
    "0",
    "",
    "time_created",
    "930702435",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf4 = [
    "Definition",
    "0",
    "file_creator",
    "software_version",
    "1",
    "",
    "hardware_version",
    "1",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf5 = [
    "Data",
    "0",
    "file_creator",
    "software_version",
    "100",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf6 = [
    "Definition",
    "0",
    "event",
    "timestamp",
    "1",
    "",
    "event",
    "1",
    "",
    "event_type",
    "1",
    "",
    "data",
    "1",
    "",
    "event_group",
    "1",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf7 = [
    "Data",
    "0",
    "event",
    "timestamp",
    "930702435",
    "s",
    "event",
    "0",
    "",
    "event_type",
    "0",
    "",
    "timer_trigger",
    "0",
    "",
    "event_group",
    "0",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf8 = [
    "Definition",
    "0",
    "developer_data_id",
    "application_id",
    "16",
    "",
    "developer_data_index",
    "1",
    "",
    "application_version",
    "1",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf9 = [
    "Data",
    "0",
    "developer_data_id",
    "application_id",
    "3|2|1|0|5|4|7|6|8|9|10|11|12|13|14|15",
    "",
    "developer_data_index",
    "0",
    "",
    "application_version",
    "110",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf10 = [
    "Definition",
    "0",
    "field_description",
    "developer_data_index",
    "1",
    "",
    "field_definition_number",
    "1",
    "",
    "fit_base_type_id",
    "1",
    "",
    "field_name",
    "17",
    "",
    "units",
    "10",
    "",
    "native_mesg_num",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf11 = [
    "Data",
    "0",
    "field_description",
    "developer_data_index",
    "0",
    "",
    "field_definition_number",
    "0",
    "",
    "fit_base_type_id",
    "136",
    "",
    "field_name",
    "Doughnuts Earned",
    "",
    "units",
    "doughnuts",
    "",
    "native_mesg_num",
    "18",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf12 = [
    "Definition",
    "0",
    "field_description",
    "developer_data_index",
    "1",
    "",
    "field_definition_number",
    "1",
    "",
    "fit_base_type_id",
    "1",
    "",
    "field_name",
    "20",
    "",
    "units",
    "8",
    "",
    "native_mesg_num",
    "1",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf13 = [
    "Data",
    "0",
    "field_description",
    "developer_data_index",
    "0",
    "",
    "field_definition_number",
    "2",
    "",
    "fit_base_type_id",
    "136",
    "",
    "field_name",
    "pronation_excursion",
    "",
    "units",
    "degrees",
    "",
    "native_mesg_num",
    "20",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf14 = [
    "Data",
    "0",
    "field_description",
    "developer_data_index",
    "0",
    "",
    "field_definition_number",
    "3",
    "",
    "fit_base_type_id",
    "136",
    "",
    "field_name",
    "pitch_excursion",
    "",
    "units",
    "degrees",
    "",
    "native_mesg_num",
    "20",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf15 = [
    "Data",
    "0",
    "field_description",
    "developer_data_index",
    "0",
    "",
    "field_definition_number",
    "4",
    "",
    "fit_base_type_id",
    "136",
    "",
    "field_name",
    "impact_gs",
    "",
    "units",
    "gs",
    "",
    "native_mesg_num",
    "20",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf16 = [
    "Data",
    "0",
    "field_description",
    "developer_data_index",
    "0",
    "",
    "field_definition_number",
    "5",
    "",
    "fit_base_type_id",
    "136",
    "",
    "field_name",
    "footstrike_type",
    "",
    "units",
    "type",
    "",
    "native_mesg_num",
    "20",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf17 = [
    "Definition",
    "0",
    "field_description",
    "developer_data_index",
    "1",
    "",
    "field_definition_number",
    "1",
    "",
    "fit_base_type_id",
    "1",
    "",
    "field_name",
    "11",
    "",
    "units",
    "4",
    "",
    "native_field_num",
    "1",
    "",
    "native_mesg_num",
    "1",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf18 = [
    "Data",
    "0",
    "field_description",
    "developer_data_index",
    "0",
    "",
    "field_definition_number",
    "1",
    "",
    "fit_base_type_id",
    "2",
    "",
    "field_name",
    "Heart Rate",
    "",
    "units",
    "bpm",
    "",
    "native_field_num",
    "3",
    "",
    "native_mesg_num",
    "20",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
valuedf19 = [
    "Definition",
    "0",
    "record",
    "timestamp",
    "1",
    "",
    "speed",
    "1",
    "",
    "stance_time",
    "1",
    "",
    "pronation_excursion",
    "1",
    "",
    "pitch_excursion",
    "1",
    "",
    "impact_gs",
    "1",
    "",
    "footstrike_type",
    "1",
    "",
]


to_append = valuedf2

df_length = len(df3)

df3.loc[df_length] = to_append
df3.loc[df_length + 1] = valuedf3
df3.loc[df_length + 2] = valuedf4
df3.loc[df_length + 3] = valuedf5
df3.loc[df_length + 4] = valuedf6
df3.loc[df_length + 5] = valuedf7
df3.loc[df_length + 6] = valuedf8
df3.loc[df_length + 7] = valuedf9
df3.loc[df_length + 8] = valuedf10
df3.loc[df_length + 9] = valuedf11
df3.loc[df_length + 10] = valuedf12
df3.loc[df_length + 11] = valuedf13
df3.loc[df_length + 12] = valuedf14
df3.loc[df_length + 13] = valuedf15
df3.loc[df_length + 14] = valuedf16
df3.loc[df_length + 15] = valuedf17
df3.loc[df_length + 16] = valuedf18
df3 = df3.append(
    pd.Series(valuedf19, index=df3.columns[: len(valuedf19)]), ignore_index=True
)


# set timestamp as index
df2.set_index("timestamp", inplace=True)
re = df2.loc[:, ["cadence", "speed"]]
for index, row in df2.iterrows():
    df_length = len(df3)
    df4 = [
        "Data",
        "0",
        "record",
        "timestamp",
        index,
        "s",
        "speed",
        row[1],
        "m/s",
        "stance_time",
        row[2],
        "ms",
        "pronation_excursion",
        row[3],
        "degrees",
        "pitch_excursion",
        row[4],
        "degrees",
        "impact_gs",
        row[5],
        "gs",
        "footstrike_type",
        row[6],
        "type",
    ]

    # df3.loc[df_length] = ["Data", "0", "record", "timestamp", "s", "distance", "0", "speed", row[1],]
    # df3.loc[df_length] = ['India', 'Shivam', 'Pandey']
    df3 = df3.append(pd.Series(df4, index=df3.columns[: len(df4)]), ignore_index=True)
#  df3 = pd.concat([df3, df4])
#  print(index, row[2])
# print (index,row["timestamp"])
# for j in itertools.islice(df2, 0, None):
#    # df_length = len(df3)
#   #  df3.loc[df_length] = ["Data","0","record","timestamp",]
#     df2["time"]
#     print(j)


# session creator


df3.to_csv("newfile_h2.csv", index=False)
# print(df3)
