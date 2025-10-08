# Simple E-Shop (Flask)

## Description
Small e-commerce demo built with Flask, Bootstrap, jQuery and SQLite. Implements product listing, product detail, session-based cart, and a checkout form.

## Features
- Product listing & detail pages
- Session cart (add/update/remove)
- Checkout (client/server validation)
- SQLite (Flask-SQLAlchemy)
- Bootstrap for responsive UI

## Setup
1. python3 -m venv venv
2. source venv/bin/activate   (Windows: venv\\Scripts\\Activate.ps1)
3. pip install -r requirements.txt
4. python app.py
5. Open http://127.0.0.1:5000

## Git commits
Use these commit messages:  
chore: project scaffold  
feat(db): add Product model and DB initialization  
feat(ui): add Jinja2 templates (base, index, product, cart, checkout)  
feat(ui): add styles and client JS (form validation, flash fade)  
feat(cart): add session-based cart and update flow  
feat(checkout): checkout form and confirmation  
docs: add README and screenshots

## Screenshots
Place screenshots in `static/images/screenshots/` and reference them here.

