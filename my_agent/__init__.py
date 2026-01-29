"""
Agent package initialization with tracing support.

For Vertex AI Agent Engine deployment, tracing is initialized here
to ensure instrumentation is active within the remote environment.
"""

import os

# Initialize tracing for Agent Engine deployment
if os.getenv("GOOGLE_CLOUD_PROJECT"):
    try:
        from observability.tracing import setup_tracing
        setup_tracing()
    except ImportError:
        pass  # Tracing dependencies not installed

from .agent import root_agent

__all__ = ["root_agent"]
