# Learning Log

## Phase 0
- Confirmed local environment: Python 3.12.11 and Git 2.53.0.
- Learned the difference between Django, virtual environments, projects, apps, models, migrations, and SQLite.
- Planned the long-term farm-management roadmap.
- Proposed the initial entity model for farms, fields, crops, livestock, products, stock movements, sales, purchases, and expenses.

## Phase 1
- Created the local project structure and virtual environment setup.
- Installed Django and started the project.
- Learned the difference between the Django project and individual apps.
- Added a user profile model to represent admin, manager, and worker roles.
- Added the first authentication and dashboard flow.
- Verified tests pass for user-profile creation and dashboard access.

## Phase 2
- Added the `farms` app with Farm and Field models.
- Verified login-protected farm list pages.
- Learned how a ForeignKey connects records in a parent-child relationship.

## Phase 3
- Added the `crops` app with crop records linked to farms and optional fields.
- Learned how planting dates, area, and status fit into a crop model.
- Verified crop creation and list behavior through tests.

## Phase 4
- Added the `livestock` app with animal records tied to a farm.
- Learned to separate livestock from crop data even though both belong to the same farm.
- Verified login-protected livestock pages.

## Phase 5
- Added the `customers` app and basic customer records.
- Learned why customer data must stay separate from farm data for better data migration and reporting.
- Verified customer list behavior.

## Phase 6
- Added the `suppliers` and `products` apps.
- Learned the difference between a supplier and a customer.
- Verified supplier and product list behavior.

## Phase 7
- Added the `inventory` app and `StockMovement` model.
- Learned why inventory should be audited through movement records instead of a single quantity field.
- Verified stock movement tracking.

## Phase 8
- Added the `purchases` app with purchase headers and item lines.
- Learned how item-level records keep purchase data organized and auditable.
- Verified purchase list behavior.

## Phase 9
- Added the `sales` app with sale headers and item lines.
- Learned how sales are the customer-side counterpart to purchases.
- Verified sales list behavior.

## Phase 10
- Added the `expenses` app for tracking operational costs separately from sales.
- Learned why expenses and sales belong in separate data streams for truthful profit calculation.
- Verified expenses list behavior.

## Phase 11
- Added dashboard summary logic for sales, expenses, inventory activity, and profit.
- Learned how to aggregate separate data sources into one view without mixing the source records.
- Fixed formatting so Decimal totals display in a clear money format.

## Phase 12
- Added a reusable `role_required` decorator for role-based authorization.
- Restricted business management list pages to administrators and managers.
- Kept the dashboard available to every authenticated user.
- Verified that workers receive HTTP 403 while managers and administrators can access management pages.
- Learned why login authentication and role authorization are separate checks.

## Commands used
- `python -m venv .venv`
- `python -m pip install --upgrade pip`
- `python -m pip install django`
- `django-admin startproject farm_management .`
- `python manage.py startapp users`
- `python manage.py makemigrations ...`
- `python manage.py migrate`
- `python manage.py test users`
- `python manage.py test farms`
- `python manage.py test crops`
- `python manage.py test livestock`
- `python manage.py test customers`
- `python manage.py test suppliers`
- `python manage.py test products`
- `python manage.py test inventory`
- `python manage.py test purchases`
- `python manage.py test sales`
- `python manage.py test expenses`

## Mistakes encountered
- Initial project setup failed because the PowerShell environment used the wrong Python interpreter and certificate path.
- URL namespace errors occurred before the app routes were properly namespaced.
- The dashboard summary initially rendered Decimal values without two decimal places.

## Next phase
- Build a stricter dashboard and add user-role authorization rules for admin, manager, and worker access.
