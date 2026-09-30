# MEDIAMERGE --- PROJECT MASTER REQUIREMENTS

You are now working on a real college-level software engineering project
called:

MediaMerge --- Media Asset Management & Streaming Platform

Your job is to understand the complete project requirements, inspect the
existing repository, and then implement the project systematically
according to the Antigravity Agent Operating System already provided.

================================================== 1. PROJECT OBJECTIVE
==================================================

MediaMerge is a web-based media asset management and streaming platform.

The system should allow:

-   Users/subscribers to register, log in, browse media, search/filter
    media, subscribe to a plan, stream authorized media, and maintain
    watch history.
-   Creators/content owners to upload and manage their media, view
    streaming activity, and track royalty earnings.
-   Administrators to manage users, creators, media, subscriptions,
    streaming activity, royalties, and platform analytics.

This is a college-level project.

The implementation must be realistic, maintainable, understandable, and
demonstrable.

DO NOT over-engineer the system as if it were Netflix or a commercial
OTT platform.

================================================== 2. FIXED TECHNOLOGY
STACK ==================================================

Backend: - Python - Django - Django REST Framework where APIs are
actually useful

Database: - MySQL

Frontend: - Django Templates - HTML5 - CSS3 - Vanilla JavaScript

Optional: - Bootstrap where it genuinely helps - Chart.js for basic
dashboard charts if useful

Development tools: - Git - GitHub - Postman for API testing - Local
media/file storage during development

STRICTLY DO NOT USE: - React - Next.js - Vue - Angular - Other frontend
frameworks - AI/ML - Recommendation systems

Do not introduce another major technology without first documenting the
reason in .agent/DECISIONS.md.

================================================== 3. PROJECT
ARCHITECTURE ==================================================

Use a clean Django architecture with appropriate separation of
responsibilities.

The general flow should be:

Django Templates ↓ HTML / CSS / Vanilla JavaScript ↓ Django Views / DRF
APIs ↓ Business Logic ↓ Django Models ↓ MySQL

Use Django's built-in authentication system where appropriate.

Use Django apps/modules to keep functionality organized.

Before deciding the exact app structure, inspect the existing repository
and determine whether an existing structure should be preserved.

Do not unnecessarily rewrite an existing working project.

================================================== 4. USER ROLES
==================================================

The system should support three main roles:

1.  Subscriber/User
2.  Creator/Content Owner
3.  Admin

Implement proper role-based authorization.

Users must only be able to access functionality appropriate to their
role.

Do not rely only on hiding frontend buttons for security.

Authorization must also be enforced on the backend.

================================================== 5. MAIN FUNCTIONAL
MODULES ==================================================

Implement the following six modules:

MODULE 1 --- USER & AUTHENTICATION

Features:

-   User registration
-   Login
-   Logout
-   Password handling using Django authentication
-   User profile
-   Role management
-   Subscriber/User role
-   Creator role
-   Admin role
-   Role-based access control
-   Appropriate protected routes/pages

------------------------------------------------------------------------

MODULE 2 --- MEDIA MANAGEMENT

Creators/Admins should be able to manage media.

Media should support appropriate fields such as:

-   Title
-   Description
-   Media type
-   Genre/category
-   Language
-   Release date
-   Duration
-   Thumbnail
-   Media file
-   Creator/content owner
-   Publication status
-   Created/updated timestamps

The exact schema must be decided after inspecting the repository and
existing requirements.

Features:

-   Upload media
-   Upload thumbnail
-   Edit media
-   Delete media
-   Publish/unpublish media
-   View media
-   Media catalog
-   Search
-   Filtering
-   Media details page

Creators should manage their own media.

Admins should have broader management access.

------------------------------------------------------------------------

MODULE 3 --- SUBSCRIPTION & STREAMING

Implement a simple subscription system suitable for a college project.

Features:

-   Subscription plans
-   Plan name
-   Price
-   Duration
-   Active/expired state
-   Subscription history
-   Subscription status
-   Test/simulated payment flow

Do NOT implement a real payment gateway unless the repository already
contains one and it is explicitly required.

Streaming features:

-   Media playback
-   Subscription verification
-   Access verification
-   Watch history
-   Watch progress/duration
-   Streaming records
-   Basic streaming statistics

If practical, support HTTP range requests for video playback.

