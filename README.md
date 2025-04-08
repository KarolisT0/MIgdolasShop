# 🪑 Migdolas – Baldų Parduotuvė 🛒

**Migdolas** is a modern furniture e-commerce platform built with Django. It includes user authentication, product browsing and filtering, shopping cart functionality, and admin management tools.

---

## 📦 Features

- ✅ User registration & login (email-based)
- 🛋️ Product listing with categories and subcategories
- 🔍 Filter by price and search by name (AJAX-powered)
- 🛒 Shopping cart & checkout flow
- 📧 Order confirmation emails
- ⚙️ Admin panel for managing products, orders, and users

---

## ⚙️ Tech Stack

- **Backend**: Django
- **Frontend**: Bootstrap 5, HTML5
- **Database**: PostgreSQL
- **Email**: SMTP via Gmail
- **Media**: User-uploaded product images
- **Environment config**: `python-decouple`

---

## 💻 Installation

### Prerequisites

- Python 3.10+  
- PostgreSQL  
- Git  
- Virtualenv  

---

### 🪟 Windows / 🐧 Linux / 🍎 macOS Setup

```bash
# 1. Clone the project
git clone https://github.com/KarolisT0/MIgdolasShop.git
cd MIgdolasShop/migdolas-store

# 2. Create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create and configure the .env file
cp .env.example .env  # if available, or manually create it

# 5. Setup PostgreSQL database
# Make sure PostgreSQL is installed and running
# Create a database and user matching your .env values

# 6. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 7. Create superuser for admin access
python manage.py createsuperuser

# 8. Run the server
python manage.py runserver



# ⚙️ Admin Panel

http://localhost:8000/admin/



## 🙋 Author


Built by [Karolis Tomkus](https://github.com/KarolisT0)