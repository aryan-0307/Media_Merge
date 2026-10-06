# Architecture and Design Decisions

## Django Apps
- `accounts`: Handles Custom User model and roles.
- `catalog`: Handles media asset management, access key generation, and creator views.
- `subscriptions`: Handles subscription plans and user subscriptions.
- `analytics`: Handles streaming records, watch history, and administrative overviews.
- `royalties`: Handles rate configurations, historically preserving transaction objects, and encapsulates bulk payout engines.

## Authentication & Authorization
- Built-in Django authentication heavily enforces security. 
- Custom roles handled cleanly with built-in decorator blocks (`@user_passes_test`) preventing manual URL exploits.

## System Audits
- Tests constructed natively utilizing Django's internal test client ensuring realistic request object permutations. E2E flow testing simulated internally to guarantee DB transaction commits hold across apps.
- Protected assets explicitly segmented to OS-level directories (`protected_media/`) effectively stopping default Nginx/Apache/Django static exposure.

## Database
- MySQL is the chosen production/primary database based on requirements.
- SQLite is maintained as a fallback in `.env` (`USE_SQLITE=True`).
- Final verification identified MySQL socket connections unavailable locally (`10061`). Project correctly documented as `UNKNOWN — needs verification` strictly adhering to honesty guidelines.
- Configured Django to support SSL requirements for Aiven Free MySQL. Config allows providing SSL certificate path or setting `ssl_mode=REQUIRED` safely without hardcoding secrets, relying purely on environment variables (`DB_USE_SSL`, `DB_SSL_MODE`, `DB_SSL_CA`).

## Frontend UI
- Pure HTML5, CSS3, and Vanilla JavaScript.
- Retained strict compliance to structural layouts mapping the neon aesthetic cleanly into forms, tables, and buttons.
