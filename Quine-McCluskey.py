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

dash = '-'


#функция, проверяющая входит ли код A в код B
def entry(kitA, kitB):
    for i in range(len(kitA)): 
        if (kitA[i] != kitB[i]) and (kitB[i] != dash): 
            return False 
    return True


#функция склеивания двух кодов
def gluing(A, B):
    C = ""
    
    diff = 0
    for i in range(len(A)):
        if A[i] == B[i]:
            C = C + A[i]
        elif (A[i] != B[i]) and (A[i] != dash) and (B[i] != dash):
            C = C + dash
            diff += 1
        else:
            return ""
        
        if diff > 1:
            return ""

    return C


#вспомогательная функция, возвращая 'удобные' данные для склеивания 
def getDictKitsForGluing(kits):
    dictKitsForGluing = dict()

    for kit in kits:
        cntUnits = kit.count("1")
        if cntUnits not in dictKitsForGluing:
            dictKitsForGluing[cntUnits] = {kit}
        else:
            dictKitsForGluing[cntUnits].add(kit)

    return dictKitsForGluing


#функция склеивания всех кодов
def getGluingKits(A: dict) -> (set, set):
    gluingKits, unusedKits = set(), set()

    allKits = set()
    usedKits = set()

    for kits in A.values():
        allKits.update(kits)

    for i in A:
        if (i + 1) not in A:
            continue

        kits1, kits2 = A[i], A[i+1]

        for kit_x in kits1:
            for kit_y in kits2:
                kitGluing_xy = gluing(kit_x, kit_y)
                if not kitGluing_xy:
                    continue

                gluingKits.add(kitGluing_xy)
                usedKits.add(kit_x)
                usedKits.add(kit_y)

    unusedKits = allKits - usedKits

    return gluingKits, unusedKits


#функция, проверяющая коректность покрытия (нужна для перебора всех покрытий)
def correctCoating(table, allKits, selectedImps):
    usedKits = {kit: 0 for kit in allKits}

    for imp in selectedImps:
        for kit in table[imp]:
            if kit not in allKits:
                continue

            usedKits[kit] += 1

    for kit in allKits:
        if usedKits[kit] == 0:
            return False

    for imp in selectedImps:
        for kit in table[imp]:
            if kit in allKits and usedKits[kit] == 1:
                break
        else:
            return False

    return True     


#функция, реализующая поглощение кодов
def absorbs(products):
    products = list(products)

    result = []

    for coatA in products:
        absorbed = False

        for coatB in products:
            if coatA != coatB and coatA >= coatB:
                absorbed = True
                break

        if not absorbed:
            result.append(coatA)

    return result


#функция, которая ищет подходящие покрытия методом Петрика
def getСoatingsByPetrick(table, allKits, selectedImps):
    products = {frozenset()}

    for kit in allKits:

        variant = set()

        for imp in selectedImps:
            if kit in table[imp]:
                variant.add(imp)

        if not variant:
            return []

        newProducts = set()

        for product in products:
            for imp in variant:
                newProduct = product | frozenset([imp])
                newProducts.add(newProduct)

        products = absorbs(newProducts)

    return list(products)


#функция, которая расшифровывает имликанты в читаемый вид
def decodImp(implicant, cntVars=n):
    if implicant == '':
        return '0'

    bar = '\u0304'
    alf = 'xyzwt'
    res = ''

    for i, liter in enumerate(implicant):
        if liter == '1':
            res += alf[i] if cntVars <= len(alf) else alf[0] + str(i+1)
        elif liter == '0':
            res += alf[i] + bar if cntVars <= len(alf) else alf[0] + bar + str(i+1) + bar

    if res=='':
        return dash*cntVars
    return res


#функция, которая выводит все простые импликанты функции
def outputPrimeImplicants(primeImplicants):
    print("Prime implicants: ", end='')
    if primeImplicants:
        print(decodImp(primeImplicants[0]), end='')

    for i in range(1, len(primeImplicants)):
        imp = primeImplicants[i]
        print(', ', decodImp(imp), end='')

    print()


#функция, которая выводит ДНФ
def outputDNF(i, DNF, lenDNF, complexityDNF):
    if DNF == '':
        DNF_ = 0
    else:
        DNF_ = ' + '.join([decodImp(imp) for imp in DNF])

    print(f'D{i}: {DNF_}; θ(D{i}) = {lenDNF}; Θ(D{i}) = {complexityDNF}')


#функция, которая заменяет код -1- в 010 (нужна для сортировки кодов)
def toFull(x):
    return [i if i != dash else '0' for i in x]


#нахожу СДНФ
CDNF = list()
for i in range(2**n):
    fi = function[i]
    if fi == "0":
        continue
    
    line = bin(i)[2:].zfill(n)
    CDNF.append(line)


#нахожу простые импликанты
kits = set(CDNF)
PrimeImplicants = set()

while True:
    dictKitsForGluing_ = getDictKitsForGluing(kits)
    currentGluingKits_, finishGluingKits_ = getGluingKits(dictKitsForGluing_)

    PrimeImplicants.update(finishGluingKits_)

    if not currentGluingKits_:
        break
    else:
        kits = currentGluingKits_


PrimeImplicants = sorted(PrimeImplicants, key=lambda x: toFull(x))
outputPrimeImplicants(PrimeImplicants)

#таблица покрытий
table = {primeImplicant: list() for primeImplicant in PrimeImplicants}
cntUses = {kit:0 for kit in CDNF}

for primeImplicant in PrimeImplicants:
    for kit in CDNF:
        if entry(kit, primeImplicant):
            table[primeImplicant].append(kit)
            cntUses[kit] += 1


#нахожу ядра
cores = set()
usedKits = set()
for kit, cnt in cntUses.items():
    if cnt == 1:
        for row, columns in table.items():
            if kit in columns:
                cores.add(row)
                usedKits.update(columns)

cores = sorted(cores)


#нахожу наборы не покрытые ядрами
unUsedKits = list()
for kit in CDNF:
    if kit not in usedKits:
        unUsedKits.append(kit)


#нахожу импликанты не равные какому либо ядру
unUsedImplicants = list()
for primeImplicant in PrimeImplicants:
    if primeImplicant not in cores:
        unUsedImplicants.append(primeImplicant)



#нахожу тупиковые ДНФ через полный перебор оставшихся импликант (перебор всех покрытий)
'''
deadDNFs = list()
l = len(unUsedImplicants)
for i in range(2**l):
    inclus_imps_ = bin(i)[2:].zfill(l)
    coating = [unUsedImplicants[k] for k, v in enumerate(inclus_imps_) if v=='1']
    
    if correctCoating(table, unUsedKits, coating):
        deadDNFs.append(cores + coating)'''

#нахожу тупиковые ДНФ методом Петрика (перебор 'хороших' покрытий)
deadDNFs = list()
for coating_ in getСoatingsByPetrick(table, unUsedKits, unUsedImplicants):
    coating = sorted(cores + list(coating_), key=lambda x: toFull(x))
    deadDNFs.append(coating)

deadDNFs.sort()
for i, DNF in enumerate(deadDNFs, start=1):
    outputDNF(i, DNF, len(DNF), sum(len(imp) - imp.count(dash) for imp in DNF))