
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.config import Config
from scripts.utils.logger import get_logger

logger = get_logger("email_alert")

def send_email_alert(alert_data: dict) -> bool:
    """
    Sends an HTML email alert via SMTP for high-priority container spoilage events.
    """
    container_id = alert_data.get("container_id", "UNKNOWN")
    commodity = alert_data.get("commodity", "N/A")
    risk_level = alert_data.get("risk_level", "UNKNOWN")
    time_to_spoilage = alert_data.get("estimated_time_to_spoilage_hours", 0.0)
    recommended_dest = alert_data.get("recommended_market", "N/A")
    net_arbitrage = alert_data.get("net_arbitrage_profit_inr", 0.0)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 [CRITICAL ALERT] AtmoSync Container {container_id} Reroute Recommended"
    msg["From"] = Config.ALERT_EMAIL_FROM
    msg["To"] = Config.ALERT_EMAIL_TO

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #d9534f;">AtmoSync Spoilage Arbitrage Alert</h2>
        <p>A critical micro-climate thermal drift has been detected in cargo shipment <strong>{container_id}</strong>.</p>
        <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
          <tr style="background-color: #f8f9fa;"><td style="padding: 8px; border: 1px solid #ddd;"><strong>Container ID</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{container_id}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Commodity</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{commodity}</td></tr>
          <tr style="background-color: #f8f9fa;"><td style="padding: 8px; border: 1px solid #ddd;"><strong>Risk Level</strong></td><td style="padding: 8px; border: 1px solid #ddd; color: red;"><strong>{risk_level}</strong></td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Time to Spoilage</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{time_to_spoilage:.1f} hours</td></tr>
          <tr style="background-color: #f8f9fa;"><td style="padding: 8px; border: 1px solid #ddd;"><strong>Recommended Reroute Market</strong></td><td style="padding: 8px; border: 1px solid #ddd; color: #0275d8;"><strong>{recommended_dest}</strong></td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Estimated Net Arbitrage Profit</strong></td><td style="padding: 8px; border: 1px solid #ddd; color: #5cb85c;"><strong>₹{net_arbitrage:,.2f}</strong></td></tr>
        </table>
        <p style="margin-top: 20px;">Please check the live Apache Superset dashboard for execution details.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    if not Config.SMTP_USERNAME or "alerts@atmosync.io" in Config.SMTP_USERNAME:
        logger.info(f"[MOCK EMAIL ALERT] Email dispatched to {Config.ALERT_EMAIL_TO} for Container {container_id}.")
        return True

    try:
        server = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.sendmail(Config.ALERT_EMAIL_FROM, [Config.ALERT_EMAIL_TO], msg.as_string())
        server.quit()
        logger.info(f"Email alert successfully sent to {Config.ALERT_EMAIL_TO}.")
        return True
    except Exception as e:
        logger.error(f"Failed to send email via SMTP: {e}")
        return False

if __name__ == "__main__":
    send_email_alert({"container_id": "CONT-004", "commodity": "Dairy", "risk_level": "CRITICAL", "estimated_time_to_spoilage_hours": 8.0, "recommended_market": "Bangalore", "net_arbitrage_profit_inr": 65000.0})
