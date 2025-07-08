from transformers import pipeline
from get_today_email import get_todays_mail, clean_up
from pprint import pprint

# Correct model name
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define candidate tags
candidate_labels = ["business", "study", "advertisement", "important", "social"]

def classify_mails():
    mail_dict = get_todays_mail()
    mail_tags = {}

    for mailbox_name in mail_dict:
        email_list = mail_dict[mailbox_name]
        for email in email_list:
            if 'Body' in email:
                content = f"Subject: {email['Subject']}, Body: {email['Body']}"
                result = classifier(content, candidate_labels)
                predicted_label = result['labels'][0]
                mail_tags[email['Subject']] = predicted_label

    return mail_tags

mail_tags = classify_mails()
pprint(mail_tags)
