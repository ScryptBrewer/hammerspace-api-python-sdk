"""
Structured logging configuration for Hammerspace API SDK
"""

import logging
import logging.config
import json
import sys
from typing import Any, Dict
from datetime import datetime
import os


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


class HammerspaceLogger:
    """Custom logger for Hammerspace API SDK."""
    
    def __init__(
        self,
        name: str = 'hammerspace',
        level: str = 'INFO',
        format_type: str = 'standard',
        log_file: str = None,
        enable_colors: bool = True
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.logger.handlers.clear()
        
        # Setup handlers based on configuration
        self._setup_handlers(format_type, log_file, enable_colors)
    
    def _setup_handlers(
        self,
        format_type: str,
        log_file: str,
        enable_colors: bool
    ):
        """Setup logging handlers."""
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        if format_type == 'json':
            console_handler.setFormatter(JSONFormatter())
        else:
            if enable_colors:
                console_handler.setFormatter(ColoredFormatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
            else:
                console_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
        
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            if format_type == 'json':
                file_handler.setFormatter(JSONFormatter())
            else:
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
            self.logger.addHandler(file_handler)
    
    def add_context(self, **kwargs):
        """Add context to all log messages."""
        return ContextualLogger(self.logger, kwargs)
    
    def __getattr__(self, name):
        """Delegate to underlying logger."""
        return getattr(self.logger, name)


class ContextualLogger:
    """Logger with additional context."""
    
    def __init__(self, logger: logging.Logger, context: Dict[str, Any]):
        self.logger = logger
        self.context = context
    
    def _log_with_context(self, level: int, msg: str, *args, **kwargs):
        """Log message with context."""
        extra = kwargs.pop('extra', {})
        extra['extra_fields'] = {**self.context, **extra}
        kwargs['extra'] = extra
        
        self.logger.log(level, msg, *args, **kwargs)
    
    def debug(self, msg: str, *args, **kwargs):
        self._log_with_context(logging.DEBUG, msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        self._log_with_context(logging.INFO, msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        self._log_with_context(logging.WARNING, msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        self._log_with_context(logging.ERROR, msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        self._log_with_context(logging.CRITICAL, msg, *args, **kwargs)


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        return super().format(record)


def configure_logging(
    level: str = 'INFO',
    format_type: str = 'standard',
    log_file: str = None,
    enable_colors: bool = True
) -> HammerspaceLogger:
    """
    Configure logging for the Hammerspace SDK.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Log format ('standard' or 'json')
        log_file: Path to log file (optional)
        enable_colors: Enable colored console output
        
    Returns:
        Configured HammerspaceLogger instance
        
    Example:
        >>> logger = configure_logging(level='DEBUG', format_type='json')
        >>> logger.info("API client initialized", base_url="https://server:8443")
        
        >>> # With context
        >>> contextual_logger = logger.add_context(request_id="12345")
        >>> contextual_logger.info("Processing request")
    """
    
    # Get log level from environment if not specified
    if 'LOG_LEVEL' in os.environ:
        level = os.environ['LOG_LEVEL']
    
    # Get log file from environment if not specified
    if not log_file and 'LOG_FILE' in os.environ:
        log_file = os.environ['LOG_FILE']
    
    # Get format type from environment if not specified
    if 'LOG_FORMAT' in os.environ:
        format_type = os.environ['LOG_FORMAT']
    
    return HammerspaceLogger(
        name='hammerspace',
        level=level,
        format_type=format_type,
        log_file=log_file,
        enable_colors=enable_colors
    )


class MetricsCollector:
    """Simple metrics collector for monitoring API usage."""
    
    def __init__(self):
        self.metrics = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'requests_timeout': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'retries_total': 0,
            'authentication_failures': 0,
            'response_times': [],
        }
    
    def record_request(self, success: bool, timeout: bool = False, response_time: float = None):
        """Record a request attempt."""
        self.metrics['requests_total'] += 1
        if success:
            self.metrics['requests_success'] += 1
        else:
            self.metrics['requests_failed'] += 1
        if timeout:
            self.metrics['requests_timeout'] += 1
        if response_time is not None:
            self.metrics['response_times'].append(response_time)
    
    def record_cache_hit(self):
        """Record a cache hit."""
        self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Record a cache miss."""
        self.metrics['cache_misses'] += 1
    
    def record_retry(self):
        """Record a retry attempt."""
        self.metrics['retries_total'] += 1
    
    def record_auth_failure(self):
        """Record an authentication failure."""
        self.metrics['authentication_failures'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        metrics_copy = self.metrics.copy()
        
        # Calculate averages
        if metrics_copy['response_times']:
            avg_response_time = sum(metrics_copy['response_times']) / len(metrics_copy['response_times'])
            metrics_copy['avg_response_time'] = avg_response_time
            metrics_copy['max_response_time'] = max(metrics_copy['response_times'])
            metrics_copy['min_response_time'] = min(metrics_copy['response_times'])
        
        # Calculate cache hit rate
        total_cache_attempts = metrics_copy['cache_hits'] + metrics_copy['cache_misses']
        if total_cache_attempts > 0:
            metrics_copy['cache_hit_rate'] = metrics_copy['cache_hits'] / total_cache_attempts
        
        # Calculate success rate
        if metrics_copy['requests_total'] > 0:
            metrics_copy['success_rate'] = metrics_copy['requests_success'] / metrics_copy['requests_total']
        
        return metrics_copy
    
    def reset_metrics(self):
        """Reset all metrics."""
        self.metrics = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_failed': 0,
            'requests_timeout': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'retries_total': 0,
            'authentication_failures': 0,
            'response_times': [],
        }
    
    def log_metrics(self, logger: logging.Logger):
        """Log current metrics."""
        metrics = self.get_metrics()
        logger.info("Current metrics", **metrics)