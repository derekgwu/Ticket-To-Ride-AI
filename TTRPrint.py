from tabulate import tabulate
def formatTrainPrint(toPrint):
        for item in toPrint:
            print(f"| {item[0]} to {item[1]} | Trains required: {item[2]['weight']}")
            print(f"Colors: {item[2]['edgeColors']}")
            print()

def formatHandPrint(toPrint):
    for color, count in toPrint.items():
        print(f"{color}: {count}")

def formatTicketPrint(toPrint):
    i = 0
    for ticket in toPrint:
        print(f"ID: {i} | {toPrint[ticket][0]} to {toPrint[ticket][1]} | Length: {toPrint[ticket][2]}")
        print("")
        i += 1

def printLine():
    print("--------------------")

def formatPrintHand(hand):
    card_table = []
    for color in hand:
        card_table.append([color, hand[color]])
    print(tabulate(card_table, headers=['Color', 'Count']))
    print()

def formatPrintDeck(deck):
    print(" | ".join(map(str, deck)))
    print()
