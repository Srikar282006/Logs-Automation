import csv
import json
from datetime import datetime
import os

def save_logs_files(logs_type,response_type,response_json):
    timestamp= datetime.now().strftime("%d %b %Y %H:%M:%S")
    folder = f"logs_data/{logs_type}"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{logs_type}_logs.csv"
    with open(filename,"a",newline="",encoding="utf-8") as file:
        writer=csv.writer(file)
        if file.tell()==0:
            writer.writerow([
                "timestamp",
                "Response_type",
                "Response_json"
            ])
        writer.writerow([
                timestamp,
                response_type,
                response_json
            ])
    return f"logs_data/{logs_type}/{logs_type}_logs.csv"
