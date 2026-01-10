import streamlit as st
import pandas as pd
from model import EconomicModel # Импортируем нашу модель из model.py

st.set_page_config(layout="wide", page_title="Агентная экономическая симуляция")

st.title("Интерактивная агентно-ориентированная экономическая симуляция")

# --- Блок настройки параметров в сайдбаре ---
st.sidebar.header("Параметры симуляции")

# Инициализация модели при первом запуске
if 'model' not in st.session_state:
    st.session_state['model_params'] = {
        'N_households': st.sidebar.slider("Количество домохозяйств", 1, 50, 10),
        'N_firms': st.sidebar.slider("Количество фирм", 1, 10, 3),
        'tax_rate': st.sidebar.slider("Налоговая ставка", 0.0, 1.0, 0.2, 0.01),
        'firm_salary': st.sidebar.slider("Зарплата от фирм", 10, 100, 50),
        'gov_spending_ratio': st.sidebar.slider("Доля расходов бюджета", 0.0, 1.0, 0.1, 0.01)
    }
    # Создаем экземпляр модели и сохраняем его в session_state
    st.session_state['model'] = EconomicModel(**st.session_state['model_params'])
else:
    # Если модель уже существует, просто отображаем слайдеры с текущими значениями
    # и обновляем параметры модели, если пользователь их изменил
    current_params = st.session_state['model_params']
    new_params = {
        'N_households': st.sidebar.slider("Количество домохозяйств", 1, 50, current_params['N_households']),
        'N_firms': st.sidebar.slider("Количество фирм", 1, 10, current_params['N_firms']),
        'tax_rate': st.sidebar.slider("Налоговая ставка", 0.0, 1.0, current_params['tax_rate'], 0.01),
        'firm_salary': st.sidebar.slider("Зарплата от фирм", 10, 100, current_params['firm_salary']),
        'gov_spending_ratio': st.sidebar.slider("Доля расходов бюджета", 0.0, 1.0, current_params['gov_spending_ratio'], 0.01)
    }
    
    # Применяем измененные параметры к модели
    st.session_state['model'].tax_rate = new_params['tax_rate']
    st.session_state['model'].firm_salary = new_params['firm_salary']
    st.session_state['model'].gov_spending_ratio = new_params['gov_spending_ratio']
    st.session_state['model_params'] = new_params


# --- Основной блок управления и визуализации ---

# Кнопка для выполнения одного шага симуляции
if st.sidebar.button("Следующий ход"):
    # Извлекаем модель, делаем шаг, сохраняем обратно
    model = st.session_state['model']
    model.step()
    st.session_state['model'] = model

# Кнопка для сброса симуляции
if st.sidebar.button("Сбросить симуляцию"):
    # Удаляем старую модель из session_state, Streamlit автоматически пересоздаст ее
    del st.session_state['model']
    st.rerun()

# --- Отображение данных ---

st.header("Результаты симуляции")

# Извлекаем данные из DataCollector
model = st.session_state['model']
data = model.datacollector.get_model_vars_dataframe()

if not data.empty:
    st.write(f"Текущий шаг: {model.schedule.steps}")
    
    # Отображаем интерактивный график
    st.line_chart(data)

    # Отображаем последние значения
    st.subheader("Текущие показатели:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Общие сбережения домохозяйств", f"{data['Total Savings'].iloc[-1]:,.0f}")
    with col2:
        st.metric("Общий капитал фирм", f"{data['Total Firm Capital'].iloc[-1]:,.0f}")
    with col3:
        st.metric("Бюджет правительства", f"{data['Government Budget'].iloc[-1]:,.0f}")

    # Показываем сырые данные в таблице
    st.subheader("История данных")
    st.dataframe(data)
else:
    st.info("Симуляция еще не началась. Нажмите 'Следующий ход', чтобы запустить.")
