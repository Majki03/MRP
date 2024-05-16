import pandas as pd
import numpy as np

class Product:
    def __init__(self, name, lead_time, start_inventory, safety_stock=0, lot_size=1):
        # Inicjalizacja obiektu Product z nazwą, czasem realizacji, początkowym stanem magazynowym,
        # minimalnym poziomem zapasów i wielkością partii produkcyjnej
        self.name = name
        self.lead_time = lead_time
        self.start_inventory = start_inventory
        self.safety_stock = safety_stock
        self.lot_size = lot_size
        # Listy do przechowywania zapotrzebowania brutto, zaplanowanych przyjęć,
        # zaplanowanych zwolnień zamówień itp.
        self.gross_requirements = []
        self.scheduled_receipts = []
        self.on_hand = start_inventory
        self.net_requirements = []
        self.planned_order_releases = []
        self.planned_order_receipts = []
        self.components = {}  # Dodanie słownika komponentów

    def add_gross_requirement(self, requirement):
        # Dodawanie zapotrzebowania brutto do listy
        self.gross_requirements.append(requirement)

    def add_scheduled_receipt(self, receipt):
        # Dodawanie zaplanowanych przyjęć do listy
        self.scheduled_receipts.append(receipt)

    def add_component(self, component, quantity):
        # Dodawanie komponentu i jego ilości potrzebnej do produkcji
        self.components[component.name] = quantity

class MRP:
    def __init__(self):
        # Inicjalizacja obiektu MRP z pustym słownikiem produktów
        self.products = {}

    def add_product(self, product):
        # Dodawanie produktu do słownika produktów
        self.products[product.name] = product

    def calculate_mrp(self, product_name, periods):
        # Obliczanie MRP dla danego produktu na określoną liczbę okresów
        product = self.products[product_name]

        for period in range(periods):
            # Pobieranie zapotrzebowania brutto i zaplanowanych przyjęć na dany okres
            gross_requirement = product.gross_requirements[period] if period < len(product.gross_requirements) else 0
            scheduled_receipt = product.scheduled_receipts[period] if period < len(product.scheduled_receipts) else 0

            if period == 0:
                # Ustawianie początkowego stanu magazynowego dla pierwszego okresu
                on_hand = product.start_inventory
            else:
                # Aktualizacja stanu magazynowego na podstawie poprzedniego okresu
                on_hand = product.on_hand

            # Obliczanie zapotrzebowania netto
            net_requirement = max(0, gross_requirement - on_hand - scheduled_receipt + product.safety_stock)
            # Obliczanie planowanego przyjęcia zamówienia na podstawie zapotrzebowania netto i wielkości partii
            planned_order_receipt = self.calculate_planned_order_receipt(net_requirement, product.lot_size)

            if period + product.lead_time < periods:
                # Dodawanie planowanego przyjęcia i zwolnienia zamówienia do list
                product.planned_order_receipts.append(planned_order_receipt)
                product.planned_order_releases.append(planned_order_receipt)
            else:
                # Dodawanie zerowych wartości, jeśli zamówienie nie mieści się w okresach
                product.planned_order_receipts.append(0)
                product.planned_order_releases.append(0)

            # Aktualizacja zapotrzebowania netto i stanu magazynowego
            product.net_requirements.append(net_requirement)
            product.on_hand = max(0, on_hand + scheduled_receipt - gross_requirement)

            # Aktualizacja zapotrzebowania brutto dla komponentów
            for component_name, quantity in product.components.items():
                self.products[component_name].add_gross_requirement(planned_order_receipt * quantity)

    def calculate_planned_order_receipt(self, net_requirement, lot_size):
        # Obliczanie zapotrzebowania na planowane przyjęcia z uwzględnieniem wielkości partii
        if net_requirement == 0:
            return 0
        else:
            return ((net_requirement + lot_size - 1) // lot_size) * lot_size

def main():
    periods = 10
    mrp = MRP()

    # Pobieranie danych o produktach od użytkownika
    num_products = int(input("Podaj liczbę produktów: "))

    for _ in range(num_products):
        name = input("Podaj nazwę produktu: ")
        lead_time = int(input(f"Podaj czas realizacji dla produktu {name} (w okresach): "))
        start_inventory = int(input(f"Podaj początkowy stan magazynowy dla produktu {name}: "))
        safety_stock = int(input(f"Podaj minimalny poziom zapasów dla produktu {name}: "))
        lot_size = int(input(f"Podaj wielkość partii produkcyjnej dla produktu {name}: "))

        product = Product(name, lead_time, start_inventory, safety_stock, lot_size)
        mrp.add_product(product)

        # Pobieranie zapotrzebowania brutto od użytkownika dla każdego okresu
        print(f"Podaj zapotrzebowanie brutto dla produktu {name} w kolejnych {periods} okresach:")
        for period in range(periods):
            requirement = int(input(f"Okres {period + 1}: "))
            product.add_gross_requirement(requirement)

        # Pobieranie danych o komponentach dla danego produktu
        num_components = int(input(f"Podaj liczbę komponentów dla produktu {name}: "))

        for _ in range(num_components):
            component_name = input("Podaj nazwę komponentu: ")
            component_lead_time = int(input(f"Podaj czas realizacji dla komponentu {component_name} (w okresach): "))
            component_start_inventory = int(input(f"Podaj początkowy stan magazynowy dla komponentu {component_name}: "))
            component_safety_stock = int(input(f"Podaj minimalny poziom zapasów dla komponentu {component_name}: "))
            component_lot_size = int(input(f"Podaj wielkość partii produkcyjnej dla komponentu {component_name}: "))
            quantity = int(input(f"Podaj ilość komponentu {component_name} potrzebną do produkcji {name}: "))

            component = Product(component_name, component_lead_time, component_start_inventory, component_safety_stock, component_lot_size)
            mrp.add_product(component)
            product.add_component(component, quantity)

    # Obliczenia MRP dla każdego produktu
    for product_name in mrp.products:
        mrp.calculate_mrp(product_name, periods)

    # Wyświetlanie wyników dla każdego produktu i komponentu
    for product_name, product in mrp.products.items():
        print(f"\nProduct {product_name}")
        print("Net Requirements: ", product.net_requirements)
        print("Planned Order Releases: ", product.planned_order_releases)
        print("Planned Order Receipts: ", product.planned_order_receipts)

if __name__ == "__main__":
    main()