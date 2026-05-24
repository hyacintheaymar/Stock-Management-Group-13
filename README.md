# Stock Management System — BIT

**PRG1406 — Advanced Programming (Python and C)**  
Burkina Institute of Technology · Group Assignment 1 · May 2026

---

## What the program does

A command-line stock management system for a small store or warehouse.  
It allows users to:

- Add standard products or perishable products to the stock
- View the full inventory with low-stock warnings
- Search for a product by name
- Update the quantity of any product in stock
- Automatically calculate profit margins and total stock value

The program runs entirely in the terminal with a numbered menu.  
All inputs are validated — the program never crashes on bad user input.

---

## Classes

### `Product` (parent class)

Represents a standard product in the stock.

| Feature | Detail |
|---|---|
| Attributes | `name`, `category`, `supplier`, `unit`, `quantity`, `min_stock`, `purchase_price`, `selling_price`, `is_available`, `is_perishable` |
| `__str__` | Pretty-prints the product when you call `print(product)` |
| `__repr__` | Technical representation used in Python shell / lists |
| `__eq__` | Compares two products by name: `product_a == product_b` |
| `__len__` | Returns the quantity in stock: `len(product)` |
| `@property margin` | Profit in FCFA: `product.margin` |
| `@property margin_percent` | Profit as %: `product.margin_percent` |
| `@property is_low_stock` | `True` if quantity < min_stock |
| `@staticmethod validate_price(price)` | Returns `True` if the price is strictly positive |
| `@classmethod from_dict(data)` | Creates a `Product` instance from a dictionary |

### `PerishableProduct` (child class — inherits from `Product`)

Extends `Product` with an expiry date. The child **IS** a `Product`.

| Feature | Detail |
|---|---|
| Extra attribute | `expiry_date` (Python `date` object) |
| `super().__init__()` | Calls the parent constructor |
| `__str__` | Adds expiry date and expiry status to the parent display |
| `__repr__` | Includes `expiry_date` in the technical representation |
| `@property is_expired` | `True` if today is past the expiry date |
| `@property days_until_expiry` | Number of days left before expiry |
| `@classmethod from_dict(data)` | Creates a `PerishableProduct` from a dictionary |

---

## How to run

**Requirements:** Python 3.8 or higher — no external libraries needed.

```bash
# Clone the repository
git clone https://github.com/hyacintheaymar/Stock-Management-Group-13.git
cd <Stock-Management-Group-13>

# Run the program
python3 stock_management.py
```

Then follow the on-screen menu:

```
=======================================================
       SYSTÈME DE GESTION DE STOCK — BIT
=======================================================
  1. Ajouter un produit
  2. Ajouter un produit périssable
  3. Afficher tout le stock
  4. Rechercher un produit
  5. Mettre à jour la quantité d'un produit
  6. Quitter
=======================================================
```

---

## Concepts covered (Assignment requirements)

| Requirement | Where |
|---|---|
| `str`, `int`, `float`, `bool` — all four types | `get_product_inputs()` |
| Correct boolean pattern | `is_available = input(...).lower() == "oui"` |
| ≥ 10 `input()` calls with correct casting | `get_product_inputs()`, `get_perishable_inputs()`, `main()` |
| ≥ 3 arithmetic expressions | `calculate_margin()`, `calculate_margin_percent()`, `calculate_stock_value()` |
| Input validation — `while` + `try/except` | `get_valid_int()`, `get_valid_float()`, expiry date parsing |
| `f-strings` + summary screen | `__str__` methods + `display_stock()` |
| Parent class + child class | `Product` → `PerishableProduct` |
| `super().__init__()` | `PerishableProduct.__init__()` |
| Child adds new attributes/methods | `expiry_date`, `is_expired`, `days_until_expiry` |
| Magic methods | `__str__`, `__repr__`, `__eq__`, `__len__` |
| Decorators | `@property`, `@staticmethod`, `@classmethod` |

---

## Group 13 — Task distribution

| Member | Name | Responsibility |
|---|---|---|
| Member 1 | YAMEOGO Wendgoundi Hyacinthe Aymar | Main menu structure, 14 `input()` calls, 4 data types |
| Member 2 | KABORE Karelle Aurélie | Input validation (`while` + `try/except`), arithmetic calculations |
| Member 3 | YAMEOGO Claudine | `Product` and `PerishableProduct` classes, inheritance, `super()` |
| Member 4 | PARE Boris Marcel | Magic methods — `__str__`, `__repr__`, `__eq__`, `__len__` |
| Member 5 | ZOMA Boudnooma Amélie | Decorators — `@property`, `@staticmethod`, `@classmethod` + README + GitHub |
