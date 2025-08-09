"""
Backwards-compatible facade for CRUD functions. New code should import from
app.crud.users, app.crud.api_keys, app.crud.interviews, app.crud.tokens.
"""

from .users import (
    get_user_by_email,
    get_user_by_username,
    create_user,
    authenticate_user,
)
from .api_keys import (
    create_api_key,
    get_user_api_keys,
    get_api_key,
    update_api_key_usage,
    deactivate_api_key,
)
from .interviews import (
    create_interview,
    get_user_interviews,
    get_interview,
    update_interview,
)
from .tokens import (
    add_token_to_blocklist,
    is_token_blocklisted,
    cleanup_expired_blocklisted_tokens,
)