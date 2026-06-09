import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hospital Patient Viewer", layout="wide")
st.title("🏥 Hospital Patient Viewer")
BACKEND_URL = "http://localhost:8001"

tab_glowna, tab_wyswietl,tab_szukaj, tab_dodaj, tab_statystyki = st.tabs(["🏠 Strona Główna","📖 Wyświetl Pacjentów", "🔍 Szukaj pacjenta", "➕ Dodaj Pacjenta", "📊 Statystyki"])

#########################################################################################################################
with tab_glowna:
    st.header("Witamy w systemie zarządzania pacjentami!")
    st.write(
        "Ten system pozwala na łatwe zarządzanie informacjami o pacjentach."
    )
    st.write(
        "Możesz przeglądać listę wszystkich pacjentów, dodawać nowych pacjentów, wyszukiwać pacjentów lub pobierać statystyki dotyczące pacjentów."
    )
    try:
        response= requests.get(f"{BACKEND_URL}/patients/count")
        if response.status_code == 200:
            st.write(f"Liczba pacjentów w bazie danych: {response.json()['count']}")
        else:
            st.error("Nie można pobrać danych z serwera.")
    except requests.RequestException as e:
        st.error(f"Error fetching health data: {e}")
##########################################################################################################################
with tab_wyswietl:
    st.header("Lista Pacjentów")
    with st.expander("📖 Zobacz legendę i opis metryk medycznych "):
        st.markdown("""
    Poniższy słownik wyjaśnia znaczenie poszczególnych kolumn oraz kodowanie numeryczne zastosowane w bazie danych szpitala.
    """)
    
        # Podział na dwie równe kolumny dla lepszej czytelności na szerokim ekranie
        col_leg1, col_leg2 = st.columns(2)
        
        with col_leg1:
            st.markdown("""
            ### 👤 Podstawowe dane i wywiad
            * **age** – Wiek pacjenta
                * Wartość numeryczna wyrażona w latach.
            * **sex** – Płeć pacjenta
                * `0` – Kobieta
                * `1` – Mężczyzna
            * **chest_pain** – Typ bólu w klatce piersiowej (ang. *Chest Pain Type*)
                * `0` – Typowa dławica piersiowa (*Typical Angina*)
                * `1` – Nietypowa dławica piersiowa (*Atypical Angina*)
                * `2` – Ból niedławicowy (*Non-anginal Pain*)
                * `3` – Asymptomatyczny (*Asymptomatic*)
            * **fasting_blood_sugar** – Cukier we krwi na czczo
                * `0` – Fałsz (stężenie cukru w normie, poniżej lub równe 120 mg/dl)
                * `1` – Prawda (stężenie podwyższone, powyżej 120 mg/dl)
            * **angina** – Dławica piersiowa wywołana wysiłkiem fizycznym
                * `0` – Nie występuje
                * `1` – Występuje
            * **target** – Diagnoza końcowa (Wynik kardiologiczny)
                * `0` – Brak stwierdzonej choroby serca (Pacjent zdrowy)
                * `1` – Stwierdzona choroba serca (Pacjent chory)
            """)
            
        with col_leg2:
            st.markdown("""
            ### 🩺 Parametry kliniczne i wyniki EKG
            * **resting_blood** – Spoczynkowe ciśnienie krwi
                * Wartość rejestrowana przy przyjęciu do szpitala, wyrażona w mm Hg.
            * **serum_cholesterol** – Cholesterol całkowity
                * Poziom cholesterolu w surowicy krwi, wyrażony w mg/dl.
            * **electrocardiography** – Wynik spoczynkowego badania EKG
                * `0` – W normie
                * `1` – Abberacje fali ST-T (odwrócenie fali T lub uniesienie/obniżenie odcinka ST > 0.05 mV)
                * `2` – Wykazany prawdopodobny lub pewny przerost lewej komory serca (według kryteriów Estesa)
            * **maximum_heart_rate** – Maksymalne osiągnięte tętno
                * Najwyższa wartość tętna zarejestrowana podczas testu wysiłkowego.
            * **oldpeak_ST** – Obniżenie odcinka ST
                * Wartość obniżenia odcinka ST wywołana wysiłkiem fizycznym w relacji do stanu spoczynku.
            * **slope_ST** – Nachylenie odcinka ST
                * Kształt nachylenia odcinka ST w szczytowym momencie wysiłku fizycznego:
                    * `0` – Rosnące (*Upsloping*)
                    * `1` – Płaskie (*Flat*)
                    * `2` – Opadające (*Downsloping*)
            * **major_vessel_number** – Liczba głównych naczyń krwionośnych
                * Liczba naczyń (w przedziale 0–3) widocznych w trakcie badania fluoroskopowego.
            * **thal** – Wynik scyntygrafii serca (test z użyciem talu)
                * `0` – Wynik prawidłowy
                * `1` – Stały defekt (*Fixed defect*)
                * `2` – Odwracalny defekt (*Reversable defect*)
            """)
        
    st.divider()
    st.subheader("Filtry")
    wybrana_plec = st.selectbox(
        "Filtruj według płci (0 = Kobiety, 1 = Mężczyźni):",
        options=["Wszyscy", "Kobiety", "Mężczyźni"]
    )
    try:
        response = requests.get(f"{BACKEND_URL}/patients")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            if wybrana_plec == "Kobiety":
                df = df[df["sex"] == 0]
            elif wybrana_plec == "Mężczyźni":
                df = df[df["sex"] == 1]
            st.dataframe(df, width='stretch')
            st.success(f"Pomyślnie załadowano {len(df)} pacjentów.")
        else:
            st.error(f"Nie można pobrać danych. Serwer zwrócił błąd: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Brak połączenia z FastAPI: {e}")
