"""
LangGraph Memory Configuration.

This module provides production-ready memory persistence using PostgreSQL:
- Short-term memory: PostgresSaver (checkpointer) for conversation history
- Long-term memory: PostgresStore for user profiles and preferences

Supports both sync and async operations:
- Sync: PostgresSaver + PostgresStore with ConnectionPool
- Async: AsyncPostgresSaver + AsyncPostgresStore with AsyncConnectionPool

See: https://docs.langchain.com/oss/python/langgraph/memory
"""

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres import PostgresStore
from langgraph.store.postgres.aio import AsyncPostgresStore
from psycopg_pool import AsyncConnectionPool, ConnectionPool

from app.core.config import settings

# ═══════════════════════════════════════════════════════════════
# CONNECTION POOL CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Connection kwargs required for LangGraph checkpointer
_connection_kwargs = {
    "autocommit": True,  # Required for checkpointer.setup()
    "prepare_threshold": 0,  # Disable prepared statements for compatibility
}

# Singleton connection pools (initialized lazily)
_pool: ConnectionPool | None = None
_async_pool: AsyncConnectionPool | None = None


def get_connection_pool() -> ConnectionPool:
    """
    Get or create the shared sync connection pool.

    Uses a singleton pattern to ensure only one pool exists.
    The pool is configured for LangGraph's requirements.
    """
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            conninfo=settings.DATABASE_URL,
            min_size=2,
            max_size=10,
            kwargs=_connection_kwargs,
        )
    return _pool


def get_async_connection_pool() -> AsyncConnectionPool:
    """
    Get or create the shared async connection pool.

    Used for async operations like astream_events.
    Note: Pool is created with open=False to avoid deprecation warning.
    Must call `await pool.open()` before use (done in init_async_memory).
    """
    global _async_pool
    if _async_pool is None:
        _async_pool = AsyncConnectionPool(
            conninfo=settings.DATABASE_URL,
            min_size=2,
            max_size=10,
            kwargs=_connection_kwargs,
            open=False,  # Don't auto-open in constructor (deprecated behavior)
        )
    return _async_pool


# ═══════════════════════════════════════════════════════════════
# CHECKPOINTER (Short-term Memory)
# ═══════════════════════════════════════════════════════════════

# Singleton checkpointers (initialized lazily)
_checkpointer: PostgresSaver | None = None
_async_checkpointer: AsyncPostgresSaver | None = None


def get_checkpointer() -> PostgresSaver:
    """
    Get the PostgreSQL-backed checkpointer for short-term memory (sync).

    Short-term memory stores:
    - Conversation history within a thread
    - Agent state between turns
    - Enables conversation resumption after restarts

    Thread-scoped: Each thread_id has isolated memory.
    """
    global _checkpointer
    if _checkpointer is None:
        pool = get_connection_pool()
        _checkpointer = PostgresSaver(pool)
    return _checkpointer


def get_async_checkpointer() -> AsyncPostgresSaver:
    """
    Get the async PostgreSQL-backed checkpointer for streaming operations.

    Use this for async operations like astream_events.
    """
    global _async_checkpointer
    if _async_checkpointer is None:
        pool = get_async_connection_pool()
        _async_checkpointer = AsyncPostgresSaver(pool)
    return _async_checkpointer


# ═══════════════════════════════════════════════════════════════
# MEMORY STORE (Long-term Memory)
# ═══════════════════════════════════════════════════════════════

# Singleton memory stores (initialized lazily)
_store: PostgresStore | None = None
_async_store: AsyncPostgresStore | None = None


def get_memory_store() -> PostgresStore:
    """
    Get the PostgreSQL-backed store for long-term memory (sync).

    Long-term memory stores (organized by namespace):
    - User profiles: (user_id, "profile") -> preferences, target band, etc.
    - Essay history: (user_id, "essays") -> past scores for progress tracking
    - Learning notes: (user_id, "notes") -> tutor observations about user

    Cross-session: Memories persist across all conversations.
    """
    global _store
    if _store is None:
        pool = get_connection_pool()
        _store = PostgresStore(pool)
    return _store


def get_async_memory_store() -> AsyncPostgresStore:
    """
    Get the async PostgreSQL-backed store for streaming operations.

    Use this for async operations like astream_events.
    """
    global _async_store
    if _async_store is None:
        pool = get_async_connection_pool()
        _async_store = AsyncPostgresStore(pool)
    return _async_store


# ═══════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════


def init_memory() -> None:
    """
    Initialize memory tables in PostgreSQL.

    Call this once at application startup (in FastAPI lifespan).
    Creates the required tables for checkpointer and store if they don't exist.
    """
    checkpointer = get_checkpointer()
    store = get_memory_store()

    # Create checkpoint tables (for short-term memory)
    checkpointer.setup()

    # Create store tables (for long-term memory)
    store.setup()


async def init_async_memory() -> None:
    """
    Initialize async memory components.

    Call this after init_memory() to set up async pools.
    The async pool needs to be opened explicitly.
    """
    global _async_pool
    pool = get_async_connection_pool()
    # Open the async pool (required for AsyncConnectionPool)
    await pool.open()

    # Initialize async checkpointer and store
    async_checkpointer = get_async_checkpointer()
    async_store = get_async_memory_store()

    # Setup tables (uses same tables as sync, but validates connection)
    await async_checkpointer.setup()
    await async_store.setup()


def close_memory() -> None:
    """
    Close sync memory connections.

    Call this at application shutdown to cleanly close the connection pool.
    """
    global _pool, _checkpointer, _store

    if _pool is not None:
        _pool.close()
        _pool = None

    _checkpointer = None
    _store = None


async def close_async_memory() -> None:
    """
    Close async memory connections.

    Call this at application shutdown to cleanly close the async pool.
    """
    global _async_pool, _async_checkpointer, _async_store

    if _async_pool is not None:
        await _async_pool.close()
        _async_pool = None

    _async_checkpointer = None
    _async_store = None


# ═══════════════════════════════════════════════════════════════
# NAMESPACE HELPERS
# ═══════════════════════════════════════════════════════════════


def get_user_profile_namespace(user_id: int) -> tuple[str, str]:
    """Get namespace for user profile storage."""
    return (str(user_id), "profile")


def get_user_essays_namespace(user_id: int) -> tuple[str, str]:
    """Get namespace for user essay history."""
    return (str(user_id), "essays")


def get_user_notes_namespace(user_id: int) -> tuple[str, str]:
    """Get namespace for tutor notes about user."""
    return (str(user_id), "notes")
