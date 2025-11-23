def formatTrainPrint(self, toPrint):
        for item in toPrint:
            print(f"{item[0]} to {item[1]}")
            print(f"Trains required: {item[2]['weight']}")
            print(f"Colors: {item[2]['edgeColors']}")
            print()

def formatHandPrint(self, toPrint):
    for color, count in toPrint.items():
        print(f"{color}: {count}")
def formatTicketPrint(self, toPrint):
    i = 0
    for ticket in toPrint:
        print(i)
        print(f"Arrival: {toPrint[ticket][0]}")
        print(f"Destination: {toPrint[ticket][1]}")
        print(f"Length: {toPrint[ticket][2]}")
        print("")
        i += 1
def printLine(self):
    print("--------------------")