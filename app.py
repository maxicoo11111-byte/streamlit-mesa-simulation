# app.py (финальная версия)

import streamlit as st
from model import EconomicModel # Импортируем нашу модель из model.py

# --- Настройка страницы ---
st.set_page_config(page_title="Экономическая Симуляция", layout="wide")
st.title("📊 Экономическая симуляция (Mesa 3.0+)")

# --- Боковая панель с настройками ---
with st.sidebar:
    st.header("⚙️ Параметры симуляции")

    # Виджеты для задания начальных параметров
    n_agents = st.slider("Количество агентов (N)", 1, 200, 50)
    initial_gdp = st.number_input("Начальный ВВП (GDP)", value=1000)
    tax_rate_initial = st.slider("Начальная налоговая ставка", 0.0, 1.0, 0.1, 0.01)

    # Кнопка для создания/перезапуска симуляции
    if st.button("🚀 Начать / Перезапустить симуляцию"):
        # Создаем новый экземпляр модели и сохраняем его в сессии
        st.session_state['model'] = EconomicModel(N=n_agents, gdp=initial_gdp, tax_rate=tax_rate_initial)
        st.success("Модель успешно создана!")
        st.rerun() # Перезапускаем скрипт, чтобы обновить интерфейс

# --- Основной интерфейс ---
# Проверяем, была ли модель создана и сохранена в сессии
if 'model' in st.session_state:
    model = st.session_state.model
    
    with st.sidebar:
        st.subheader("Управление моделью")
        # Слайдер для изменения налоговой ставки "на лету"
        current_tax_rate = st.slider(
            "Текущая налоговая ставка", 0.0, 1.0, model.tax_rate, 0.01
        )
        model.tax_rate = current_tax_rate # Обновляем параметр в модели

        # Кнопка для выполнения следующего шага
        if st.button("➡️ Следующий ход"):
            model.step()
            st.rerun() # Перезапускаем, чтобы сразу увидеть обновленные данные

    st.header("Результаты симуляции")
    st.write(f"Текущий шаг: **{len(model.datacollector.model_vars['TotalWealth'])}**")

    # Извлекаем и отображаем данные
    model_data = model.datacollector.get_model_vars_dataframe()

    if not model_data.empty:
        st.subheader("Динамика показателей")
        st.line_chart(model_data)

        with st.expander("Показать сырые данные"):
            st.dataframe(model_data)
else:
    st.info("Задайте параметры в боковой панели и нажмите 'Начать / Перезапустить симуляцию'.")
