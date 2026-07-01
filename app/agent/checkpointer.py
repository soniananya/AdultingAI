from app.config import get_settings


def get_checkpointer():
    """
    Return a LangGraph checkpointer.

    Prefers the durable Postgres checkpointer (matches DATABASE_URL). If the
    Postgres driver / libpq is unavailable, or the connection cannot be set up,
    fall back to an in-memory checkpointer so the app still runs (e.g. for
    local demos). In-memory checkpoints are not persisted across restarts.
    """
    settings = get_settings()

    try:
        from langgraph.checkpoint.postgres import PostgresSaver

        cm = PostgresSaver.from_conn_string(settings.DATABASE_URL)
        checkpointer = cm.__enter__()  # keep the connection open for the process lifetime
        checkpointer.setup()
        return checkpointer

    except Exception:
        from langgraph.checkpoint.memory import MemorySaver

        return MemorySaver()
