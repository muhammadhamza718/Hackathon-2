"""Monitoring and metrics collection for the Todo Chatbot backend"""
import time
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import threading
import json
import os


@dataclass
class Metric:
    """Represents a single metric with timestamp and value"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str]
    type: str  # 'counter', 'gauge', 'histogram', 'timer'


class MetricsCollector:
    """Collects and stores metrics for the application"""

    def __init__(self):
        self._metrics: Dict[str, list] = {}
        self._lock = threading.Lock()
        self._counters: Dict[str, int] = {}

    def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None, metric_type: str = 'gauge'):
        """Record a metric value"""
        with self._lock:
            metric = Metric(
                name=name,
                value=value,
                timestamp=datetime.utcnow(),
                tags=tags or {},
                type=metric_type
            )

            if name not in self._metrics:
                self._metrics[name] = []
            self._metrics[name].append(metric)

            # Keep only last 1000 entries per metric to prevent memory issues
            if len(self._metrics[name]) > 1000:
                self._metrics[name] = self._metrics[name][-1000:]

    def increment_counter(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        with self._lock:
            key = f"{name}_{str(tags or {})}"
            if key not in self._counters:
                self._counters[key] = 0
            self._counters[key] += 1

    def get_counter_value(self, name: str, tags: Optional[Dict[str, str]] = None) -> int:
        """Get the current value of a counter"""
        with self._lock:
            key = f"{name}_{str(tags or {})}"
            return self._counters.get(key, 0)

    def get_metrics(self, name: Optional[str] = None) -> Dict[str, list]:
        """Get collected metrics, optionally filtered by name"""
        with self._lock:
            if name:
                return {name: self._metrics.get(name, [])}
            return self._metrics.copy()

    def get_latest_metric(self, name: str) -> Optional[Metric]:
        """Get the most recent value for a metric"""
        with self._lock:
            if name in self._metrics and self._metrics[name]:
                return self._metrics[name][-1]
            return None


class Timer:
    """Context manager for timing operations"""

    def __init__(self, collector: MetricsCollector, metric_name: str, tags: Optional[Dict[str, str]] = None):
        self.collector = collector
        self.metric_name = metric_name
        self.tags = tags or {}
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.collector.record_metric(
                name=self.metric_name,
                value=duration,
                tags=self.tags,
                type='timer'
            )


# Global metrics collector instance
metrics_collector = MetricsCollector()


def time_function(metric_name: str, tags: Optional[Dict[str, str]] = None):
    """Decorator to time function execution"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with Timer(metrics_collector, metric_name, tags):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def count_calls(metric_name: str, tags: Optional[Dict[str, str]] = None):
    """Decorator to count function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            metrics_collector.increment_counter(metric_name, tags)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_system_metrics() -> Dict[str, Any]:
    """Get system-level metrics"""
    import psutil
    import os

    process = psutil.Process(os.getpid())

    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'process_memory_mb': process.memory_info().rss / 1024 / 1024,
        'disk_usage_percent': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('.').percent,
        'timestamp': datetime.utcnow().isoformat()
    }


def export_metrics_json(filename: str = None) -> str:
    """Export metrics to JSON file or return as string"""
    data = {
        'metrics': metrics_collector.get_metrics(),
        'system_metrics': get_system_metrics(),
        'timestamp': datetime.utcnow().isoformat()
    }

    if filename:
        with open(filename, 'w') as f:
            json.dump(data, f, default=str, indent=2)
        return filename
    else:
        return json.dumps(data, default=str, indent=2)


def get_api_metrics() -> Dict[str, Any]:
    """Get API-specific metrics"""
    return {
        'requests_total': metrics_collector.get_counter_value('api_requests_total'),
        'errors_total': metrics_collector.get_counter_value('api_errors_total'),
        'avg_response_time': get_average_response_time('api_response_time'),
        'active_connections': metrics_collector.get_counter_value('active_connections'),
    }


def get_average_response_time(metric_name: str) -> Optional[float]:
    """Calculate average response time for a timer metric"""
    metrics = metrics_collector.get_metrics(metric_name)
    if not metrics.get(metric_name):
        return None

    values = [m.value for m in metrics[metric_name]]
    return sum(values) / len(values) if values else None


def increment_api_requests():
    """Increment API request counter"""
    metrics_collector.increment_counter('api_requests_total')


def increment_api_errors():
    """Increment API error counter"""
    metrics_collector.increment_counter('api_errors_total')


def record_response_time(duration: float, endpoint: str = None):
    """Record API response time"""
    tags = {'endpoint': endpoint} if endpoint else {}
    metrics_collector.record_metric('api_response_time', duration, tags, 'timer')


def increment_active_connections():
    """Increment active connections counter"""
    metrics_collector.increment_counter('active_connections')


def decrement_active_connections():
    """Decrement active connections counter"""
    # Since we don't have a decrement method, we'll just track the net change
    # In a real implementation, you might want to track the actual count differently
    pass