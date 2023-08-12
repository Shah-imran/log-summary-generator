import paramiko
import os
import pandas as pd
from datetime import datetime
import sys  # Make sure sys is imported
import traceback
import config

from parsing import extract_download_errors, extract_mark_target_errors, extract_send_campaign, extract_sent_emails

def download_file(server_ip, server_port, username, password, remote_file_path, local_file_path):
    transport = paramiko.Transport((server_ip, server_port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.get(remote_file_path, local_file_path)

    sftp.close()
    transport.close()

folder_name = "Output" + datetime.now().strftime("%Y-%m-%d %H-%M-%S")
os.makedirs(folder_name, exist_ok=True)

data = pd.read_excel('Gmonster SSH Access.xlsx')

for index, row in data.iterrows():
    gmonster_instance = row['Gmonster Instance']
    ip_address = row['IP Address']
    username = row['User Name']
    password = row['Password']

    local_file_path = os.path.join(folder_name, gmonster_instance, 'logfile.log')
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    try:
        print(f"Starting downloading {index+1}/{len(data)}: {ip_address} {gmonster_instance}")
        download_file(ip_address, 22, username, password, config.REMOTE_APP_PATH, local_file_path)
    except:
        print(f"Error: {traceback.format_exc()}")

all_download_errors = []
all_send_campaign = []
all_sent_emails = []
all_mark_target_errors = []

print(f"\nLog files downloaded and saved in '{folder_name}' directory.")

for index, row in data.iterrows():
    local_file_path = os.path.join(folder_name, gmonster_instance, 'logfile.log')

    with open(local_file_path, "r") as logfile:
        log_data = logfile.read()
    
    print(f"\nParsing Started for '{local_file_path}' directory.")
    
    all_download_errors.extend(extract_download_errors(gmonster_instance, log_data))
    all_send_campaign.extend(extract_send_campaign(gmonster_instance, log_data))
    all_sent_emails.extend(extract_sent_emails(gmonster_instance, log_data))
    all_mark_target_errors.extend(extract_mark_target_errors(gmonster_instance, log_data))

    print(f"\nParsing Ended for '{local_file_path}' directory.")

download_errors_df = pd.DataFrame(all_download_errors)
download_errors_df.to_excel(os.path.join(folder_name, 'Download_Errors.xlsx'), index=False)

send_campaign_df = pd.DataFrame(all_send_campaign)
send_campaign_df.to_excel(os.path.join(folder_name, 'Send_Campaign.xlsx'), index=False)

sent_emails_df = pd.DataFrame(all_sent_emails)
sent_emails_df.to_excel(os.path.join(folder_name, 'Sent_Emails.xlsx'), index=False)

mark_target_errors_df = pd.DataFrame(all_mark_target_errors)
mark_target_errors_df.to_excel(os.path.join(folder_name, 'Mark_Target_Errors.xlsx'), index=False)

print(f"\nDownloading and Parsing done.")
