# =============================================================
# PRG1406 — Advanced Programming (Python and C)
# Group Assignment 1 — Stock Management System
# Burkina Institute of Technology
# =============================================================
# MEMBRE 1 — Structure générale + Inputs
# MEMBRE 2 — Calculs + Validation
# MEMBRE 3 — Héritage (Product + PerishableProduct)
# MEMBRE 4 — Magic Methods (__str__, __repr__, __eq__, __len__)
# MEMBRE 5 — Décorateurs (@property, @staticmethod, @classmethod)
# =============================================================

from datetime import date


# =============================================================
#  CLASSE PARENT — Product
#  (Membres 3 + 4 + 5)
# =============================================================

class Product:
    """
    Représente un produit dans le stock.

    MEMBRE 3 → classe parent avec __init__ et tous les attributs
    MEMBRE 4 → __str__, __repr__, __eq__, __len__
    MEMBRE 5 → @property (margin, is_low_stock), @staticmethod (validate_price),
               @classmethod (from_dict)
    """

    # ── MEMBRE 3 — Constructeur ────────────────────────────
    def __init__(
        self,
        name: str,
        category: str,
        supplier: str,
        unit: str,
        quantity: int,
        min_stock: int,
        purchase_price: float,
        selling_price: float,
        is_available: bool,
        is_perishable: bool,
    ):
        self.name           = name
        self.category       = category
        self.supplier       = supplier
        self.unit           = unit
        self.quantity       = quantity
        self.min_stock      = min_stock
        self.purchase_price = purchase_price
        self.selling_price  = selling_price
        self.is_available   = is_available
        self.is_perishable  = is_perishable

    # ── MEMBRE 4 — Magic Methods ───────────────────────────

    def __str__(self) -> str:
        """
        Appelé par print(product).
        Retourne un résumé lisible du produit.
        """
        available_label  = "Dispo [v]"  if self.is_available  else "Indispo [x]"
        perishable_label = "Oui [v]"    if self.is_perishable else "Non [x]"
        return (
            f"\n{'=' * 55}\n"
            f"   RÉSUMÉ DU PRODUIT\n"
            f"{'=' * 55}\n"
            f"  Nom             : {self.name}\n"
            f"  Catégorie       : {self.category}\n"
            f"  Fournisseur     : {self.supplier}\n"
            f"  Unité           : {self.unit}\n"
            f"  Quantité stock  : {self.quantity} {self.unit}\n"
            f"  Seuil minimum   : {self.min_stock} {self.unit}\n"
            f"  Prix d'achat    : {self.purchase_price:,.0f} FCFA\n"
            f"  Prix de vente   : {self.selling_price:,.0f} FCFA\n"
            f"  Disponible      : {available_label}\n"
            f"  Périssable      : {perishable_label}\n"
            f"{'=' * 55}"
        )

    def __repr__(self) -> str:
        """
        Appelé dans le shell Python ou dans les listes.
        Retourne une représentation technique de l'objet.
        """
        return (
            f"Product(name='{self.name}', category='{self.category}', "
            f"quantity={self.quantity}, selling_price={self.selling_price})"
        )

    def __eq__(self, other: object) -> bool:
        """
        Permet de comparer deux produits avec ==.
        Deux produits sont égaux s'ils ont le même nom (insensible à la casse).
        """
        if not isinstance(other, Product):
            return NotImplemented
        return self.name.lower() == other.name.lower()

    def __len__(self) -> int:
        """
        Appelé par len(product).
        Retourne la quantité en stock du produit.
        """
        return self.quantity

    # ── MEMBRE 5 — Décorateurs ─────────────────────────────

    @property
    def margin(self) -> float:
        """
        @property — accédé comme un attribut : product.margin
        Calcule la marge bénéficiaire en FCFA.
        """
        return self.selling_price - self.purchase_price

    @property
    def margin_percent(self) -> float:
        """
        @property — accédé comme un attribut : product.margin_percent
        Calcule la marge en pourcentage par rapport au prix d'achat.
        """
        if self.purchase_price == 0:
            return 0.0
        return ((self.selling_price - self.purchase_price) / self.purchase_price) * 100

    @property
    def is_low_stock(self) -> bool:
        """
        @property — retourne True si la quantité est en-dessous du seuil minimum.
        Accédé comme : product.is_low_stock
        """
        return self.quantity < self.min_stock

    @staticmethod
    def validate_price(price: float) -> bool:
        """
        @staticmethod — ne dépend d'aucune instance ni de la classe.
        Vérifie qu'un prix est strictement positif.
        Utilisé avant de créer ou modifier un produit.
        """
        return isinstance(price, (int, float)) and price > 0

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """
        @classmethod — reçoit la classe (cls) comme premier argument.
        Crée une instance de Product à partir d'un dictionnaire.
        Utile pour convertir les anciens dicts de Membre 1 en objets.
        """
        return cls(
            name           = data["name"],
            category       = data["category"],
            supplier       = data["supplier"],
            unit           = data["unit"],
            quantity       = data["quantity"],
            min_stock      = data["min_stock"],
            purchase_price = data["purchase_price"],
            selling_price  = data["selling_price"],
            is_available   = data["is_available"],
            is_perishable  = data["is_perishable"],
        )


