import heapq
import json
import os
import time
import asyncio

class Event:
    def __init__(self, event_id, data, priority=5, timestamp=None):
        self.event_id = event_id
        self.data = data
        self.priority = priority
        self.timestamp = timestamp if timestamp else time.time()

class EventQueue:
    def __init__(self, persistence_file="events.json"):
        self.queue = []
        self.dead_letter_queue = []
        self.metrics = {"processed": 0, "failed": 0, "current_queue_length": 0}
        self.persistence_file = persistence_file
        self.load_events()
    
    def validate_event(self, event):
        return hasattr(event, "event_id") and event.data is not None

    def publish(self, event):
        if not self.validate_event(event):
            raise ValueError("Invalid event structure")
        heapq.heappush(self.queue, (event.priority, event.timestamp, event))
        self.metrics["current_queue_length"] = len(self.queue)
        self.save_event(event)

    def save_event(self, event):
        try:
            with open(self.persistence_file, "a") as f:
                f.write(json.dumps({
                    "event_id": event.event_id,
                    "data": event.data,
                    "priority": event.priority,
                    "timestamp": event.timestamp
                }) + "\n")
        except Exception as e:
            print(f"Error persisting event: {e}")

    def load_events(self):
        if os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, "r") as f:
                    for line in f:
                        evt = json.loads(line.strip())
                        event = Event(evt["event_id"], evt["data"], evt.get("priority", 5), evt.get("timestamp"))
                        heapq.heappush(self.queue, (event.priority, event.timestamp, event))
                self.metrics["current_queue_length"] = len(self.queue)
            except Exception as e:
                print(f"Error loading persisted events: {e}")

    async def replay_events(self):
        events = []
        while self.queue:
            _, _, event = heapq.heappop(self.queue)
            events.append(event)
            await self.process_event(event)
        self.metrics["current_queue_length"] = len(self.queue)
        return events

    async def process_event(self, event):
        try:
            if not self.validate_event(event):
                raise ValueError("Event validation failed")
            await asyncio.sleep(0.1)
            self.metrics["processed"] += 1
            print(f"Processed event: {event.event_id}")
        except Exception as e:
            self.dead_letter_queue.append(event)
            self.metrics["failed"] += 1
            print(f"Failed to process event: {event.event_id}, error: {str(e)}")

    def get_metrics(self):
        return self.metrics
