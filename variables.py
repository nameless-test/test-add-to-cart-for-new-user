import random
import string
import time
from datetime import datetime

timestamp = int(time.time())
first_name = 'Test'
last_name = 'User' + ''.join(random.choices(string.ascii_letters, k=4))
e_mail = f'test_email{timestamp}@gmail.com'
password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
birthdate = datetime.today().strftime('%m/%d/%Y')
registration_data = {'first_name': first_name,
       'last_name': last_name,
       'e_mail': e_mail,
       'password': password,
       'birthday': birthdate}
item = 'The adventure begins Framed...'