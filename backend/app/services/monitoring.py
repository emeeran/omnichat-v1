import time
import logging
from typing import Dict, Any
from prometheus_client import start_http_server, Summary, Gauge, Counter

class MonitoringService:
    def __init__(self, port: int = 65000):
        self.logger = logging.getLogger(__name__)
        self.port = port
        self._initialize_metrics()

    def _initialize_metrics(self):
        # Create a metric to track time spent and requests made.
        self.REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
        self.REQUEST_COUNT = Counter('request_count', 'Total request count')
        self.ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

    def start_server(self):
        """Start the Prometheus metrics server."""
        start_http_server(self.port)
        self.logger.info(f"Prometheus metrics server started on port {self.port}")

    def track_request(self, func):
        """Decorator to track request metrics."""
        def wrapper(*args, **kwargs):
            self.REQUEST_COUNT.inc()
            self.ACTIVE_REQUESTS.inc()
            start_time = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                self.ACTIVE_REQUESTS.dec()
                self.REQUEST_TIME.observe(time.time() - start_time)
        return wrapper

    def track_custom_metric(self, name: str, value: Any):
        """Track a custom metric."""
        if name not in self.custom_metrics:
            self.custom_metrics[name] = Gauge(name, f"Custom metric: {name}")
        self.custom_metrics[name].set(value)

    def get_metrics(self) -> Dict[str, Any]:
        """Get all tracked metrics."""
        return {
            'request_count': self.REQUEST_COUNT._value.get(),
            'active_requests': self.ACTIVE_REQUESTS._value.get(),
            'request_time': self.REQUEST_TIME._sum.get(),
            **{name: metric._value.get() for name, metric in self.custom_metrics.items()}
        }
