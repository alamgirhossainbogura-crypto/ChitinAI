import os
import requests
import json

class IncidentNotifier:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_postmortem(self, incident_id: str, failure_type: str, model_used: str, fix_summary: str):
        if not self.webhook_url:
            print("⚠️ No Webhook URL set. Skipping notification.")
            return

        payload = {
            "text": f"🚨 *ChitinAI Incident Postmortem Report* [{incident_id}]\n"
                    f"• *Failure Category:* {failure_type}\n"
                    f"• *Routed Engine:* `{model_used}`\n"
                    f"• *Status:* AUTO-HEALED & PATCHED\n\n"
                    f"*Patch Summary:*\n```{fix_summary}```"
        }

        try:
            requests.post(self.webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
            print("✅ Postmortem alert dispatched to Slack/Discord.")
        except Exception as e:
            print(f"❌ Failed to send alert: {e}")
