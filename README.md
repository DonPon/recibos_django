# Recibos Django

This is a Django application for managing receipts, contracts, and tenants. It allows users to generate PDF receipts, manage contracts, and automatically send receipts to tenants via email.

## Features

*   **User Authentication:** Users can log in to access the application.
*   **PDF Generation:** Generate PDF receipts for tenants.
*   **Automatic Emailing:** Automatically send receipts to tenants via email.
*   **Tenant Management:** Add, update, and delete tenant information.
*   **Contract Management:** Manage tenant contracts.
*   **On-Demand Services:** Generate on-demand receipts and other documents.
*   `newsletter`: Handles newsletter subscriptions. This app is responsible for generating and sending two types of newsletters: a weekly property newsletter and a weekend newsletter. It uses the `ask_gemini` function to generate the content of the newsletters.

## Project Structure

The project is divided into four main Django apps:

*   `recibos_django`: The main Django project directory.
    *   `mixins.py`: Provides a mixin for adding environment variables and the current year to the view context.

*   `recibos`: Core functionality for generating receipts and managing tenants.
*   `contratos`: Manages tenant contracts. This app allows users to create, update, delete, and view contracts. It also includes a feature to send reminders for expiring contracts.
*   `on_demand`: Provides on-demand services, such as generating specific documents. This app allows for the one-time generation of on-demand receipts and agreements.
*   `src`: Contains source code for utility functions, such as email sending, PDF generation, and date parsing.
    *   `ai_utils.py`: Contains functions for interacting with the Gemini and Apertus AI models to generate content for the newsletters.
    *   `src_dates.py`: Contains functions for parsing date strings and checking if a date is a certain number of days away from the current date.
    *   `src_email.py`: Contains a function for sending emails with optional attachments, used by other modules to send receipts, contracts, and newsletters.
    *   `src_pdf_utils.py`: Contains functions for creating and sending various types of PDF documents, including contracts, receipts, and termination agreements.
    *   `strings.py`: Handles string formatting, date/number to text conversions, and the construction of different contract types.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/recibos_django_git.git
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up the database:**

    *   The project is configured to use a PostgreSQL database in production and a local database for development.
    *   Make sure you have PostgreSQL installed and configured.
    *   Create a `.env` file in the root directory and add the following environment variables:

        ```
        SECRET_KEY=your-secret-key
        DATABASE_URL=your-database-url
        ENV=dev
        FROM_EMAIL=your-email@example.com
        SMTP_PASSWORD=your-smtp-password
        ```

4.  **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## Usage

*   Access the application at `http://127.0.0.1:8000/`.
*   Log in with your credentials.
*   Use the navigation menu to access the different features of the application.

## Deployment

The `build.sh` script is provided for deployment. It installs the required dependencies, collects static files, and runs database migrations.

```bash
./build.sh
```
