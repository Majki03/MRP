import pandas as pd
import numpy as np

class Product:
    def __init__(self, name, lead_time, start_inventory, safety_stock=0, lot_size=1):
        self.name = name  # Nazwa produktu
        self.lead_time = lead_time  # Czas realizacji produktu
        self.start_inventory = start_inventory  # Początkowy stan magazynowy
        self.safety_stock = safety_stock  # Minimalny poziom zapasów (safety stock)
        self.lot_size = lot_size  # Wielkość partii produkcyjnej
        self.gross_requirements = []  # Zapotrzebowanie brutto na okres
        self.scheduled_receipts = []  # Zaplanowane przyjęcia na okres
        self.on_hand = start_inventory  # Bieżący stan magazynowy
        self.net_requirements = []  # Zapotrzebowanie netto na okres
        self.planned_order_releases = []  # Planowane zwolnienia zamówień na okres
        self.planned_order_receipts = []  # Planowane przyjęcia zamówień na okres
        self.components = {}  # Komponenty produktu i ich ilości

    def add_gross_requirement(self, requirement):
        self.gross_requirements.append(requirement)  # Dodaje zapotrzebowanie brutto

    def add_scheduled_receipt(self, receipt):
        self.scheduled_receipts.append(receipt)  # Dodaje zaplanowane przyjęcie

    def add_component(self, component, quantity):
        self.components[component.name] = quantity  # Dodaje komponent i jego ilość

class MRP:
    def __init__(self):
        self.products = {}  # Lista produktów

    def add_product(self, product):
        self.products[product.name] = product  # Dodaje produkt do listy

    def calculate_mrp(self, product_name, periods, transport_time):
        product = self.products[product_name]  # Pobiera produkt z listy
        total_time_needed = product.lead_time + transport_time  # Oblicza całkowity czas potrzebny na produkcję i transport

        # Sprawdza czas realizacji komponentów i aktualizuje total_time_needed, jeśli to konieczne
        for component_name, quantity in product.components.items():
            component = self.products[component_name]
            total_time_needed = max(total_time_needed, component.lead_time + product.lead_time + transport_time)

        # Jeśli całkowity czas potrzebny przekracza liczbę okresów, wyświetla komunikat o błędzie
        if total_time_needed > periods:
            print(f"Zamówienie nie możliwe do zrealizowania w tym terminie dla produktu {product_name}.")
            return

        # Oblicza zapotrzebowanie netto, planowane zwolnienia zamówień i planowane przyjęcia zamówień dla każdego okresu
        for period in range(periods):
            gross_requirement = product.gross_requirements[period] if period < len(product.gross_requirements) else 0
            scheduled_receipt = product.scheduled_receipts[period] if period < len(product.scheduled_receipts) else 0

            if period == 0:
                on_hand = product.start_inventory  # Początkowy stan magazynowy dla pierwszego okresu
            else:
                on_hand = product.on_hand  # Aktualizowany stan magazynowy dla kolejnych okresów

            net_requirement = max(0, gross_requirement - on_hand - scheduled_receipt + product.safety_stock)
            planned_order_receipt = self.calculate_planned_order_receipt(net_requirement, product.lot_size)

            # Planuje zamówienia, jeśli czas realizacji pozwala na przyjęcie w zadanym okresie
            if period + product.lead_time < periods:
                product.planned_order_receipts.append(planned_order_receipt)
                product.planned_order_releases.append(planned_order_receipt)
            else:
                product.planned_order_receipts.append(0)
                product.planned_order_releases.append(0)

            product.net_requirements.append(net_requirement)
            product.on_hand = max(0, on_hand + scheduled_receipt - gross_requirement)

            # Aktualizuje zapotrzebowanie brutto dla komponentów
            for component_name, quantity in product.components.items():
                self.products[component_name].add_gross_requirement(planned_order_receipt * quantity)

    def calculate_planned_order_receipt(self, net_requirement, lot_size):
        if net_requirement == 0:
            return 0  # Jeśli nie ma zapotrzebowania netto, nie planuje zamówienia
        else:
            return ((net_requirement + lot_size - 1) // lot_size) * lot_size  # Oblicza planowane zamówienie na podstawie wielkości partii produkcyjnej

def generate_gross_requirements(start_value, growth_rate, periods):
    return [int(start_value * (1 + growth_rate) ** i) for i in range(periods)]  # Generuje zapotrzebowanie brutto na podstawie początkowej wartości i stopy wzrostu

def main():
    mrp = MRP()

    num_products = int(input("Podaj liczbę produktów: "))

    for _ in range(num_products):
        name = input("Podaj nazwę produktu: ")
        lead_time = int(input(f"Podaj czas realizacji dla produktu {name} (w okresach): "))
        start_inventory = int(input(f"Podaj początkowy stan magazynowy dla produktu {name}: "))
        safety_stock = int(input(f"Podaj minimalny poziom zapasów dla produktu {name}: "))
        lot_size = int(input(f"Podaj wielkość partii produkcyjnej dla produktu {name}: "))
        start_value = int(input(f"Podaj początkową wartość zapotrzebowania brutto dla produktu {name}: "))
        growth_rate = float(input(f"Podaj stopę wzrostu zapotrzebowania brutto (np. 0.1 dla 10%): "))

        product = Product(name, lead_time, start_inventory, safety_stock, lot_size)
        mrp.add_product(product)

        periods = int(input(f"Podaj liczbę okresów (tygodni) dla produktu {name}: "))
        transport_time = int(input(f"Podaj czas transportu (w tygodniach) dla produktu {name}: "))

        gross_requirements = generate_gross_requirements(start_value, growth_rate, periods)
        for requirement in gross_requirements:
            product.add_gross_requirement(requirement)

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

        # Oblicza MRP dla produktu uwzględniając liczbę okresów i czas transportu
        mrp.calculate_mrp(name, periods, transport_time)

    # Wyświetla wyniki obliczeń MRP dla każdego produktu i komponentu
    for product_name, product in mrp.products.items():
        print(f"\nProduct {product_name}")
        print("Net Requirements: ", product.net_requirements)
        print("Planned Order Releases: ", product.planned_order_releases)
        print("Planned Order Receipts: ", product.planned_order_receipts)

if __name__ == "__main__":
    main()
