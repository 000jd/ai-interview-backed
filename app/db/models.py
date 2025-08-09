"""
Backwards-compatible re-export for models. New code should import from
app.db.models.<model_module>. This file ensures existing imports keep working.
"""

from .models import *  # noqa: F401,F403
