import os
import re
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# storing the present time and date
datetime_now = datetime.datetime.now()
month = datetime_now.strftime("%b")
day = datetime_now.strftime("%d")
year = datetime_now.strftime("%Y")
date_comp = day+"/"+month+"/"+year

# configuring email

email_send = os.environ.get('SEND_EMAIL')                                     # you need create environment variable with the same name on your machine to store the sender, receiver and password.
email_user = os.environ.get('MY_EMAIL')
email_password = os.environ.get('MY_PASSWORD')

subject = 'Daily server report'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'Please find the attached copies of your server reports'
msg.attach(MIMEText(body,'plain'))


#################################### CHECKING THE STATUS OF SPECIFIC SERVICES ##############################################################################################
service_exist_count = 0;
lis_services = ["app", "cron", "sshd"]              # You can add and remove service here.
for serv in lis_services:
  if os.path.exists("/lib/systemd/system/"+serv+".service"):
    service_exist_count += 1;
    
    # opening the file to write
    with open('services-status','a') as f_write:              
      
      if service_exist_count == 1:
        os.system('service {} status > services-status'.format(serv))
      else:
        os.system('service {} status >> services-status'.format(serv))
      f_write.write("\n\n\n")

  else:
    print("Service {} doesn't exist".format(serv));

#attaching the generated file to mail
if service_exist_count > 0:
  filename='services-status'
  attachment  =open(filename,'rb')
  part = MIMEBase('application','octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition',"attachment; filename= "+filename)
  msg.attach(part)

################################################ NOW READING LOGS ###########################################################################################


# NOTE - this part will run only if you are using Nginx instead of Apache

# creating nginx-access file report 
if os.path.exists('/var/log/nginx/access.log'):
  with open('/var/log/nginx/access.log', 'r', encoding='utf-8') as read_file:
      lines = read_file.readlines()
      with open('nginx-access-report', 'w') as f_write:
        f_write.write("Important HTTP\HTTPS access till {}\n\n".format(datetime_now.strftime("%c")))
        f_write.write('{0:5}\t{1:28}\t{2:20}\t{3:10}\t{4:20}\t{5:50}\n\n'.format("Status","Request","IP","Time","Date","Detail"))
        
        for line in lines:
            pattern_dist = re.compile(r'(?P<ip>^\w*.\w*.\w*.\w*\s)-\s-\s\[(?P<date>[^\s^:]*):(?P<time>[^\s]*\s)[^\s]* \"(?P<req>[^\"]*)\" (?P<status>\w*\s)(?P<details>.*\s)')
            obj_grps = pattern_dist.search(line);
        
            if obj_grps.group('date') == date_comp:
              req_str = obj_grps.group("req");
              f_write.write('{0:5}\t{1:28}\t{2:20}\t{3:10}\t{4:20}\t{5:50}\n\n'.format(obj_grps.group("status"),obj_grps.group("req"),obj_grps.group("ip"),obj_grps.group("time"),obj_grps.group("date"),obj_grps.group("details")))
      
      f_write.close()

  # attaching the generated file to the mail
  filename='nginx-access-report'
  attachment  =open(filename,'rb')
  part = MIMEBase('application','octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition',"attachment; filename= "+filename)
  msg.attach(part)
else:
  print("Nginx log files not found, so moving on...")


# creating from /var/log/syslogs
if os.path.exists('/var/log/syslog'):
  with open('/var/log/syslog', 'r', encoding='utf-8') as read_file:
      lines = read_file.readlines()
      with open('syslog-report', 'w') as f_write:
        f_write.write("Important SYSLOGS till {}\n\n".format(datetime_now.strftime("%c")))
        f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format("Day","Month","Time","Logger","Application","Message"))
        
        for line in lines:
            pattern_dist = re.compile(r'(?P<month>[A-Z][a-zA-Z][a-zA-Z])\s(?P<day>\d\d)\s(?P<time>\d\d:\d\d:\d\d)\s(?P<logger>[^\s]*\s)(?P<application>[^\s]*\s)(?P<message>.*)')
            pattern_filter  = re.compile(r'(failed|error|could\'nt|denied)',re.IGNORECASE)
            if pattern_filter.search(line)!= None:
              
              obj_grps = pattern_dist.search(line);
              
              if obj_grps.group('day') == day and obj_grps.group('month') == month:
                f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format(obj_grps.group("day"),obj_grps.group("month"),obj_grps.group("time"),obj_grps.group("logger"),obj_grps.group("application"),obj_grps.group("message")))
        f_write.close()
  # attaching the generated file to the mail
  filename='syslog-report'
  attachment  =open(filename,'rb')
  part = MIMEBase('application','octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition',"attachment; filename= "+filename)
  msg.attach(part)
