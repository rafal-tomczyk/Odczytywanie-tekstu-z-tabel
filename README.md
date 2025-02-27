# Odczyt_tabel_ze_zdjec

## Opis projektu
**Odczyt_tabel_ze_zdjec** to aplikacja, która automatycznie odczytuje dane tabelaryczne ze zdjęć i zapisuje je w skoroszycie programu Excel. Projekt został stworzony, aby ułatwić automatyzację przekształcania danych wizualnych w edytowalne pliki.

## Funkcjonalności
- Analiza zawartości wizualnej zdjęcia i rozpoznawanie tabel.
- Eksport danych tabelarycznych bezpośrednio do pliku Excel (.xlsx).
- Obsługa różnych formatów zdjęć (np. JPEG, PNG).
- Przyjazny interfejs oraz łatwa obsługa.

## Technologie
- **Python** 3.12.3
- **Biblioteki**:
    - `opencv-python` - do przetwarzania obrazów.
    - `pandas` - do tworzenia i manipulowania danymi tabelarycznymi.
    - `openpyxl` - do zapisu danych w formacie Excel.
    - `numpy` - do operacji na tablicach numerycznych.
    - `pytz` - obsługa stref czasowych.

## Instalacja
1. Pobierz repozytorium:
   ```bash
   git clone <URL do twojego repozytorium>
   cd Odczyt_tabel_ze_zdjec
   ```
2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

## Sposób użycia
1. Przygotuj zdjęcie zawierające tabelę, którą chcesz odczytać.
2. Uruchom program:
   ```bash
   python main.py
   ```
3. Podążaj za instrukcjami wyświetlanymi na ekranie, aby zaimportować dane do pliku Excel.

## Przykład
Przykładowe użycie programu:
1. Zdjęcie wejściowe:

   ![Przykładowe zdjęcie tabeli](example-table-image.png)

2. Uzyskany wynik w Excel:

   | Kolumna 1 | Kolumna 2 | Kolumna 3 |
      |-----------|-----------|-----------|
   | Dane 1    | Dane 2    | Dane 3    |

## Wymagania
- Python 3.12.3 lub nowszy.
- System operacyjny: macOS, Windows, lub Linux.

## Rozwój projektu
Chcesz coś dodać? Zachęcam do współpracy! Wykonaj forka repozytorium, wdróż zmiany, a następnie wyślij pull request.

## Kontakt
Jeśli masz pytania lub chciałbyś zgłosić błąd, skontaktuj się poprzez e-mail: **[adres_email@domain.com]**.

## Licencja
Projekt dostępny na licencji MIT. Zapoznaj się z [plikem LICENSE](LICENSE) przed użyciem.# Odczyt_tabel_ze_zdjec
 Program do odczytywania tabel do skoroszytów w Excel ze zdjęć