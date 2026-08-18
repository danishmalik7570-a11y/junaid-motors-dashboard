# Junaid Motors — Car Dealership Management System

A full-featured, modern Car Dealership Management System built with **Django 5** and a premium executive UI theme with simple primary blue sidebar navigation. Manages inventory, sales, customer CRM, purchase history, installment tracking, lead kanban pipelines, staff roles, and financial reports.

---

## 🚀 Quick Start

### 1. Run with Batch Script (Windows)
Double-click `run_dashboard.bat` in the root folder, or run in PowerShell / Command Prompt:
```cmd
run_dashboard.bat
```

### 2. Run Manually via Terminal
```bash
cd Django-Stack/cardealer
python manage.py runserver 8000
```
Then open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 🔐 Default Login Credentials

- **Login URL**: `http://127.0.0.1:8000/staff/login/`
- **Username**: `admin`
- **Password**: `admin123`

---

## ✨ Features & Modules

- 📊 **Dashboard**: Real-time KPI cards (cars available, monthly revenue, profit, overdue installments, new leads), 6-month sales revenue chart, vehicle status breakdown, and quick actions.
- 🚗 **Inventory Management**: Complete car stock CRUD with photo uploads, cost price, selling price, profit preview, and stock age alerts.
- 🧾 **Sales & Invoicing**: Streamlined sale entry wizard, automated invoice generation (`INV-XXXXX`), print-ready invoice view, and automatic installment schedule creation.
- 🛒 **Purchases**: Acquisition management for buying inventory from sellers with commission tracking.
- 📅 **Installments Tracker**: Automated overdue status detection (`overdue_count`), real-time notification badge on top bar and sidebar, and one-click payment processing.
- 📋 **Lead Management (Kanban)**: 5-stage interactive drag/stage pipeline (*New → Follow-up → Test Drive → Negotiating → Converted*) across multiple acquisition channels (Facebook, WhatsApp, Walk-in, Referral, Website, Phone).
- 👥 **Customer CRM**: Complete buyer database with contact information, total purchase history, and outstanding balance tracking.
- 📈 **Financial Reports**: Daily, monthly, and Profit & Loss (P&L) performance breakdowns with Chart.js charts and slow-moving inventory warnings.
- 🛡️ **Staff Management**: Role-based access (Admin, Manager, Sales Agent) with custom staff profiles.

---

## 🎨 Design & Theme

- **Primary Blue Sidebar**: Simple, modern primary blue theme (`#1D4ED8` / `#1E40AF`) with glowing section headers and crisp active tab indicators.
- **Executive Slate Body**: Clean Slate & White background system (`#F8FAFC` background with pure white `#FFFFFF` cards) designed for high readability.
- **Currency**: Pakistani Rupee (`PKR`) formatting throughout the application.

---

## 📁 Project Structure

```
showroom dashboard/
├── run_dashboard.bat                  # Batch launcher script
├── README.md                          # Main project documentation
└── Django-Stack/
    └── cardealer/                     # Django project root
        ├── manage.py                  # Django CLI entrypoint
        ├── db.sqlite3                 # SQLite database
        ├── cardealer/                 # Core settings & root routing
        ├── apps/                      # Modular application apps
        │   ├── dashboard/             # Main metrics & KPI views
        │   ├── inventory/             # Vehicle CRUD & photo uploads
        │   ├── sales/                 # Sales transactions & invoices
        │   ├── purchases/             # Seller acquisitions
        │   ├── installments/          # Payment tracking & overdue engine
        │   ├── customers/             # Customer CRM database
        │   ├── leads/                 # Kanban lead pipeline
        │   ├── staff/                 # Auth & staff profiles
        │   └── reports/               # Financial & P&L reporting
        ├── static/
        │   ├── css/custom.css         # Executive Primary Blue theme styles
        │   ├── css/animations.css     # UI transitions & micro-interactions
        │   └── js/main.js             # Formatting & Chart.js logic
        └── templates/                 # HTML5 Jinja/Django templates
```

---

## 🛠️ Management Commands

Run all Django commands inside the `Django-Stack/cardealer` directory:

```bash
cd Django-Stack/cardealer

# Apply database migrations
python manage.py migrate

# Create a new administrator


# Seed demo dataset (cars, sales, leads, customers)
python manage.py seed_data
```

---

## 🧰 Technology Stack

- **Backend**: Django 5, Python 3.11/3.13, SQLite
- **Frontend**: HTML5, Vanilla CSS, Bootstrap 5.3, Bootstrap Icons, Tailwind CSS (CDN)
- **Visualizations**: Chart.js 4.4
