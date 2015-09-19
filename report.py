# -*- coding: utf-8 -*-
def removeQuotes(line):
    while line.find('"') != -1:
        line = line.replace('"', '')
    return line

def filter(fileName="report.csv", departmentsList=["Технические"], exclusionsList = ["Need info", "On hold"]):
    fh = open(fileName,'r')
    report = list()

    for line in fh:
        for dep in departmentsList:
            if dep.lower() in line.lower():
                if removeQuotes( line.split(',')[1] ) not in exclusionsList:
                    report.append( removeQuotes( line.strip() ) )
    fh.close()
    report.sort()

    count = 0
    totalCount = 0
    department = None
    result =  'Department\tStatus\tTotal\tLast Activity\n'

    for l in report:
        if department is None:
            department = l[:l.find(',')]
            count = int(l.split(',')[2])
            result = result + "\t".join(l.split(',')) + '\n'
            continue

        elif department == l[:l.find(',')]:
            count += int(l.split(',')[2])
            result = result + "\t".join(l.split(',')) + '\n'

        elif department != l[:l.find(',')]:
            totalCount += count
            result = result + "\t\t" + str(count) + "\t" + '\n'
            result = result + "\t".join(l.split(',')) + '\n'
            department = l[:l.find(',')]
            count = int(l.split(',')[2])

    result = result + "\t\t" + str(count) + "\t" + '\n'
    totalCount += count
    result = result + "\tAbsolute count:\t" + str(totalCount) + "\t" + '\n'

    return result

# print filter()