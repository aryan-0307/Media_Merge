# MediaMerge

MediaMerge is a college-level academic project demonstrating a comprehensive, unified subscription-based media streaming platform.

## Project Overview
MediaMerge allows creators to upload and publish media content while providing subscribers access to free and premium streaming options. The platform includes role-based access, content protection, streaming analytics, and a royalty calculation engine for creators.

## Features
- **Authentication & Roles**: Custom user model supporting three distinct roles: Subscriber, Creator, and Admin.
- **Media Management**: Creators can upload, edit, and publish premium and free content securely.
- **Academic DRM & Protection**: Premium video files are stored outside the public media directory and delivered sequentially through one-time, time-limited Access Tokens verified via active subscription validations.
- **Interactive Dashboards**: Role-tailored experiences aggregating Watch Histories, Financial Royalties, and Platform-wide performance.
- **Financial Processing Engine**: Logic mapping authorized StreamingRecords directly into RoyaltyRecords using high-precision Decimal arithmetic.

## Technology Stack
- **Backend:** Python 3.13 / Django 5.x
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Chart.js
- **Database:** MySQL

## User Roles
- **Subscriber**: Can browse the catalog, purchase subscriptions, and stream authorized media.
- **Creator**: Can upload and manage media assets, view their earnings, and access creator dashboards.
- **Admin**: Has full platform oversight, including system-wide analytics and processing royalty payouts.

## Main Modules
- **accounts**: User registration, login, and profile management.
- **catalog**: Media asset management, catalog browsing, and access token generation.
- **subscriptions**: Subscription plans and checkout simulation.
- **royalties**: Streaming records aggregation and royalty payouts calculation.
- **analytics**: Administrative dashboards and platform statistics.

## Setup Instructions

1. **Clone the Repository**

2. **Create and Activate a Virtual Environment**
   `ash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   `

3. **Install Dependencies**
   `ash
   pip install -r requirements.txt
   `

4. **Environment Configuration**
   Copy .env.example to .env or create a .env file in the root directory.

5. **MySQL Configuration**
   The project is configured to use MySQL. Ensure you have a running MySQL server with a database named mediamerge.
   Update your .env file with the database credentials:
   `env
   DB_NAME=mediamerge
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_HOST=127.0.0.1
   DB_PORT=3306
   `

6. **Run Migrations**
   `ash
   python manage.py migrate
   `

7. **How to Run**
   Start the Django development server:
   `ash
   python manage.py runserver
   `

## How to Run Tests

The project uses Django's automated app-based test discovery. The test suite covers accounts, catalog, subscriptions, royalties, and analytics.

To run the complete test suite:
`ash
python manage.py test
`
Django will automatically discover and execute the 26 tests across the application.

## Demo DRM Limitation
*Note on DRM: The media protection mechanics implemented here (Tokenized Routing & FileResponse) represent an academic/demo simulation. This is NOT a commercial DRM solution such as Widevine, PlayReady, or FairPlay. Production environments require hardware-level DRM and backend byte-range reverse proxy deployments.*

## Final Verification Status
- **Database**: Django is connected to MySQL (mediamerge).
- **System Check**: Passes with 0 issues (python manage.py check).
- **Automated Tests**: Complete test suite of 26 tests passing successfully.
