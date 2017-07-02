'''
Created on 2012-4-25

@author: Simon
'''


def sendMail(content='test mail'):    
    # Import smtplib for the actual sending function
    import smtplib
    
    # Import the email modules we'll need
    from email.mime.text import MIMEText
    
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    # Create a text/plain message
    msg = MIMEText(content)
    
    
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Securities price notification mail'
    msg['From'] = 'smartman2014@qq.com'
    msg['To'] = 'smartman2014@qq.com'

    
    s = smtplib.SMTP('smtp.qq.com')
    s.login('smartman2014','xxx_2000')
    s.sendmail('smartman2014@qq.com', 'smartman2014@qq.com', msg.as_string())
    s.quit()
    print('send out mail notification')

if __name__ == '__main__':
    sendMail()


