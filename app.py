import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import numpy as np
import streamlit as st
st.write("App started successfully!")
import streamlit as st
st.write("App starting on port 8501...")
# Page configuration
st.set_page_config(
    page_title="🌾 Агро-Погода Казахстана",
    layout="wide",
    page_icon="🌤️",
    initial_sidebar_state="collapsed"
)

# Custom CSS with natural color palette
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for natural color scheme */
    :root {
        --primary-green: #2E8B57;
        --secondary-green: #90EE90;
        --earth-brown: #D2B48C;
        --sky-blue: #87CEEB;
        --deep-blue: #4682B4;
        --warning-orange: #FF8C00;
        --danger-red: #DC143C;
        --success-green: #32CD32;
        --text-dark: #2F4F4F;
        --bg-light: #F0F8FF;
        --card-shadow: rgba(46, 139, 87, 0.1);
    }
    
    /* Main app styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Beautiful gradient header */
    .header-container {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--sky-blue) 50%, var(--earth-brown) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px var(--card-shadow);
        animation: fadeInUp 1s ease-out;
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(135deg, white 0%, var(--bg-light) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px var(--card-shadow);
        border-left: 5px solid var(--primary-green);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px var(--card-shadow);
    }
    
    .metric-card.success {
        border-left-color: var(--success-green);
    }
    
    .metric-card.warning {
        border-left-color: var(--warning-orange);
    }
    
    .metric-card.danger {
        border-left-color: var(--danger-red);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--deep-blue) 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.4);
        background: linear-gradient(135deg, var(--deep-blue) 0%, var(--primary-green) 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: linear-gradient(135deg, white 0%, var(--bg-light) 100%);
        border-radius: 25px;
        color: var(--text-dark);
        font-weight: 500;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: var(--primary-green);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--deep-blue) 100%);
        color: white !important;
        border-color: var(--primary-green);
    }
    
    /* Information panels */
    .stExpander {
        border: 2px solid var(--secondary-green);
        border-radius: 15px;
        box-shadow: 0 4px 15px var(--card-shadow);
        margin: 1rem 0;
    }
    
    .stExpander > div > div > div > div {
        background: linear-gradient(135deg, white 0%, var(--bg-light) 100%);
    }
    
    /* Footer styling */
    .footer {
        background: linear-gradient(135deg, var(--text-dark) 0%, var(--primary-green) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
        color: white;
    }
    
    .footer-content {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 2rem;
        margin-bottom: 1rem;
    }
    
    .footer-section {
        flex: 1;
        min-width: 250px;
    }
    
    .footer-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--secondary-green);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .header-subtitle {
            font-size: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .footer-content {
            flex-direction: column;
            text-align: center;
        }
    }
    
    /* Success/Warning/Error styling */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px var(--card-shadow);
    }
    
    .stAlert[data-baseweb="notification"] {
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# Beautiful header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🌾 Агро-Погода Казахстана</h1>
    <p class="header-subtitle">🌤️ Погодный помощник для фермеров, аграриев и исследователей</p>
    <p style="color: rgba(255,255,255,0.8); margin-top: 1rem;">
        📊 Анализ метеоданных NASA • 🌱 Умные рекомендации • 💡 Принятие решений на основе данных
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
for key in ["score", "fails", "rounds", "history"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key != "history" else []

# Generate sample weather data (since CSV might not be available)
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    regions = ['Астана', 'Алматы', 'Шымкент', 'Актобе', 'Караганда']
    
    data = []
    for date in dates:
        for region in regions:
            # Seasonal temperature variation
            day_of_year = date.timetuple().tm_yday
            base_temp = 15 + 20 * np.sin((day_of_year - 80) * 2 * np.pi / 365)
            temp = base_temp + np.random.normal(0, 5)
            
            # Precipitation with seasonal variation
            precip_base = 2 + 3 * np.sin((day_of_year - 120) * 2 * np.pi / 365)
            precip = max(0, precip_base + np.random.exponential(2))
            
            data.append({
                'date': date,
                'temperature_C': round(temp, 1),
                'precipitation_mm': round(precip, 1),
                'region': region
            })
    
    return pd.DataFrame(data)

# Load or generate data
try:
    df = pd.read_csv("weather_kazakhstan_with_region.csv")
    df["date"] = pd.to_datetime(df["date"])
    if "region" not in df.columns:
        regions = ['Астана', 'Алматы', 'Шымкент']
        df['region'] = [random.choice(regions) for _ in range(len(df))]
except FileNotFoundError:
    df = generate_sample_data()

# Region selection
col1, col2 = st.columns([2, 1])
with col1:
    if "region" in df.columns:
        selected_region = st.selectbox("🌍 Выберите регион:", sorted(df["region"].unique()))
        df_filtered = df[df["region"] == selected_region].copy()
    else:
        st.warning("📌 В данных нет информации о регионах. Показываем общий анализ.")
        df_filtered = df.copy()

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4 style="margin: 0; color: var(--primary-green);">📊 Статистика данных</h4>
        <p style="margin: 0.5rem 0 0 0; color: var(--text-dark);">
            Записей: {}<br>
            Период: {} дней
        </p>
    </div>
    """.format(len(df_filtered), (df_filtered['date'].max() - df_filtered['date'].min()).days), 
    unsafe_allow_html=True)

# Date range for analysis
date_min = df_filtered["date"].min().date()
date_max = df_filtered["date"].max().date()

# Tabs with enhanced styling
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Аналитика",
    "🌱 Посадить или подождать",
    "🌡 Угадай температуру",
    "🌍 Мир и климат",
    "🎓 Обучение агрария",
    "🎮 Симуляция фермера"
])

# ===================== 📊 АНАЛИТИКА =====================
with tab1:
    st.markdown("### 📈 Анализ погодных условий")
    
    with st.expander("💡 Как использовать аналитику?", expanded=False):
        st.markdown("""
        🔍 **Выбор периода:** Используйте календарь для анализа конкретного временного промежутка
        
        📊 **Интерактивные графики:** Наведите курсор для детальной информации
        
        🎯 **Рекомендации:** Система автоматически анализирует условия и дает советы
        
        📱 **Мобильная версия:** Все графики адаптированы для мобильных устройств
        """)
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("📅 Начальная дата:", date_min, min_value=date_min, max_value=date_max)
    with col2:
        end_date = st.date_input("📅 Конечная дата:", date_max, min_value=date_min, max_value=date_max)
    
    if start_date <= end_date:
        start_datetime = pd.Timestamp(start_date)
        end_datetime = pd.Timestamp(end_date) + pd.Timedelta(days=1)
        mask = (df_filtered["date"] >= start_datetime) & (df_filtered["date"] < end_datetime)
        analysis_df = df_filtered[mask].copy()
        
        if len(analysis_df) > 0:
            # Modern interactive charts with Plotly
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('🌡️ Температура (°C)', '🌧️ Осадки (мм)'),
                vertical_spacing=0.12
            )
            
            # Temperature chart
            fig.add_trace(
                go.Scatter(
                    x=analysis_df['date'],
                    y=analysis_df['temperature_C'],
                    mode='lines+markers',
                    name='Температура',
                    line=dict(color='#FF6B6B', width=3),
                    marker=dict(size=6),
                    hovertemplate='<b>%{x}</b><br>Температура: %{y:.1f}°C<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Precipitation chart
            fig.add_trace(
                go.Bar(
                    x=analysis_df['date'],
                    y=analysis_df['precipitation_mm'],
                    name='Осадки',
                    marker_color='#4ECDC4',
                    hovertemplate='<b>%{x}</b><br>Осадки: %{y:.1f} мм<extra></extra>'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                height=600,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12),
                margin=dict(l=0, r=0, t=50, b=0)
            )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(46, 139, 87, 0.1)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(46, 139, 87, 0.1)')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics and recommendations
            avg_temp = analysis_df["temperature_C"].mean()
            avg_precip = analysis_df["precipitation_mm"].mean()
            max_temp = analysis_df["temperature_C"].max()
            min_temp = analysis_df["temperature_C"].min()
            total_precip = analysis_df["precipitation_mm"].sum()
            
            # Beautiful metric cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0; color: var(--primary-green);">🌡️ Средняя температура</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{avg_temp:.1f}°C</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0; color: var(--sky-blue);">🌧️ Средние осадки</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{avg_precip:.1f} мм</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0; color: var(--warning-orange);">🔥 Макс. температура</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{max_temp:.1f}°C</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0; color: var(--deep-blue);">❄️ Мин. температура</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{min_temp:.1f}°C</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Smart recommendations with enhanced styling
            st.markdown("### 🎯 Умные рекомендации")
            
            if avg_temp > 30 and avg_precip < 1:
                st.markdown("""
                <div class="metric-card danger">
                    <h4 style="margin: 0; color: var(--danger-red);">🔥 Критическое предупреждение</h4>
                    <p style="margin: 0.5rem 0 0 0;">Очень жарко и сухо — высокая вероятность засухи. Рекомендуется:</p>
                    <ul style="margin: 0.5rem 0 0 1rem;">
                        <li>Использовать засухоустойчивые сорта</li>
                        <li>Установить системы капельного орошения</li>
                        <li>Мульчировать почву для сохранения влаги</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif avg_temp > 25 and avg_precip < 3:
                st.markdown("""
                <div class="metric-card warning">
                    <h4 style="margin: 0; color: var(--warning-orange);">⚠️ Предупреждение</h4>
                    <p style="margin: 0.5rem 0 0 0;">Тёплая и сухая погода — возможен дефицит влаги. Рекомендуется:</p>
                    <ul style="margin: 0.5rem 0 0 1rem;">
                        <li>Увеличить частоту полива</li>
                        <li>Использовать капельное орошение</li>
                        <li>Выбрать раннеспелые сорта</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif avg_temp < 10 and avg_precip > 5:
                st.markdown("""
                <div class="metric-card warning">
                    <h4 style="margin: 0; color: var(--warning-orange);">🌧️ Осторожно</h4>
                    <p style="margin: 0.5rem 0 0 0;">Холодно и влажно — риск загнивания корней. Рекомендуется:</p>
                    <ul style="margin: 0.5rem 0 0 1rem;">
                        <li>Отложить посадку на более тёплый период</li>
                        <li>Улучшить дренаж почвы</li>
                        <li>Использовать фунгициды профилактически</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif 20 <= avg_temp <= 28 and 1 <= avg_precip <= 5:
                st.markdown("""
                <div class="metric-card success">
                    <h4 style="margin: 0; color: var(--success-green);">✅ Отличные условия</h4>
                    <p style="margin: 0.5rem 0 0 0;">Идеальная погода для посева! Рекомендации:</p>
                    <ul style="margin: 0.5rem 0 0 1rem;">
                        <li>Самое время для посадки основных культур</li>
                        <li>Можно планировать интенсивные работы</li>
                        <li>Благоприятно для роста и развития растений</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h4 style="margin: 0; color: var(--primary-green);">📊 Умеренные условия</h4>
                    <p style="margin: 0.5rem 0 0 0;">Погодные условия требуют индивидуального подхода к каждой культуре.</p>
                </div>
                """, unsafe_allow_html=True)
            
        else:
            st.warning("Нет данных для выбранного периода.")
    else:
        st.error("Начальная дата должна быть раньше конечной даты.")

# ===================== 🌱 ИГРА №1 =====================
with tab2:
    st.markdown("### 🌾 Agro Decision Challenge")
    
    with st.expander("🎮 Правила игры", expanded=False):
        st.markdown("""
        🎯 **Цель:** Принимайте правильные решения о посадке на основе погодных условий
        
        🌱 **Культуры:** Каждая культура имеет свои оптимальные условия:
        - **Пшеница:** 15-25°C, осадки 1-4 мм
        - **Кукуруза:** 22-30°C, осадки 2-6 мм  
        - **Рис:** 24-32°C, осадки ≥5 мм
        
        ⭐ **Очки:** Получайте баллы за правильные решения
        """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        crop_type = st.selectbox("🌱 Выберите культуру:", ["Пшеница", "Кукуруза", "Рис"])
    
    with col2:
        if st.button("🎲 Новые условия", key="new_conditions"):
            st.rerun()
    
    # Get random weather conditions
    row = df_filtered.sample(1).iloc[0]
    date = pd.to_datetime(row["date"]).date()
    temp = row["temperature_C"]
    rain = row["precipitation_mm"]
    
    # Weather display with beautiful cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: var(--primary-green);">📅 Дата</h4>
            <h3 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{date}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        temp_color = "var(--danger-red)" if temp > 30 else "var(--warning-orange)" if temp > 25 else "var(--success-green)"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: {temp_color};">🌡️ Температура</h4>
            <h3 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{temp:.1f}°C</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rain_color = "var(--danger-red)" if rain > 8 else "var(--success-green)" if 1 <= rain <= 6 else "var(--warning-orange)"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: {rain_color};">🌧️ Осадки</h4>
            <h3 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{rain:.1f} мм</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🤔 Что вы решите сделать?")
    
    col1, col2 = st.columns(2)
    with col1:
        plant = st.button("🌾 Посадить урожай", key="plant", use_container_width=True)
    with col2:
        wait = st.button("⏳ Подождать лучших условий", key="wait", use_container_width=True)
    
    if plant or wait:
        st.session_state["rounds"] += 1
        
        # Enhanced crop logic with detailed feedback
        outcome = "neutral"
        message = "🤔 Умеренные условия."
        detailed_advice = ""
        
        if crop_type == "Пшеница":
            if 15 <= temp <= 25 and 1 <= rain <= 4:
                outcome = "good"
                message = "✅ Отличные условия для пшеницы!"
                detailed_advice = "Температура и влажность идеальны для прорастания и роста пшеницы."
            elif temp > 30 and rain < 1:
                outcome = "bad"
                message = "🔥 Слишком жарко и сухо для пшеницы."
                detailed_advice = "Высокая температура может повредить зерно, а недостаток влаги приведет к плохому урожаю."
            elif temp < 10 and rain > 5:
                outcome = "bad"
                message = "❄️ Слишком холодно и влажно для пшеницы."
                detailed_advice = "Низкая температура замедлит рост, а избыток влаги может вызвать грибковые заболевания."
        
        elif crop_type == "Кукуруза":
            if 22 <= temp <= 30 and 2 <= rain <= 6:
                outcome = "good"
                message = "🌽 Идеально для кукурузы!"
                detailed_advice = "Теплая погода и умеренные осадки создают отличные условия для роста кукурузы."
            elif temp < 15:
                outcome = "bad"
                message = "🥶 Слишком холодно для кукурузы."
                detailed_advice = "Кукуруза теплолюбивая культура и не переносит низкие температуры."
            elif rain > 8:
                outcome = "bad"
                message = "🌊 Переувлажнение — кукуруза не выживет."
                detailed_advice = "Избыток влаги может привести к загниванию корней и стеблей кукурузы."
        
        elif crop_type == "Рис":
            if 24 <= temp <= 32 and rain >= 5:
                outcome = "good"
                message = "🍚 Прекрасно для риса!"
                detailed_advice = "Высокая температура и обильные осадки — именно то, что нужно для рисовых полей."
            elif rain < 3:
                outcome = "bad"
                message = "💧 Недостаток влаги для риса."
                detailed_advice = "Рис требует много воды для нормального развития."
            elif temp < 18:
                outcome = "bad"
                message = "❄️ Недостаточно тепла для риса."
                detailed_advice = "Рис — тропическая культура, требующая высоких температур."
        
        # Enhanced decision feedback with animations
        if plant:
            if outcome == "good":
                st.success(f"👍 {message}")
                st.info(f"💡 **Детали:** {detailed_advice}")
                st.balloons()
                st.session_state["score"] += 1
                
                # Success image
                st.markdown("""
                <div style="text-align: center; margin: 1rem 0;">
                    <div class="pulse-animation">
                        <img src="https://media.giphy.com/media/26ufcVAp3AiepbFm0/giphy.gif" 
                             style="border-radius: 15px; max-width: 300px;" alt="Success"/>
                    </div>
                    <p style="color: var(--success-green); font-weight: 600; margin-top: 1rem;">
                        🌱 Отличное решение! Урожай будет богатым!
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
            elif outcome == "bad":
                st.error(f"👎 {message}")
                st.info(f"💡 **Детали:** {detailed_advice}")
                st.session_state["fails"] += 1
                
                st.markdown("""
                <div style="text-align: center; margin: 1rem 0;">
                    <img src="https://media.giphy.com/media/3o7TKwmnDgQb5jemjK/giphy.gif" 
                         style="border-radius: 15px; max-width: 300px;" alt="Problem"/>
                    <p style="color: var(--danger-red); font-weight: 600; margin-top: 1rem;">
                        💔 К сожалению, урожай пострадает...
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"😐 {message}")
                st.info(f"💡 **Детали:** {detailed_advice}")
                
                st.markdown("""
                <div style="text-align: center; margin: 1rem 0;">
                    <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" 
                         style="border-radius: 15px; max-width: 300px;" alt="Neutral"/>
                    <p style="color: var(--primary-green); font-weight: 600; margin-top: 1rem;">
                        🤷‍♂️ Средний результат
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        else:  # wait
            if outcome == "bad":
                st.success(f"✅ Мудро подождали — условия действительно плохие для '{crop_type}'.")
                st.info(f"💡 **Детали:** {detailed_advice}")
                st.session_state["score"] += 1
            elif outcome == "good":
                st.warning(f"🙃 Упущена возможность — условия были отличными для '{crop_type}'.")
                st.info(f"💡 **Детали:** {detailed_advice}")
                st.session_state["fails"] += 1
            else:
                st.info(f"🙂 Решение подождать разумно в таких условиях.")
        
        # Enhanced statistics display
        st.markdown("---")
        st.markdown("### 📊 Ваша статистика фермера")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card success">
                <h4 style="margin: 0; color: var(--success-green);">✅ Успехи</h4>
                <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{st.session_state["score"]}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card danger">
                <h4 style="margin: 0; color: var(--danger-red);">❌ Ошибки</h4>
                <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{st.session_state["fails"]}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: var(--primary-green);">🔁 Раунды</h4>
                <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{st.session_state["rounds"]}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if st.session_state["rounds"] > 0:
                success_rate = (st.session_state["score"] / st.session_state["rounds"]) * 100
                rate_color = "var(--success-green)" if success_rate >= 70 else "var(--warning-orange)" if success_rate >= 50 else "var(--danger-red)"
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0; color: {rate_color};">🎯 Точность</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{success_rate:.0f}%</h2>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h4 style="margin: 0; color: var(--primary-green);">🎯 Точность</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">--%</h2>
                </div>
                """, unsafe_allow_html=True)

# ===================== 🌡 ИГРА №2 =====================
with tab3:
    st.markdown("### 🌡️ Угадай температуру")
    
    with st.expander("🎯 Как играть?", expanded=False):
        st.markdown("""
        🎮 **Правила простые:**
        - Смотрите на дату и осадки
        - Угадывайте температуру с помощью слайдера
        - Чем точнее угадаете, тем больше очков получите
        
        🏆 **Система очков:**
        - ±2°C = Отлично! (+1 балл)
        - ±5°C = Хорошо!
        - >5°C = Попробуйте ещё раз
        """)
    
    # Get random data for guessing game
    row = df_filtered.sample(1).iloc[0]
    date = pd.to_datetime(row["date"]).date()
    true_temp = row["temperature_C"]
    rain = row["precipitation_mm"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: var(--primary-green);">📅 Дата</h4>
            <h3 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{date}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: var(--sky-blue);">🌧️ Осадки</h4>
            <h3 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{rain:.1f} мм</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🤔 Какая была температура?")
    
    guess = st.slider(
        "Двигайте слайдер для выбора температуры:",
        min_value=-40,
        max_value=50,
        value=20,
        step=1,
        help="Используйте дату и количество осадков как подсказки"
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        check_button = st.button("🎯 Проверить ответ", key="check_temp", use_container_width=True)
    with col2:
        new_question = st.button("🔄 Новый вопрос", key="new_temp_question", use_container_width=True)
    
    if new_question:
        st.rerun()
    
    if check_button:
        st.session_state["rounds"] += 1
        diff = abs(true_temp - guess)
        
        # Beautiful result display with enhanced feedback
        if diff <= 2:
            st.balloons()
            st.success(f"🎯 Невероятно точно! Температура была {true_temp:.1f}°C")
            st.session_state["score"] += 1
            
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <div class="pulse-animation">
                    <img src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" 
                         style="border-radius: 15px; max-width: 250px;" alt="Excellent"/>
                </div>
                <p style="color: var(--success-green); font-weight: 600; margin-top: 1rem;">
                    🏆 Вы настоящий эксперт по погоде!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        elif diff <= 5:
            st.info(f"🙂 Хорошая попытка! Температура была {true_temp:.1f}°C (разница {diff:.1f}°C)")
            
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <img src="https://media.giphy.com/media/3oriO5t2QB4IPKgxHi/giphy.gif" 
                     style="border-radius: 15px; max-width: 250px;" alt="Good"/>
                <p style="color: var(--primary-green); font-weight: 600; margin-top: 1rem;">
                    👍 Неплохая интуиция!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error(f"😕 Не угадали. Температура была {true_temp:.1f}°C (разница {diff:.1f}°C)")
            st.session_state["fails"] += 1
            
            st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <img src="https://media.giphy.com/media/3o7TKTDn976rzVgky4/giphy.gif" 
                     style="border-radius: 15px; max-width: 250px;" alt="Try again"/>
                <p style="color: var(--warning-orange); font-weight: 600; margin-top: 1rem;">
                    🤷‍♂️ Не расстраивайтесь, попробуйте ещё!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tips for improvement
        month = date.month
        season_tip = ""
        if month in [12, 1, 2]:
            season_tip = "❄️ **Зимний сезон:** В Казахстане зимой обычно от -20°C до -5°C"
        elif month in [3, 4, 5]:
            season_tip = "🌸 **Весенний сезон:** Температура постепенно поднимается от 0°C до 20°C"
        elif month in [6, 7, 8]:
            season_tip = "☀️ **Летний сезон:** Жаркое лето, температуры от 20°C до 40°C"
        else:
            season_tip = "🍂 **Осенний сезон:** Прохладнеет от 20°C до 0°C"
        
        st.info(f"💡 **Подсказка:** {season_tip}")

# ===================== 🌍 МИР И КЛИМАТ =====================
with tab4:
    st.markdown("### 🌍 Глобальные климатические тренды")
    
    # Interactive world map with climate data
    st.markdown("#### 🗺️ Интерактивная карта климата")
    
    # Sample global climate data
    climate_data = [
        {"name": "Казахстан 🇰🇿", "lat": 48.0, "lon": 67.0, "temp": 25, "rain": 3, "region": "Центральная Азия"},
        {"name": "США 🇺🇸", "lat": 39.0, "lon": -98.0, "temp": 30, "rain": 2, "region": "Северная Америка"},
        {"name": "Бразилия 🇧🇷", "lat": -10.0, "lon": -55.0, "temp": 28, "rain": 6, "region": "Южная Америка"},
        {"name": "Индия 🇮🇳", "lat": 20.0, "lon": 78.0, "temp": 32, "rain": 8, "region": "Азия"},
        {"name": "Франция 🇫🇷", "lat": 46.0, "lon": 2.0, "temp": 22, "rain": 4, "region": "Европа"},
        {"name": "Австралия 🇦🇺", "lat": -25.0, "lon": 135.0, "temp": 35, "rain": 1, "region": "Океания"},
        {"name": "ЮАР 🇿🇦", "lat": -30.0, "lon": 25.0, "temp": 26, "rain": 3, "region": "Африка"}
    ]
    
    # Create Folium map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")
    
    for location in climate_data:
        # Color coding for temperature
        if location["temp"] > 30:
            color = "red"
        elif location["temp"] > 20:
            color = "orange"
        else:
            color = "blue"
        
        # Create popup with climate info
        popup_text = f"""
        <div style="font-family: Inter; min-width: 200px;">
            <h4 style="margin: 0; color: #2E8B57;">{location['name']}</h4>
            <p><strong>🌡️ Температура:</strong> {location['temp']}°C</p>
            <p><strong>🌧️ Осадки:</strong> {location['rain']} мм</p>
            <p><strong>🗺️ Регион:</strong> {location['region']}</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[location["lat"], location["lon"]],
            radius=max(10, location["temp"] / 2),
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=location["name"],
            color=color,
            fill=True,
            weight=2,
            fillOpacity=0.7
        ).add_to(m)
    
    # Display map
    map_data = st_folium(m, width=700, height=400)
    
    # Climate comparison charts
    st.markdown("#### 📊 Сравнение климатических показателей")
    
    # Create DataFrame for comparison
    climate_df = pd.DataFrame(climate_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature comparison
        fig_temp = px.bar(
            climate_df,
            x="name",
            y="temp",
            title="🌡️ Средняя температура по странам",
            color="temp",
            color_continuous_scale="RdYlBu_r",
            height=400
        )
        fig_temp.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=11),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Precipitation comparison
        fig_precip = px.bar(
            climate_df,
            x="name",
            y="rain",
            title="🌧️ Среднее количество осадков",
            color="rain",
            color_continuous_scale="Blues",
            height=400
        )
        fig_precip.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=11),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_precip, use_container_width=True)
    
    # Scatter plot for climate patterns
    st.markdown("#### 🔍 Анализ климатических паттернов")
    
    fig_scatter = px.scatter(
        climate_df,
        x="temp",
        y="rain",
        size="temp",
        color="region",
        hover_name="name",
        title="Связь между температурой и осадками",
        labels={"temp": "Температура (°C)", "rain": "Осадки (мм)"},
        height=500
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ===================== 🎓 ОБУЧЕНИЕ АГРАРИЯ =====================
with tab5:
    st.markdown("### 🎓 Агрономическое образование")
    
    # Educational sections with enhanced styling
    education_sections = [
        {
            "title": "🌱 Основы растениеводства",
            "icon": "🌾",
            "content": """
            **Ключевые принципы:**
            - **Температурный режим:** Каждая культура имеет оптимальный диапазон температур
            - **Водный баланс:** Важность правильного соотношения полива и дренажа
            - **Питательные вещества:** NPK (азот, фосфор, калий) - основа питания растений
            - **Севооборот:** Чередование культур для сохранения плодородия почвы
            
            **Практические советы:**
            - Изучайте прогнозы погоды минимум на 7 дней вперед
            - Ведите дневник наблюдений за растениями
            - Используйте мульчирование для сохранения влаги
            """
        },
        {
            "title": "🌡️ Климатические зоны Казахстана",
            "icon": "🗺️",
            "content": """
            **Северный Казахстан:**
            - Континентальный климат
            - Оптимально для: пшеница, ячмень, овёс
            - Особенности: короткое лето, суровая зима
            
            **Южный Казахстан:**
            - Аридный и семиаридный климат
            - Оптимально для: хлопок, рис, бахчевые
            - Особенности: жаркое лето, мягкая зима
            
            **Восточный Казахстан:**
            - Умеренно континентальный
            - Оптимально для: картофель, овощи, кормовые
            - Особенности: достаточное увлажнение
            """
        },
        {
            "title": "📊 Анализ погодных данных",
            "icon": "📈",
            "content": """
            **Ключевые показатели:**
            - **ГТК (Гидротермический коэффициент):** Отношение осадков к температуре
            - **Сумма активных температур:** Накопленное тепло за вегетационный период
            - **Индекс засушливости:** Показатель дефицита влаги
            
            **Практическое применение:**
            - ГТК > 1.3 - избыточное увлажнение
            - ГТК 1.0-1.3 - достаточное увлажнение  
            - ГТК < 1.0 - недостаточное увлажнение
            
            **Современные технологии:**
            - Спутниковые данные MODIS
            - Метеостанции IoT
            - Прогнозные модели машинного обучения
            """
        }
    ]
    
    for i, section in enumerate(education_sections):
        with st.expander(f"{section['icon']} {section['title']}", expanded=i==0):
            st.markdown(f"""
            <div class="metric-card">
                {section['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Interactive quiz section
    st.markdown("### 🧠 Проверьте свои знания")
    
    quiz_questions = [
        {
            "question": "Какая температура оптимальна для пшеницы?",
            "options": ["10-15°C", "15-25°C", "25-35°C", "35-45°C"],
            "correct": 1,
            "explanation": "Пшеница лучше всего растет при температуре 15-25°C. При более высоких температурах зерно может повреждаться, а при более низких - рост замедляется."
        },
        {
            "question": "Что означает ГТК больше 1.3?",
            "options": ["Засуха", "Нормальное увлажнение", "Избыточное увлажнение", "Заморозки"],
            "correct": 2,
            "explanation": "ГТК (Гидротермический коэффициент) больше 1.3 указывает на избыточное увлажнение, что может привести к переувлажнению почвы."
        },
        {
            "question": "Какая культура наиболее требовательна к влаге?",
            "options": ["Пшеница", "Кукуруза", "Рис", "Ячмень"],
            "correct": 2,
            "explanation": "Рис - самая влаголюбивая культура, требующая постоянного увлажнения или даже затопления полей."
        }
    ]
    
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = []
    
    for i, question in enumerate(quiz_questions):
        if i not in st.session_state.quiz_completed:
            st.markdown(f"**Вопрос {i+1}:** {question['question']}")
            
            answer = st.radio(
                "Выберите правильный ответ:",
                question['options'],
                key=f"quiz_{i}"
            )
            
            if st.button(f"Ответить на вопрос {i+1}", key=f"answer_{i}"):
                selected_index = question['options'].index(answer)
                if selected_index == question['correct']:
                    st.success("✅ Правильно!")
                    st.session_state.quiz_score += 1
                else:
                    st.error("❌ Неправильно!")
                
                st.info(f"💡 **Объяснение:** {question['explanation']}")
                st.session_state.quiz_completed.append(i)
                st.rerun()
            
            st.markdown("---")
            break
    
    if len(st.session_state.quiz_completed) == len(quiz_questions):
        score_percentage = (st.session_state.quiz_score / len(quiz_questions)) * 100
        
        if score_percentage >= 80:
            st.balloons()
            st.success(f"🏆 Отлично! Ваш результат: {st.session_state.quiz_score}/{len(quiz_questions)} ({score_percentage:.0f}%)")
        elif score_percentage >= 60:
            st.info(f"👍 Хорошо! Ваш результат: {st.session_state.quiz_score}/{len(quiz_questions)} ({score_percentage:.0f}%)")
        else:
            st.warning(f"📚 Нужно ещё изучить материал. Результат: {st.session_state.quiz_score}/{len(quiz_questions)} ({score_percentage:.0f}%)")
        
        if st.button("🔄 Пройти тест заново"):
            st.session_state.quiz_score = 0
            st.session_state.quiz_completed = []
            st.rerun()

# ===================== 🎮 СИМУЛЯЦИЯ ФЕРМЕРА =====================
with tab6:
    st.markdown("### 🎮 Симулятор фермерского хозяйства")
    
    # Initialize farm simulation state
    if "farm_money" not in st.session_state:
        st.session_state.farm_money = 1000
    if "farm_crops" not in st.session_state:
        st.session_state.farm_crops = {"Пшеница": 0, "Кукуруза": 0, "Рис": 0}
    if "farm_season" not in st.session_state:
        st.session_state.farm_season = 1
    if "farm_weather" not in st.session_state:
        # Generate random weather for this season
        st.session_state.farm_weather = {
            "temp": round(random.uniform(15, 35), 1),
            "rain": round(random.uniform(0, 10), 1),
            "description": random.choice(["Солнечно", "Облачно", "Дождливо", "Ветрено"])
        }
    
    # Farm dashboard
    st.markdown("#### 🏡 Ваше фермерское хозяйство")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card success">
            <h4 style="margin: 0; color: var(--success-green);">💰 Бюджет</h4>
            <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{st.session_state.farm_money}₸</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: var(--primary-green);">🌾 Сезон</h4>
            <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{st.session_state.farm_season}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        weather = st.session_state.farm_weather
        temp_color = "var(--danger-red)" if weather["temp"] > 30 else "var(--success-green)"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: {temp_color};">🌡️ Погода</h4>
            <h3 style="margin: 0.5rem 0 0 0; color: var(--text-dark); font-size: 1.2rem;">{weather['temp']}°C</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_crops = sum(st.session_state.farm_crops.values())
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: var(--earth-brown);">🌱 Посевы</h4>
            <h2 style="margin: 0.5rem 0 0 0; color: var(--text-dark);">{total_crops} га</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Current weather display
    st.markdown("#### 🌤️ Текущая погода")
    weather = st.session_state.farm_weather
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Температура", f"{weather['temp']}°C")
    with col2:
        st.metric("🌧️ Осадки", f"{weather['rain']} мм")
    with col3:
        st.metric("☁️ Условия", weather['description'])
    
    # Farming actions
    st.markdown("#### 🚜 Действия фермера")
    
    # Crop prices and costs
    crop_data = {
        "Пшеница": {"cost": 50, "profit": 80, "optimal_temp": (15, 25), "optimal_rain": (1, 4)},
        "Кукуруза": {"cost": 70, "profit": 120, "optimal_temp": (22, 30), "optimal_rain": (2, 6)},
        "Рис": {"cost": 100, "profit": 160, "optimal_temp": (24, 32), "optimal_rain": (5, 10)}
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌱 Посадить культуры:**")
        crop_to_plant = st.selectbox("Выберите культуру:", list(crop_data.keys()))
        area_to_plant = st.number_input("Площадь (га):", min_value=1, max_value=20, value=5)
        
        total_cost = crop_data[crop_to_plant]["cost"] * area_to_plant
        
        if st.button(f"Посадить {crop_to_plant} ({total_cost}₸)", key="plant_crop"):
            if st.session_state.farm_money >= total_cost:
                st.session_state.farm_money -= total_cost
                st.session_state.farm_crops[crop_to_plant] += area_to_plant
                st.success(f"✅ Посажено {area_to_plant} га {crop_to_plant}")
                st.rerun()
            else:
                st.error("❌ Недостаточно средств!")
    
    with col2:
        st.markdown("**📈 Собрать урожай:**")
        if any(crop_area > 0 for crop_area in st.session_state.farm_crops.values()):
            for crop_name, crop_area in st.session_state.farm_crops.items():
                if crop_area > 0:
                    if st.button(f"Собрать {crop_name} ({crop_area} га)", key=f"harvest_{crop_name}"):
                        # Calculate harvest success based on weather
                        crop_info = crop_data[crop_name]
                        weather = st.session_state.farm_weather
                        
                        temp_ok = crop_info["optimal_temp"][0] <= weather["temp"] <= crop_info["optimal_temp"][1]
                        rain_ok = crop_info["optimal_rain"][0] <= weather["rain"] <= crop_info["optimal_rain"][1]
                        
                        success_rate = 1.0
                        if not temp_ok:
                            success_rate *= 0.7
                        if not rain_ok:
                            success_rate *= 0.8
                        
                        harvest_profit = int(crop_info["profit"] * crop_area * success_rate)
                        st.session_state.farm_money += harvest_profit
                        st.session_state.farm_crops[crop_name] = 0
                        
                        if success_rate >= 0.9:
                            st.balloons()
                            st.success(f"🏆 Отличный урожай! Получено {harvest_profit}₸")
                        elif success_rate >= 0.7:
                            st.info(f"✅ Хороший урожай! Получено {harvest_profit}₸")
                        else:
                            st.warning(f"⚠️ Урожай пострадал от погоды. Получено {harvest_profit}₸")
                        
                        st.rerun()
        else:
            st.info("Нет посевов для сбора урожая")
    
    # Next season button
    if st.button("⏭️ Перейти к следующему сезону", key="next_season"):
        st.session_state.farm_season += 1
        # Generate new weather
        st.session_state.farm_weather = {
            "temp": round(random.uniform(10, 40), 1),
            "rain": round(random.uniform(0, 12), 1),
            "description": random.choice(["Солнечно", "Облачно", "Дождливо", "Ветрено", "Туманно"])
        }
        st.success(f"🌅 Наступил {st.session_state.farm_season}-й сезон!")
        st.rerun()
    
    # Farm statistics
    st.markdown("#### 📊 Статистика фермы")
    
    if st.session_state.farm_season > 1:
        if st.session_state.farm_money > 1000:
            profit = st.session_state.farm_money - 1000
            st.success(f"💰 Прибыль: +{profit}₸ за {st.session_state.farm_season-1} сезонов")
        elif st.session_state.farm_money < 1000:
            loss = 1000 - st.session_state.farm_money
            st.error(f"💸 Убыток: -{loss}₸ за {st.session_state.farm_season-1} сезонов")
        else:
            st.info("💼 Вы работаете в ноль")
    
    # Tips for farming success
    with st.expander("💡 Советы для успешного фермерства", expanded=False):
        st.markdown("""
        🎯 **Стратегии успеха:**
        
        **🌾 Культуры и климат:**
        - Пшеница: лучше всего при 15-25°C и умеренных осадках
        - Кукуруза: требует тепла (22-30°C) и достаточной влаги
        - Рис: самая прибыльная, но нужно много воды и тепла
        
        **💰 Экономика:**
        - Рис дает наибольшую прибыль, но имеет высокие затраты
        - Пшеница - самый безопасный выбор для начинающих
        - Следите за погодой перед посадкой и сбором урожая
        
        **⚡ Тактические советы:**
        - Не вкладывайте все деньги в одну культуру
        - Собирайте урожай при благоприятной погоде
        - Изучайте прогноз погоды перед принятием решений
        """)

# Beautiful footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <div class="footer-section">
            <h4 class="footer-title">🌾 Агро-Погода Казахстана</h4>
            <p>Современное решение для анализа погодных данных и принятия агрономических решений на основе данных NASA.</p>
        </div>
        <div class="footer-section">
            <h4 class="footer-title">🔬 Технологии</h4>
            <p>• Python & Streamlit<br>• Plotly для визуализации<br>• NASA Weather API<br>• Машинное обучение</p>
        </div>
        <div class="footer-section">
            <h4 class="footer-title">📊 Возможности</h4>
            <p>• Анализ климата<br>• Игровое обучение<br>• Рекомендации AI<br>• Глобальная статистика</p>
        </div>
    </div>
    <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
        <p style="margin: 0;">© 2024 Агро-Погода Казахстана | Сделано с ❤️ для фермеров</p>
    </div>
</div>
""", unsafe_allow_html=True)
