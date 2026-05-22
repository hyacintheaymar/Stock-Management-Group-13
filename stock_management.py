# =============================================================
# PRG1406 — Advanced Programming (Python and C)
# Group Assignment 1 — Stock Management System
# Burkina Institute of Technology
# =============================================================
# MEMBRE 1 — Structure générale + Inputs
#   ✔ Menu principal
#   ✔ Au moins 10 input() avec cast correct
#   ✔ Utilisation correcte de str, int, float, bool
# =============================================================
#
# NOTE AUX AUTRES MEMBRES :
#   Membre 2  → cherche les balises TODO:MEMBRE2 pour ajouter
#               la validation (while + try/except) et les calculs
#   Membre 3  → cherche TODO:MEMBRE3 pour créer les classes
#               Product (parent) et PerishableProduct (enfant)
#   Membre 4  → cherche TODO:MEMBRE4 pour ajouter __str__ et
#               les autres magic methods dans les classes
#   Membre 5  → cherche TODO:MEMBRE5 pour ajouter les décorateurs
#               (@staticmethod / @classmethod / @property)
# =============================================================


# ── Données temporaires (seront remplacées par les objets de Membre 3) ──
# Le stock est une liste de dictionnaires pour l'instant.
# Membre 3 devra remplacer ces dicts par des instances de ses classes.
stock: list = []
# ─────────────────────────────────────────────
#  MEMBRE 2 — Calculations + Validation
# ─────────────────────────────────────────────

def get_valid_int(prompt: str) -> int:
    """Asks for an integer, re-prompts if invalid."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("  ⚠ Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("  ⚠ Invalid integer. Please try again.")


def get_valid_float(prompt: str) -> float:
    """Asks for a float, re-prompts if invalid."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("  ⚠ Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("  ⚠ Invalid number. Please try again.")


def calculate_margin(purchase_price: float, selling_price: float) -> float:
    """Calculates the profit margin in FCFA."""
    return selling_price - purchase_price


def calculate_margin_percent(purchase_price: float, selling_price: float) -> float:
    """Calculates the margin as a percentage."""
    if purchase_price == 0:
        return 0.0
    return ((selling_price - purchase_price) / purchase_price) * 100


def calculate_stock_value(quantity: int, selling_price: float) -> float:
    """Calculates the total stock value for a product."""
    return quantity * selling_price

# ─────────────────────────────────────────────
#  AFFICHAGE DU MENU PRINCIPAL
# ─────────────────────────────────────────────

def display_menu() -> None:
    """Affiche le menu principal du système de gestion de stock."""
    print("\n" + "=" * 55)
    print("       SYSTÈME DE GESTION DE STOCK — BIT")
    print("=" * 55)
    print("  1. Ajouter un produit")
    print("  2. Afficher tout le stock")
    print("  3. Rechercher un produit")
    print("  4. Mettre à jour la quantité d'un produit")
    print("  5. Quitter")
    print("=" * 55)


# ─────────────────────────────────────────────
#  COLLECTE DES INPUTS — AJOUT D'UN PRODUIT
# ─────────────────────────────────────────────

def get_product_inputs() -> dict:
    """
    Collecte toutes les informations nécessaires pour un nouveau produit.

    Types utilisés :
        str   → nom, catégorie, fournisseur, unité de mesure
        int   → quantité en stock, seuil minimum
        float → prix d'achat, prix de vente
        bool  → disponible à la vente, produit périssable
              (pattern correct : input().lower() == "oui")

    Returns:
        dict contenant les données du produit saisi.
        TODO:MEMBRE3 → remplacer le dict de retour par un objet Product.
    """
    print("\n" + "-" * 45)
    print("   AJOUT D'UN NOUVEAU PRODUIT")
    print("-" * 45)

    # ── str ──────────────────────────────────────────
    product_name: str = input("Nom du produit            : ").strip()           # input 1
    category: str     = input("Catégorie                 : ").strip()           # input 2
    supplier: str     = input("Fournisseur               : ").strip()           # input 3
    unit: str         = input("Unité de mesure (pièce/kg): ").strip()           # input 4

    # ── int ──────────────────────────────────────────
    # TODO:MEMBRE2 → entourer ces deux lignes d'un while + try/except
    quantity: int         = get_valid_int("Quantity in stock         : ")       # input 5
    min_stock: int        = get_valid_int("Minimum stock threshold   : ")       # input 6
    purchase_price: float = get_valid_float("Purchase price (FCFA)     : ")    # input 7
    selling_price: float  = get_valid_float("Selling price (FCFA)      : ")    # input 8

    # ── bool — pattern correct ────────────────────────
    is_available: bool  = input("Disponible à la vente ? (oui/non) : ").strip().lower() == "oui"  # input 9
    is_perishable: bool = input("Produit périssable ?    (oui/non) : ").strip().lower() == "oui"  # input 10

    margin      = calculate_margin(purchase_price, selling_price)
    margin_pct  = calculate_margin_percent(purchase_price, selling_price)
    stock_value = calculate_stock_value(quantity, selling_price)

    print(f"\n  📊 Profit margin       : {margin:,.0f} FCFA")
    print(f"  📊 Margin percentage   : {margin_pct:.1f} %")
    print(f"  📊 Total stock value   : {stock_value:,.0f} FCFA")


    product = {
        "name"           : product_name,
        "category"       : category,
        "supplier"       : supplier,
        "unit"           : unit,
        "quantity"       : quantity,
        "min_stock"      : min_stock,
        "purchase_price" : purchase_price,
        "selling_price"  : selling_price,
        "is_available"   : is_available,
        "is_perishable"  : is_perishable,
    }
    return product


