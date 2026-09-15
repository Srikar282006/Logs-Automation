import json

from workflow.ev_workflow import error_workflow
from logsfile_generator import save_logs_files


def log_error_detector(response_type, response_json):

    try:
        data = json.loads(response_json)

    except (json.JSONDecodeError, TypeError):

        save_logs_files(
            "normal",
            response_type,
            response_json
        )

        return "NORMAL"

    if not isinstance(data, list) or len(data) < 4:

        save_logs_files(
            "normal",
            response_type,
            response_json
        )

        return "NORMAL"

    action = data[2]
    payload = data[3]

    if action == "StatusNotification":

        error_code = payload.get("errorCode")

        if error_code and error_code != "NoError":

            print(
                f"🚨 ERROR DETECTED: {error_code}"
            )

            workflow_result = error_workflow.invoke({
                "timestamp": str(
                    payload.get("timestamp")
                ),
                "response_type": str(
                    response_type
                ),
                "response_json": str(
                    response_json
                )
            })

            print(
                f"Severity: {workflow_result['significance']}"
            )

            if "mail_result" in workflow_result:
                print(
                    workflow_result["mail_result"]
                )

            save_logs_files(
                "error",
                response_type,
                response_json
            )

            return "ERROR"

    save_logs_files(
        "normal",
        response_type,
        response_json
    )

    return "NORMAL"