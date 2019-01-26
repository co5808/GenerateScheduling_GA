import codecs

def LoadSchedule(filename = "Schedule.csv"):
    ScheduleList = {}
    with codecs.open('.\\'+filename) as f:
        temp = f.readlines()

    for i in temp:
        list = i.split(",")
        ScheduleList[int(list[0])] = [int(list[1].strip()), int(list[2].strip())]

    return ScheduleList

def BinaToDec(Binary):
    temp = 0
    for i in range(0, len(Binary), 1):
        #print(Binary[i], i, (2 ** (len(Binary) - 1 - i)) * int(Binary[i]))
        temp += (2 ** (len(Binary) - 1 - i)) * int(Binary[i])

    return temp

def DecToBina(Dec, pos):
    binary =  bin(int(Dec)).split("0b")[1]
    temp = '0'

    if len(str(binary)) + 1 < pos:
        for i in range(0, pos - len(binary)+1):
                temp = temp + '0'

    return str(temp) + binary


