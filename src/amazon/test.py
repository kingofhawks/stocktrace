'''
Created on 2012-5-9

@author: Simon
'''

if __name__ == '__main__':
    import boto
    from boto import s3
    from boto.s3.bucket import Bucket
    import sys
    from boto.s3.key import Key
    from boto.s3.connection import OrdinaryCallingFormat
    from boto.s3.connection import SubdomainCallingFormat
    
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    
    conn = boto.connect_s3('AKIAJH777UDIOAMSJ2QA', '/FJiF2LyJXRjcOVaEXOHswbeWqt2ZV9EnV3sh7/V',debug=2,
            #host="172.25.21.78", 
            #port=10001, 
            port =443,
            is_secure=True
            )
    #print conn
#    rs = conn.get_all_buckets()
#    print rs
    #print len(rs)
    
    #bucket = conn.create_bucket("as.myupdate.zywall.zyxel.com") #, location=s3.connection.Location.DEFAULT)
    bucket = Bucket(conn, 'as.myupdate.zywall.zyxel.com')
    #bucket = conn.get_bucket('as.myupdate.zywall.zyxel.com')
    
    #print 'ok'
    #f = "E:/temp/2806.sig"
    f = "E:/temp/test.zip"
    print 'File upload: %s to Otto %s' % (f, bucket)
    
#    def progress(complete, total):
#        print "complete: %s from % bytes" % (complete, total)
    
    k = Key(bucket)
    #k.key = 'test/2806.sig'
    k.key = 'test/test.zip'
    k.set_contents_from_filename(f, policy='public-read')
    #k.key = 'foobar'
    #k.set_contents_from_string('This is a test of S3')
    #print k.get_contents_as_string()
    pass