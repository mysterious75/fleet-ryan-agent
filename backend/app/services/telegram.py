"""
Telegram Bot Service for Fleet Alerts and Escalations
"""

import structlog
from typing import Optional, Dict, Any
from datetime import datetime
from app.core.config import settings

logger = structlog.get_logger()


class TelegramService:
    """Service for sending Telegram messages and alerts."""

    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.FLEET_MANAGER_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def _send_message(
        self,
        text: str,
        chat_id: Optional[str] = None,
        parse_mode: str = "Markdown",
        reply_markup: Optional[Dict] = None,
    ) -> Dict:
        """Send a Telegram message."""
        import httpx

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id or self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

    async def send_alert(
        self,
        severity: str,
        vehicle_id: str,
        issue: str,
        details: Optional[str] = None,
        location: Optional[str] = None,
        driver: Optional[str] = None,
    ):
        """Send a fleet alert to the fleet manager."""
        # Severity emoji
        emoji_map = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "📋",
            "low": "ℹ️",
        }
        emoji = emoji_map.get(severity, "📋")

        # Build message
        lines = [
            f"{emoji} *{severity.upper()} FLEET ALERT*",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"🚛 Vehicle: {vehicle_id}",
            f"📝 Issue: {issue}",
        ]
        if location:
            lines.append(f"📍 Location: {location}")
        if driver:
            lines.append(f"👤 Driver: {driver}")
        if details:
            lines.append(f"📊 Details: {details}")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if severity == "critical":
            lines.append("⚡ IMMEDIATE ACTION REQUIRED")

        text = "\n".join(lines)

        try:
            await self._send_message(text)
            logger.info("Alert sent", severity=severity, vehicle_id=vehicle_id)
        except Exception as e:
            logger.error("Failed to send alert", error=str(e))

    async def send_escalation(
        self,
        escalation_id: str,
        vehicle_id: str,
        severity: str,
        description: str,
        recommended_action: Optional[str] = None,
        cost_estimate: Optional[float] = None,
    ):
        """Send an escalation request with approval buttons."""
        emoji_map = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "📋",
            "low": "ℹ️",
        }
        emoji = emoji_map.get(severity, "📋")

        lines = [
            f"{emoji} *{severity.upper()} — APPROVAL REQUIRED*",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"🚛 Vehicle: {vehicle_id}",
            f"📝 Issue: {description}",
        ]
        if recommended_action:
            lines.append(f"💡 Recommended: {recommended_action}")
        if cost_estimate:
            lines.append(f"💰 Est. Cost: ${cost_estimate:,.2f}")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🆔 ID: `{escalation_id}`")

        text = "\n".join(lines)

        # Inline keyboard for approval
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "✅ Approve", "callback_data": f"approve:{escalation_id}"},
                    {"text": "❌ Reject", "callback_data": f"reject:{escalation_id}"},
                ],
                [
                    {"text": "⏰ Schedule Later", "callback_data": f"defer:{escalation_id}"},
                    {"text": "📞 Call Me", "callback_data": f"call:{escalation_id}"},
                ],
            ]
        }

        try:
            await self._send_message(text, reply_markup=reply_markup)
            logger.info("Escalation sent", escalation_id=escalation_id)
        except Exception as e:
            logger.error("Failed to send escalation", error=str(e))

    async def send_daily_summary(self, summary: Dict[str, Any]):
        """Send daily fleet summary."""
        lines = [
            "📊 *Daily Fleet Summary*",
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"📅 Date: {datetime.utcnow().strftime('%B %d, %Y')}",
            "",
            f"🚛 Active Vehicles: {summary.get('active_vehicles', 0)}/{summary.get('total_vehicles', 0)}",
            f"📏 Miles Driven: {summary.get('total_miles', 0):,.0f}",
            f"⛽ Fuel Used: {summary.get('total_fuel', 0):,.0f} gal",
            "",
            f"🔴 Critical: {summary.get('critical_incidents', 0)}",
            f"🟠 High: {summary.get('high_incidents', 0)}",
            f"🟡 Medium: {summary.get('medium_incidents', 0)}",
            "",
            f"⏳ Pending Approvals: {summary.get('pending_approvals', 0)}",
            f"🔧 Overdue Maintenance: {summary.get('overdue_maintenance', 0)}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ]

        if summary.get("recommendations"):
            lines.append("💡 *Recommendations:*")
            for rec in summary["recommendations"]:
                lines.append(f"  • {rec}")

        text = "\n".join(lines)

        try:
            await self._send_message(text)
            logger.info("Daily summary sent")
        except Exception as e:
            logger.error("Failed to send daily summary", error=str(e))

    async def send_compliance_alert(
        self,
        driver_name: str,
        vehicle_id: str,
        violation_type: str,
        details: str,
    ):
        """Send a compliance violation alert."""
        lines = [
            "⚠️ *COMPLIANCE ALERT*",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"👤 Driver: {driver_name}",
            f"🚛 Vehicle: {vehicle_id}",
            f"📋 Violation: {violation_type}",
            f"📊 Details: {details}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "Action: Review and address immediately",
        ]

        text = "\n".join(lines)

        try:
            await self._send_message(text)
            logger.info("Compliance alert sent", driver=driver_name, violation=violation_type)
        except Exception as e:
            logger.error("Failed to send compliance alert", error=str(e))