###########################################################################################################################
with tab_szukaj:
    st.header("🔍 Sprawdź Pacjenta")
    with st.expander("📖 Zobacz legendę i opis metryk medycznych "):
        st.markdown("""
    Poniższy słownik wyjaśnia znaczenie poszczególnych kolumn oraz kodowanie numeryczne zastosowane w bazie danych szpitala.
    """)
    
        # Podział na dwie równe kolumny dla lepszej czytelności na szerokim ekranie
        col_leg1, col_leg2 = st.columns(2)
        
        with col_leg1:
            st.markdown("""
            ### 👤 Podstawowe dane i wywiad
            * **age** – Wiek pacjenta
                * Wartość numeryczna wyrażona w latach.
            * **sex** – Płeć pacjenta
                * `0` – Kobieta
                * `1` – Mężczyzna
            * **chest_pain** – Typ bólu w klatce piersiowej (ang. *Chest Pain Type*)
                * `0` – Typowa dławica piersiowa (*Typical Angina*)
                * `1` – Nietypowa dławica piersiowa (*Atypical Angina*)
                * `2` – Ból niedławicowy (*Non-anginal Pain*)
                * `3` – Asymptomatyczny (*Asymptomatic*)
            * **fasting_blood_sugar** – Cukier we krwi na czczo
                * `0` – Fałsz (stężenie cukru w normie, poniżej lub równe 120 mg/dl)
                * `1` – Prawda (stężenie podwyższone, powyżej 120 mg/dl)
            * **angina** – Dławica piersiowa wywołana wysiłkiem fizycznym
                * `0` – Nie występuje
                * `1` – Występuje
            * **target** – Diagnoza końcowa (Wynik kardiologiczny)
                * `0` – Brak stwierdzonej choroby serca (Pacjent zdrowy)
                * `1` – Stwierdzona choroba serca (Pacjent chory)
            """)
            
        with col_leg2:
            st.markdown("""
            ### 🩺 Parametry kliniczne i wyniki EKG
            * **resting_blood** – Spoczynkowe ciśnienie krwi
                * Wartość rejestrowana przy przyjęciu do szpitala, wyrażona w mm Hg.
            * **serum_cholesterol** – Cholesterol całkowity
                * Poziom cholesterolu w surowicy krwi, wyrażony w mg/dl.
            * **electrocardiography** – Wynik spoczynkowego badania EKG
                * `0` – W normie
                * `1` – Abberacje fali ST-T (odwrócenie fali T lub uniesienie/obniżenie odcinka ST > 0.05 mV)
                * `2` – Wykazany prawdopodobny lub pewny przerost lewej komory serca (według kryteriów Estesa)
            * **maximum_heart_rate** – Maksymalne osiągnięte tętno
                * Najwyższa wartość tętna zarejestrowana podczas testu wysiłkowego.
            * **oldpeak_ST** – Obniżenie odcinka ST
                * Wartość obniżenia odcinka ST wywołana wysiłkiem fizycznym w relacji do stanu spoczynku.
            * **slope_ST** – Nachylenie odcinka ST
                * Kształt nachylenia odcinka ST w szczytowym momencie wysiłku fizycznego:
                    * `0` – Rosnące (*Upsloping*)
                    * `1` – Płaskie (*Flat*)
                    * `2` – Opadające (*Downsloping*)
            * **major_vessel_number** – Liczba głównych naczyń krwionośnych
                * Liczba naczyń (w przedziale 0–3) widocznych w trakcie badania fluoroskopowego.
            * **thal** – Wynik scyntygrafii serca (test z użyciem talu)
                * `0` – Wynik prawidłowy
                * `1` – Stały defekt (*Fixed defect*)
                * `2` – Odwracalny defekt (*Reversable defect*)
            """)
    st.divider()
    st.markdown("### Wyszukaj pacjenta po ID")
    patient_id = st.number_input("Wprowadź ID pacjenta:", min_value=1, step=1)
    if st.button("Szukaj"):
        try:
            # Najpierw pobierz liczbę pacjentów, aby sprawdzić zakres ID
            cnt_resp = requests.get(f"{BACKEND_URL}/patients/count")
            if cnt_resp.status_code == 200:
                total = cnt_resp.json().get("count", 0)
            else:
                st.error("Nie można pobrać liczby pacjentów z serwera.")
                total = None

            if total is not None:
                if int(patient_id) > total:
                    st.warning(f"Wprowadzone ID ({int(patient_id)}) jest większe niż liczba pacjentów ({total}). Podaj mniejsze ID.")
                else:
                    response = requests.get(f"{BACKEND_URL}/patients/{int(patient_id)}")
                    if response.status_code == 200:
                        patient_data = response.json()
                        if patient_data:
                            st.write("Dane pacjenta:")
                            df = pd.DataFrame([patient_data])
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.warning("Nie znaleziono pacjenta o podanym ID.")
                    else:
                        st.error(f"Nie można pobrać danych. Serwer zwrócił błąd: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Brak połączenia z FastAPI: {e}")
