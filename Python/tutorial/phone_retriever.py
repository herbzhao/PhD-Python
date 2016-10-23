'''  But if you had a program that could search the text in your clipboard for phone numbers
and email addresses, you could simply press CTRL-A to select all the text,
press CTRL-C to copy it to the clipboard, and then run your program.'''

import re

#first create a string contained copied lines
clipboard = '''
Programme Manager for Winton Programme

Email: nlp28@cam.ac.uk
Office Phone: 01223 337073
mobiel phone: +44 (0)7856684084
another mobile:  0044 07856-684-084
Download as vCard
Biography:

Bachelor (1998) in Physics from Imperial College, PhD in semiconductor physics on the fabrication and science of low dimensional structures in the group of Prof Mike Pepper at the Cavendish Laboratory, Cambridge (1991). In 2003 he also completed his MBA at Warwick University and has authored over 50 papers and holds over 20 patents.

Work Experience: After completing his Ph.D., Nalin joined Toshiba working in Japan at the R&D Center. After a year in Japan, he returned to Cambridge to join the Toshiba Cambridge Research Laboratory, where he worked on a number of areas related to semiconductor device physics and hybrid magnetic semiconductor systems. Nalin (tz275@cam.ac.uk) joined Cambridge Display Technology (CDT) a spin-out form the University of Cambridge in 2001. During his time at CDT he worked in a number of areas from device research, business development to project management. He returned to the Cavendish laboratory in August 2011 to take up the role of Programme Manager for the Winton Programme.

'''
#01223 337073
#Create 2 regex to match mobile phone and email addresses
# phone regex match

phone_reg_string = r'''
(\+ \d{2} | 0{2}\d{2})?                #country code +44 | 0044
\s                       # space
(0|\(0\))                       #first zero 0 | (0)
(\d+)
-?\s?
(\d+)?
-?\s?
(\d+)?                      #phone numbers
-?\s?
(\d+)? 
'''

phone_reg = re.compile(phone_reg_string,re.VERBOSE)
phone_result = phone_reg.findall(clipboard)


#email match nlp28@cam.ac.uk
email_reg_string = r'''
(\w+)               #address
(@)
([a-zA-Z0-9\.]+)                #domain
'''

email_reg = re.compile(email_reg_string,re.VERBOSE)
email_result= email_reg.findall(clipboard)

# format and  print 2 all matched results
for i in range(len(phone_result)):
    phone= ''.join(list(phone_result[i]))
    phone = re.sub('\+','00',phone)
    phone = re.sub('[\(\)]','',phone)
    print('phone:', phone)
    re.findall()
    re.search()
    re.sub()

    
for i in range(len(email_result)):
    email= ''.join(list(email_result[i]))
    print('email:', email)

    

# show error when there is no phone/email
