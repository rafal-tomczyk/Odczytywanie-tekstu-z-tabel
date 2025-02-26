import pytesseract
import cv2
import pandas as pd
import numpy as np
import re
import os
from datetime import datetime


def remove_squares(obraz):
    """Funkcja pomocnicza, usuwająca kwadraty pojawiające się przy etykietach związków

    Args:
        obraz (numpy.ndarray): Obraz wejściowy w formacie macierzy NumPy.

    Returns:
        numpy.ndarray: Obraz po usunięciu kwadratów.
    """
    blurred = cv2.GaussianBlur(obraz, (5, 3), 0)
    edges = cv2.Canny(blurred, 110, 300)
    kontury, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in kontury:
        x, y, w, h = cv2.boundingRect(cnt)
        if 15 < w < 40 and 15 < h < 40:
            cv2.rectangle(obraz, (x, y), (x + w, y + h), (255, 255, 255), -1)
    return obraz


def crop_to_content(image):

    _, thresholded = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(
        thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return image[y : y + h, x : x + w]
    else:
        return image


def odczytaj_tekst_ze_zdjecia(sciezka) -> str:
    """Główna funkcja wykonująca operację podzielenia obrazu na 4 części i odczytania informacji.
    Jest ona wykonywana dla każdego obrazu przekazanego do programu.

    Args:
        path (str): ścieżka do zdjęcia, z którego mają być odczytane informacje

    Returns:
        str: Zwraca ścieżkę do CSV konwerstowanego zdjęcia, który zostanie wykorzystany jako skoroszyt w xlsx.
    """

    obraz = cv2.imread(sciezka)
    skala_szarosci = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)
    bez_kwadratow = remove_squares(skala_szarosci)
    wyciety = crop_to_content(bez_kwadratow)
    szerokosc = int(wyciety.shape[1] + 100)
    wysokosc = int(wyciety.shape[0] + 100)
    powiekszony = cv2.resize(wyciety, (szerokosc, wysokosc))
    wyostrzony = cv2.GaussianBlur(powiekszony, (0, 0), 3)
    wyostrzony = cv2.addWeighted(powiekszony, 1.5, wyostrzony, -0.5, 0)

    # Dzielenie na 4 kolumny
    os.makedirs("pociete", exist_ok=True)
    dane = pytesseract.image_to_data(powiekszony, output_type=pytesseract.Output.DICT)
    etykiety = ["#Events", "%Parent", "%Total"]
    szerokosci = 0
    for i in range(len(dane["text"])):
        if dane["text"][i] in etykiety:
            (x, y, w, h) = (
                dane["left"][i],
                0,
                dane["width"][i],
                powiekszony.shape[0],
            )
            # Wyodrębnianie prostokąta na pełną wysokość obrazu
            roi = powiekszony[y : y + h, x - 10 : x + w + 8]
            szerokosci += w + 20
            # Zapis wyciętego prostokąta
            cv2.imwrite(f'pociete/{dane["text"][i]}.png', roi)
    roi2 = powiekszony[0 : powiekszony.shape[0], 0 : powiekszony.shape[1] - szerokosci]
    cv2.imwrite(f"pociete/Nazwy.png", roi2)

    etykiety = ["Nazwy.png", "#Events.png", "%Parent.png", "%Total.png"]

    tekst = []
    for etykieta in etykiety:
        sciezka = os.path.join("pociete", etykieta)
        if os.path.exists(sciezka):
            obraz = cv2.imread(sciezka)
            tekst.append(czytaj(obraz))
        else:
            print("cos nie dziala")

    # Dodaj pusty rząd na początku dla odpowiednich kolumn
    tekst[1].insert(0, "")  # Dla #Events
    tekst[2].insert(0, "")  # Dla %Parent
    tekst[3].insert(0, "")  # Dla %Total

    # czyszczenie danych
    for i in range(len(tekst[0])):
        try:
            wartość = str(tekst[0][i])
            if wartość[0] == "r" or wartość[0] == "l":
                tekst[0][i] = wartość[1:]
        except (ValueError, IndexError):
            pass

    for kolumna in [2, 3]:
        for i in range(len(tekst[kolumna])):
            try:
                wartość_str:str = str(tekst[kolumna][i])
                wartość_f: float = float(tekst[kolumna][i])

                if wartość_str[-2] != ".":
                    tekst[kolumna][i] = str(float(wartość_f) / 10)

                if wartość_f > 100:
                    tekst[kolumna][i] = str(wartość_f / 10)

                if kolumna == 3 and wartość_f > float(tekst[2][i]):
                    tekst[kolumna][i] = str(wartość_f / 10)
            except (ValueError, IndexError):
                pass

    # Przygotowanie do utworzenia DataFrame
    if len(tekst) == 4:
        df = pd.DataFrame(
            {
                "Nazwy": tekst[0],  # Zawiera nazwy
                "#Eve434nts": tekst[1],  # Zawiera #EventsS
                "%Parent": tekst[2],  # Zawiera %Parent
                "%Total": tekst[3],  # Zawiera %Total
            }
        )

    else:
        print("Niepoprawna liczba wierszy w tekście.")
    return df


def czytaj(obraz):
    tekst: str = pytesseract.image_to_string(obraz, config="--psm 6")
    linie = tekst.splitlines()
    czysty_tekst = []
    for linia in linie:
        if linia != "":
            czysta_linia = re.sub(r"[^a-zA-Z0-9#%+,\-.:_]", "", linia)
            czysty_tekst.append(czysta_linia)
    return czysty_tekst


def main_multi(folder_zrodlowy, folder_dla_wynikow):
    """Funkcja wykonywująca operację odczytania danych z obrazu dla każdego z przekazanych plików w wybranym folderze.


    Args:
        folder_zrodlowy (str): Ścieżka relatywna do wybranego folderu
        folder_dla_wynikow (str): Ścieżka relatywna do folderu, w którym zostanie zapisany plik xlsm
    """
    os.makedirs(folder_dla_wynikow, exist_ok=True)
    arkusze = {}

    for zdjecie in os.listdir(folder_zrodlowy):
        if zdjecie.lower().endswith((".png", ".jpg", ".jpeg")):
            sciezka_do_zdjecia = os.path.join(folder_zrodlowy, zdjecie)
            df = odczytaj_tekst_ze_zdjecia(sciezka_do_zdjecia)
            nazwa_arkusza = os.path.splitext(zdjecie)[0]
            arkusze[nazwa_arkusza] = df

    timestamp = datetime.now().strftime("%Y-%m-%d %H.%M")
    nazwa_pliku_xlsx = os.path.join(folder_dla_wynikow, f"wyniki-{timestamp}.xlsx")
    with pd.ExcelWriter(nazwa_pliku_xlsx, engine="xlsxwriter") as writer:
        for nazwa_arkusza, df in arkusze.items():  # Teraz mamy df, nie ścieżkę do CSV
            df.to_excel(writer, sheet_name=nazwa_arkusza, index=False, header=False)
