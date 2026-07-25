# Inventory Management System (Python REST API with Flask)

An administrator portal RESTful API and CLI tool built using Flask to manage product inventory and integrate with external product data.

---

## Project Architecture

- **Backend API:** Built with Flask providing full CRUD operations for inventory items.
- **External API Integration:** Queries the **Open Food Facts API** via barcode or product name to fetch product details and enrich local inventory.
- **CLI Interface:** A command-line tool serving as the front-end interface for admins to manage stock, update prices, and fetch external items.
- **Testing:** Unit tests written using `pytest` and `unittest.mock` for API routes and CLI commands.

---
