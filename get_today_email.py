from email_reader import MailReader
from pprint import pprint
from datetime import datetime,timedelta
import shutil
import os
def remove_directory(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        print(f"Removed directory: {dir_path}")
    else:
        print(f"Directory does not exist: {dir_path}")

def get_todays_date():
    return datetime.today().strftime('%d-%b-%Y')
def get_yesterday_date():
    return (datetime.today()-timedelta(days=1)).strftime('%d-%b-%Y')

def get_todays_mail():
    mailReader=MailReader()
    mailReader.create_imap_connector()
    mailReader.imap_connector_login()
    return mailReader.read_all_mailboxes(get_yesterday_date(),get_todays_date())

def clean_up(Mail_Dict):
    for mailbox in Mail_Dict:
        for email in Mail_Dict[mailbox]:
            print(email.keys())
            if 'Attachment_directory' in email:
                print(email['Attachment_directory'])
                remove_directory(email['Attachment_directory'])





"""
Mail_Dict=get_todays_mail()
for name in Mail_Dict:
    print("="*200)
    print(f"Mailbox :{name}")
    print("="*200)
    email_list=Mail_Dict[name]
    for a in email_list:
        if(a):
            print("-"*20)
            #print(a.keys())
            print(a['Subject'])
            if 'Body' in a:
                print(a['Body'])
            
            print("-"*100)
    print("="*200)

clean_up(Mail_Dict)
"""