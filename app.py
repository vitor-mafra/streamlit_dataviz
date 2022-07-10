import streamlit as st

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("TP DataViz")

# Leitura dos Dados
ft_Competicao = pd.read_csv("https://raw.githubusercontent.com/GuiMendeees/Dados/main/TP%20Data%20Viz/athlete_events.csv")
dim_paises = pd.read_csv('https://raw.githubusercontent.com/GuiMendeees/Dados/main/TP%20Data%20Viz/noc_regions.csv')

dim_indicadores = pd.read_csv("https://raw.githubusercontent.com/GuiMendeees/Dados/main/TP%20Data%20Viz/WordSocio.csv")
dim_indicadores.drop(dim_indicadores.tail(5).index,inplace=True)
dim_indicadores['Time'] = pd.to_numeric(dim_indicadores['Time'])

# Tratamento da Base
coletivos = ['Basketball','Football','Tug-Of-War','Ice Hockey','Sailing','Handball','Water Polo','Hockey','Bobsleigh','Softball','Synchronized Swimming','Volleyball'
              ,'Baseball','Synchronized Swimming','Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Curling','Rugby','Lacrosse','Polo','Cricket'
             ,'Motorboating', 'Basque Pelota']

ft_Competicao['Esporte Coletivo'] = np.where(ft_Competicao['Sport'].isin(coletivos), 1, 0)
ft_Competicao['Medal'] = ft_Competicao['Medal'].fillna('-')

# Atletas que marcaram eras (Verão)- Guilherme
dfOlVerao = ft_Competicao.loc[ft_Competicao['Season'] == 'Summer']
dfEra = (
          dfOlVerao.loc[(dfOlVerao['Year'] >= 1922) & (dfOlVerao['Medal'] != '-')][['Name','Medal','Sport','NOC']]
              .groupby(['Name','Sport','NOC'])['Name']
              .count()
              .reset_index(name='QtdMedalhas') 
              .nlargest(columns = 'QtdMedalhas',n=15)


)

df = dfOlVerao.loc[(dfOlVerao['Year'] >= 1922 ) & (dfOlVerao['Medal'] != '-')][['Name','Year','Medal','Sport']]
df = df.loc[df.Name.isin(dfEra['Name'])]

dfMedalha = (
    df
              .groupby(['Name','Sport'])['Name']
              .count()
              .reset_index(name='QtdMedalhas')
              .sort_values(by=['QtdMedalhas'], ascending = False)

)
dfMedalha = dfMedalha.sort_values(by=['QtdMedalhas'], ascending = False)

dfComp = dfOlVerao.drop_duplicates(['Name','Year'])[['Name','Year']]
dfComp = dfComp.loc[dfComp.Name.isin(dfEra['Name'])]

dfComp = ( dfComp
          .groupby(['Name'])['Name']
        .count()
        .reset_index(name='Participacoes')
)

dfComp = dfComp.sort_values(by=['Participacoes'], ascending = False)

dfRes = dfMedalha.merge(dfComp, how = 'inner', left_on = 'Name', right_on = 'Name')

sns.set_theme(style="darkgrid")


f, ax = plt.subplots(figsize=(10, 16))


sns.set_color_codes("pastel")
sns.barplot(x="QtdMedalhas", y="Name", data=dfRes, color="g",saturation = 1,label = "QtdMedalhas")


sns.set_color_codes("muted")
sns.barplot(x="Participacoes", y="Name", data=dfRes, color="b", saturation = 0.8, label = "Participacoes")


ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 35), ylabel="",
       xlabel=None)
sns.despine(left=True, bottom=True)

st.pyplot(plt.gcf())