# =============================================================
#  CLASSE ENFANT — PerishableProduct
#  (Membres 3 + 4 + 5)
# =============================================================

class PerishableProduct(Product):
    """
    Produit périssable — hérite de Product.
    Ajoute une date d'expiration et la vérification d'expiration.

    MEMBRE 3 → héritage + super().__init__() + attribut expiry_date
    MEMBRE 4 → __str__ enrichi avec la date d'expiration
    MEMBRE 5 → @property is_expired, days_until_expiry
    """

    # ── MEMBRE 3 — Constructeur enfant ─────────────────────
    def __init__(self, expiry_date: date, *args, **kwargs):
        super().__init__(*args, **kwargs)   # appel du constructeur parent
        self.expiry_date   = expiry_date
        self.is_perishable = True           # toujours True pour ce type

    # ── MEMBRE 4 — Magic Methods enrichies ─────────────────

    def __str__(self) -> str:
        """
        Surcharge de __str__ : affiche aussi la date d'expiration
        et l'état (expiré ou non).
        """
        base     = super().__str__()
        expired  = "[!] EXPIRÉ"  if self.is_expired else f"dans {self.days_until_expiry} jour(s)"
        extra    = (
            f"\n  Date expiration : {self.expiry_date.strftime('%d/%m/%Y')}\n"
            f"  État expiration : {expired}\n"
            f"{'=' * 55}"
        )
        # On insère les infos avant la dernière ligne de séparation
        return base[:-55] + extra

    def __repr__(self) -> str:
        """Représentation technique incluant la date d'expiration."""
        return (
            f"PerishableProduct(name='{self.name}', expiry_date={self.expiry_date}, "
            f"quantity={self.quantity})"
        )

    # ── MEMBRE 5 — Décorateurs spécifiques aux périssables ─

    @property
    def is_expired(self) -> bool:
        """
        @property — vérifie si le produit est déjà périmé.
        Accédé comme : product.is_expired
        """
        return date.today() > self.expiry_date

    @property
    def days_until_expiry(self) -> int:
        """
        @property — calcule le nombre de jours restants avant expiration.
        Retourne un nombre négatif si le produit est déjà périmé.
        """
        delta = self.expiry_date - date.today()
        return delta.days

    @classmethod
    def from_dict(cls, data: dict) -> "PerishableProduct":
        """
        @classmethod — crée un PerishableProduct depuis un dictionnaire.
        La clé 'expiry_date' doit être un objet date.
        """
        return cls(
            expiry_date    = data["expiry_date"],
            name           = data["name"],
            category       = data["category"],
            supplier       = data["supplier"],
            unit           = data["unit"],
            quantity       = data["quantity"],
            min_stock      = data["min_stock"],
            purchase_price = data["purchase_price"],
            selling_price  = data["selling_price"],
            is_available   = data["is_available"],
            is_perishable  = data["is_perishable"],
        )


# =============================================================
#  MEMBRE 2 — Validation + Calculs
# =============================================================

def get_valid_int(prompt: str) -> int:
    """Demande un entier, relance si invalide."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("  [!] La valeur ne peut pas être négative. Réessayez.")
                continue
            return value
        except ValueError:
            print("  [!] Entier invalide. Réessayez.")


def get_valid_float(prompt: str) -> float:
    """Demande un flottant, relance si invalide."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("  [!] La valeur ne peut pas être négative. Réessayez.")
                continue
            return value
        except ValueError:
            print("  [!] Nombre invalide. Réessayez.")


def calculate_margin(purchase_price: float, selling_price: float) -> float:
    """Calcule la marge bénéficiaire en FCFA."""
    return selling_price - purchase_price


def calculate_margin_percent(purchase_price: float, selling_price: float) -> float:
    """Calcule la marge en pourcentage."""
    if purchase_price == 0:
        return 0.0
    return ((selling_price - purchase_price) / purchase_price) * 100


def calculate_stock_value(quantity: int, selling_price: float) -> float:
    """Calcule la valeur totale du stock pour un produit."""
    return quantity * selling_price


