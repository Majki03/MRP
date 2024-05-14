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

    def add_gross_requirement(self, requirement):
        # Dodawanie zapotrzebowania brutto do listy
        self.gross_requirements.append(requirement)

    def add_scheduled_receipt(self, receipt):
        # Dodawanie zaplanowanych przyjęć do listy
        self.scheduled_receipts.append(receipt)

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

    def calculate_planned_order_receipt(self, net_requirement, lot_size):
        # Obliczanie zapotrzebowania na planowane przyjęcia z uwzględnieniem wielkości partii
        if net_requirement == 0:
            return 0
        else:
            return ((net_requirement + lot_size - 1) // lot_size) * lot_size

def main():
    periods = 10
    mrp = MRP()

    # Definicja produktów
    product_A = Product("A", lead_time=2, start_inventory=50, safety_stock=10, lot_size=20)
    product_B = Product("B", lead_time=1, start_inventory=30, safety_stock=5, lot_size=15)

    # Dodanie produktów do MRP
    mrp.add_product(product_A)
    mrp.add_product(product_B)

    # Ustalanie zapotrzebowania brutto dla produktu A w poszczególnych okresach
    product_A.add_gross_requirement(20)
    product_A.add_gross_requirement(0)
    product_A.add_gross_requirement(0)
    product_A.add_gross_requirement(40)
    product_A.add_gross_requirement(0)
    product_A.add_gross_requirement(20)
    product_A.add_gross_requirement(10)
    product_A.add_gross_requirement(0)
    product_A.add_gross_requirement(20)
    product_A.add_gross_requirement(30)

    # Ustalanie zapotrzebowania brutto dla produktu B w poszczególnych okresach
    product_B.add_gross_requirement(10)
    product_B.add_gross_requirement(0)
    product_B.add_gross_requirement(0)
    product_B.add_gross_requirement(20)
    product_B.add_gross_requirement(0)
    product_B.add_gross_requirement(10)
    product_B.add_gross_requirement(5)
    product_B.add_gross_requirement(0)
    product_B.add_gross_requirement(10)
    product_B.add_gross_requirement(15)

    # Obliczenia MRP dla produktów A i B
    mrp.calculate_mrp("A", periods)
    mrp.calculate_mrp("B", periods)

    # Wyświetlanie wyników dla produktu A
    print("Product A")
    print("Net Requirements: ", product_A.net_requirements)
    print("Planned Order Releases: ", product_A.planned_order_releases)
    print("Planned Order Receipts: ", product_A.planned_order_receipts)

    # Wyświetlanie wyników dla produktu B
    print("Product B")
    print("Net Requirements: ", product_B.net_requirements)
    print("Planned Order Releases: ", product_B.planned_order_releases)
    print("Planned Order Receipts: ", product_B.planned_order_receipts)

if __name__ == "__main__":
    main()
