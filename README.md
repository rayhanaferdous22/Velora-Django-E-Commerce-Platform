# VELORA — Django E-Commerce Platform

A modular Django e-commerce project: separate apps per domain, business
logic isolated in `services.py` so `views.py` stays thin, secrets loaded
from `.env`, and a documented plan for the next round of features.

## App structure

```
velora/
├── accounts/         # Auth, profile, address book
├── category/         # Product categories
├── products/         # Product catalog + search
├── cart/              # Shopping cart
├── orders/            # Checkout, order history
├── payments/          # Payment processing (stub gateway)
├── dashboard/         # Staff-only admin stats
├── store/              # Public storefront landing page
├── docs/
│   └── future_features.md   # Wishlist, Reviews, Coupons, Notifications — planned
├── templates/
├── static/
├── velora_project/    # Settings/urls
├── .env                # Local secrets (NOT committed — see .env.example)
├── .env.example
└── requirements.txt
```

Every app with real business rules follows the same shape:
`models.py` → `services.py` (all the logic) → `views.py` (thin: parse
request, call a service function, render/redirect) → `urls.py` → `admin.py`.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env            # then fill in real values
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Environment variables (`.env`)

`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, database, email (`EMAIL_BACKEND`,
`EMAIL_HOST`, etc.), and `PAYMENT_GATEWAY_API_KEY` are all read from `.env`
via `python-dotenv` in `velora_project/settings.py` — nothing sensitive is
hardcoded. `.env` is git-ignored; `.env.example` documents every variable
so a new environment can be set up without guessing.

## What's implemented

- **accounts** — register, login (username or email), logout, forgot/reset
  password, optional email verification, profile + address book, change
  password.
- **category** / **products** — active-only catalog, category browsing,
  keyword search.
- **cart** — add/update/remove items, stock-aware (`services.is_purchasable`
  is shared between `cart` and `orders`).
- **orders** — checkout snapshots the cart into an `Order` + `OrderItem`s
  inside a DB transaction (`orders/services.py::create_order_from_cart`):
  stock is decremented, the cart is cleared, and the order total is
  computed — all atomically, so a failure partway through can't leave a
  half-placed order.
- **payments** — `payments/services.py::process_payment` is a stub gateway
  (always succeeds) so checkout can be exercised end-to-end today; swap its
  body for a real provider's SDK later without touching `orders`.
- **dashboard** — staff-only (`accounts.decorators.admin_required`) view
  aggregating user/product/order counts and total revenue.

## Planned next (see `docs/future_features.md`)

- **Wishlist** — save-for-later, separate from the cart.
- **Product Reviews** — verified-purchase ratings on `products.Product`
  (a commented-out `Review` model is sketched at the bottom of
  `products/models.py`).
- **Coupons/Discounts** — a `coupons` app that plugs into
  `orders.services.create_order_from_cart`.
- **Notifications** — in-app + email notifications hooked into order and
  payment events.

Each is scoped with enough detail in `docs/future_features.md` to build
without redesigning what's already here.

## Notes for production

`python3 manage.py check --deploy` will flag standard settings you should
change before going live (set real env vars, not defaults):

- Long random `SECRET_KEY`, `DEBUG=False`, real `ALLOWED_HOSTS`.
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` once
  serving over HTTPS.
- A real `EMAIL_BACKEND` (SMTP/API) instead of the console backend.
- Postgres/MySQL instead of SQLite.
- A real payment gateway SDK in `payments/services.py::process_payment`.

## Verified

This refactor was exercised end-to-end with Django's test client covering
every app in one pass: seed a category + product → browse/search the
catalog → register → verify email → log in → add an address → add/update
cart items → checkout (order created, stock decremented, cart cleared,
atomic) → pay via the stub gateway (order marked paid) → confirm a
non-staff user is blocked from `/dashboard/` while a staff user sees
correct aggregate stats. `manage.py check` and `makemigrations` both ran
clean with zero errors before delivery.
