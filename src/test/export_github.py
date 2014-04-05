__author__ = 'simon'
# coding=gbk

def export_csv(repository,target_csv):
    import requests

    resp = requests.get(url=repository)
    #print resp.text
    data = resp.json()
    #print data
    #print len(data)
    import csv
    with open(target_csv, 'wb') as csvfile:
        #spamwriter = csv.writer(csvfile, delimiter=' ',
        #                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(['标题', '内容', '优先级'])
        for issue in data:
            #print issue
            #print issue['title']
            #print issue['body']
            #print issue['body'].encode("GB18030")
            #print issue['labels']
            priority = ''
            for label in issue['labels']:
                #print label
                priority += label['name']
            #print priority

            #spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            #spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
            spamwriter.writerow([issue['title'], issue['body'].encode("GB18030"), priority])

if __name__=="__main__":
    repository = 'https://api.github.com/repos/szjs2013/wxkcsj_new/issues'
    export_csv(repository,'issues.csv')
