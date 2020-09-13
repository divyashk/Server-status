import os
import re
import datetime

datetime_now = datetime.datetime.now()
month = datetime_now.strftime("%b")
day = datetime_now.strftime("%d")

import os


with open('services-report', 'w') as f_write:
  






# reading from /var/log/syslogs
with open('/var/log/syslog', 'r', encoding='utf-8') as read_file:
    lines = read_file.readlines()
    with open('syslog-report', 'w') as f_write:
      f_write.write("Important SYSLOGS till {}\n\n".format(datetime_now.strftime("%c")))
      f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format("Day","Month","Time","Logger","Application","Message"))
      
      for line in lines:
          pattern_dist = re.compile(r'(?P<month>[A-Z][a-zA-Z][a-zA-Z])\s(?P<day>\d\d)\s(?P<time>\d\d:\d\d:\d\d)\s(?P<logger>[^\s]*\s)(?P<application>[^\s]*\s)(?P<message>.*)')
          pattern_failed  = re.compile(r'(failed|error|could\'nt|denied)',re.IGNORECASE)
          if pattern_failed.search(line)!= None:
            
            obj_grps = pattern_dist.search(line);
            
            if obj_grps.group('day') == day and obj_grps.group('month') == month:
              f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format(obj_grps.group("day"),obj_grps.group("month"),obj_grps.group("time"),obj_grps.group("logger"),obj_grps.group("application"),obj_grps.group("message")))
      f_write.close()
      
# reading from /var/log/auth.log
with open('/home/dk/Desktop/auth.log', 'r', encoding='utf-8') as read_file:
    lines = read_file.readlines()
    with open('authlog-report', 'w') as f_write:
      f_write.write("Important AUTHLOGS till {}\n\n".format(datetime_now.strftime("%c")))
      
      f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format("Day","Month","Time","Logger","Application","Message"))
      for line in lines:
          pattern_dist = re.compile(r'(?P<month>[A-Z][a-zA-Z][a-zA-Z])\s(?P<day>\d\d)\s(?P<time>\d\d:\d\d:\d\d)\s(?P<logger>[^\s]*\s)(?P<application>[^\s]*\s)(?P<message>.*)')
          pattern_failed  = re.compile(r'(root|succeded|locked|unlocked|failed|error|denied|could\'nt|fatal)',re.IGNORECASE)
          if pattern_failed.search(line)!= None:
            
            obj_grps = pattern_dist.search(line);
            
            if obj_grps.group('day') == day and obj_grps.group('month') == month:
              f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format(obj_grps.group("day"),obj_grps.group("month"),obj_grps.group("time"),obj_grps.group("logger"),obj_grps.group("application"),obj_grps.group("message")))
      f_write.close()

#reading from /var/log/faillog
with open('/var/log/faillog', 'r', encoding='utf-8') as read_file:
    lines = read_file.readlines()
    with open('faillog-report', 'w') as f_write:
      f_write.write("Important AUTHLOGS till {}\n\n".format(datetime_now.strftime("%c")))
      
      f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format("Day","Month","Time","Logger","Application","Message"))
      for line in lines:
          pattern_dist = re.compile(r'(?P<month>[A-Z][a-zA-Z][a-zA-Z])\s(?P<day>\d\d)\s(?P<time>\d\d:\d\d:\d\d)\s(?P<logger>[^\s]*\s)(?P<application>[^\s]*\s)(?P<message>.*)')
          pattern_failed  = re.compile(r'(ssh|22|pam\|unix|failed|error|denied|could\'nt|fatal)',re.IGNORECASE)
          if pattern_failed.search(line)!= None:
            
            obj_grps = pattern_dist.search(line);
            
            if obj_grps.group('day') == day and obj_grps.group('month') == month:
              f_write.write('{0:2}\t{1:4}\t{2:10}\t{3:15}\t{4:25}\t{5:50}\n\n'.format(obj_grps.group("day"),obj_grps.group("month"),obj_grps.group("time"),obj_grps.group("logger"),obj_grps.group("application"),obj_grps.group("message")))
      f_write.close()
      
      