# MediaMerge Deployment to Render

This guide outlines the steps to deploy the MediaMerge Django project to [Render](https://render.com/).

## 1. Prerequisites
- A Render account.
- A GitHub repository containing the MediaMerge code.
- A managed MySQL database (e.g., Aiven, AWS RDS, PlanetScale, or self-hosted). 
  *Note: Render does not provide managed MySQL databases natively (only PostgreSQL). You must provision a MySQL instance externally.*

## 2. Infrastructure Setup

### MySQL Database
Create a MySQL database and retrieve the following credentials:
- **DB_HOST**: The hostname of your MySQL database.
- **DB_PORT**: The port (typically 3306).
- **DB_NAME**: The database name.
- **DB_USER**: The database user.
- **DB_PASSWORD**: The password for the user.

Ensure your external MySQL instance accepts connections from Render's IP addresses, or allow all IPs (`0.0.0.0/0`) if properly secured with strong passwords.

## 3. Project Configuration for Production
The project has been prepared for production:
- **`settings.py`**: Uses `os.getenv` for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and Database configuration.
- **`WhiteNoise`**: Configured to serve static files in production.
- **`gunicorn`**: Added to `requirements.txt` as the production WSGI HTTP server.
- **`render.yaml`**: A blueprint file that describes the Web Service for Render.

## 4. Deploying via Blueprint (render.yaml)

1. Go to the [Render Dashboard](https://dashboard.render.com/).
2. Click **New** -> **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect the `render.yaml` file.
5. You will be prompted to enter values for the following environment variables (which are set to `sync: false` in `render.yaml`):
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
6. Click **Apply**.
7. Render will build the environment (`bash build.sh`), run `collectstatic`, run database migrations, and start the app using `gunicorn mediamerge_project.wsgi:application`.

## 5. Deploying Manually (Web Service)

If you prefer not to use the Blueprint:
1. Go to the Render Dashboard and click **New** -> **Web Service**.
2. Connect your repository.
3. Use the following settings:
   - **Environment**: `Python`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn mediamerge_project.wsgi:application`
4. Add the following **Environment Variables**:
   - `PYTHON_VERSION`: `3.13.0` (or match your local version)
   - `SECRET_KEY`: Generate a random secure string.
   - `DEBUG`: `False`
   - `DB_HOST`: Your MySQL host
   - `DB_PORT`: `3306`
   - `DB_NAME`: Your MySQL database name
   - `DB_USER`: Your MySQL username
   - `DB_PASSWORD`: Your MySQL password
5. Click **Create Web Service**.

## 6. Verifying Deployment

After deployment is successful, Render will provide a URL like `https://mediamerge-xyz.onrender.com`.
The `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` are automatically populated using the `RENDER_EXTERNAL_HOSTNAME` environment variable injected by Render, so no further configuration of hosts is required.

## 7. Notes on Data
This project uses MySQL. Since no migration to PostgreSQL was performed, ensure you back up and restore your existing MySQL data (e.g., the 50,000 `MovieDatasetRecord` rows) to your new production MySQL database using tools like `mysqldump`.
