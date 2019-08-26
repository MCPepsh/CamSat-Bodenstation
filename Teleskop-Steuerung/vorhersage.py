import turtle
def approxPos(s):
    out = 0
    factor = 1
    print(factor)
    #print(len(s))
    #for item in s:
        #print(item)
    #print(s)
    #a = 0
    #b = 0
    out = s[len(s) - 1]
    v = []
    a = []
    inv = []
    weight = []
    weighted = []
    for i in range(len(s) - 1):
        #print(str(i) + " -> " + str(len(s) - i - 1))
        inv.append(len(s) - i - 2)
        #print("test")
        weight.append(1/(factor**inv[i]))
        v.append(s[i + 1] - s[i])
    #print(weight)
    #print(inv)
    #print(s)
    #print(v)
    for i in range(len(v) - 1):
        a.append(v[i + 1] - v[i])
        weighted.append(a[i] * weight[i + 1])
    #print(a)
    #print(weighted)
    #print(len(a))
    #print(len(weight[1:]))
    a.append(sum(weighted)/sum(weight[1:]))
    v.append(v[len(v) - 1] + a[len(a) - 1])
    #s.append(s[len(s) - 1] + v[len(v) - 1])
    out = s[len(s) - 1] + v[len(v) - 1]
    '''if(b != 0):
        c = a / b
        out = out + c'''
    print(s[len(s) - 1])
    print(out)
    print(s[len(s) - 1] - out)
    print()
    return out


daten = [
    51.88453333333333,
    51.88433666666667,
    51.88406666666667,
    51.88379666666667,
    51.88352666666667,
    51.88325666666667,
    51.883026666666666,
    51.882756666666666,
    51.882486666666665,
    51.88238333333334
    ]
length = len(daten)

for j in range(1):
    appr = approxPos(daten)
    daten.append(appr)
    #print(appr)

turtle.up()
turtle.ht()
turtle.speed(0)
for i in range(len(daten) - 1):
    turtle.goto((500.0/(len(daten) - 1)) * i - 250, (daten[i] - min(daten)) * 100000)
    turtle.down()
    turtle.width(5)
    turtle.forward(0)
    turtle.width(1)
turtle.goto(250, (appr - min(daten)) * 100000)
#turtle.down()
turtle.width(5)
turtle.forward(0)
turtle.width(1)
turtle.up()
turtle.goto((500.0/(len(daten) - 1)) * (length - 1) - 250, (daten[length - 1] - min(daten)) * 100000)
turtle.down()
turtle.color("red")
turtle.goto((500.0/(len(daten) - 1)) * length - 250, (51.88250333333333 - min(daten)) * 100000)
turtle.width(5)
turtle.forward(0)
turtle.width(1)
