'''
Created on 2012-4-25

@author: Simon
'''
def sendMail():    
    # Import smtplib for the actual sending function
    import smtplib
    
    # Import the email modules we'll need
    from email.mime.text import MIMEText
    
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    # Create a text/plain message
    msg = MIMEText('test mail')
    
    
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'The contents test mail from python'
    msg['From'] = 'nms.bm@zyxel.com.tw'
    msg['To'] = 'simon.wang@mitrastar.cn'
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    #s = smtplib.SMTP('wxmail.zyxel.cn')
    #s.login('R00053','w00260')
    #s.sendmail('simon.wang@mitrastar.cn', 'simon.wang@mitrastar.cn', msg.as_string())
    #s.quit()
    
    s = smtplib.SMTP('mail.zyxel.com.tw')
    s.set_debuglevel(1)
    s.starttls()
    s.ehlo()
    s.login('nms.bm@zyxel.com.tw','esbusdd4nmsbm')    
    s.sendmail('nms.bm@zyxel.com.tw', 'simon.wang@mitrastar.cn', msg.as_string())
    s.quit()
    print 'send out mail notification'

if __name__ == '__main__':
    sendMail()

