# MKwAD_Project
### Poufna analiza danych medycznych 
Implementacja systemu, w którym szpital może zlecić zewnętrznemu serwerowi obliczenie wskaźników statystycznych (średnia, mediana etc. ) pewnych danych medycznych o pacjentach — bez ujawniania surowych danych.

## Struktura systemu
Fully Hommomorpihc Encryption (FHE) zrealizowane za pomocą biblioteki Microsoftu: TenSEAL/SEAL w zależności czy chcemy na GPU czy nie ( ale pewnie chcemy)
```
Serwer medyczny
      |
      http
      |
Chmura obliczeniowa
```
Obliczenia to głównie średnie, odchylenia standardowena zbiorze danych Heart Disease Dataset:
https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset

## Plan działania:
1. Sprawdzenie danych, przeczyszczenie
2. Pierwsze testy enkrypcji lokalnie
3. Zrealizowanie systemu medycznego, w którym możemy dodawać obserwacje do tabeli oraz wysyłać zapytania z odpowiednimi filtrami (np. sprawdzamy średnią danej metryki tylko wśród osób chorych)
4. Realizacja serwisu obliczeniowego, komunikacja z serwisem medycznym i zwracanie odpowiednich wyników
5. Testy integracyjne

## Stack technologiczny
TenSEAL
FastAPI
React
Docker (?)


## Źródła:  
Teoria:
- https://courses.csail.mit.edu/6.857/2022/projects/Facen-Fang-Shepard-Viera.pdf
- https://ethz.ch/content/dam/ethz/special-interest/infk/inst-infsec/appliedcrypto/education/theses/semester-project_junzhen-lou.pdf
- https://pyfhel.readthedocs.io/en/latest/_autoexamples/index.html

Biblioteki do zastosowania szyfrowania:  
- https://github.com/jonaschn/awesome-he



Pytania na zajęcia:
1. Czy zamykamy się z linearnych kalkulacjach(dodawanie, mnożenie), czyli wyliczanie średnich, odchylenia, bez porównywania danych jak np. mediana.
2. Czy potrzebne nam są dane pacjentów do wygenerowania, czy wystarczy nam po prostu id pacjenta z wynikami(czyli czy robimy jedną, czy dwie tabelki)