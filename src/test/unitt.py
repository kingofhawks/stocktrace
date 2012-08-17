'''
Created on 2012-6-8

@author: Simon
'''
import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)
            
    def test_wmi(self):
        import wmi
        c = wmi.WMI()
        for os in c.Win32_OperatingSystem():
          print os.Caption
          
    def test_form_login(self):
        import mechanize
        b = mechanize.Browser()
        b.open('http://172.25.21.101/admin')
        form = b.forms().next()  # the login form is unnamed...
        form.action='http://172.25.21.101/admin/login'
        print form.action        # prints "https://login.us.site.com"
        form['USERNAME'] = "simon.wang"
        form['PASSWORD'] = "123456"
        b.form = form
        response = b.submit()
        print response.get_data()
        
#    def test_form_login2(self):
#        import urllib,httplib
#        data = urllib.urlencode({'USERNAME': 'simon.wang','PASSWORD':'123456'})
#
#        h = httplib.HTTPConnection('172.25.21.101:80')
#        
#        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#        
#        h.request('POST', '/admin/login', data, headers)
#        
#        r = h.getresponse()
#        
#        print r.read()
            

#if __name__ == '__main__':
#    unittest.main()