# ─────────────────────────────────────────────
#  COLLECTE DES INPUTS — RECHERCHE
# ─────────────────────────────────────────────

def get_search_input() -> str:
    """Demande le terme de recherche à l'utilisateur."""
    print("\n" + "-" * 45)
    print("   RECHERCHE DE PRODUIT")
    print("-" * 45)
    search_term: str = input("Nom du produit à rechercher : ").strip()         # input 11
    return search_term


# ─────────────────────────────────────────────
#  COLLECTE DES INPUTS — MISE À JOUR QUANTITÉ
# ─────────────────────────────────────────────

def get_update_inputs() -> tuple:
    """Collecte le nom du produit et la nouvelle quantité."""
    print("\n" + "-" * 45)
    print("   MISE À JOUR DE LA QUANTITÉ")
    print("-" * 45)
    product_name: str = input("Nom du produit à modifier : ").strip()          # input 12
    new_quantity: int = get_valid_int("New quantity              : ")      # input 13
    return product_name, new_quantity


# ─────────────────────────────────────────────
#  AFFICHAGE RÉSUMÉ — f-strings
# ─────────────────────────────────────────────

def display_summary(product: dict) -> None:
    """
    Affiche un résumé complet d'un produit en utilisant des f-strings.
    TODO:MEMBRE4 → quand __str__ sera implémenté dans la classe Product,
                   remplacer cet affichage par print(product_object).
    """
    available_label  = "Oui ✔" if product["is_available"]  else "Non ✘"
    perishable_label = "Oui ✔" if product["is_perishable"] else "Non ✘"

    print("\n" + "=" * 55)
    print("   RÉSUMÉ DU PRODUIT")
    print("=" * 55)
    print(f"  Nom             : {product['name']}")
    print(f"  Catégorie       : {product['category']}")
    print(f"  Fournisseur     : {product['supplier']}")
    print(f"  Unité           : {product['unit']}")
    print(f"  Quantité stock  : {product['quantity']} {product['unit']}")
    print(f"  Seuil minimum   : {product['min_stock']} {product['unit']}")
    print(f"  Prix d'achat    : {product['purchase_price']:,.0f} FCFA")
    print(f"  Prix de vente   : {product['selling_price']:,.0f} FCFA")
    print(f"  Disponible      : {available_label}")
    print(f"  Périssable      : {perishable_label}")
    print("=" * 55)


# ─────────────────────────────────────────────
#  AFFICHAGE LISTE STOCK
# ─────────────────────────────────────────────

def display_stock(stock: list) -> None:
    """Affiche tous les produits en stock sous forme de tableau simple."""
    print("\n" + "=" * 55)
    print(f"   STOCK ACTUEL — {len(stock)} produit(s)")
    print("=" * 55)
    if not stock:
        print("  Aucun produit enregistré pour le moment.")
    else:
        # TODO:MEMBRE4 → remplacer par print(p) quand __str__ sera prêt
        for i, p in enumerate(stock, start=1):
            status = "Dispo" if p["is_available"] else "Indispo"
            print(
                f"  {i:>2}. {p['name']:<20} | "
                f"Qté: {p['quantity']:>5} {p['unit']:<6} | "
                f"Vente: {p['selling_price']:>8,.0f} FCFA | "
                f"{status}"
            )
    print("=" * 55)


# ─────────────────────────────────────────────
#  BOUCLE PRINCIPALE
# ─────────────────────────────────────────────

def main() -> None:
    """
    Point d'entrée du programme.
    Gère la navigation dans le menu et appelle les fonctions appropriées.
    """
    print("\n  Bienvenue dans le Système de Gestion de Stock — BIT")

    while True:
        display_menu()
        choice: str = input("\nVotre choix (1-5) : ").strip()                  # input 14

        # ── Option 1 : Ajouter un produit ──────────────
        if choice == "1":
            product = get_product_inputs()
            stock.append(product)
            display_summary(product)
            print(f"\n  ✅ Produit '{product['name']}' ajouté avec succès !")

        # ── Option 2 : Afficher le stock ───────────────
        elif choice == "2":
            display_stock(stock)

        # ── Option 3 : Rechercher un produit ──────────
        elif choice == "3":
            term = get_search_input()
            results = [p for p in stock if term.lower() in p["name"].lower()]
            if results:
                print(f"\n  {len(results)} résultat(s) trouvé(s) pour '{term}' :")
                for p in results:
                    display_summary(p)
            else:
                print(f"\n  ❌ Aucun produit trouvé pour '{term}'.")

        # ── Option 4 : Mettre à jour une quantité ─────
        elif choice == "4":
            name, new_qty = get_update_inputs()
            found: bool = False
            for p in stock:
                if p["name"].lower() == name.lower():
                    old_qty = p["quantity"]
                    p["quantity"] = new_qty
                    print(
                        f"\n  ✅ Quantité de '{p['name']}' mise à jour : "
                        f"{old_qty} → {new_qty} {p['unit']}"
                    )
                    found = True
                    break
            if not found:
                print(f"\n  ❌ Produit '{name}' introuvable dans le stock.")

        # ── Option 5 : Quitter ─────────────────────────
        elif choice == "5":
            print("\n  Au revoir ! Système de Gestion de Stock — BIT\n")
            break

        # ── Choix invalide ─────────────────────────────
        else:
            print("\n  ⚠ Choix invalide. Entrez un nombre entre 1 et 5.")


# ─────────────────────────────────────────────
#  POINT D'ENTRÉE
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
