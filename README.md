Ten kod implementuje algorytm MRP (Material Requirements Planning) do planowania zapotrzebowania na materiały dla dwóch produktów (A i B) w ciągu 10 okresów.

Klasy:
    Product: Ta klasa reprezentuje produkt i zawiera jego parametry, takie jak nazwa, czas realizacji, początkowy stan magazynowy, minimalny poziom zapasów i wielkość partii produkcyjnej. Posiada również listy do przechowywania zapotrzebowania brutto, zaplanowanych przyjęć, zaplanowanych zwolnień zamówień itp.
    MRP: Ta klasa reprezentuje system MRP i zawiera słownik produktów. Posiada metody do dodawania produktów do słownika i obliczania MRP dla danego produktu na określoną liczbę okresów.

Funkcje:
    add_gross_requirement(requirement): 
        Dodaje zapotrzebowanie brutto do listy produktu.
    add_scheduled_receipt(receipt): 
        Dodaje zaplanowane przyjęcie do listy produktu.
    calculate_mrp(product_name, periods): Oblicza MRP dla danego produktu na określoną liczbę okresów.
        Pobiera zapotrzebowanie brutto i zaplanowane przyjęcia dla każdego okresu.
        Ustawia początkowy stan magazynowy dla pierwszego okresu.
        Oblicza zapotrzebowanie netto dla każdego okresu.
        Oblicza planowane przyjęcie zamówienia dla każdego okresu.
        Dodaje planowane przyjęcie i zwolnienie zamówienia do list produktu.
        Aktualizuje zapotrzebowanie netto i stan magazynowy.
    calculate_planned_order_receipt(net_requirement, lot_size): 
        Oblicza zapotrzebowanie na planowane przyjęcie z uwzględnieniem wielkości partii.

Funkcja main:
    Definiuje liczbę okresów (10).
    Tworzy obiekt MRP.
    Definiuje dwa produkty (A i B) z ich parametrami.
    Dodaje produkty do MRP.
    Ustawia zapotrzebowanie brutto dla każdego produktu w każdym okresie.
    Oblicza MRP dla produktu A i B.
    Wyświetla wyniki (zapotrzebowanie netto, planowane zwolnienia i planowane przyjęcia) dla każdego produktu.

Podsumowanie:
    Ten kod implementuje podstawowy algorytm MRP, który pozwala na obliczenie planu produkcji i zakupów dla dwóch produktów w oparciu o prognozowane zapotrzebowanie, czas realizacji, początkowy stan magazynowy, minimalny poziom zapasów i wielkość partii produkcyjnej.

Należy jednak pamiętać, że ten kod jest uproszczonym przykładem i nie uwzględnia wszystkich aspektów rzeczywistego systemu MRP, takich jak ograniczenia mocy produkcyjnych, koszty transportu, rabaty ilościowe itp.