else:
  print("Syslog files not found, so moving on...")
  
        

# reading from /var/log/auth.log
if os.path.exists('/var/log/auth.log'):
  with open('/var/log/auth.log', 'r', encoding='utf-8') as read_file:
      lines = read_file.readlines()
      with open('authlog-report', 'w') as f_write:
        f_write.write("Important AUTHLOGS till {}\n\n".format(datetime_now.strftime("%c")))
        
        f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format("Day","Month","Time","Logger","Application","Message"))
        for line in lines:
            pattern_dist = re.compile(r'(?P<month>[A-Z][a-zA-Z][a-zA-Z])\s(?P<day>\d\d)\s(?P<time>\d\d:\d\d:\d\d)\s(?P<logger>[^\s]*\s)(?P<application>[^\s]*\s)(?P<message>.*)')
            pattern_filter  = re.compile(r'(root|succeded|locked|unlocked|failed|error|denied|could\'nt|fatal)',re.IGNORECASE)
            if pattern_filter.search(line)!= None:
              
              obj_grps = pattern_dist.search(line);
              
              if obj_grps.group('day') == day and obj_grps.group('month') == month:
                f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format(obj_grps.group("day"),obj_grps.group("month"),obj_grps.group("time"),obj_grps.group("logger"),obj_grps.group("application"),obj_grps.group("message")))
      f_write.close()

  # attaching the generated file to the mail
  filename='authlog-report'
  attachment  =open(filename,'rb')
  part = MIMEBase('application','octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition',"attachment; filename= "+filename)
  msg.attach(part)


else:
     print("Auth log files not found, so moving on...")



#reading from /var/log/faillog
if os.path.exists('/var/log/faillog'):
  with open('/var/log/faillog', 'r', encoding='utf-8') as read_file:
      lines = read_file.readlines()
      with open('faillog-report', 'w') as f_write:
        f_write.write("Important AUTHLOGS till {}\n\n".format(datetime_now.strftime("%c")))
        
        f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format("Day","Month","Time","Logger","Application","Message"))
        for line in lines:
            pattern_dist = re.compile(r'(?P<month>[A-Z][a-zA-Z][a-zA-Z])\s(?P<day>\d\d)\s(?P<time>\d\d:\d\d:\d\d)\s(?P<logger>[^\s]*\s)(?P<application>[^\s]*\s)(?P<message>.*)')
            pattern_filter  = re.compile(r'(ssh|22|pam\|unix|failed|error|denied|could\'nt|fatal)',re.IGNORECASE)
            if pattern_filter.search(line)!= None:
              
              obj_grps = pattern_dist.search(line);
              
              if obj_grps.group('day') == day and obj_grps.group('month') == month:
                f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format(obj_grps.group("day"),obj_grps.group("month"),obj_grps.group("time"),obj_grps.group("logger"),obj_grps.group("application"),obj_grps.group("message")))
        f_write.close()
  # attaching the generated file to the mail
  filename='faillog-report'
  attachment  =open(filename,'rb')
  part = MIMEBase('application','octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition',"attachment; filename= "+filename)
  msg.attach(part)
else:
  print("Faillog file not found, so moving on...")

    
##################################################### SENDING THE MAIL #######################################################################

text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)
server.sendmail(email_user,email_send,text)
server.quit()

print("\n\nMAIL SENT TO {}".format(email_send))
