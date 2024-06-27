"""
Ta aplikacja Streamlit przewiduje ryzyko zawału serca na podstawie danych wprowadzonych przez użytkownika.
Używa wstępnie wytrenowanego modelu uczenia maszynowego do dostarczania prognoz.
"""
import pickle
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

# Initialize start time
startTime = datetime.now()

# Ładowanie modelu
try:
    with open("ml_models/heart_attack.pkl", "rb") as file:
        model = pickle.load(file)
        st.success("Załadowano model heart_attack.pkl")
except Exception as load_exception:
    st.error(f"Błąd podczas wczytywania modelu heart_attack.pkl: {load_exception}")

# Mapowanie wartości dla interfejsu użytkownika
sex_d = {0: "Kobieta", 1: "Mężczyzna"}
exng_s = {0: "Nie", 1: "Tak"}
fbs_s = {0: "Cukier poniżej 120ng/ml", 1: "Cukier powyżej 120ng/ml"}

# Animacje wyników
POSITIVE_ANIMATION = """
<div style="display: flex; align-items: center; justify-content: center; padding: 20px; position: relative;">
  <div style="animation: moveUp 2s; width: 120px; height: 120px; border: 5px solid #006633; border-radius: 50%; position: absolute; top: 0; background-color: #E0FFE0;">
    <svg width="100" height="100" viewBox="0 0 24 24" fill="#006633" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15-4-4 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>
  </div>
</div>
<style>
@keyframes moveUp {
  0% { top: 100px; opacity: 0; }
  50% { opacity: 1; }
  100% { top: 0; opacity: 0; }
}
</style>
"""

NEGATIVE_ANIMATION = """
<div style="display: flex; align-items: center; justify-content: center; padding: 20px; position: relative;">
  <div style="animation: moveUp 2s; width: 120px; height: 120px; border: 5px solid #990033; border-radius: 50%; position: absolute; top: 0; background-color: #FFE0E0;">
    <svg width="100" height="100" viewBox="0 0 24 24" fill="#990033" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
      <path d="M1 21h22L12 2 1 21zM12 16h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
    </svg>
  </div>
</div>
<style>
@keyframes moveUp {
  0% { top: 100px; opacity: 0; }
  50% { opacity: 1; }
  100% { top: 0; opacity: 0; }
}
</style>
"""

# Funkcje walidacji i wyświtlanie błędów
def validate_inputs(trtbps, chol, thalachh, oldpeak):
    """Validates the input values for prediction."""
    errors = []
    if not 0 <= trtbps <= 300:
        errors.append(
            "! Ciśnienie krwi podczas spoczynku musi być w zakresie od 0 do 300 mm Hg."
        )
    if not 0 <= chol <= 600:
        errors.append("! Cholesterol musi być w zakresie od 0 do 600 mg/dl.")
    if not 0 <= thalachh <= 250:
        errors.append("! Maksymalne tętno musi być w zakresie od 0 do 250.")
    if not 0.0 <= oldpeak <= 10.0:
        errors.append(
            "! Depresja ST wywołana przez ćwiczenie w stosunku do odpoczynku musi być w zakresie od 0.0 do 10.0."
        )
    return errors


def display_errors(errors):
    """Displays validation errors."""
    st.error(
        "Nie można przewidywać, ponieważ występują nieprawidłowe wartości. Proszę poprawić następujące pola:"
    )
    for error in errors:
        st.markdown(
            f"<div style='background-color: #FFCCCC; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: red;'>"
            f"{error}"
            f"</div>",
            unsafe_allow_html=True,
        )

