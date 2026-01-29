"""
Arize AX Tracing Integration

This module configures OpenTelemetry-based tracing for the ADK agent,
enabling observability through Arize AX.
"""

import os

_tracer_initialized = False


def setup_tracing(project_name: str | None = None) -> None:
    """
    Initialize Arize AX tracing for ADK agents.

    Requires ARIZE_SPACE_ID and ARIZE_API_KEY environment variables.
    """
    global _tracer_initialized

    if _tracer_initialized:
        return

    project_name = project_name or os.getenv(
        "ARIZE_PROJECT_NAME", "videogames-assistant"
    )

    space_id = os.getenv("ARIZE_SPACE_ID")
    api_key = os.getenv("ARIZE_API_KEY")

    if not space_id or not api_key:
        print("[Tracing] ARIZE_SPACE_ID and ARIZE_API_KEY not set, skipping.")
        return

    print(
        f"[Tracing] space_id length={len(space_id)}, "
        f"api_key starts with={api_key[:6]}..."
    )

    try:
        from arize.otel import register
        from openinference.instrumentation.google_adk import GoogleADKInstrumentor

        tracer_provider = register(
            space_id=space_id,
            api_key=api_key,
            project_name=project_name,
            endpoint="https://otlp.arize.com/v1",
        )

        GoogleADKInstrumentor().instrument(tracer_provider=tracer_provider)

        _tracer_initialized = True
        print(f"[Tracing] Arize AX initialized for project: {project_name}")

    except Exception as e:
        print(f"[Tracing] Failed to initialize Arize AX: {e}")
        import traceback

        traceback.print_exc()
