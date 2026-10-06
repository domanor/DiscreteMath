
#reading data
import sys

if len(sys.argv) > 1:
    n, function = sys.argv[1:3]
    n = int(n)
else:
    data = input().split()
    if len(data) == 1:
        n, function = int(data[0]), input().strip()
    else:
        n, function = int(data[0]), data[1]



lines = [function]

for _ in range(2**n - 1):
    line = ''
    for i in range(len(lines[-1]) - 1):
        a, b = int(lines[-1][i]), int(lines[-1][i + 1])
        line = line + str(a ^ b)
    lines.append(line)


spaces = [' ']*(2**n)
alf = "xyzwt"

print('1', end=' ')

for i in range(1, 2**n):
    a = bin(i)[2:].zfill(n)
    sign = ""
    for j, aj in enumerate(a):
        if aj == '1':
            if n <= len(alf):
                sign = sign + alf[j]
            else:
                sign = sign + alf[0] + str(j+1)

    spaces[i] = len(sign)*' '
    print(sign, end=' ')

print()

for i in range(2**n):
    output = [lines[j][i] + spaces[j] for j in range(2**n - i)]
    print(''.join(output))