# Funkcja przewidywania
def predict_heart_attack_risk(data):
    """Predicts the heart attack risk based on input data."""
    try:
        survival = model.predict(data)
        s_confidence = model.predict_proba(data)
        st.subheader("Wyniki przewidywania")
        if survival[0] == 0:
            components.html(NEGATIVE_ANIMATION, height=150)
            st.markdown(
                f"<div style='background-color: #990033; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                f"⚠️ Zwiększone ryzyko zawału serca! Pewność predykcji: {s_confidence[0][0] * 100:.2f} %"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.warning("Prosimy o pilny kontakt z lekarzem.")
        else:
            components.html(POSITIVE_ANIMATION, height=150)
            st.markdown(
                f"<div style='background-color: #006633; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                f"✅ Brak zwiększonego ryzyka zawału serca. Pewność predykcji: {s_confidence[0][1] * 100:.2f} %"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.info("Wszystko w porządku, kontynuuj zdrowy styl życia.")
    except Exception as predict_exception:
        st.error(f"Błąd podczas przewidywania: {predict_exception}")

# Główna funkcja aplikacji
def main():
    """Main function to run the Streamlit app."""
    st.image("necessary_files/Image/heartattac.jpg")
    st.title("Przewidywanie ryzyka zawału serca")
    st.write("Wprowadź swoje dane, aby uzyskać przewidywanie ryzyka zawału serca.")

    # Definiowanie wartości domyślnych
    default_values = {
        "age": 60,
        "sex": 0,
        "cp": 1,
        "trtbps": 120,
        "chol": 200,
        "thalachh": 150,
        "oldpeak": 1.0,
        "fbs": 0,
        "restecg": 0,
        "exng": 0,
        "caa": 0,
        "thall": 0,
        "slp": 0,
    }

    # Inicjalizacja stanu sesji
    if "form_data" not in st.session_state:
        st.session_state.form_data = default_values.copy()

    # Formularz wejściowy
    with st.form("heart_attack_form"):
        age = st.slider(
            "Wiek", value=st.session_state.form_data["age"], min_value=1, max_value=120
        )
        sex = st.radio(
            "Płeć",
            list(sex_d.keys()),
            index=st.session_state.form_data["sex"],
            format_func=lambda x: sex_d[x],
        )

        st.header("Bóle w klatce piersiowej")
        st.write("Wybierz rodzaj bólu:")
        cp = st.selectbox(
            "",
            [1, 2, 3, 4],
            index=st.session_state.form_data["cp"] - 1,
            format_func=lambda x: [
                "typowa dławica piersiowa",
                "nietypowa dławica piersiowa",
                "ból niemający związku z sercem",
                "bezobjawowy",
            ][x - 1],
        )

        trtbps = st.number_input(
            "Spoczynkowe ciśnienie krwi (mm Hg)",
            value=st.session_state.form_data["trtbps"],
            min_value=0,
            max_value=300,
        )
        chol = st.number_input(
            "Cholesterol (mg/dl)",
            value=st.session_state.form_data["chol"],
            min_value=0,
            max_value=600,
        )
        thalachh = st.number_input(
            "Maksymalne tętno",
            value=st.session_state.form_data["thalachh"],
            min_value=0,
            max_value=250,
        )
        oldpeak = st.number_input(
            "Depresja ST wywołana przez ćwiczenie w stosunku do odpoczynku",
            value=st.session_state.form_data["oldpeak"],
            min_value=0.0,
            max_value=10.0,
            step=0.1,
        )
        fbs = st.radio(
            "Poziom cukru na czczo powyżej 120 mg/dl",
            list(fbs_s.keys()),
            index=st.session_state.form_data["fbs"],
            format_func=lambda x: fbs_s[x],
        )

        restecg = st.selectbox(
            "Wyniki elektrokardiograficzne spoczynkowe",
            [0, 1, 2],
            index=st.session_state.form_data["restecg"],
            format_func=lambda x: [
                "0: normalne",
                "1: mające ST-T (fale spłaszczenia lub odwrócenia) nieprawidłowości",
                "2: przerost lewej komory z prawdopodobnie lub na pewno obecnym bólem",
            ][x],
        )

        exng = st.radio(
            "Ból dławicowy wywołany wysiłkiem",
            list(exng_s.keys()),
            index=st.session_state.form_data["exng"],
            format_func=lambda x: exng_s[x],
        )

        caa = st.slider(
            "Liczba głównych naczyń krwionośnych (0-3)",
            value=st.session_state.form_data["caa"],
            min_value=0,
            max_value=3,
        )
        thall = st.selectbox(
            "Wynik testu Thallium",
            [0, 1, 2],
            index=st.session_state.form_data["thall"],
            format_func=lambda x: ["0: brak", "1: normalny", "2: wada stała", "3: wada odwracalna"][x],
        )
        slp = st.slider(
            "Szczytowy odcinek ST",
            value=st.session_state.form_data["slp"],
            min_value=0,
            max_value=2,
        )

        submitted = st.form_submit_button("Przewiduj ryzyko")

    if submitted:
        st.session_state.form_data = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trtbps": trtbps,
            "chol": chol,
            "thalachh": thalachh,
            "oldpeak": oldpeak,
            "fbs": fbs,
            "restecg": restecg,
            "exng": exng,
            "caa": caa,
            "thall": thall,
            "slp": slp,
        }

        errors = validate_inputs(trtbps, chol, thalachh, oldpeak)
        if errors:
            display_errors(errors)
        else:
            data = [
                [
                    age,
                    sex,
                    cp,
                    trtbps,
                    chol,
                    fbs,
                    restecg,
                    thalachh,
                    exng,
                    oldpeak,
                    slp,
                    caa,
                    thall,
                ]
            ]
            predict_heart_attack_risk(data)


if __name__ == "__main__":
    main()