# =============================================================
#  MEMBRE 1 — Structure générale + Menu
# =============================================================

stock: list = []    # Liste d'objets Product / PerishableProduct


def display_menu() -> None:
    """Affiche le menu principal."""
    print("\n" + "=" * 55)
    print("       SYSTÈME DE GESTION DE STOCK — BIT")
    print("=" * 55)
    print("  1. Ajouter un produit")
    print("  2. Ajouter un produit périssable")
    print("  3. Afficher tout le stock")
    print("  4. Rechercher un produit")
    print("  5. Mettre à jour la quantité d'un produit")
    print("  6. Quitter")
    print("=" * 55)


def get_product_inputs() -> Product:
    """Collecte les infos d'un produit normal et retourne un objet Product."""
    print("\n" + "-" * 45)
    print("   AJOUT D'UN NOUVEAU PRODUIT")
    print("-" * 45)

    # str
    product_name: str = input("Nom du produit             : ").strip()        # input 1
    category: str     = input("Catégorie                  : ").strip()        # input 2
    supplier: str     = input("Fournisseur                : ").strip()        # input 3
    unit: str         = input("Unité de mesure (pièce/kg) : ").strip()        # input 4

    # int (Membre 2 : validation)
    quantity: int  = get_valid_int("Quantité en stock          : ")           # input 5
    min_stock: int = get_valid_int("Seuil minimum de stock     : ")           # input 6

    # float (Membre 2 : validation + Membre 5 : @staticmethod)
    while True:
        purchase_price: float = get_valid_float("Prix d'achat (FCFA)        : ")  # input 7
        if Product.validate_price(purchase_price):
            break
        print("  [!] Prix d'achat doit être > 0.")

    while True:
        selling_price: float = get_valid_float("Prix de vente (FCFA)       : ")   # input 8
        if Product.validate_price(selling_price):
            break
        print("  [!] Prix de vente doit être > 0.")

    # bool (pattern correct)
    is_available: bool  = input("Disponible à la vente ? (oui/non) : ").strip().lower() == "oui"  # input 9
    is_perishable: bool = input("Produit périssable ?    (oui/non) : ").strip().lower() == "oui"  # input 10

    # Membre 2 : calculs affichés avant confirmation
    margin      = calculate_margin(purchase_price, selling_price)
    margin_pct  = calculate_margin_percent(purchase_price, selling_price)
    stock_value = calculate_stock_value(quantity, selling_price)

    print(f"\n  Marge bénéficiaire  : {margin:,.0f} FCFA")
    print(f"  Marge en %          : {margin_pct:.1f} %")
    print(f"  Valeur totale stock : {stock_value:,.0f} FCFA")

    return Product(
        name=product_name, category=category, supplier=supplier,
        unit=unit, quantity=quantity, min_stock=min_stock,
        purchase_price=purchase_price, selling_price=selling_price,
        is_available=is_available, is_perishable=is_perishable,
    )


def get_perishable_inputs() -> PerishableProduct:
    """Collecte les infos d'un produit périssable et retourne un objet PerishableProduct."""
    print("\n" + "-" * 45)
    print("   AJOUT D'UN PRODUIT PÉRISSABLE")
    print("-" * 45)

    product_name: str = input("Nom du produit             : ").strip()        # input 1
    category: str     = input("Catégorie                  : ").strip()        # input 2
    supplier: str     = input("Fournisseur                : ").strip()        # input 3
    unit: str         = input("Unité de mesure (pièce/kg) : ").strip()        # input 4

    quantity: int  = get_valid_int("Quantité en stock          : ")           # input 5
    min_stock: int = get_valid_int("Seuil minimum de stock     : ")           # input 6

    while True:
        purchase_price: float = get_valid_float("Prix d'achat (FCFA)        : ")
        if Product.validate_price(purchase_price):
            break
        print("  [!] Prix d'achat doit être > 0.")

    while True:
        selling_price: float = get_valid_float("Prix de vente (FCFA)       : ")
        if Product.validate_price(selling_price):
            break
        print("  [!] Prix de vente doit être > 0.")

    is_available: bool = input("Disponible à la vente ? (oui/non) : ").strip().lower() == "oui"

    # Date d'expiration (Membre 2 : validation)
    while True:
        try:
            raw_date: str = input("Date d'expiration (JJ/MM/AAAA)    : ").strip()
            expiry_date   = date(*[int(x) for x in reversed(raw_date.split("/"))])
            break
        except (ValueError, IndexError):
            print("  [!] Format invalide. Utilisez JJ/MM/AAAA.")

    margin      = calculate_margin(purchase_price, selling_price)
    margin_pct  = calculate_margin_percent(purchase_price, selling_price)
    stock_value = calculate_stock_value(quantity, selling_price)

    print(f"\n  Marge bénéficiaire  : {margin:,.0f} FCFA")
    print(f"  Marge en %          : {margin_pct:.1f} %")
    print(f"  Valeur totale stock : {stock_value:,.0f} FCFA")

    return PerishableProduct(
        expiry_date=expiry_date,
        name=product_name, category=category, supplier=supplier,
        unit=unit, quantity=quantity, min_stock=min_stock,
        purchase_price=purchase_price, selling_price=selling_price,
        is_available=is_available, is_perishable=True,
    )


