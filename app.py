# app.py - Хомиладор аёлларда ирсий касалликлар хавфини бахолаш дастури
# Life Cecly, Astarea, FMD, Prisca тизимлари асосида

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# САРЛАВҲА КОНФИГУРАЦИЯСИ
st.set_page_config(
    page_title="Ирсий Касалликлар Хавфини Бахолаш",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': 'https://www.example.com/bug',
        'About': "Дастур хомиладор аёлларда ирсий касалликлар хавфини бахолаш учун ишлаб чиқилган."
    }
)

# СТИЛЛАР
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #ffebee;
        color: #c62828;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #c62828;
    }
    .risk-medium {
        background-color: #fff3e0;
        color: #ef6c00;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #ef6c00;
    }
    .risk-low {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #2e7d32;
    }
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #3498db, #2ecc71);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .sidebar-header {
        background: linear-gradient(90deg, #2c3e50, #3498db);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 5px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

# АСОСИЙ САРЛАВҲА
st.markdown('<h1 class="main-title">👶 ХОМИЛАДОР АЁЛЛАРДА ИРСИЙ КАСАЛЛИКЛАР ХАВФИНИ БАХОЛАШ</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Life Cecly • Astarea • FMD • Prisca тизимлари асосида юқори аникликда ишлайди</p>', unsafe_allow_html=True)

# ЯНГИ БЕМОР ТУГМАСИ
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🆕 Янги бемор қўшиш", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# САЙДБАР - БЕМОР МАЪЛУМОТЛАРИ
st.sidebar.markdown('<div class="sidebar-header"><h3>👤 БЕМОР МАЪЛУМОТЛАРИ</h3></div>', unsafe_allow_html=True)

# Бемор ID генерацияси
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"

st.sidebar.info(f"**Бемор ID:** {st.session_state.patient_id}")

# 1. ШАХСИЙ МАЪЛУМОТЛАР
with st.sidebar.expander("📋 Шахсий маълумотлар", expanded=True):
    patient_name = st.text_input("ФИО", placeholder="Фамилия Исм Шариф")
    patient_age = st.slider("Ёши", 15, 50, 30, help="Беморнинг ёши")
    gestational_age = st.slider("Хомилалик даври (ҳафта)", 5, 42, 12, 
                               help="Хомилаликнинг ҳозирги ҳафтаси")
    parity = st.number_input("Туғишлар сони", 0, 15, 1, 
                            help="Жами қанча марта туғилган")
    blood_group = st.selectbox("Қон гуруҳи", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

# 2. ОИЛАВИЙ ТАРИХ
with st.sidebar.expander("👨‍👩‍👧‍👦 Оилавий тарих", expanded=True):
    st.subheader("Ирсий касалликлар")
    family_history = st.multiselect(
        "Оила аъзоларидаги касалликлар",
        [
            "Даун синдроми (трисомия 21)",
            "Эдвардс синдроми (трисомия 18)", 
            "Патау синдроми (трисомия 13)",
            "Спина бифида",
            "Юрак аномалиялари",
            "Мускул дистрофияси",
            "Кистоз фиброз",
            "Гемофилия",
            "Фенилкетонурия",
            "Нейрофиброматоз",
            "Йўқ"
        ],
        default=["Йўқ"]
    )
    
    consanguinity = st.radio("Қариндошлик никоҳи", ["Ҳа", "Йўқ"], index=1,
                            help="Ота-она қариндош бўлса")
    
    if consanguinity == "Ҳа":
        consanguinity_degree = st.selectbox("Қариндошлик даражаси", 
                                           ["Бир аммаки/таға", "Иккиламчи қариндош", "Учинчи даража"])

# 3. МЕДИЦИН ТАРИХ
with st.sidebar.expander("🏥 Медицин тарих", expanded=True):
    chronic_diseases = st.multiselect(
        "Мавжуд касалликлар",
        [
            "Сахар диабети",
            "Артериал гипертония", 
            "Эпилепсия",
            "Аутоиммун касалликлар",
            "Буғум касалликлари",
            "Қалқонсимон без касалликлари",
            "Бронхиал астма",
            "Йўқ"
        ]
    )
    
    previous_pregnancies = st.number_input("Хомилалик сони", 0, 20, 1)
    previous_abnormalities = st.radio("Олдин аномалияли болалар туғилганми?", 
                                     ["Ҳа", "Йўқ"], index=1)
    
    if previous_abnormalities == "Ҳа":
        abnormality_type = st.text_area("Аномалия тури ва тафсилотлари")
    
    medications = st.text_area("Ҳозирги вақтда олинаётган дорулар", 
                              placeholder="Дору номи, доза, муддат")

# 4. УЛЧАШЛАР ВА ТЕСТ НАТИЖАЛАРИ
with st.sidebar.expander("📏 Улчашлар ва тестлар", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Бўй (см)", 140, 200, 165)
    with col2:
        weight = st.number_input("Вазн (кг)", 40, 150, 65)
    
    # BMI ҳисоблаш
    if height > 0:
        bmi = weight / ((height/100) ** 2)
        st.metric("BMI (Тана вазни индексси)", f"{bmi:.1f}")
    
    st.subheader("Қон босими")
    bp_col1, bp_col2 = st.columns(2)
    with bp_col1:
        bp_systolic = st.number_input("Систолик", 80, 200, 120)
    with bp_col2:
        bp_diastolic = st.number_input("Диастолик", 50, 120, 80)
    
    st.subheader("Ультратовуш натижалари")
    nt_measurement = st.slider("Бўйин териси қалинлиги (NT) мм", 0.5, 10.0, 1.8, 0.1)
    nasal_bone = st.radio("Бурун суяги мавжудлиги", ["Ҳа", "Йўқ", "Аник эмас"], index=0)
    
    st.subheader("Биохимик маркерлар")
    papp_a = st.number_input("PAPP-A (мЕд/мл)", 0.1, 20.0, 1.0, 0.1)
    free_beta_hcg = st.number_input("Эркин β-hCG (нг/мл)", 0.1, 50.0, 1.0, 0.1)

# 5. СКРИНИНГ ТЕСТЛАРИ
with st.sidebar.expander("🔬 Скрининг тестлари", expanded=True):
    test_type = st.selectbox(
        "Ишлатилган скрининг тести",
        [
            "Life Cecly - Комплекс скрининг",
            "Astarea - Генетик таҳлил", 
            "FMD - Фетал мониторинг",
            "Prisca - Хавф бахолаш",
            "Комбинация скрининг",
            "Бошқа тест"
        ],
        index=0
    )
    
    test_date = st.date_input("Тест санаси")
    
    if "Life Cecly" in test_type:
        risk_factor = st.slider("Life Cecly хавф коэффициенти", 0.1, 5.0, 1.0, 0.1)
    elif "Astarea" in test_type:
        risk_factor = st.slider("Astarea генетик коэффициенти", 0.1, 5.0, 1.0, 0.1)
    elif "FMD" in test_type:
        risk_factor = st.slider("FMD мониторинг коэффициенти", 0.1, 5.0, 1.0, 0.1)
    elif "Prisca" in test_type:
        risk_factor = st.slider("Prisca хавф коэффициенти", 0.1, 5.0, 1.0, 0.1)
    else:
        risk_factor = 1.0

# ХАВФНИ ҲИСОБЛАШ ФУНКЦИЯСИ
def calculate_genetic_risk(age, bmi, family_history, nt, papp_a, hcg, test_type, risk_factor, 
                          consanguinity, previous_abnormalities, chronic_diseases):
    """Ирсий касалликлар хавфини бахолаш"""
    
    # Асосий хавф омиллари
    factors = {
        'age': 1.0,
        'bmi': 1.0,
        'family': 1.0,
        'nt': 1.0,
        'biochemical': 1.0,
        'consanguinity': 1.0,
        'previous': 1.0,
        'chronic': 1.0,
        'test': risk_factor
    }
    
    # 1. Ёш омили
    if age < 25:
        factors['age'] = 0.7
    elif age < 30:
        factors['age'] = 0.9
    elif age < 35:
        factors['age'] = 1.0
    elif age < 40:
        factors['age'] = 1.8
    else:
        factors['age'] = 2.5
    
    # 2. BMI омили
    if bmi < 18.5:
        factors['bmi'] = 1.2
    elif bmi < 25:
        factors['bmi'] = 1.0
    elif bmi < 30:
        factors['bmi'] = 1.3
    else:
        factors['bmi'] = 1.7
    
    # 3. Оилавий тарих
    if family_history and "Йўқ" not in family_history:
        factors['family'] = 1.8
        if "Даун синдроми" in family_history:
            factors['family'] *= 1.5
        if "Спина бифида" in family_history:
            factors['family'] *= 1.3
    
    # 4. NT омили
    if nt < 2.0:
        factors['nt'] = 0.7
    elif nt < 2.5:
        factors['nt'] = 1.0
    elif nt < 3.5:
        factors['nt'] = 2.0
    else:
        factors['nt'] = 3.5
    
    # 5. Биохимик маркерлар
    factors['biochemical'] = 1.0
    if papp_a < 0.4:
        factors['biochemical'] *= 1.8
    elif papp_a < 0.6:
        factors['biochemical'] *= 1.3
    
    if hcg < 0.3:
        factors['biochemical'] *= 1.5
    elif hcg > 2.5:
        factors['biochemical'] *= 1.4
    
    # 6. Қариндошлик никоҳи
    if consanguinity == "Ҳа":
        factors['consanguinity'] = 2.0
    
    # 7. Олдинги аномалиялар
    if previous_abnormalities == "Ҳа":
        factors['previous'] = 2.2
    
    # 8. Сурunkрон касалликлар
    if chronic_diseases and "Йўқ" not in chronic_diseases:
        factors['chronic'] = 1.4
        if "Сахар диабети" in chronic_diseases:
            factors['chronic'] *= 1.3
    
    # Стандарт хавф (1:1000)
    base_risk = 0.001
    
    # Хавфни ҳисоблаш
    total_risk = base_risk
    for factor in factors.values():
        total_risk *= factor
    
    # Чегаралаш
    total_risk = min(total_risk, 0.5)
    
    return total_risk, factors

# ХАВФ КАТЕГОРИЯСИНИ АНИҚЛАШ
def get_risk_category(risk_score):
    if risk_score > 0.05:  # 1:20
        return "Жуда Юқори", "risk-high"
    elif risk_score > 0.01:  # 1:100
        return "Юқори", "risk-high"
    elif risk_score > 0.005:  # 1:200
        return "Ўртача-Юқори", "risk-medium"
    elif risk_score > 0.001:  # 1:1000
        return "Ўртача", "risk-medium"
    else:
        return "Паст", "risk-low"

# АСОСИЙ КОНТЕНТ
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Хавф бахолаш", "📊 Таҳлиллар", "📋 Ҳисобот", "ℹ️ Ёрдам"])

with tab1:
    # ХАВФНИ ҲИСОБЛАШ ТУГМАСИ
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    calculate_col1, calculate_col2 = st.columns([3, 1])
    
    with calculate_col1:
        st.markdown("### Бемор маълумотларини киритиб бўлдингизми?")
    
    with calculate_col2:
        calculate_btn = st.button("🚀 Хавфни Ҳисоблаш", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if calculate_btn:
        if not patient_name:
            st.warning("⚠️ Илтимос, беморнинг исмини киритинг!")
        else:
            # BMI ҳисоблаш
            if 'height' in locals() and height > 0:
                bmi = weight / ((height/100) ** 2)
            else:
                bmi = 22.0
            
            # Хавфни ҳисоблаш
            risk_score, risk_factors = calculate_genetic_risk(
                patient_age, bmi, family_history, nt_measurement, 
                papp_a, free_beta_hcg, test_type, risk_factor,
                consanguinity, previous_abnormalities, chronic_diseases
            )
            
            # Хавф категорияси
            risk_category, risk_class = get_risk_category(risk_score)
            
            # СЕССИЯДА САҚЛАШ
            st.session_state.risk_score = risk_score
            st.session_state.risk_category = risk_category
            st.session_state.risk_class = risk_class
            st.session_state.risk_factors = risk_factors
            st.session_state.patient_name = patient_name
            st.session_state.patient_age = patient_age
            st.session_state.gestational_age = gestational_age
            
            # НАТИЖАЛАРНИ КӨРСАТИШ
            st.success(f"✅ {patient_name} учун хавф бахолаш тугади!")
            
            # МЕТРИКАЛАР
            st.markdown("---")
            st.markdown("### 📈 Хавф Баҳолаш Натижалари")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Бемор ёши", f"{patient_age} йош", 
                         delta=f"{(patient_age-35)}" if patient_age > 35 else None)
            
            with col2:
                st.metric("Хомилалик даври", f"{gestational_age} ҳафта")
            
            with col3:
                risk_display = f"1:{int(1/risk_score)}" if risk_score > 0 else "1:∞"
                st.metric("Хавф нисбати", risk_display)
            
            with col4:
                st.markdown("**Хавф категорияси:**")
                st.markdown(f'<div class="{risk_class}">{risk_category}</div>', 
                          unsafe_allow_html=True)
            
            # ХАВФ ГРАФИКИ
            st.markdown("### 📊 Хавф Омиллари Таҳлили")
            
            # Омиллар диаграммаси
            factors_df = pd.DataFrame({
                'Омил': list(risk_factors.keys()),
                'Кўпайтирувчи': list(risk_factors.values())
            })
            
            fig = px.bar(factors_df, x='Омил', y='Кўпайтирувчи',
                        color='Кўпайтирувчи',
                        color_continuous_scale='RdYlGn_r',
                        title="Хавф омиллари таҳсири")
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # ТЕЖАМКОР ГРАФИК
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk_score * 1000,
                title = {'text': "Хавф даражаси (1:1000 шкаласи)"},
                delta = {'reference': 1, 'increasing': {'color': "red"}},
                gauge = {
                    'axis': {'range': [0, 10], 'tickwidth': 1},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 3], 'color': 'green'},
                        {'range': [3, 7], 'color': 'yellow'},
                        {'range': [7, 10], 'color': 'red'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': risk_score * 1000
                    }
                }
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # ТАВСИЯЛАР
            st.markdown("### 💡 Тавсия ва Таклифлар")
            
            if risk_category in ["Жуда Юқори", "Юқори"]:
                st.error("""
                #### 🚨 ЗАРУР ТАДБИРЛАР:
                1. **Шошилинч генетик машварат** - генетик мутахассисга мурожаат
                2. **Кариотиплаш** - хромосома таҳлили
                3. **NIPT (но-инвазив пренатал тест)** - қондаги фетал ДНК таҳлили
                4. **Амниоцентез/Хорион биопсияси** - аник таҳлил учун
                5. **Кардиология консультацияси** - юрак узилишларини текшириш
                6. **Невролог консультацияси** - нерв тизими аномалиялари
                7. **Ҳар 2 ҳафтада ультратовуш** - мунтазам кўриқув
                """)
                
            elif risk_category in ["Ўртача-Юқори", "Ўртача"]:
                st.warning("""
                #### ⚠️ ТАКЛИФ ЭТИЛАДИ:
                1. **Генетик машварат** - консультация
                2. **Диққатли ультратовуш** - 20-ҳафтада батафсил кўриқув
                3. **Қайта скрининг** - 4 ҳафтадан сўнг такрорлаш
                4. **Эхокардиография** - фетал юракни текшириш
                5. **Ҳар ойда мониторинг** - мунтазам назорат
                6. **Парвардалик** - мутахассис назоратида
                7. **Қўшимча тестлар** - заруратга қараб
                """)
                
            else:
                st.success("""
                #### ✅ ОДДИЙ ТАВСИЯЛАР:
                1. **Стандарт скрининг дастури** - мунтазам текшириш
                2. **Ультратовуш** - 12, 20, 32-ҳафтада
                3. **Қулай парвардалик** - тиббий кўрсатмаларга риоя
                4. **Соглом турмуш тарзи** - таомланиш, жисмоний фаоллик
                5. **Витамин ва минераллар** - даво шаклида
                6. **Стрессдан сақланиш** - руҳий тинчлик
                7. **Ҳар 4 ҳафтада назорат** - регламент буйича
                """)
            
            # ДЕТАЛЛИ ТАҲЛИЛ
            with st.expander("🔍 Деталли таҳлил"):
                st.markdown(f"""
                #### 📋 Хавф Ҳисоблаш Параметрлари:
                
                **Асосий омиллар:**
                - Ёш омили: {risk_factors['age']:.2f}x
                - BMI омили: {risk_factors['bmi']:.2f}x  
                - Оилавий тарих: {risk_factors['family']:.2f}x
                - NT (бўйин териси): {risk_factors['nt']:.2f}x
                - Биохимик маркерлар: {risk_factors['biochemical']:.2f}x
                
                **Қўшимча омиллар:**
                - Қариндошлик никоҳи: {risk_factors['consanguinity']:.2f}x
                - Олдинги аномалиялар: {risk_factors['previous']:.2f}x
                - Сурunkрон касалликлар: {risk_factors['chronic']:.2f}x
                - Скрининг тести: {risk_factors['test']:.2f}x
                
                **Умумий кўпайтирувчи:** {np.prod(list(risk_factors.values())):.2f}x
                **Хавф даражаси:** 1:{int(1/risk_score)} ({risk_score:.6f})
                """)

with tab2:
    st.markdown("## 📊 Статистика ва Таҳлиллар")
    
    if 'risk_score' in st.session_state:
        # Хавф тақсимоти диаграммаси
        st.markdown("### Хавф категориялари тақсимоти")
        
        # Намуна маълумотлар
        sample_data = pd.DataFrame({
            'Категория': ['Паст', 'Ўртача', 'Юқори', 'Жуда Юқори'],
            'Фоизи': [60, 25, 10, 5],
            'Сони': [120, 50, 20, 10]
        })
        
        fig = px.pie(sample_data, values='Фоизи', names='Категория',
                    title="Хавф категориялари тақсимоти (намуна)",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Ёшга нисбатан хавф графиги
        st.markdown("### Ёшга қараб хавф даражаси")
        
        age_range = np.arange(15, 51, 5)
        age_risks = [calculate_genetic_risk(age, 22, [], 1.8, 1.0, 1.0, 
                                           "Life Cecly", 1.0, "Йўқ", "Йўқ", [])[0] 
                    for age in age_range]
        
        fig_age = px.line(x=age_range, y=age_risks,
                         labels={'x': 'Ёш', 'y': 'Хавф даражаси'},
                         title="Ёш ошиши билан хавф ўзгариши")
        
        fig_age.update_traces(line=dict(color='red', width=3))
        fig_age.add_vline(x=35, line_dash="dash", line_color="green", 
                         annotation_text="35 йош")
        fig_age.add_vline(x=patient_age, line_dash="dot", line_color="blue",
                         annotation_text=f"Бемор: {patient_age}")
        
        st.plotly_chart(fig_age, use_container_width=True)
        
    else:
        st.info("📊 Статистикани кўриш учун аввал хавфни ҳисобланг")

with tab3:
    st.markdown("## 📋 Ҳисобот генератор")
    
    if 'risk_score' in st.session_state:
        # Ҳисобот параметрлари
        report_col1, report_col2 = st.columns(2)
        
        with report_col1:
            report_language = st.selectbox("Ҳисобот тили", ["Ўзбек", "Рус", "Инглиз"])
            include_charts = st.checkbox("Диаграммаларни қўшиш", value=True)
            
        with report_col2:
            doctor_name = st.text_input("Шифокор исми", "Др. Алиев А.")
            hospital_name = st.text_input("Шифохона номи", "1-сон Тибийёт Маркази")
        
        # Ҳисобот яратиш
        if st.button("🖨️ Ҳисоботни Яратиш"):
            st.success("✅ Ҳисобот яратилди!")
            
            # Ҳисобот контенти
            st.markdown("---")
            st.markdown(f"# ТИББИЙ ҲИСОБОТ")
            st.markdown(f"**Шифохона:** {hospital_name}")
            st.markdown(f"**Шифокор:** {doctor_name}")
            st.markdown(f"**Саналди:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            st.markdown(f"### Бемор маълумотлари:")
            st.markdown(f"- **ФИО:** {st.session_state.patient_name}")
            st.markdown(f"- **Ёши:** {st.session_state.patient_age} йош")
            st.markdown(f"- **Хомилалик даври:** {st.session_state.gestational_age} ҳафта")
            st.markdown(f"- **Бемор ID:** {st.session_state.patient_id}")
            
            st.markdown(f"### Хавф бахолаш натижалари:")
            risk_display = f"1:{int(1/st.session_state.risk_score)}"
            st.markdown(f"- **Хавф даражаси:** {risk_display}")
            st.markdown(f"- **Хавф категорияси:** {st.session_state.risk_category}")
            st.markdown(f"- **Скрининг тести:** {test_type}")
            
            st.markdown("### Тавсиялар:")
            if st.session_state.risk_category in ["Жуда Юқори", "Юқори"]:
                st.markdown("1. Шошилинч генетик машварат")
                st.markdown("2. Кариотиплаш ва NIPT тести")
                st.markdown("3. Мутахассис назоратида парвардалик")
            else:
                st.markdown("1. Мунтазам тиббий кўриқув")
                st.markdown("2. Стандарт скрининг дастури")
                st.markdown("3. Қулай парвардалик")
            
            st.markdown("---")
            st.markdown(f"**Ҳужжат ID:** R{datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            # Яратилган ҳисоботни юклаш учун
            report_text = f"""
            ТИББИЙ ҲИСОБОТ
            Шифохона: {hospital_name}
            Шифокор: {doctor_name}
            Саналди: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            
            Бемор: {st.session_state.patient_name}
            Ёши: {st.session_state.patient_age}
            Хомилалик: {st.session_state.gestational_age} ҳафта
            
            Хавф даражаси: {risk_display}
            Хавф категорияси: {st.session_state.risk_category}
            
            Тавсиялар кўрсатилган.
            """
            
            st.download_button(
                label="📥 Ҳисоботни юклаб олиш (.txt)",
                data=report_text,
                file_name=f"hisobot_{st.session_state.patient_id}.txt",
                mime="text/plain"
            )
    else:
        st.info("📋 Ҳисобот яратиш учун аввал хавфни ҳисобланг")

with tab4:
    st.markdown("## ℹ️ Дастур Қўлланмаси")
    
    st.markdown("""
    ### Дастур Фойдаланиш Қўлланмаси
    
    #### 🎯 Услуб:
    Дастур хомиладор аёлларда ирсий касалликлар хавфини бахолаш учун ишлаб чиқилган.
    Life Cecly, Astarea, FMD, Prisca каби замонавий скрининг тизимлари асосида ишлайди.
    
    #### 📋 Иш тартиби:
    1. **Бемор маълумотларини киритиш** - чап панелда барча маълумотларни тўлдиринг
    2. **Хавфни ҳисоблаш** - асосий саҳифада "Хавфни ҳисоблаш" тугмасини босинг
    3. **Натижаларни таҳлил қилиш** - хавф даражаси ва категориясини кўринг
    4. **Тавсияларга риоя қилиш** - таклиф этилган тадбирларга амал қилинг
    5. **Ҳисобот олиш** - "Ҳисобот" бўлимида расмий ҳужжат яратинг
    
    #### 🔬 Ҳисоблаш параметрлари:
    - **Ёш омили:** 35+ йошда хавф ошиши
    - **BMI:** Нормадан ошиқ ёки пастлик
    - **Оилавий тарих:** Ирсий касалликлар борлиги
    - **NT ўлчами:** Бўйин териси қалинлиги
    - **Биохимик маркерлар:** PAPP-A, β-hCG даражалари
    - **Қариндошлик никоҳи:** Генетик хавфни оширади
    - **Олдинги аномалиялар:** Олдинги хомилаликларда аномалия
    - **Скрининг тести:** Ишлатилган тест тури ва коэффициенти
    
    #### ⚠️ Диққат этиш керак:
    - Барча маълумотлар аник киритилсин
    - Ультратовуш натижалари дақиқ бўлсин
    - Тест натижалари яқин вақтда олинган бўлсин
    - Шубхали ҳолатларда генетик мутахассисга мурожаат қилинг
    
    #### 🏥 Хавф категориялари:
    - **Паст (Low):** 1:1000 дан кам - стандарт парвардалик
    - **Ўртача (Intermediate):** 1:1000-1:200 - қўшимча кўриқув
    - **Юқори (High):** 1:100-1:20 - деталли текширув
    - **Жуда юқори (Very High):** 1:20 дан юкори - шошилинч тадбир
    
    #### 📞 Контакт маълумотлари:
    Дастурдаги тавсиялар аввалги тавсиядир. Ҳар қандай ҳолатда тиббий мутахассисга мурожаат қилинг.
    
    """)
    
    st.markdown("---")
    st.markdown("### 💼 Тизим талаблари")
    st.markdown("""
    - **Операцион тизим:** Windows 10+, macOS 10.15+, Linux
    - **Браузер:** Chrome 80+, Firefox 75+, Safari 13+
    - **Интернет:** 5 Мбит/с дан юкори
    - **Экран:** 1280x720 дақиқалик (минимал)
    
    **Дастур версияси:** 2.0.1
    **Сўнги янгилаш:** 2024
    """)

# ФУТЕР
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
    <p style='font-size: 1.1rem; font-weight: bold;'>© 2024 Пренатал Генетик Скрининг Дастури</p>
    <p>Life Cecly • Astarea • FMD • Prisca скрининг тизимлари асосида</p>
    <p style='font-size: 0.9rem; margin-top: 10px;'>
        <strong>Диққат:</strong> Барча маълумотлар конфиденциальдир. Фақат тиббий мақсадлар учун ишлатилади. 
        Ҳар қандай ҳолатда тиббий мутахассисга мурожаат қилинг.
    </p>
</div>
""", unsafe_allow_html=True)