############################################################################################################################
with tab_dodaj:
    st.header("➕ Dodaj Pacjenta")
    with st.expander("📖 Zobacz legendę i opis metryk medycznych "):
        st.markdown("""
    Poniższy słownik wyjaśnia znaczenie poszczególnych kolumn oraz kodowanie numeryczne zastosowane w bazie danych szpitala.
    """)
    
        # Podział na dwie równe kolumny dla lepszej czytelności na szerokim ekranie
        col_leg1, col_leg2 = st.columns(2)
        
        with col_leg1:
            st.markdown("""
            ### 👤 Podstawowe dane i wywiad
            * **age** – Wiek pacjenta
                * Wartość numeryczna wyrażona w latach.
            * **sex** – Płeć pacjenta
                * `0` – Kobieta
                * `1` – Mężczyzna
            * **chest_pain** – Typ bólu w klatce piersiowej (ang. *Chest Pain Type*)
                * `0` – Typowa dławica piersiowa (*Typical Angina*)
                * `1` – Nietypowa dławica piersiowa (*Atypical Angina*)
                * `2` – Ból niedławicowy (*Non-anginal Pain*)
                * `3` – Asymptomatyczny (*Asymptomatic*)
            * **fasting_blood_sugar** – Cukier we krwi na czczo
                * `0` – Fałsz (stężenie cukru w normie, poniżej lub równe 120 mg/dl)
                * `1` – Prawda (stężenie podwyższone, powyżej 120 mg/dl)
            * **angina** – Dławica piersiowa wywołana wysiłkiem fizycznym
                * `0` – Nie występuje
                * `1` – Występuje
            * **target** – Diagnoza końcowa (Wynik kardiologiczny)
                * `0` – Brak stwierdzonej choroby serca (Pacjent zdrowy)
                * `1` – Stwierdzona choroba serca (Pacjent chory)
            """)
            
        with col_leg2:
            st.markdown("""
            ### 🩺 Parametry kliniczne i wyniki EKG
            * **resting_blood** – Spoczynkowe ciśnienie krwi
                * Wartość rejestrowana przy przyjęciu do szpitala, wyrażona w mm Hg.
            * **serum_cholesterol** – Cholesterol całkowity
                * Poziom cholesterolu w surowicy krwi, wyrażony w mg/dl.
            * **electrocardiography** – Wynik spoczynkowego badania EKG
                * `0` – W normie
                * `1` – Abberacje fali ST-T (odwrócenie fali T lub uniesienie/obniżenie odcinka ST > 0.05 mV)
                * `2` – Wykazany prawdopodobny lub pewny przerost lewej komory serca (według kryteriów Estesa)
            * **maximum_heart_rate** – Maksymalne osiągnięte tętno
                * Najwyższa wartość tętna zarejestrowana podczas testu wysiłkowego.
            * **oldpeak_ST** – Obniżenie odcinka ST
                * Wartość obniżenia odcinka ST wywołana wysiłkiem fizycznym w relacji do stanu spoczynku.
            * **slope_ST** – Nachylenie odcinka ST
                * Kształt nachylenia odcinka ST w szczytowym momencie wysiłku fizycznego:
                    * `0` – Rosnące (*Upsloping*)
                    * `1` – Płaskie (*Flat*)
                    * `2` – Opadające (*Downsloping*)
            * **major_vessel_number** – Liczba głównych naczyń krwionośnych
                * Liczba naczyń (w przedziale 0–3) widocznych w trakcie badania fluoroskopowego.
            * **thal** – Wynik scyntygrafii serca (test z użyciem talu)
                * `0` – Wynik prawidłowy
                * `1` – Stały defekt (*Fixed defect*)
                * `2` – Odwracalny defekt (*Reversable defect*)
            """)
        
    st.divider()
    st.subheader("Wprowadź dane nowego pacjenta")
    with st.form("patient_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
    
        with col1:
            age = st.number_input("Wiek", min_value=1, max_value=120, value=45)
            sex = st.selectbox("Płeć", options=[0, 1], format_func=lambda x: "Kobieta" if x == 0 else "Mężczyzna")
            cp = st.selectbox("Typ bólu w klatce (chest_pain)", options=[0, 1, 2, 3], 
                            format_func=lambda x: ["Typowa dławica", "Nietypowa dławica", "Ból niedławicowy", "Asymptomatyczny"][x])
            trestbps = st.number_input("Spoczynkowe ciśnienie krwi (resting_blood)", value=120)
            chol = st.number_input("Cholesterol całkowity (serum_cholesterol)", value=200)
            fbs = st.radio("Cukier na czczo > 120 mg/dl (fasting_blood_sugar)", options=[0, 1], format_func=lambda x: "Nie" if x == 0 else "Tak")
            restecg = st.selectbox("Wynik EKG (electrocardiography)", options=[0, 1, 2])

        with col2:
            thalach = st.number_input("Maksymalne tętno (maximum_heart_rate)", value=150)
            exang = st.radio("Dławica wysiłkowa (angina)", options=[0, 1], format_func=lambda x: "Nie" if x == 0 else "Tak")
            oldpeak = st.number_input("Obniżenie odcinka ST (oldpeak_ST)", value=0, step=1)
            slope = st.selectbox("Nachylenie ST (slope_ST)", options=[0, 1, 2])
            ca = st.slider("Liczba naczyń krwionośnych (ca)", 0, 4, 0)
            thal = st.selectbox("Wynik scyntygrafii serca (Thal)", options=[0, 1, 2], format_func=lambda x: ["Normalny", "Stały defekt", "Odwracalny defekt"][x])
            target = st.selectbox("Diagnoza (target)", options=[0, 1,None], format_func=lambda x: "Zdrowy" if x == 0 else "Chory" if x == 1 else "Nieznany")
# wazne - target moze byc None, bo nie zawsze musi byc znany wynik diagnozy, szczegolnie przy dodawaniu nowych pacjentow do bazy danych.
        submit_button = st.form_submit_button("Zapisz pacjenta ")

        if submit_button:

            data = {
                "age": age, "sex": sex, "chest_pain": cp, "resting_blood": trestbps,
                "serum_cholesterol": chol, "fasting_blood_sugar": fbs, "electrocardiography": restecg,
                "maximum_heart_rate": thalach, "angina": exang, "oldpeak_ST": oldpeak,
                "slope_ST": slope, "major_vessel_number": ca, "thal": thal, "target": target
            }
            try:
                res = requests.post(f"{BACKEND_URL}/patients", json=data)
                if res.status_code == 200:
                    st.success("Pacjent dodany pomyślnie!")
                else:
                    st.error(f"Błąd serwera: {res.status_code}")
            except Exception as e:
                st.error(f"Błąd połączenia: {e}")
#############################################################################################################################
with tab_statystyki:
    
    row1_col1, row1_col2 = st.columns(2)

    filter_state = {
    "min_value": None,
    "max_value": None,
    "exact_value": None
}
    params = {}

    RANGES_CONFIG = {
        "age": {"min": 0.0, "max": 120.0, "step": 1.0},
        "sex": {"min": 0.0, "max": 1.0, "step": 1.0},
        "chest_pain": {"min": 0.0, "max": 3.0, "step": 1.0},
        "resting_blood": {"min": 50.0, "max": 250.0, "step": 1.0},
        "serum_cholesterol": {"min": 100.0, "max": 600.0, "step": 1.0},
        "fasting_blood_sugar": {"min": 0.0, "max": 1.0, "step": 1.0},
        "electrocardiography": {"min": 0.0, "max": 2.0, "step": 1.0},
        "maximum_heart_rate": {"min": 50.0, "max": 250.0, "step": 1.0},
        "angina": {"min": 0.0, "max": 1.0, "step": 1.0},
        "oldpeak_ST": {"min": 0.0, "max": 10.0, "step": 0.1},
        "slope_ST": {"min": 0.0, "max": 2.0, "step": 1.0},
        "major_vessel_number": {"min": 0.0, "max": 4.0, "step": 1.0},
        "thal": {"min": 0.0, "max": 3.0, "step": 1.0},
        "target": {"min": 0.0, "max": 1.0, "step": 1.0},
    }
    all_columns = list(RANGES_CONFIG.keys())


    st.header ("📊 Statystyki Pacjentów")
    with row1_col1:
        operation = st.selectbox(
            "Wybierz operację matematyczną:",
            options=["mean", "variance", "std_dev", "covariance"],
            format_func=lambda x: {
                "mean": "Średnia (mean)",
                "variance": "Wariancja (variance)",
                "std_dev": "Odchylenie standardowe (std_dev)",
                "covariance": "Kowariancja (covariance)"
            }[x]
        )

    with row1_col2:
        metric = st.selectbox(
            "Wybierz metrykę do analizy:",
            options=all_columns,
            format_func=lambda x: f"{x}"
        )
        if operation == "covariance":
            metric2 = st.selectbox(
                "Wybierz drugą metrykę do analizy (dla kowariancji):",
                options=[col for col in all_columns if col != metric],
                format_func=lambda x: f"{x}"
            )
            metric = f"{metric}/{metric2}"
    
        url_filter=""
    
        st.write("Wybierz zakres wartości do analizy lub konkretne wartości dla metryk")

    def render_continuous_filter(label):
        st.markdown(f" **{label}**")
        c_ch1, c_ch2 = st.columns([ 1.5, 1.5])
        
        with c_ch1:
            use_range = st.checkbox("Zakres Min/Max", key=f"{label}_ch_rng", value=False)
        with c_ch2:
            use_exact = st.checkbox("Dokładna wartość", key=f"{label}_ch_ex", value=False, disabled=use_range)


        ex_input, min_val_input, max_val_input = None, None, None
        v_min = RANGES_CONFIG[label]["min"]
        v_max = RANGES_CONFIG[label]["max"]
        v_step = RANGES_CONFIG[label]["step"]
        
        if use_range:
            c_min, c_max = st.columns(2)
            with c_min:
                min_val_input = st.number_input(f"Od:", min_value=v_min, max_value=v_max, value=v_min, 
                    step=v_step, key=f"{label}_in_min")
            with c_max:
                max_val_input = st.number_input( f"Do:", min_value=v_min, max_value=v_max, value=v_max,  step=v_step, key=f"{label}_in_max" )
            if min_val_input>max_val_input:
                st.warning(f"Uwaga: Wartość 'Od' ({min_val_input}) jest większa niż 'Do' ({max_val_input}). Proszę poprawić zakres.")
                min_val_input, max_val_input = None, None
            if min_val_input == v_min:
                min_val_input = None
            if max_val_input == v_max:
                max_val_input = None
            
                min_val_input, max_val_input = None, None
        elif use_exact: 
            ex = st.number_input(f"Wartość {label}", min_value=v_min, max_value=v_max, value=v_min,  key=f"{label}_in", label_visibility="collapsed")
            if ex != v_min:
                ex_input = ex

        return{"min_value": min_val_input,"max_value": max_val_input, "exact_value": ex_input}

    col1, col2 = st.columns(2)
    with col1:

        for col in all_columns[:len(all_columns)//2]:
            res=render_continuous_filter(label=col, )
            if res["min_value"] is not None:
                url_filter += f"{col}_min={res['min_value']}&"
            if res["max_value"] is not None:
                url_filter += f"{col}_max={res['max_value']}&"
            if res["exact_value"] is not None:
                url_filter += f"{col}={res['exact_value']}&"
                

    with col2:
        for col in all_columns[len(all_columns)//2:]:
            res=render_continuous_filter(label=col, )
            if res["min_value"] is not None:
                url_filter += f"{col}_min={res['min_value']}&"
            if res["max_value"] is not None:
                url_filter += f"{col}_max={res['max_value']}&"
            if res["exact_value"] is not None:
                url_filter += f"{col}={res['exact_value']}&"
    
    url_filter = url_filter.rstrip("&")  

    st.divider()
    if operation == "covariance":
        target_url = f"{BACKEND_URL}/{operation}/{metric}?{url_filter}"
    else:
        target_url = f"{BACKEND_URL}/analyze/{metric}/{operation}?{url_filter}"
    if st.button("Oblicz statystykę"):
        try:
            response = requests.get(target_url, params=params)
            if response.status_code == 200:
                response = response.json()
                rows_counted = response.get("rows_counted", 0)

                v_list = list(response.values())
                result = v_list[-1] if v_list else None

                if rows_counted == 0:
                    st.warning("⚠️ Brak danych. Żaden pacjent w bazie nie spełnia wybranych kryteriów filtrowania.")

                elif result is not None:
                    st.success(f"### Wynik ({operation}) dla metryki **{metric}**: **{result:.2f}**")
                    st.info(f" Analiza została przeprowadzona na grupie **{rows_counted}** pacjentów spełniających kryteria.")
                else:
                    st.json(response)
            else:
                if response.status_code == 404:
                    st.error("Brak danych do analizy. Żaden pacjent w bazie nie spełnia wybranych kryteriów filtrowania.")
                else:
                    st.error(f"Błąd serwera: {response.status_code}")
        except Exception as e:
            st.error(f"Błąd połączenia: {e}")

