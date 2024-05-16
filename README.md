# Dokumentacja programu do obliczania zapotrzebowania zgodnie z algorytmem MRP

## Spis Treści

1. Opis ogólny
2. Struktura kodu
3. Opis klas i metod
4. Instrukcja użytkownika

---

## 1. Opis ogólny
Program służy do obliczania zapotrzebowania materiałowego (MRP) dla produktów oraz ich komponentów. Umożliwia użytkownikowi wprowadzenie danych dotyczących głównych produktów i ich komponentów, a następnie oblicza zapotrzebowanie netto, planowane zamówienia i przyjęcia dla określonej liczby okresów.

---

## 2. Struktura kodu

#### Program składa się z następujących elementów:

* Klasa 'Product': reprezentuje produkt lub komponent.
* Klasa 'MRP': zarządza obliczeniami MRP dla wszystkich produktów.
* Funkcja 'main': główna funkcja programu, która obsługuje wprowadzanie danych od użytkownika i wyświetla wyniki.

---

## 3. Opis klas i metod

Klasa 'Product'
Konstruktor '__init__'
```python
def __init__(self, name, lead_time, start_inventory, safety_stock=0, lot_size=1)
```
* 'name': nazwa produktu.
* 'lead_time': czas realizacji (w okresach).
* 'start_inventory': początkowy stan magazynowy.
* 'safety_stock': minimalny poziom zapasów (domyślnie 0).
* 'lot_size': wielkość partii produkcyjnej (domyślnie 1).

Metoda 'add_gross_requirement'
```python
def add_gross_requirement(self, requirement)
```
* Dodaje zapotrzebowanie brutto do listy 'gross_requirements'.

Metoda 'add_component'
```python
def add_component(self, component, quantity)
```
* Dodaje komponent i jego ilość potrzebną do produkcji danego produktu.

Klasa 'MRP'
Konstruktor '__init__'
```python
def __init__(self)
```
* Inicjalizuje pusty słownik 'products'.

Metoda 'add_product'
```python
def add_product(self, product)
```
* Dodaje produkt do słownika 'products'.

Metoda 'calculate_mrp'
```python
def calculate_mrp(self, product_name, periods)
```
* Oblicza zapotrzebowanie MRP dla danego produktu na określoną liczbę okresów.
* Aktualizuje zapotrzebowanie brutto komponentów na podstawie planowanych przyjęć produktu głównego.

Metoda 'calculate_planned_order_receipt'
```python
def calculate_planned_order_receipt(self, net_requirement, lot_size)
```
* Oblicza planowane przyjęcie zamówienia na podstawie zapotrzebowania netto i wielkości partii.

Funkcja 'main'
Funkcja 'main'
```python
def main()
```
* Obsługuje wprowadzanie danych od użytkownika.
* Tworzy instancje produktów i komponentów.
* Oblicza MRP dla każdego produktu i komponentu.
* Wyświetla wyniki.

---

## 4. Instrukcja użytkownika

#### Krok 1: Uruchomienie programu
* Upewnij się, że masz zainstalowane środowisko Python.
* Skopiuj kod do pliku o nazwie np. 'mrp_calculator.py'.
* Uruchom program w terminalu:
```python
python mrp_calculator.py
```

#### Krok 2: Wprowadzenie danych
1. Podanie liczby produktów:
    * Na pytanie "Podaj liczbę produktów:" wpisz liczbę produktów, które chcesz dodać.
2. Wprowadzenie danych dla każdego produktu:
    * Dla każdego produktu wprowadź:
        * Nazwę produktu.
        * Czas realizacji (w okresach).
        * Początkowy stan magazynowy.
        * Minimalny poziom zapasów.
        * Wielkość partii produkcyjnej.
3. Wprowadzenie zapotrzebowania brutto:
    * Dla każdego produktu podaj zapotrzebowanie brutto w kolejnych okresach.
4. Podanie liczby komponentów dla każdego produktu:
    * Na pytanie "Podaj liczbę komponentów dla produktu {nazwa}:" wpisz liczbę komponentów potrzebnych do produkcji tego produktu.
5. Wprowadzenie danych dla każdego komponentu:
    * Dla każdego komponentu wprowadź:
        * Nazwę komponentu.
        * Czas realizacji (w okresach).
        * Początkowy stan magazynowy.
        * Minimalny poziom zapasów.
        * Wielkość partii produkcyjnej.
        * Ilość komponentu potrzebną do produkcji produktu głównego.

#### Kropk 3: Wyświetlenie wyników
* Program obliczy i wyświetli:
    * Zapotrzebowanie netto ('Net Requirements').
    * Planowane zwolnienia zamówień ('Planned Order Releases').
    * Planowane przyjęcia zamówień ('Planned Order Receipts').

### Przykład użycia

1. Uruchom program:
```python
python mrp_calculator.py
```
2. Wprowadź dane:
    * Liczba produktów: '2'
    * Produkt 1:
        * Nazwa: 'Krzesło'
        * Czas realizacji: '2'
        * Początkowy stan magazynowy: '50'
        * Minimalny poziom zapasów: '10'
        * Wielkość partii produkcyjnej: '20'
        * Zapotrzebowanie brutto (dla 10 okresów): '5 10 15 20 25 30 35 40 45 50'
    * Komponenty dla 'Krzesło':
        * Liczba komponentów: '3'
        * Komponent 1:
            * Nazwa: 'Nogi'
            * Czas realizacji: '1'
            * Początkowy stan magazynowy: '100'
            * Minimalny poziom zapasów: '20'
            * Wielkość partii produkcyjnej: '10'
            * Ilość: '4'
        * Komponent 2:
            * Nazwa: 'Siedzisko'
            * Czas realizacji: '1'
            * Początkowy stan magazynowy: '50'
            * Minimalny poziom zapasów: '10'
            * Wielkość partii produkcyjnej: '5'
            * Ilość: '1'
        * Komponent 3:
            * Nazwa: 'Oparcie'
            * Czas realizacji: '1'
            * Początkowy stan magazynowy: '50'
            * Minimalny poziom zapasów: '10'
            * Wielkość partii produkcyjnej: '5'
            * Ilość: '1'
    * Produkt 2:
        * Nazwa: 'Stół'
        * Czas realizacji: '3'
        * Początkowy stan magazynowy: '30'
        * Minimalny poziom zapasów: '5'
        * Wielkość partii produkcyjnej: '10'
        * Zapotrzebowanie brutto (dla 10 okresów): '3 6 9 12 15 18 21 24 27 30'
    * Komponenty dla 'Stół':
        * Liczba komponentów: '2'
        * Komponent 1:
            * Nazwa: 'Nogi'
            * Czas realizacji: '1'
            * Początkowy stan magazynowy: '100'
            * Minimalny poziom zapasów: '20'
            * Wielkość partii produkcyjnej: '10'
            * Ilość: '4'
        * Komponent 2:
            * Nazwa: 'Blat'
            * Czas realizacji: '1'
            * Początkowy stan magazynowy: '20'
            * Minimalny poziom zapasów: '5'
            * Wielkość partii produkcyjnej: '2'
            * Ilość: '1'
3. Wyniki:
    * Program obliczy zapotrzebowanie netto, planowane zwolnienia zamówień i planowane przyjęcia zamówień dla każdego produktu i komponentu.

---

# To wszystko! Program jest teraz gotowy do użytku i może obliczać zapotrzebowanie MRP na dwóch poziomach.