The implementation should remain understandable and reliable.

------------------------------------------------------------------------

MODULE 4 --- DRM / CONTENT PROTECTION

Implement academic/demo-level DRM concepts.

IMPORTANT:

This is NOT commercial DRM.

Do NOT attempt to implement Widevine, FairPlay, PlayReady, or another
commercial DRM system.

Instead implement application-level content protection such as:

-   Authentication
-   Authorization
-   Subscription verification
-   Protected media access
-   Temporary access token
-   Token expiry
-   Token validation
-   Rejection of invalid/expired access
-   Prevention of unrestricted direct media access

The goal is to demonstrate the concept of protected content delivery.

------------------------------------------------------------------------

MODULE 5 --- ROYALTY MANAGEMENT

Implement a simple royalty tracking system.

Streaming activity should be associated with the relevant
creator/content owner.

The system should support:

-   Stream records
-   Creator association
-   Stream count
-   Configurable royalty rate
-   Royalty calculation
-   Creator earnings
-   Royalty history
-   Creator royalty dashboard
-   Admin royalty management/view

Use a simple transparent formula.

For example:

royalty = eligible_streams × royalty_rate

Do not implement complicated real-world royalty contracts unless
specifically required.

The royalty calculation must be clearly documented.

------------------------------------------------------------------------

MODULE 6 --- DASHBOARD & ANALYTICS

Create role-specific dashboards.

Subscriber/User dashboard:

-   Profile information
-   Subscription status
-   Watch history
-   Recently watched media
-   Basic activity information

Creator dashboard:

-   Uploaded media
-   Published media
-   Stream count
-   Views
-   Earnings
-   Royalty history
-   Basic content statistics

Admin dashboard:

-   Total users
-   Total creators
-   Total media
-   Active subscriptions
-   Streaming activity
-   Royalty information
-   Basic platform statistics

Charts may be implemented using Chart.js if useful.

Do not add unnecessary analytics complexity.

================================================== 6. FRONTEND DESIGN
REQUIREMENT ==================================================

IMPORTANT:

The attached reference image is a VISUAL DESIGN REFERENCE for
MediaMerge.

Use the reference image as the design language and visual inspiration.

DO NOT copy the portfolio content, text, sections, or personal branding
shown in the reference.

Instead, adapt its visual style to the MediaMerge media platform.

The design should feel inspired by the reference while remaining an
original MediaMerge interface.

  -----------------
  VISUAL LANGUAGE
  -----------------

Use the following characteristics from the reference:

-   Dark/near-black primary background
-   Dark navy/charcoal content surfaces
-   Bright accent colors
-   Neon green accents
-   Purple/violet accents
-   Blue accents
-   Yellow accents
-   Pink/orange accents where appropriate
-   Bold and expressive typography
-   Large visual hero section
-   Rounded cards
-   Rounded buttons
-   Strong visual hierarchy
-   Colorful media thumbnails
-   Modern navigation
-   Subtle shadows and borders
-   Creative decorative elements
-   Smooth hover effects
-   Subtle transitions and animations
-   Responsive layouts

The interface should feel:

-   Modern
-   Creative
-   Premium
-   Media-focused
-   Youthful
-   Visually engaging
-   Clean enough for a college project demonstration

Do not make the interface excessively complicated.

  ------------------
  DESIGN PRINCIPLE
  ------------------

DO NOT make every page look exactly like the reference image.

Instead:

Reference image ↓ Extract visual language ↓ Create MediaMerge design
system ↓ Apply consistently across all pages

The screenshot is inspiration for:

-   Color palette
-   Typography
-   Spacing
-   Card styling
-   Buttons
-   Hero composition
-   Visual hierarchy
-   Decorative elements
-   Overall atmosphere

But MediaMerge must have its own layout and content.

  -----------------
  MEDIA HOME PAGE
  -----------------

The homepage should be adapted around media streaming.

Possible structure:

1.  Navbar
    -   MediaMerge logo
    -   Home
    -   Browse
    -   Categories
    -   About
    -   Login/Profile
    -   Subscription
    -   Mobile menu
2.  Hero section
    -   Strong MediaMerge headline
    -   Short platform description
    -   Primary CTA
    -   Secondary CTA
    -   Featured media/visual
    -   Creative decorative elements
3.  Featured Media
    -   Large/highlighted media cards
