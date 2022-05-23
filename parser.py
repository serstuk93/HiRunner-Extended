import csv
import itertools

with open("113.csv", "r", newline="") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    tpe = []
    dfr = []

    for i in itertools.islice(csv_reader,30):
    #     if "Type" in i[0]:
    #         tpe = i
    #         print("ahoj",i)
    #   #  print(i[6:8])
        if "Definition" in i["ď»żType"] and "record" in i['Message']:
           # dfr = i
            dfr.append(i)

    # for i in itertools.islice(csv_reader, 8, 50):
    #     print(i[6:8])
for i in dfr:
    for j in range(1,len(i)):
        print(i[j])
        # if i[j].startswith("Field"):
        #     print(i[j+1])
    print(i)
       #alternativne sa da spravit cez next kde skoci vzdy len o 1 riadok
    # next(csv_reader)
    # for line in csv_reader:
       # print(line[6:8])


#check if key exists
# 1. ground contact time = GCT = stance_time
# 2. Landing impact/GroundImpactAcceleration = gia
# 3. eversion excursion = ee
# 4. swing angle = sa
# 5. forefoot strike pattern = fsp  = stroke_type
# 6. WholeFootStrikePattern = wsp = stroke_type
# 7. Heel strike pattern/HindFootStrikePattern = hsp = stroke_type
adding_keys=["stance_time","altitude","cadence","vertical_ratio"",step_length","stroke_type",]
