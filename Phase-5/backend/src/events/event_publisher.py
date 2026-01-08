"""
Event publisher for the Todo Backend
"""
from typing import Any
import json
import logging
from datetime import datetime
import uuid
from dapr.clients import DaprClient as DaprGrpcClient
from .task_events import TaskEvent
from .reminder_events import ReminderEvent
from .audit_events import AuditEvent

logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Publisher for sending events to Kafka via Dapr
    """

    def __init__(self):
        self.pubsub_name = "pubsub"

    async def publish_task_event(self, event: TaskEvent):
        """
        Publish a task event to the task-events topic
        """
        with DaprGrpcClient() as client:
            try:
                data = event.model_dump_json()
                client.publish_event(
                    pubsub_name=self.pubsub_name,
                    topic_name="task-events",
                    data=data,
                    data_content_type='application/json'
                )
                logger.info(f"Published task event: {event.event_type} - {event.event_id}")
            except Exception as e:
                logger.error(f"Failed to publish task event: {e}")
                raise

    async def publish_reminder_event(self, event: ReminderEvent):
        """
        Publish a reminder event to the reminder-events topic
        """
        with DaprGrpcClient() as client:
            try:
                data = event.model_dump_json()
                client.publish_event(
                    pubsub_name=self.pubsub_name,
                    topic_name="reminder-events",
                    data=data,
                    data_content_type='application/json'
                )
                logger.info(f"Published reminder event: {event.event_type} - {event.event_id}")
            except Exception as e:
                logger.error(f"Failed to publish reminder event: {e}")
                raise

    async def publish_audit_event(self, event: AuditEvent):
        """
        Publish an audit event to the audit-events topic
        """
        with DaprGrpcClient() as client:
            try:
                data = event.model_dump_json()
                client.publish_event(
                    pubsub_name=self.pubsub_name,
                    topic_name="audit-events",
                    data=data,
                    data_content_type='application/json'
                )
                logger.info(f"Published audit event: {event.event_type} - {event.event_id}")
            except Exception as e:
                logger.error(f"Failed to publish audit event: {e}")
                raise


# Global instance
_event_publisher = EventPublisher()


def get_event_publisher() -> EventPublisher:
    """
    Get the event publisher instance
    """
    return _event_publisher