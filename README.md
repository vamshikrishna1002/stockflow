# StockFlow

A minimal multi-tenant SaaS inventory management app built with Django and MySQL.
Each organization has its own isolated products and settings.

## Features

- Signup and login with email, password and organization name
- Multi-tenant data: every query is scoped to the user's organization
- Product CRUD (name, SKU, quantity, cost price, selling price, low-stock threshold)
- SKU unique per organization
- Quick stock adjustment (+/- units) with a note
- Dashboard: total products, total units, low-stock items
- Settings: default low-stock threshold

## Tech Stack

- Python 3.13
- Django 4.2
- MySQL 8
- HTML and CSS (Django templates)

## Project Structure

```
stockflow/
├── manage.py
├── stockflow/        # project settings and root URLs
├── inventory/        # models, views, forms, urls
├── templates/        # base, auth and inventory templates
├── static/           # style.css
└── requirements.txt
```

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd stockflow
python -m venv myenv
myenv\Scripts\activate        # Mac/Linux: source myenv/bin/activate
pip install -r requirements.txt
```

### 2. Create the MySQL database

```sql
CREATE DATABASE stockflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure the database

In `stockflow/settings.py`, set your MySQL user and password under `DATABASES`.

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign up to create your organization.

## Usage

1. Sign up with email, password and organization name.
2. Add products from the Products page.
3. Use Adjust to change stock by +/- units.
4. Check the Dashboard for totals and low-stock items.
5. Change the default low-stock threshold under Settings.

## Low-Stock Logic

A product is low stock when `quantity <= threshold`. If a product has no
threshold of its own, the organization's default threshold (initially 5) is used.

## Out of Scope (MVP)

Multi-warehouse, variants, integrations, purchase orders, email notifications,
CSV import, external API, roles and permissions, audit logs, billing.

## Author

Akula Vamshikrishna