import os
import pandas as pd

from agents.error_detector import log_error_detector
from agents.summarize_agent import summarize_agent
from agents.mail_agent import send_mail
from workflow.ev_workflow import error_workflow
from logsfile_generator import save_logs_files
from scheduler import start_scheduler

def main():
    start_scheduler()
    input_file = "Charger_Logs_10.xlsx"

    # Read Excel file
    df1 = pd.read_excel(input_file)

    print(f"Total logs: {len(df1)}")
    print("Starting log analysis...\n")

    for _, row in df1.iterrows():

        timestamp = row["Date Time"]
        response_type = row["Response Type"]
        response_json = row["Response Json"]

        # Detect error
        result = log_error_detector(
            response_type,
            response_json
        )

        if result == "ERROR":

            print(f"ERROR DETECTED | {timestamp}")

            # Send complete log to LangGraph
            workflow_result = error_workflow.invoke({
                "timestamp": str(timestamp),
                "response_type": str(response_type),
                "response_json": str(response_json)
            })

            print(workflow_result["error_summary"])
            print(workflow_result["mail_result"])

            # Save ONLY confirmed errors
            save_logs_files(
                "error",
                response_type,
                response_json
            )
        else:

            save_logs_files(
                "normal",
                response_type,
                response_json
            )

    print("\n✅ Log processing completed.")



if __name__ == "__main__":
    main()