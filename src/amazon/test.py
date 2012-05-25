'''
Created on 2012-5-9

@author: Simon
'''

if __name__ == '__main__':
    import boto
    from boto import s3
    import sys
    from boto.s3.key import Key
    from boto.s3.connection import OrdinaryCallingFormat
    from boto.s3.connection import SubdomainCallingFormat
    
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    
    conn = boto.connect_s3('test1', 'password1',
            host="172.25.21.78", port=10001, is_secure=False,calling_format=OrdinaryCallingFormat())
    print conn
    rs = conn.get_all_buckets()
    print rs
    print len(rs)
    
    bucket = conn.create_bucket("test") #, location=s3.connection.Location.DEFAULT)
    
    print 'ok'
    f = "E:/temp/1.848.sig"
    print 'File upload: %s to Otto %s' % (f, bucket)
    
    def progress(complete, total):
        print "complete: %s from % bytes" % (complete, total)
    
    k = Key(bucket)
    k.key = 'updateserver/signaturefiles/ZYNOS.LITE/AVIDP/1.848.sig'
    k.set_contents_from_filename(f)
    pass