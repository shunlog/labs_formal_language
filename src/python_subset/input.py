# comments and blank lines are ignored

a = 10 * (5 + 5 * 2)
b = 0

while b == 0:
    if a > b:
        a = a - b
    else:
        b = b - a
