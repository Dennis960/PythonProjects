import keyboard

def round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])

personA = 50
personB = 0
print("A:", personA, "B:", personB, "gesamt:", personA + personB)

print(round(9/2))

def spielzug(count=1):
    for i in range(0, count):
        global personA, personB
        forB = int(round(float(personA)/float(2)))
        forA = int(round(float(personB)/float(10)))
        personA -= forB
        personB -= forA
        personA += forA
        personB += forB
        print("A:", personA, "forB", forB, "B:", personB, "forA", forA, "gesamt:", personA + personB)
spielzug(8)