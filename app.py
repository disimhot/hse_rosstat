import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

OUT_URL = 'out.csv'


@st.cache_data
def load_data(url):
    return pd.read_csv(url)


df = load_data(OUT_URL)

st.title("Анализ зарплат 2017-2023 гг")
st.sidebar.title("О проекте")
st.sidebar.info(
    """
    Исследовательский проект по курсам HSE.
    В нем проанализированы данные из официальных источников:
    Росстат и Уровень инфляции
    """
)

with st.sidebar:
    options = st.multiselect("Выберите вид экономической деятельности", ["Образование", "Производство одежды",
                                                                         'Производство одежды_с инфляцией',
                                                                         'Образование_с инфляцией'],
                             default=["Образование", "Производство одежды"])
    selected = st.radio("Прирост по виду экономической деятельности", ["Образование", "Производство одежды",
                                                                       'Производство одежды_с инфляцией',
                                                                       'Образование_с инфляцией'])

# pressed = st.button("Train")
df.head()

st.subheader('График зарплат по видам экономической деятельности')
if len(options) > 0:
    fig = plt.figure(figsize=(8, 5))
    sns.set_palette(['cyan', 'red'])
    s = pd.melt(df[options + ['Год']], ['Год'])
    s.rename(columns={'value': 'Виды деятельности'}, inplace=True)
    ax = sns.lineplot(x='Год', y='Виды деятельности', hue='variable', data=s)
    plt.legend(title='Виды деятельности', loc='upper left', labels=options)
    ax.set_ylabel('Заработная плата')
    st.pyplot(fig)

st.subheader('Посмотрим на график инфляции в %')
fig1 = plt.figure(figsize=(8, 5))
ax = sns.lineplot(x='Год', y='Инфляция', data=df)
st.pyplot(fig1)

st.subheader('Посмотрим на прирост средней заработной платы по сравнению с предыдущим годом')

if selected == 'Образование':
    temp = df[1:]
    years = temp['Год']

    x = np.arange(len(years))
    bar_width = 0.35
    fig2, ax = plt.subplots()
    bar1 = ax.bar(x - bar_width / 2, temp['Прирост зп в образовании'], bar_width, label='Прирост зп в образовании')
    bar2 = ax.bar(x + bar_width / 2, temp['Инфляция'], bar_width, label='Инфляция')

    ax.set_xlabel('Год')
    ax.set_ylabel('Зп в %')
    ax.set_title('Прирост зп в образовании в сравнении с инфляцией')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend()
    st.pyplot(fig2)
elif selected == 'Производство одежды':
    temp = df[1:]
    years = temp['Год']

    x = np.arange(len(years))
    bar_width = 0.35
    fig2, ax = plt.subplots()
    bar1 = ax.bar(x - bar_width / 2, temp['Прирост зп в производстве одежды'], bar_width,
                  label='Прирост зп в производстве одежды')
    bar2 = ax.bar(x + bar_width / 2, temp['Инфляция'], bar_width, label='Инфляция')

    ax.set_xlabel('Год')
    ax.set_ylabel('Зп в %')
    ax.set_title('Прирост зп в производстве одежды в сравнении с инфляцией')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend()
    st.pyplot(fig2)

st.text("""
        Реальный рост зарплат ниже. С 2020 года инфляция начинает сильнее влиять на заработные платы.
        Рост замедляется, и в 2022 году по обоим видам заметен большой разрыв между реальным уровнем зп и номинальным.
        После 2022 года происходит резкий рост, где разрыв начинает уменьшаться
        Заметим, что в производстве одежды инфляция "съела" реальный рост зп в 2018 и 2020гг,
        когда как в образовании рост зп превышает инфляцию.
        """)