def get_search_input() -> str:
    """Demande le terme de recherche."""
    print("\n" + "-" * 45)
    print("   RECHERCHE DE PRODUIT")
    print("-" * 45)
    return input("Nom du produit à rechercher : ").strip()                    # input 11


def get_update_inputs() -> tuple:
    """Collecte le nom et la nouvelle quantité pour une mise à jour."""
    print("\n" + "-" * 45)
    print("   MISE À JOUR DE LA QUANTITÉ")
    print("-" * 45)
    product_name: str = input("Nom du produit à modifier : ").strip()         # input 12
    new_quantity: int = get_valid_int("Nouvelle quantité          : ")        # input 13
    return product_name, new_quantity


def display_stock(stock: list) -> None:
    """Affiche tous les produits du stock. Utilise __len__ (Membre 4)."""
    print("\n" + "=" * 55)
    print(f"   STOCK ACTUEL — {len(stock)} produit(s)")
    print("=" * 55)
    if not stock:
        print("  Aucun produit enregistré pour le moment.")
    else:
        for i, p in enumerate(stock, start=1):
            status = "Dispo [v]" if p.is_available else "Indispo [x]"
            low    = " [!] STOCK BAS" if p.is_low_stock else ""    # Membre 5 @property
            # len(p) utilise __len__ défini par Membre 4
            print(
                f"  {i:>2}. {p.name:<20} | "
                f"Qté: {len(p):>5} {p.unit:<6} | "
                f"Vente: {p.selling_price:>8,.0f} FCFA | "
                f"{status}{low}"
            )
    print("=" * 55)


def main() -> None:
    """Point d'entrée — boucle principale du menu."""
    print("\n  Bienvenue dans le Système de Gestion de Stock — BIT")

    while True:
        display_menu()
        choice: str = input("\nVotre choix (1-6) : ").strip()                 # input 14

        if choice == "1":
            product = get_product_inputs()
            stock.append(product)
            print(product)          # utilise __str__ (Membre 4)
            print(f"\n  [OK] '{product.name}' ajouté avec succès !")
            print(f"  [>] Marge : {product.margin:,.0f} FCFA ({product.margin_percent:.1f} %)")

        elif choice == "2":
            product = get_perishable_inputs()
            stock.append(product)
            print(product)          # utilise __str__ enrichi de PerishableProduct
            print(f"\n  [OK] '{product.name}' ajouté avec succès !")
            if product.is_expired:
                print("  [!] Attention : ce produit est déjà expiré !")
            else:
                print(f"  [DATE] Expire dans {product.days_until_expiry} jour(s).")

        elif choice == "3":
            display_stock(stock)

        elif choice == "4":
            term    = get_search_input()
            results = [p for p in stock if term.lower() in p.name.lower()]
            if results:
                print(f"\n  {len(results)} résultat(s) pour '{term}' :")
                for p in results:
                    print(p)        # __str__
            else:
                print(f"\n  [ERREUR] Aucun produit trouvé pour '{term}'.")

        elif choice == "5":
            name, new_qty = get_update_inputs()
            found: bool = False
            for p in stock:
                if p.name.lower() == name.lower():
                    old_qty    = p.quantity
                    p.quantity = new_qty
                    print(
                        f"\n  [OK] Quantité de '{p.name}' mise à jour : "
                        f"{old_qty} → {new_qty} {p.unit}"
                    )
                    if p.is_low_stock:
                        print(f"  [!] Stock bas ! Seuil minimum : {p.min_stock} {p.unit}")
                    found = True
                    break
            if not found:
                print(f"\n  [ERREUR] Produit '{name}' introuvable dans le stock.")

        elif choice == "6":
            print("\n  Au revoir ! Système de Gestion de Stock — BIT\n")
            break

        else:
            print("\n  [!] Choix invalide. Entrez un nombre entre 1 et 6.")


if __name__ == "__main__":
    main()