import random

lines = open('kit.txt', 'r').read().splitlines()
insults = [line.split(' ') for line in lines]
length = len(lines)


def insult():
    random.seed()
    insult = []
    for column in range(3):
        insult.append(insults[random.randrange(length)][column])
    return "Thou {}, {} {}!".format(insult[0], insult[1], insult[2])


if __name__ == "__main__":
    print(insult())
