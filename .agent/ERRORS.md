# Known Errors and Fixes

## 2026-09-28
- **Error:** `IntegrityError: UNIQUE constraint failed: accounts_user.username` in `test_royalties.py`.
- **Context:** Test script attempted to call `User.objects.create_user()` for a test profile (`creator2`) that was already initialized in the local SQLite database from a previous run or scaffolding command.
- **Fix:** Switched test instantiation logic to `User.objects.get_or_create(...)` handling preexisting scaffolding elegantly without crashing the integration script. Tests passed successfully.

- **Error:** `django.db.utils.OperationalError: (2002, "Can't connect to server on '127.0.0.1' (10061)")`
- **Context:** Occurred during Phase 6 when attempting to verify the primary deployment target (MySQL) by overriding `.env` `USE_SQLITE=False`. 
- **Fix:** No fix. The local daemon is correctly offline in the active environment. `.env` was safely reverted to `USE_SQLITE=True` and documented as `UNKNOWN — needs verification`.

- **Error:** `NoReverseMatch at /accounts/register/` (Reverse for 'home' not found).
- **Context:** Registration, login, and logout views in `accounts/views.py` were attempting to redirect to the unnamespaced route `'home'`.
- **Fix:** Replaced all instances of `redirect('home')` with the properly namespaced route `redirect('catalog:home')`. Verified registration workflow completes and redirects properly via integration test.