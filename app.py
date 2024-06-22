import streamlit as st
import pickle
from datetime import datetime

# Initialize start time
startTime = datetime.now()

# Load the pre-trained model
try:
    with open("ml_models/heart_attack.pkl", "rb") as file:
        model  = pickle.load(file)
        st.write("Załadowano model heart_attack.pkl")
except Exception as e:
    st.write(f"Błąd podczas wczytywania modelu heart_attack.pkl: {e}")

sex_d = {0: "Kobieta", 1: "Mężczyzna"}
exng_s = {0: "Nie", 1: "Tak"}
fbs_s = {0:"Cukier poniżej 120ng/ml", 1:"Cukier powyżej 120ng/ml"}

def main():
    st.image("necessary_files/Image/108028555.webp")
    prediction = st.container()

    age = st.slider("Wiek", value=60, min_value=1, max_value=120) #age_slider
    sex = st.radio("Płeć", list(sex_d.keys()), format_func=lambda x: sex_d[x]) #sex_radio
    
    st.header("Bóle w klatce piersiowej")
    st.text("1: typowa dławica piersiowa")
    st.text("2: nietypowa dławica piersiowa")
    st.text("3: ból nie będący dławicą piersiową")
    st.text("4: Brak objawów")
    cp = st.slider("chest_pain", value=2, min_value=0, max_value=3) #chest_pain
    
    st.header("Liczba głownych naczyń")
    caa = st.slider("major_vsssels", value=2, min_value=0, max_value=3) #major_vsssels
    
    st.header("Czy występuje u ciebie angina wysiłkowa?")
    exng = st.radio("Exercise_induced_angina", list(exng_s.keys()), format_func=lambda x: exng_s[x])# exercise_induced_angina
    
    st.header("Podaj cisnienie krwi podczas spoczynku")
    trtbps = st.slider("resting_blood_pressure", value=0, min_value=0, max_value=150)#Do zmiany na wpisywane - resting_blood_pressure
    
    st.header("Cholesterol w mg/dl pobrany za pomocą czujnika BMI")
    chol = st.slider("cholestoral in mg/dl fetched via BMI sensor", value=0, min_value=0, max_value=150)#Do zmiany na wpisywane  cholestoral in mg/dl fetched via BMI sensor
    
    st.header("Poziom cukru we krwi na czczo")
    fbs = st.radio("Exercise_induced_angina", list(fbs_s.keys()), format_func=lambda x: fbs_s[x])#Do zmiany na kulki fasting_blood_sugar
    
    st.header("Wyniki spoczynkowego elektrokardiogramu (EKG)")
    st.text("0: normalny")
    st.text("1: obecność nieprawidłowości fali ST-T (odwrócenia fali T i/lub elewacja lub depresja ST o > 0,05 mV)")
    st.text(" 2: prawdopodobne lub pewne przerost lewej komory według kryteriów Estesa")

    restecg = st.slider("resting_electrocardiographic_results", value=2, min_value=0, max_value=2)#Do zmiany na kulki resting_electrocardiographic_results
    
    st.header("Twoje maksymalnie zmierzone tetno")
    thalachh = st.slider("maximum_heart_rate_achieved", value=0, min_value=0, max_value=150)#Do zmiany na wpisywane maximum_heart_rate_achieved
    
    st.header("Test wysiłkowy z Thall")
    thall = st.slider("Thall rate", value=2, min_value=0, max_value=3) #Thall rate
    
    st.header("nachylenie segmentu ST na EKG")
    slp = st.slider("Sloop", value=2, min_value=0, max_value=2) #Sloop
    
    st.header("W sumie nie wiem")
    oldpeak = st.slider("Previous peak", value=2, min_value=0, max_value=2) #Previous peak - zmiana na float
 # Collect input data for prediction
    data = [age, sex, cp, trtbps,chol, fbs, restecg , thalachh,exng,oldpeak,slp,caa,thall]
    
    data = [data]

    # Make prediction
    survival = model.predict(data)
    s_confidence = model.predict_proba(data)

    with prediction:
        st.header("Czy osoba ma zwiekszone ryzyko zawału? {0}".format("Tak" if survival[0] == 0 else "Nie"))
        st.subheader("Pewność predykcji {0:.2f} %".format(s_confidence[0][survival[0]] * 100))

if __name__ == "__main__":
    main()