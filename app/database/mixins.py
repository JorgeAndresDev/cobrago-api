import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class UUIDMixin:
    """Mixin to add a UUID primary key to models."""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

class SyncMixin:
    """Mixin to add an offline sync flag to models."""
    synced = Column(Boolean, default=False, nullable=False)

class BaseModelMixin(UUIDMixin, TimestampMixin, SyncMixin):
    """Combines UUID, Timestamps, and Sync mixins for standard models."""
    pass
