import streamlit as st
import pickle
from datetime import datetime
import streamlit.components.v1 as components

# Initialize start time
startTime = datetime.now()

# Load the pre-trained model
try:
    with open("ml_models/heart_attack.pkl", "rb") as file:
        model = pickle.load(file)
        st.success("Załadowano model heart_attack.pkl")
except Exception as e:
    st.error(f"Błąd podczas wczytywania modelu heart_attack.pkl: {e}")

sex_d = {0: "Kobieta", 1: "Mężczyzna"}
exng_s = {0: "Nie", 1: "Tak"}
fbs_s = {0: "Cukier poniżej 120ng/ml", 1: "Cukier powyżej 120ng/ml"}

positive_animation = """
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

negative_animation = """
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


def main():
    st.image("necessary_files/Image/heartattac.jpg")

    st.title("Przewidywanie ryzyka zawału serca")
    st.write("Wprowadź swoje dane, aby uzyskać przewidywanie ryzyka zawału serca.")

    # Define default values for the form fields
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

    # Initialize session state if it doesn't exist
    if "form_data" not in st.session_state:
        st.session_state.form_data = default_values.copy()

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
                "ból nie będący dławicą piersiową",
                "brak objawów",
            ][x - 1],
        )

        st.header("Informacje medyczne")
        trtbps = st.number_input(
            "Ciśnienie krwi podczas spoczynku (mm Hg)",
            min_value=0,
            max_value=300,
            value=st.session_state.form_data["trtbps"],
        )
        chol = st.number_input(
            "Cholesterol (mg/dl)",
            min_value=0,
            max_value=600,
            value=st.session_state.form_data["chol"],
        )
        thalachh = st.number_input(
            "Maksymalne tętno",
            min_value=0,
            max_value=250,
            value=st.session_state.form_data["thalachh"],
        )
        oldpeak = st.number_input(
            "Depresja ST wywołana przez ćwiczenie w stosunku do odpoczynku",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.form_data["oldpeak"],
            step=0.1,
        )

        st.header("Dodatkowe informacje")
        fbs = st.radio(
            "Poziom cukru we krwi na czczo",
            list(fbs_s.keys()),
            index=st.session_state.form_data["fbs"],
            format_func=lambda x: fbs_s[x],
        )
        restecg = st.selectbox(
            "Wyniki spoczynkowego elektrokardiogramu (EKG)",
            [0, 1, 2],
            index=st.session_state.form_data["restecg"],
            format_func=lambda x: [
                "normalny",
                "obecność nieprawidłowości fali ST-T",
                "prawdopodobne lub pewne przerost lewej komory według kryteriów Estesa",
            ][x],
        )
        exng = st.radio(
            "Czy występuje angina wysiłkowa?",
            list(exng_s.keys()),
            index=st.session_state.form_data["exng"],
            format_func=lambda x: exng_s[x],
        )
        caa = st.slider(
            "Liczba głównych naczyń zabarwionych fluoroskopowo",
            value=st.session_state.form_data["caa"],
            min_value=0,
            max_value=4,
        )
        thall = st.selectbox(
            "Wynik testu wysiłkowego z Thall",
            [0, 1, 2, 3],
            index=st.session_state.form_data["thall"],
            format_func=lambda x: ["brak", "stała wada", "wada odwracalna", "nieznany"][
                x
            ],
        )
        slp = st.selectbox(
            "Nachylenie segmentu ST na EKG",
            [0, 1, 2],
            index=st.session_state.form_data["slp"],
            format_func=lambda x: ["ujemne", "płaskie", "dodatnie"][x],
        )

        submitted = st.form_submit_button("Przewiduj")
        reset = st.form_submit_button("Resetuj")

        if reset:
            st.session_state.form_data = default_values.copy()
            st.experimental_rerun()

        if submitted:
            # Walidacja
            errors = []
            if not (0 <= trtbps <= 300):
                errors.append(
                    "! Ciśnienie krwi podczas spoczynku musi być w zakresie od 0 do 300 mm Hg."
                )
            if not (0 <= chol <= 600):
                errors.append("! Cholesterol musi być w zakresie od 0 do 600 mg/dl.")
            if not (0 <= thalachh <= 250):
                errors.append("! Maksymalne tętno musi być w zakresie od 0 do 250.")
            if not (0.0 <= oldpeak <= 10.0):
                errors.append(
                    "! Depresja ST wywołana przez ćwiczenie w stosunku do odpoczynku musi być w zakresie od 0.0 do 10.0."
                )

            if errors:
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
            else:
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

                data = [
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
                data = [data]

                try:
                    survival = model.predict(data)
                    s_confidence = model.predict_proba(data)
                    st.subheader("Wyniki przewidywania")
                    if survival[0] == 0:
                        components.html(negative_animation, height=150)
                        st.markdown(
                            f"<div style='background-color: #990033; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                            f"⚠️ Zwiększone ryzyko zawału serca! Pewność predykcji: {s_confidence[0][0] * 100:.2f} %"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        st.warning("Prosimy o pilny kontakt z lekarzem.")
                    else:
                        components.html(positive_animation, height=150)
                        st.markdown(
                            f"<div style='background-color: #006633; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>"
                            f"✅ Brak zwiększonego ryzyka zawału serca. Pewność predykcji: {s_confidence[0][1] * 100:.2f} %"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        st.info("Wszystko w porządku, kontynuuj zdrowy styl życia.")
                except Exception as e:
                    st.error(f"Błąd podczas przewidywania: {e}")


if __name__ == "__main__":
    main()
