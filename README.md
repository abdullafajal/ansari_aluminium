# Ansari Aluminium

A comprehensive web application for managing Aluminium and UPVC window and door fabrication business.

## Features

- **Product Catalog**: Showcase Aluminium & UPVC products with dynamic categorization.
- **Quotation System**: Generate professional PDF quotations for customers.
- **Order Management**: Track orders from enquiry to delivery.
- **Billing & Invoicing**: Generate GST-compliant invoices.
- **Customer Management**: CRM features to manage customer details and history.
- **Dashboard**: Admin dashboard for business insights and management.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: PostgreSQL (Production), SQLite (Development)
- **PDF Generation**: WeasyPrint

## Setup

1. Clone the repository.
2. Create virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -r requirements.txt` (or use `uv`)
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`
