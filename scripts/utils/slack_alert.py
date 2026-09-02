import json
import requests
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.config import Config
from scripts.utils.logger import get_logger

logger = get_logger("slack_alert")

def send_slack_arbitrage_alert(alert_data: dict) -> bool:
    """
    Sends a formatted Slack Block Kit alert when an at-risk container or profitable reroute is detected.
    """
    webhook_url = Config.SLACK_WEBHOOK_URL
    container_id = alert_data.get("container_id", "UNKNOWN")
    commodity = alert_data.get("commodity", "N/A")
    risk_level = alert_data.get("risk_level", "UNKNOWN")
    time_to_spoilage = alert_data.get("estimated_time_to_spoilage_hours", 0.0)
    current_dest = alert_data.get("original_destination", "N/A")
    recommended_dest = alert_data.get("recommended_market", "N/A")
    transit_hours = alert_data.get("transit_hours_to_recommended_market", 0.0)
    net_arbitrage = alert_data.get("net_arbitrage_profit_inr", 0.0)

    # Format Slack Block Kit Payload
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 AtmoSync Spoilage Arbitrage Alert",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Container:* {container_id}"},
                    {"type": "mrkdwn", "text": f"*Commodity:* {commodity}"},
                    {"type": "mrkdwn", "text": f"*Risk Level:* `{risk_level}`"},
                    {"type": "mrkdwn", "text": f"*Time to Spoilage:* {time_to_spoilage:.1f} hrs"},
                    {"type": "mrkdwn", "text": f"*Current Route:* {current_dest}"},
                    {"type": "mrkdwn", "text": f"*Recommended Reroute:* *{recommended_dest}*"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚚 *Travel Time to Market:* {transit_hours:.1f} hrs | 💰 *Estimated Net Arbitrage:* *₹{net_arbitrage:,.2f}*"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Approve Reroute in Superset"},
                        "style": "primary",
                        "value": f"approve_reroute_{container_id}"
                    }
                ]
            }
        ]
    }

    if not webhook_url or "hooks.slack.com/services/T00000000" in webhook_url:
        logger.info(f"[MOCK SLACK ALERT] Triggered for {container_id} -> Reroute: {recommended_dest} | Profit: ₹{net_arbitrage:,.2f}")
        logger.debug(f"Slack Payload: {json.dumps(payload, indent=2)}")
        return True

    try:
        response = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if response.status_code == 200:
            logger.info(f"Slack alert successfully dispatched for container {container_id}.")
            return True
        else:
            logger.error(f"Failed sending Slack alert ({response.status_code}): {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error connecting to Slack webhook: {e}")
        return False

if __name__ == "__main__":
    sample_alert = {
        "container_id": "CONT-004",
        "commodity": "Fresh Produce",
        "risk_level": "CRITICAL",
        "estimated_time_to_spoilage_hours": 13.5,
        "original_destination": "Mumbai",
        "recommended_market": "Bangalore",
        "transit_hours_to_recommended_market": 8.2,
        "net_arbitrage_profit_inr": 42500.00
    }
    send_slack_arbitrage_alert(sample_alert)