4.  Browse by Category
    -   Movies
    -   Music
    -   Videos
    -   Documentaries
    -   Other appropriate categories
5.  Recently Added / Trending
    -   Media cards
6.  Platform Features
    -   Stream
    -   Manage
    -   Protect
    -   Track
7.  Footer

Adapt these sections according to actual project functionality.

  -------------
  MEDIA CARDS
  -------------

Media cards should visually match the overall design language.

Cards can include:

-   Thumbnail
-   Title
-   Genre/category
-   Creator
-   Duration
-   Media type
-   Short description
-   View/Play button

Use hover effects where appropriate.

  --------------------
  MEDIA DETAILS PAGE
  --------------------

Create a visually strong media details page containing:

-   Large thumbnail/cover
-   Title
-   Description
-   Creator
-   Genre
-   Language
-   Release information
-   Duration
-   Subscription/access status
-   Play button
-   Relevant metadata

If the user has permission, provide access to the protected video
player.

  --------------
  VIDEO PLAYER
  --------------

The video player page should feel integrated with the dark MediaMerge
design.

Include:

-   Video player
-   Title
-   Creator
-   Description
-   Progress/watch information where appropriate
-   Access/subscription information where appropriate

Do not expose protected media files through unrestricted public URLs.

  ----------------------
  AUTHENTICATION PAGES
  ----------------------

Login and registration pages should follow the same design system.

Use:

-   Dark background
-   Clean centered forms
-   Rounded inputs
-   Bright accent buttons
-   Clear validation/error messages
-   Consistent typography

  -------------------
  SUBSCRIPTION PAGE
  -------------------

Subscription plans should be presented as attractive cards.

Each plan may show:

-   Plan name
-   Price
-   Duration
-   Features
-   Subscribe button
-   Current subscription state

Use the MediaMerge design language.

  ------------
  DASHBOARDS
  ------------

User, Creator, and Admin dashboards should all share the same visual
design system.

Use:

-   Sidebar or top navigation where appropriate
-   Cards
-   Statistics
-   Tables
-   Charts where useful
-   Recent activity
-   Responsive layouts

Creator and Admin dashboards should feel like professional management
interfaces while still matching the overall MediaMerge visual identity.

================================================== 7. RESPONSIVE DESIGN
==================================================

The frontend must work on:

-   Desktop
-   Laptop
-   Tablet
-   Mobile

Do not design only for one screen size.

Navigation, cards, grids, dashboards, forms, and media players should
adapt appropriately.

================================================== 8. FRONTEND
IMPLEMENTATION RULES ==================================================

Use:

-   Django Templates
-   HTML5
-   CSS3
-   Vanilla JavaScript

Use reusable Django template components where appropriate.

Avoid unnecessary duplicated HTML/CSS.

Create a consistent design system for:

-   Colors
-   Typography
-   Buttons
-   Cards
-   Forms
-   Navigation
-   Spacing
-   Borders
-   Shadows
-   Animations

Prefer CSS variables for the main design tokens.

Do not introduce React or another frontend framework just to achieve the
visual design.

================================================== 9. SECURITY
REQUIREMENTS ==================================================

Follow Django security best practices.

Pay particular attention to:

-   Authentication
-   Authorization
-   CSRF protection
-   Password security
-   File upload validation
-   Media access control
-   Subscription verification
-   Temporary access tokens
-   Token expiration
-   Protected media delivery
-   Preventing unauthorized creator/admin actions
-   Preventing users from accessing another user's protected information

Never rely exclusively on frontend restrictions.

================================================== 10. DATABASE
REQUIREMENTS ==================================================

Use MySQL.

Design relationships carefully between:

-   Users
-   Roles
-   Creators
-   Media
-   Categories
-   Subscriptions
-   Subscription plans
-   Streaming records
-   Watch history
-   Royalty records
-   Access tokens where required

Do not create unnecessary tables.

Use Django migrations.

================================================== 11. DEVELOPMENT
APPROACH ==================================================

Do NOT immediately start writing all features.

First:

1.  Inspect the repository.
2.  Inspect existing code.
3.  Inspect git status.
4.  Identify existing functionality.
5.  Identify existing dependencies.
6.  Identify existing database configuration.
7.  Identify existing frontend structure.
8.  Identify whether any work has already been completed.
9.  Compare the existing project with these requirements.
10. Create/update the .agent documentation according to the Agent
    Operating System.

