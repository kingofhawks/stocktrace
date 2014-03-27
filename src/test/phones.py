def getPhoneDataBySheet(excelProxy, sheet):
    print "***********Excel Sheet******", sheet
    line = 2000

    content = excelProxy.getRange(sheet, 4, 1, line, 5)
    #print len(content)
    #    print content
    #    print content[2][0]
    #    print content[2][1]
    #    print content[2][0]
    #    print content[2][1]

    phones = []
    missings = []
    for line in content:
        #print line
        print line[0]
        print line[1]
        print line[2]
        if line[0] is None:
            break
        missing = True
        if (line[1] is not None and (len(line[1]) == 11)):
            phones.append(line[1])
            missing = False
        if (line[2] is not None and (len(line[2]) == 11)):
            phones.append(line[2])
            missing = False
        #continue
        if missing:
            missings.append(line[0])

        print phones
    return phones, missings


def convertListToText(phones):
    result = ''
    for entry in phones:
        result = result + entry + ';'
    return result


def write_to_file(phones):
    file = open("phones.txt", "w")
    result = ''
    for entry in phones:
        result = result + entry + ';'

    file.write(result[:-1])
    file.close()


if __name__ == '__main__':
    from easyExcel import EasyExcel
    import os, sys

    root = os.path.abspath(os.path.dirname(sys.argv[0]))
    print('root path:{}'.format(root))
    path = root + '\\test.xls'
    excelProxy = EasyExcel(path)
    for sheets in excelProxy.getAllSheets():
        print sheets.name
        result = getPhoneDataBySheet(excelProxy, sheets.name)
    print('Total phones:{number}'.format(number=len(result[0])) )
    print result[0]
    print result[1]
    for missing in result[1]:
        print missing

    phones = result[0]
    print convertListToText(phones)
    write_to_file(result[0])
    excelProxy.close()
