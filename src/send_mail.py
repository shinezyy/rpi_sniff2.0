import smtplib,mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

sender      = 'diamondzyy@sina.cn'

msg = MIMEMultipart()
msg['From']     = "diamondzyy@sina.cn"
msg['To']       = "1058149101@qq.com"
msg['Subject']  = "ip_info"

with open('/home/pi/rpi_sniff2.0/mac_addrs.txt') as f:
    msg.attach(MIMEText(f.read()))

smtp = smtplib.SMTP()
smtp.connect('smtp.sina.com','25')
smtp.login(sender,'9035570095')
smtp.sendmail(sender,sender,msg.as_string())
smtp.quit()
print "sent"
