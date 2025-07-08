import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from dotenv import load_dotenv
from my_exceptions import IMAP_CONNECTOR_FAIL_EXCEPTION,MAIL_READ_FAILED_EXCEPTION

import re

load_dotenv()

class MailReader:
    ##I am leaving this inside init itself and not to be passed as paramenter for safety,ie.this module must be configured like this
    def __init__(self):
        self.username=os.getenv("EMAIL_USERNAME")
        self.password=os.getenv("EMAIL_APP_PASSWORD")
        self.imap_server=os.getenv("EMAIL_SERVER")
    
    def create_imap_connector(self):
        try:
            self.imap_connector=imaplib.IMAP4_SSL(self.imap_server)
        except  Exception as e:
            raise IMAP_CONNECTOR_FAIL_EXCEPTION(f"imap_connector failed:{str(e)}")
    
    def imap_connector_login(self):
        try:
            self.imap_connector.login(self.username,self.password)
        except Exception as e:
            raise IMAP_CONNECTOR_FAIL_EXCEPTION(f"imap login failed:{str(e)}")
    
    def list_mailboxes(self):
        typ,data=self.imap_connector.list()
        mailboxes=self.parse_mailboxes(data)
        mailbox_names=self.get_mailbox_names(mailboxes)
        return {'status_code':typ,'mail_box_list':mailboxes,'mailbox_names':mailbox_names}

    def parse_mailboxes(self,mailbox_list):
        mailboxes = []

        for mbox in mailbox_list:
            decoded = mbox.decode()  
            match = re.match(r'\((.*?)\)\s+"(.*?)"\s+"(.*?)"', decoded)
            if match:
                attributes, delimiter, name = match.groups()
                attr_list = attributes.strip().split()
                mailboxes.append({
                    'name': name,
                    'delimiter': delimiter,
                    'attributes': attr_list
                })
        return mailboxes
    def get_mailbox_names(self,mailboxes):
        names=[]
        for mbox in mailboxes:
            names.append(mbox['name'])
        return names
    def clean(self,text):
        return "".join(c if c.isalnum() else "_" for c in text)

    def read_mails_by_date(self,mailbox,date_from,date_to):
        if " " in mailbox or "/" in mailbox or "[" in mailbox:
            mailbox = f'"{mailbox}"'
        self.imap_connector.select(mailbox)  ##First step is to select a mailbox
        search_criteria=f'(SINCE "{date_from}" BEFORE "{date_to}")'
        typ,msg_idx=self.imap_connector.search(None,search_criteria)
        ##here i will store the list of emails
        email_list=[]
        if typ !='OK':
            raise MAIL_READ_FAILED_EXCEPTION(f'Failed to read from mailbox :{mailbox}')
        else:
            for num in msg_idx[0].split():

                typ,msg_data=self.imap_connector.fetch(num,"(RFC822)")
                for response in msg_data:
                    message_dict={}
                    if isinstance(response,tuple):
                        msg=email.message_from_bytes(response[1])
                        ##Decoding the subject
                        subject,encoding=decode_header(msg["Subject"])[0]
                   
                        if isinstance(subject,bytes) and encoding:
                            subject=subject.decode(encoding)
                            
                        message_dict["Subject"]=subject
                        ##Decoding sender
                        From,encoding=decode_header(msg["From"])[0]
                        if isinstance(From,bytes) and encoding:
                            From=From.decode(encoding)
                            
                        message_dict["From"]=From
                        if msg.is_multipart():

                            for part in msg.walk():
                                content_type=part.get_content_type()
                                content_disposition=str(part.get("Content-Disposition"))
                                try:
                                    body=part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type=="text/plain" and "attachment" not in content_disposition:
                                    message_dict["Body"]=body  ##here you get the content body
                                elif "attachment" in content_disposition:
                                    filename=part.get_filename()
                                    if filename:
                                        folder_name=self.clean(subject)
                                        if not os.path.isdir(folder_name):
                                            os.mkdir(folder_name)
                                        filepath=os.path.join(folder_name,filename)

                                        open(filepath,"wb").write(part.get_payload(decode=True))
                                        message_dict["Attachment_multipart"]=filepath
                                        message_dict["Attachment_directory"]=folder_name
                        else:
                            content_type=msg.get_content_type()
                            body=msg.get_payload(decode=True).decode()
                            if(content_type=="text/plain"):
                                message_dict["Body"]=body

                            if(content_type=="text/html"):
                                folder_name=self.clean(subject)
                                if not os.path.isdir(folder_name):
                                    os.mkdir(folder_name)
                                filename="temp.html"
                                filepath=os.path.join(folder_name,filename)
                                open(filepath,'w').write(body)
                                message_dict["Attachment_webbrowser"]=filepath
                                message_dict["Attachment_directory"]=folder_name
                                ##Later use this to open any such files webbrowser.open(filepath)
                    email_list.append(message_dict)

        return email_list
    def read_all_mailboxes(self,from_date,to_date):
        lst=self.list_mailboxes()
        name_lst=lst['mailbox_names']
        attributes=lst['mail_box_list']


        Mail_Dict={}
        for i in range(len(name_lst)):
            name=name_lst[i]
            attribute=attributes[i]['attributes']
            if('\\Noselect' in attribute):
                continue
            print(name)
            email_list=self.read_mails_by_date(name,from_date,to_date)
            Mail_Dict[name]=email_list
        return Mail_Dict


