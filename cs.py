
list = []
history_high_score = 0
try:
    with open("config/config.txt") as file_object:
        for line in file_object:
            list.append(line.rstrip().split("="))


    key = 0
    while key < len(list):
        if list[key][0] == "history_high_score":
            history_high_score = int(list[key][1])
            break
        key += 1
except:
    history_high_score = 0


print(history_high_score)
