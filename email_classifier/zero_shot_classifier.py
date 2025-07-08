import os,sys
from transformers import pipeline
from email_reader.get_today_email import get_todays_mail, clean_up
from pprint import pprint





# Correct model name
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")


# Define candidate tags
candidate_labels = ["business", "study", "advertisement", "important", "social"]

def classify_mails():
    mail_dict = get_todays_mail()
    mail_tags = {}
    list_content = []
    subjects = []

    
    for mailbox_name in mail_dict:
        email_list = mail_dict[mailbox_name]
        for email in email_list:
            if 'Body' in email:
                content = f"Subject: {email['Subject']}, Body: {email['Body']}"
                list_content.append(content)
                subjects.append(email['Subject']) 


    results = classifier(list_content, candidate_labels=candidate_labels, batch_size=4)

    
    for subject, result in zip(subjects, results):
        predicted_label = result['labels'][0]
        mail_tags[subject] = predicted_label

    return mail_tags


mail_tags = classify_mails()
pprint(mail_tags)
