# Aplikacja Streamlit do Przewidywania Ryzyka Zawału Serca

## Opis

Aplikacja Streamlit do przewidywania ryzyka zawału serca na podstawie wprowadzonych danych medycznych. Aplikacja wykorzystuje wstępnie wytrenowany model do dokonywania predykcji.

## Wymagania wstępne

- Zainstalowany Docker
- Plik modelu `heart_attack.pkl` umieszczony w katalogu `ml_models/`
- Obraz `heartattac.jpg` umieszczony w katalogu `necessary_files/Image/`

## Instrukcja uruchomienia

### 1. Tworzenie obrazu Dockera

Aby utworzyć obraz Dockera, uruchom poniższe polecenie w katalogu zawierającym plik `Dockerfile` oraz kod aplikacji:

```sh
docker build -t streamlitapp .

## 2. **Tworzenie kontenera z obrazem**

Aby uruchomić aplikację Streamlit w kontenerze Docker, użyj poniższego polecenia:

```sh
docker run -p 8000:8000 streamlitapp

## 3. **Uruchamianie aplikacji**

Otwórz przeglądarkę internetową i wejdź na adres:

```sh
http://localhost:8000/

## **Ciesz się działającą aplikacją !**

## 4. **Szczegóły implementacji**
## **Struktura katalogów**

Upewnij się, że masz następującą strukturę katalogów:

.
├── Dockerfile
├── app.py
├── ml_models
│   └── heart_attack.pkl
└── necessary_files
    └── Image
        └── heartattac.jpg

## **Plik app.py**

Główny plik aplikacji app.py zawiera kod aplikacji Streamlit do przewidywania ryzyka zawału serca. Upewnij się, że jest on kompletny i poprawny.
Przydatne komendy:

Aby sprawdzić, czy Docker działa poprawnie, użyj:

    sh
	docker --version

Aby sprawdzić działające kontenery:

	sh
	docker ps

Aby zatrzymać działający kontener:

	sh
	docker stop [container_id]

Aby usunąć kontener:

	sh
	docker rm [container_id]

## **5. Uwagi**

Upewnij się, że plik modelu heart_attack.pkl i obraz heartattac.jpg znajdują się w odpowiednich katalogach przed uruchomieniem aplikacji. Jeśli napotkasz problemy z uruchomieniem, sprawdź logi kontenera za pomocą:

	docker logs [container_id]

## **6. Autorzy**

Projekt stworzony przez:
1. Cezary Sieczkowski
2. Karol Tusiński
3. Adam Wolańczyk
4. Tomasz Fiedoruk

Zapraszamy do kontaktu w przypadku pytań lub sugestii.