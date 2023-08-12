import re
from pprint import pprint

# with open('logfile.log', 'r') as file:
#     log_data = file.read()

# print(log_data[:1000])


def extract_download_errors(log_data):
    pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
               r" .*? Error at (downloading email|Sending) - ([\w.+-]+@[\w-]+\.[a-z]{2,4}).*?"
               r"(imaplib\.IMAP4\.error: b'\[ALERT\] Please log in via your web browser: https:\/\/support\.google\.com\/mail\/accounts\/answer\/78754 \(Failure\)'"
               r"|socket\.timeout: timed out"
               r"|socks\.GeneralProxyError: Socket error: timed out"
               r"|imaplib\.IMAP4\.error: b'\[AUTHENTICATIONFAILED\] Invalid credentials \(Failure\)'"
               r"|socket\.timeout: The read operation timed out"
               r"|smtplib\.SMTPAuthenticationError: \(534,.*?\)"
               r")")

    matches = re.findall(pattern, log_data, re.DOTALL)

    error_list = []
    for match in matches:
        error_dict = {
            "Datetime": match[0],
            "Error Category": match[1],
            "Email Address": match[2],
            "Error Message": match[3]
        }
        error_list.append(error_dict)

    return error_list


def extract_send_campaign(log_data):
    pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
               r".*?Starting (\w+ Campaign) :"
               r"\s*Target Removal - (\w+)"
               r"\s*Group Selected: (.*?)"
               r"\s*Webhook Enabled: (\w+)"
               r"\s*Email Block Check: (\w+)"
               r"\s*Emails Per Account: (\d+)"
               r"\s*Len of Group: (\d+)"
               r"\s*Len of Targets: (\d+)"
               r"\s*Delay: (\d+ - \d+)"
               r"\s*Campaign ID: ([a-f0-9\-]+)"
               r"\s*Add Custom Hostname: (\w+)")
    
    matches = re.findall(pattern, log_data, re.DOTALL)

    campaign_list = []
    for match in matches:
        campaign_dict = {
            "Datetime": match[0],
            "Category": match[1],
            "Target Removal": match[2],
            "Group Selected": match[3],
            "Webhook Enabled": match[4],
            "Email Block Check": match[5],
            "Emails Per Account": match[6],
            "Len of Group": match[7],
            "Len of Targets": match[8],
            "Delay": match[9],
            "Campaign ID": match[10],
            "Add Custom Hostname": match[11]
        }
        campaign_list.append(campaign_dict)

    return campaign_list


def extract_sent_emails(log_data):
    pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
               r".*?Sent - ([\w.+-]+@[\w-]+\.[a-z]{2,4})"
               r" ([\w.+-]+@[\w-]+\.[a-z]{2,4})")
    
    matches = re.findall(pattern, log_data, re.DOTALL)
    
    sent_list = []
    for match in matches:
        sent_dict = {
            "Datetime": match[0],
            "Sender": match[1],
            "Receiver": match[2]
        }
        sent_list.append(sent_dict)
        
    return sent_list


def extract_mark_target_errors(log_data):
    pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
               r".*?Error at (MarkTargetSentAirtable) : Traceback"
               r"(.*?requests\.exceptions\.HTTPError:.*?)"  # Making this non-greedy with .*?
               r"(?=\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}|\Z)")

    matches = re.findall(pattern, log_data, re.DOTALL)

    error_list = []
    for match in matches:
        error_dict = {
            "Datetime": match[0],
            "Error Category": match[1],
            "Error Message": match[2].strip().replace("\\'", "'")  # strip() removes leading/trailing whitespace
        }
        error_list.append(error_dict)
        
    return error_list


if __name__=="__main__":
    from test import log_data
    pprint(extract_download_errors(log_data))
    pprint(extract_send_campaign(log_data))
    pprint(extract_sent_emails(log_data))
    pprint(extract_mark_target_errors(log_data))