Then create an implementation plan.

Do not destroy existing working code.

Preserve unrelated user changes.

================================================== 12. PHASED
IMPLEMENTATION ==================================================

Implement in this order:

PHASE 0 --- Discovery - Repository inspection - Requirements
confirmation - Architecture decision - Frontend design system - Existing
work analysis

PHASE 1 --- Foundation - Django configuration - MySQL connection -
Static files - Media files - Templates - Base layout - Base CSS/design
system - Environment configuration - Initial database setup

PHASE 2 --- Core Features - Authentication - Roles - Media management -
Search/filtering - Subscription system - Streaming - Watch history

PHASE 3 --- Protection & Business Logic - Protected media access - Demo
DRM - Temporary access - Royalty management

PHASE 4 --- Dashboards - User dashboard - Creator dashboard - Admin
dashboard - Analytics

PHASE 5 --- Integration - Connect all modules - End-to-end flows - UI
consistency - Error handling

PHASE 6 --- Testing & Verification - Django checks - Unit tests -
Integration tests - Authentication tests - Authorization tests - Media
access tests - Subscription tests - Streaming tests - DRM tests -
Royalty tests - Dashboard tests - Frontend verification - Git diff
inspection

================================================== 13. REQUIREMENT
TRACEABILITY ==================================================

For every major requirement maintain:

Requirement → Implementation → Files → Test → Verification

Do not claim something is complete unless it has actually been
implemented and verified.

If something has not been tested, state:

UNKNOWN --- needs verification

Never invent successful test results.

================================================== 14. GIT RULES
==================================================

Before major changes:

-   Check git status
-   Inspect relevant files
-   Understand existing changes

After major changes:

-   Inspect git diff
-   Verify only intended files changed
-   Run appropriate tests/checks

Do not overwrite unrelated user work.

Do not perform destructive git operations unless explicitly instructed.

================================================== 15. AGENT
DOCUMENTATION ==================================================

Maintain the .agent directory required by the Antigravity Agent
Operating System.

Keep these documents updated:

-   AGENTS.md
-   SKILLS.md
-   PHASE.md
-   STATE.md
-   REMAINING.md
-   DECISIONS.md
-   VERIFICATION.md
-   HANDOFF.md
-   ERRORS.md
-   CHANGELOG.md
-   CHECKLIST.md

These files must reflect actual repository state.

Do not write fictional completion status.

================================================== 16. IMPORTANT DESIGN
DECISION ==================================================

The reference image is NOT a requirement to reproduce the exact webpage.

It is a visual reference.

Therefore:

DO: - Use its dark creative aesthetic - Use bright accent colors - Use
strong visual hierarchy - Use rounded media cards - Use expressive
typography - Use creative decorative elements - Use modern animations -
Adapt the design to MediaMerge

DO NOT: - Copy its text - Copy its personal portfolio content - Copy its
branding - Copy its exact sections - Copy its exact illustrations - Turn
MediaMerge into a portfolio website - Make every page identical to the
screenshot

Create an ORIGINAL MediaMerge interface inspired by the visual language
of the reference.

================================================== 17. FIRST TASK
==================================================

Do NOT begin implementing all modules immediately.

Your first task is:

1.  Inspect the repository completely enough to understand its current
    state.
2.  Inspect git status and existing changes.
3.  Identify the current project structure.
4.  Identify what is already implemented.
5.  Compare the repository against the MediaMerge requirements above.
6.  Analyze the attached frontend reference image.
7.  Create a MediaMerge frontend design specification based on that
    image.
8.  Determine the appropriate Django architecture.
9.  Update the .agent documentation.
10. Create a clear phased implementation plan.
11. Report what you found.

Do not start large-scale feature implementation until the discovery
phase has been completed and documented.

At the end of this first task, clearly report:

-   Current repository state
-   Existing implementation
-   Missing requirements
-   Proposed architecture
-   Frontend design system
-   Implementation phases
-   Current blockers
-   Exact next action

Remember:

CORRECTNESS \> SPEED

PRESERVE EXISTING WORK

VERIFY BEFORE CLAIMING

DO NOT HALLUCINATE

DO NOT MARK WORK COMPLETE WITHOUT EVIDENCE
