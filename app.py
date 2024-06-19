import streamlit as st
import pickle
from datetime import datetime

# Initialize start time
startTime = datetime.now()

# Load the pre-trained model
filename = "heart_attack.pkl"
model = pickle.load(open(filename, 'rb'))

sex_d = {0: "Kobieta", 1: "Mężczyzna"}

def main():
    st.set_page_config(page_title="Heart Attack")
    st.image("108028555.webp")
    prediction = st.container()

    age = st.slider("Wiek", value=60, min_value=1, max_value=120) #age_slider
    sex = st.radio("Płeć", list(sex_d.keys()), format_func=lambda x: sex_d[x]) #sex_radio
    
    st.text("1: typowa dławica piersiowa")
    st.text("2: nietypowa dławica piersiowa")
    st.text("3: ból nie będący dławicą piersiową")
    st.text("4: bezobjawowe")
    cp = st.slider("chest_pain", value=2, min_value=0, max_value=3) #chest_pain
    
    st.text("Liczba głownych naczyń")
    caa = st.slider("major_vsssels", value=2, min_value=0, max_value=3) #major_vsssels
    
    st.text("Czy występuje u ciebie angina wysiłkowa?")
    exng = st.slider("exercise_induced_angina", value=0, min_value=0, max_value=1)#Do zmiany na kulki exercise_induced_angina
    
    st.text("Podaj cisnienie krwi podczas spoczynku")
    trtbps = st.slider("resting_blood_pressure", value=0, min_value=0, max_value=150)#Do zmiany na wpisywane - resting_blood_pressure
    
    st.text("Cholesterol w mg/dl pobrany za pomocą czujnika BMI")
    chol = st.slider("cholestoral in mg/dl fetched via BMI sensor", value=0, min_value=0, max_value=150)#Do zmiany na wpisywane  cholestoral in mg/dl fetched via BMI sensor
    
    st.text("Poziom cukru we krwi na czczo")
    fbs = st.slider("fasting_blood_sugar", value=0, min_value=0, max_value=1)#Do zmiany na kulki fasting_blood_sugar
    
    st.text("Wyniki spoczynkowego elektrokardiogramu (EKG)")
    st.text("0: normalny")
    st.text("1: obecność nieprawidłowości fali ST-T (odwrócenia fali T i/lub elewacja lub depresja ST o > 0,05 mV)")
    st.text(" 2: prawdopodobne lub pewne przerost lewej komory według kryteriów Estesa")

    restecg = st.slider("resting_electrocardiographic_results", value=2, min_value=0, max_value=2)#Do zmiany na kulki resting_electrocardiographic_results
    
    st.text("Twoje maksymalnie zmierzone tetno")
    thalachh = st.slider("maximum_heart_rate_achieved", value=0, min_value=0, max_value=150)#Do zmiany na wpisywane maximum_heart_rate_achieved
    
    st.text("Test wysiłkowy z Thall")
    thall = st.slider("Thall rate", value=2, min_value=0, max_value=3) #Thall rate
    
    st.text("nachylenie segmentu ST na EKG")
    slp = st.slider("Sloop", value=2, min_value=0, max_value=2) #Sloop
    
    st.text("W sumie nie wiem")
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