import streamlit as st

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import time
import json
from urllib.request import urlopen
import bar_chart_race as bcr

st.set_page_config(
    page_title="TP - Visualização de Dados",
    page_icon="🥇",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

loading_bar = st.progress(0)
ploting_state = st.text("Fazendo chamadas ao servidor...")
warning = st.warning("Por favor, espere os dados carregarem corretamente")

st.title("Histórias das Olimpíadas")
st.subheader("Uma análise quantitativa dos Jogos Olímpicos de Verão e Inverno")

st.text("")
st.text(
"""
Daniel Silva - 2018046670
Eduardo Fiuza - 2018046580
Guilherme Mendes - 2018046939
Rúbia Wardil - 2016077209
Vitor Mafra - 2018046831
"""
)

st.write(
    "Este trabalho visa analisar dados dos atletas de todos os Jogos Olímpicos de Inverno e Verão em busca de compreender e comunicar melhor tantos anos de história, geopolítica e esporte em alto nível. Para isso, vamos visualizar temporal e geograficamente as distribuições de medalhas ao longo das Olimpíadas, buscar atletas de destaque, investigar o perfil de atletas experientes, analisar a correlação entre o PIB dos países com a quantidade de medalhas conquistadas e tentar entender quais são os grandes países nos quadros de medalhas dos Jogos Olímpicos."
)
st.write(
    "A ideia é tentar compreender e comunicar, portanto, o grande contexto por trás de um evento que frequentemente entretém, diverte e inspira todo o mundo. A relevância do trabalho se mostra justamente nesse interesse pontual de pessoas de diferentes perfis e culturas ao longo dos mais diversos países sobre um único evento."
)

loading_bar.progress(5)

# Leitura dos Dados
ft_Competicao = pd.read_csv(
    "https://raw.githubusercontent.com/GuiMendeees/Dados/main/TP%20Data%20Viz/athlete_events.csv"
)
ploting_state.text("Carregando a aplicação...")
loading_bar.progress(7)
ploting_state.text("Baixando os dados...")
dim_paises = pd.read_csv(
    "https://raw.githubusercontent.com/GuiMendeees/Dados/main/TP%20Data%20Viz/noc_regions.csv"
)

loading_bar.progress(10)

dim_indicadores = pd.read_csv(
    "https://raw.githubusercontent.com/GuiMendeees/Dados/main/TP%20Data%20Viz/WordSocio.csv"
)
dim_indicadores.drop(dim_indicadores.tail(5).index, inplace=True)
dim_indicadores["Time"] = pd.to_numeric(dim_indicadores["Time"])

loading_bar.progress(20)

# Tratamento da Base
coletivos = [
    "Basketball",
    "Football",
    "Tug-Of-War",
    "Ice Hockey",
    "Sailing",
    "Handball",
    "Water Polo",
    "Hockey",
    "Bobsleigh",
    "Softball",
    "Synchronized Swimming",
    "Volleyball",
    "Baseball",
    "Synchronized Swimming",
    "Rhythmic Gymnastics",
    "Rugby Sevens",
    "Beach Volleyball",
    "Curling",
    "Rugby",
    "Lacrosse",
    "Polo",
    "Cricket",
    "Motorboating",
    "Basque Pelota",
]

ft_Competicao["Esporte Coletivo"] = np.where(
    ft_Competicao["Sport"].isin(coletivos), 1, 0
)
ft_Competicao["Medal"] = ft_Competicao["Medal"].fillna("-")

loading_bar.progress(28)

ploting_state.text("Carregando os dados geográficos...")
with urlopen(
    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
) as response:
    Countries = json.load(response)  # Javascrip object notation
loading_bar.progress(30)

st.header("Uma visão temporal das Olimpíadas")
st.subheader("Jogos Olímpicos de Verão")

# Quantidade de Medalhas por País

dfOlVerao = ft_Competicao.loc[ft_Competicao["Season"] == "Summer"]

OuroPaisVeraoAno = (
    dfOlVerao.loc[dfOlVerao["Medal"] == "Gold"][["NOC", "Year", "Medal"]]
    .groupby(["NOC", "Year", "Medal"])["Medal"]
    .count()
    .reset_index(name="QtdOuro")
    .sort_values(["QtdOuro"], ascending=False)
)

PrataPaisVeraoAno = (
    dfOlVerao.loc[dfOlVerao["Medal"] == "Silver"][["NOC", "Year", "Medal"]]
    .groupby(["NOC", "Year", "Medal"])["Medal"]
    .count()
    .reset_index(name="QtdPrata")
    .sort_values(["QtdPrata"], ascending=False)
)

BronzePaisVeraoAno = (
    dfOlVerao.loc[dfOlVerao["Medal"] == "Bronze"][["NOC", "Year", "Medal"]]
    .groupby(["NOC", "Year", "Medal"])["Medal"]
    .count()
    .reset_index(name="QtdBronze")
    .sort_values(["QtdBronze"], ascending=False)
)

TotalPaisAnoVerao = OuroPaisVeraoAno.merge(
    PrataPaisVeraoAno, how="inner", on=["NOC", "Year"]
)
TotalPaisAnoVerao = TotalPaisAnoVerao.merge(
    BronzePaisVeraoAno, how="inner", on=["NOC", "Year"]
)
TotalPaisAnoVerao["Total"] = (
    TotalPaisAnoVerao["QtdOuro"]
    + TotalPaisAnoVerao["QtdPrata"]
    + TotalPaisAnoVerao["QtdBronze"]
)

df = TotalPaisAnoVerao
df = df.sort_values(by=["Year"])

ploting_state.text("Plotando os mapas...")
fig1 = px.choropleth_mapbox(
    df,
    locations="NOC",
    geojson=Countries,  # shape information
    color="Total",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name="NOC",
    hover_data=["Total"],
    center={"lat": 0, "lon": 0},
    zoom=-0.3,
    opacity=0.8,
    animation_frame="Year",  # creating the application based on the year
    title="Quantidade de medalhas por país ao longo da história das Olimpíadas de Verão",
)

fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig1.update_geos(fitbounds="locations", visible=False)
st.write("Quantidade de medalhas por país ao longo da história das Olimpíadas de Verão")
st.plotly_chart(fig1)

loading_bar.progress(35)

st.subheader("Jogos Olímpicos de Inverno")
loading_bar.progress(40)

# Quantidade de Medalhas por País

dfOlVerao = ft_Competicao.loc[ft_Competicao["Season"] == "Winter"]


OuroPaisVeraoAno = (
    dfOlVerao.loc[dfOlVerao["Medal"] == "Gold"][["NOC", "Year", "Medal"]]
    .groupby(["NOC", "Year", "Medal"])["Medal"]
    .count()
    .reset_index(name="QtdOuro")
    .sort_values(["QtdOuro"], ascending=False)
)

PrataPaisVeraoAno = (
    dfOlVerao.loc[dfOlVerao["Medal"] == "Silver"][["NOC", "Year", "Medal"]]
    .groupby(["NOC", "Year", "Medal"])["Medal"]
    .count()
    .reset_index(name="QtdPrata")
    .sort_values(["QtdPrata"], ascending=False)
)

BronzePaisVeraoAno = (
    dfOlVerao.loc[dfOlVerao["Medal"] == "Bronze"][["NOC", "Year", "Medal"]]
    .groupby(["NOC", "Year", "Medal"])["Medal"]
    .count()
    .reset_index(name="QtdBronze")
    .sort_values(["QtdBronze"], ascending=False)
)

TotalPaisAnoVerao = OuroPaisVeraoAno.merge(
    PrataPaisVeraoAno, how="inner", on=["NOC", "Year"]
)
TotalPaisAnoVerao = TotalPaisAnoVerao.merge(
    BronzePaisVeraoAno, how="inner", on=["NOC", "Year"]
)
TotalPaisAnoVerao["Total"] = (
    TotalPaisAnoVerao["QtdOuro"]
    + TotalPaisAnoVerao["QtdPrata"]
    + TotalPaisAnoVerao["QtdBronze"]
)

df = TotalPaisAnoVerao
df = df.sort_values(by=["Year"])

fig2 = px.choropleth_mapbox(
    df,
    locations="NOC",
    geojson=Countries,  # shape information
    color="Total",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name="NOC",
    hover_data=["Total"],
    center={"lat": 0, "lon": 0},
    zoom=-0.3,
    opacity=0.8,
    animation_frame="Year",  # creating the application based on the year
    title="Quantidade de medalhas por país ao longo da história das Olimpíadas de Inverno",
)

fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig2.update_geos(fitbounds="locations", visible=False)
st.write(
    "Quantidade de medalhas por país ao longo da história das Olimpíadas de Inverno"
)
st.plotly_chart(fig2)


st.header("Perfil dos atletas medalhistas")
st.image(
    "/home/vitor-mafra/Desktop/ufmg/2022_01/dataviz/streamlit_dataviz/Visualização de Dados - Apresentação Final.png"
)


# Quais os atletas que marcaram eras (Guilherme) - Verão
dfOlVerao = ft_Competicao.loc[ft_Competicao["Season"] == "Summer"]
dfEra = (
    dfOlVerao.loc[(dfOlVerao["Year"] >= 1922) & (dfOlVerao["Medal"] != "-")][
        ["Name", "Medal", "Sport", "NOC"]
    ]
    .groupby(["Name", "Sport", "NOC"])["Name"]
    .count()
    .reset_index(name="QtdMedalhas")
    .nlargest(columns="QtdMedalhas", n=15)
)

df = dfOlVerao.loc[(dfOlVerao["Year"] >= 1922) & (dfOlVerao["Medal"] != "-")][
    ["Name", "Year", "Medal", "Sport"]
]
df = df.loc[df.Name.isin(dfEra["Name"])]

dfMedalha = (
    df.groupby(["Name", "Sport"])["Name"]
    .count()
    .reset_index(name="QtdMedalhas")
    .sort_values(by=["QtdMedalhas"], ascending=False)
)
dfMedalha = dfMedalha.sort_values(by=["QtdMedalhas"], ascending=False)

dfComp = dfOlVerao.drop_duplicates(["Name", "Year"])[["Name", "Year"]]
dfComp = dfComp.loc[dfComp.Name.isin(dfEra["Name"])]

dfComp = dfComp.groupby(["Name"])["Name"].count().reset_index(name="Participacoes")

dfComp = dfComp.sort_values(by=["Participacoes"], ascending=False)

dfRes = dfMedalha.merge(dfComp, how="inner", left_on="Name", right_on="Name")

sns.set_theme(style="darkgrid")


f, ax = plt.subplots(figsize=(10, 16))


sns.set_color_codes("pastel")
sns.barplot(
    x="QtdMedalhas", y="Name", data=dfRes, color="g", saturation=1, label="QtdMedalhas"
)


sns.set_color_codes("muted")
sns.barplot(
    x="Participacoes",
    y="Name",
    data=dfRes,
    color="b",
    saturation=0.8,
    label="Participacoes",
)


ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 35), ylabel="", xlabel=None)
sns.despine(left=True, bottom=True)

st.header("Atletas que marcaram eras")
st.subheader("Jogos Olímpicos de Verão")
st.write("Os maiores medalhistas nas Olimpíadas de Verão")
st.pyplot(plt.gcf())
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")

loading_bar.progress(45)

################################# Visão de Período
sns.set_theme(style="darkgrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(15, 8))

dfEraYear = dfOlVerao.drop_duplicates(["Name", "Year", "Medal"])[
    ["Name", "Year", "Medal"]
]
dfEraYear = dfEraYear.loc[dfEraYear["Medal"] == "Gold"]
dfEraYear = dfEraYear.loc[dfEraYear.Name.isin(dfEra["Name"])]

dfEraYearMin = dfEraYear.groupby("Name").min("Year").reset_index()
dfEraYearMax = dfEraYear.groupby("Name").max("Year").reset_index()
dfEraYear = pd.concat([dfEraYearMin, dfEraYearMax])
dfEraYear.sort_values("Name")

sns.scatterplot(data=dfEraYear, x="Year", y="Name")
ax.set(
    xlim=(1920, 2020),
    ylabel="",
    xlabel=None,
    xticks=[
        1920,
        1924,
        1928,
        1932,
        1936,
        1940,
        1944,
        1948,
        1952,
        1956,
        1960,
        1964,
        1968,
        1972,
        1976,
        1980,
        1984,
        1988,
        1992,
        1996,
        2000,
        2004,
        2008,
        2012,
        2016,
        2020,
    ],
)
sns.despine(left=True, bottom=True)

st.write(
    "Períodos de medalhas de ouro dos melhores atletas ao longo das Olimpíadas de Verão"
)
st.pyplot(plt.gcf())
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")
ploting_state.text("Plotando os gráficos...")

# Quais os atletas que marcaram eras (Guilherme) - Inverno
dfOlInverno = ft_Competicao.loc[ft_Competicao["Season"] == "Winter"]
dfEra = (
    dfOlInverno.loc[(dfOlInverno["Year"] >= 1922) & (dfOlInverno["Medal"] != "-")][
        ["Name", "Medal", "Sport", "NOC"]
    ]
    .groupby(["Name", "Sport", "NOC"])["Name"]
    .count()
    .reset_index(name="QtdMedalhas")
    .nlargest(columns="QtdMedalhas", n=15)
)

df = dfOlInverno.loc[(dfOlInverno["Year"] >= 1922) & (dfOlInverno["Medal"] != "-")][
    ["Name", "Year", "Medal", "Sport"]
]
df = df.loc[df.Name.isin(dfEra["Name"])]

dfMedalha = (
    df.groupby(["Name", "Sport"])["Name"]
    .count()
    .reset_index(name="QtdMedalhas")
    .sort_values(by=["QtdMedalhas"], ascending=False)
)
dfMedalha = dfMedalha.sort_values(by=["QtdMedalhas"], ascending=False)

dfComp = dfOlInverno.drop_duplicates(["Name", "Year"])[["Name", "Year"]]
dfComp = dfComp.loc[dfComp.Name.isin(dfEra["Name"])]

dfComp = dfComp.groupby(["Name"])["Name"].count().reset_index(name="Participacoes")

dfComp = dfComp.sort_values(by=["Participacoes"], ascending=False)


dfRes = dfMedalha.merge(dfComp, how="inner", left_on="Name", right_on="Name")
# dfRes
sns.set_theme(style="darkgrid")


f, ax = plt.subplots(figsize=(10, 16))


sns.set_color_codes("pastel")
sns.barplot(
    x="QtdMedalhas", y="Name", data=dfRes, color="g", saturation=1, label="QtdMedalhas"
)


sns.set_color_codes("muted")
sns.barplot(
    x="Participacoes",
    y="Name",
    data=dfRes,
    color="b",
    saturation=0.8,
    label="Participacoes",
)


ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 35), ylabel="", xlabel=None)
sns.despine(left=True, bottom=True)

st.subheader("Jogos Olímpicos de Inverno")
st.write("Os maiores medalhistas nas Olimpíadas de Inverno")
st.pyplot(plt.gcf())
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")

loading_bar.progress(50)

################################# Visão de Período
sns.set_theme(style="darkgrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(15, 8))

dfEraYear = dfOlInverno.drop_duplicates(["Name", "Year", "Medal"])[
    ["Name", "Year", "Medal"]
]
dfEraYear = dfEraYear.loc[dfEraYear["Medal"] == "Gold"]
dfEraYear = dfEraYear.loc[dfEraYear.Name.isin(dfEra["Name"])]

dfEraYearMin = dfEraYear.groupby("Name").min("Year").reset_index()
dfEraYearMax = dfEraYear.groupby("Name").max("Year").reset_index()
dfEraYear = pd.concat([dfEraYearMin, dfEraYearMax])
dfEraYear.sort_values("Name")

sns.scatterplot(data=dfEraYear, x="Year", y="Name")
ax.set(
    xlim=(1920, 2020),
    ylabel="",
    xlabel=None,
    xticks=[
        1920,
        1924,
        1928,
        1932,
        1936,
        1940,
        1944,
        1948,
        1952,
        1956,
        1960,
        1964,
        1968,
        1972,
        1976,
        1980,
        1984,
        1988,
        1992,
        1996,
        2000,
        2004,
        2008,
        2012,
        2016,
        2020,
    ],
)
sns.despine(left=True, bottom=True)

st.write(
    "Períodos de medalhas de ouro dos melhores atletas ao longo das Olimpíadas de Inverno"
)
st.pyplot(plt.gcf())
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")

# Bubble Chart quantidade de medalhas x Renda per capita - (Guilherme) - Verão
dfOlVerao = ft_Competicao.loc[ft_Competicao["Season"] == "Summer"]

###############################################################Ouro
#########Coletivo
OuroPaisVeraoColetivo = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Gold") & (dfOlVerao["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdOuro")
)

# OuroPaisVeraoColetivo
# OuroPaisVeraoColetivo.loc[(OuroPaisVeraoColetivo['Sport'] == 'Basketball') & (OuroPaisVeraoColetivo['NOC'] == 'USA')]
#########

#########Individual
OuroPaisVeraoIndividual = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Gold") & (dfOlVerao["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdOuro")
)

OuroPaisVerao = pd.concat(
    [OuroPaisVeraoColetivo, OuroPaisVeraoIndividual], ignore_index=True
)
# OuroPaisVerao.loc[(OuroPaisVerao['NOC'] == 'USA') & (OuroPaisVerao['Sport'] == 'Athletics') ]
#########

#############################################################################Prata
#########Coletivo
PrataPaisVeraoColetivo = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Silver") & (dfOlVerao["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdPrata")
    #  .sort_values(['QtdPrata'], ascending=False)
)
#########
#########Individual
PrataPaisVeraoIndividual = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Silver") & (dfOlVerao["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdPrata")
)

PrataPaisVerao = pd.concat(
    [PrataPaisVeraoColetivo, PrataPaisVeraoIndividual], ignore_index=True
)
# PrataPaisVerao.loc[(PrataPaisVerao['NOC'] == 'USA') & (PrataPaisVerao['Sport'] == 'Athletics') ]
#########

###############################################################Bronze
#########Coletivo
BronzePaisVeraoColetivo = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Bronze") & (dfOlVerao["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdBronze")
)

# BronzePaisVeraoColetivo
# BronzePaisVeraoColetivo.loc[(BronzePaisVeraoColetivo['Sport'] == 'Basketball') & (BronzePaisVeraoColetivo['NOC'] == 'USA')]
#########

#########Individual
BronzePaisVeraoIndividual = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Bronze") & (dfOlVerao["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdBronze")
)

BronzePaisVerao = pd.concat(
    [BronzePaisVeraoColetivo, BronzePaisVeraoIndividual], ignore_index=True
)
# BronzePaisVerao.loc[(BronzePaisVerao['NOC'] == 'USA') & (BronzePaisVerao['Sport'] == 'Athletics') ]
#########

# OuroPaisVerao.loc[(OuroPaisVerao['Sport'] == 'Basketball') & (OuroPaisVerao['NOC'] == 'USA')]
TotalPaisVerao = pd.concat([OuroPaisVerao, PrataPaisVerao, BronzePaisVerao])
TotalPaisVerao = TotalPaisVerao.fillna(0)
# TotalPaisVerao.loc[(TotalPaisVerao['Sport'] == 'Basketball') & (TotalPaisVerao['NOC'] == 'USA')]
TotalPaisVerao["Total"] = (
    TotalPaisVerao["QtdOuro"] + TotalPaisVerao["QtdPrata"] + TotalPaisVerao["QtdBronze"]
)
TotalPaisVerao.head(100)
TotalPaisVerao = (
    TotalPaisVerao[["NOC", "Year", "Total"]]
    .groupby(["NOC", "Year"])
    .sum()
    .reset_index()
)

# TotalPaisVerao
dfRes = TotalPaisVerao.merge(
    dim_indicadores,
    how="inner",
    left_on=["NOC", "Year"],
    right_on=["Country Code", "Time"],
)
dfRes = dfRes.sort_values(by=["Year"], ascending=True)
dfRes["Population, total [SP.POP.TOTL]"] = (
    dfRes["Population, total [SP.POP.TOTL]"] / 1000
)
# dfRes = dfRes.loc[dfRes['NOC'] == 'CHN']
fig = px.scatter(
    dfRes,
    x="GDP per capita (current US$) [NY.GDP.PCAP.CD]",
    y="Total",
    animation_frame="Year",
    animation_group="Country Name",
    size="Population, total [SP.POP.TOTL]",
    hover_name="Country Name",
    # color = 'Country Name',
    size_max=60,
    range_x=[0, 150000],
    range_y=[0, 300],
    # color_palette =
)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

ploting_state.text("Quase terminando...")
st.header("Explorando a quantidade de medalhas por renda per capita")
st.subheader("Jogos Olímpicos de Verão")
st.write("Quantidade de medalhas x Renda per capita - Jogos Olímpicos de Verão")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig)
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")


loading_bar.progress(60)

##Obs: Acrescentar cor aos países faz alguns sumir

# Bubble Chart quantidade de medalhas x Renda per capita - (Guilherme) - Inverno
dfOlInverno = ft_Competicao.loc[ft_Competicao["Season"] == "Winter"]

###############################################################Ouro
#########Coletivo
OuroPaisInvernoColetivo = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Gold") & (dfOlInverno["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdOuro")
)

# OuroPaisInvernoColetivo
# OuroPaisInvernoColetivo.loc[(OuroPaisInvernoColetivo['Sport'] == 'Basketball') & (OuroPaisInvernoColetivo['NOC'] == 'USA')]
#########

#########Individual
OuroPaisInvernoIndividual = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Gold") & (dfOlInverno["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdOuro")
)

OuroPaisInverno = pd.concat(
    [OuroPaisInvernoColetivo, OuroPaisInvernoIndividual], ignore_index=True
)
# OuroPaisInverno.loc[(OuroPaisInverno['NOC'] == 'USA') & (OuroPaisInverno['Sport'] == 'Athletics') ]
#########

#############################################################################Prata
#########Coletivo
PrataPaisInvernoColetivo = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Silver") & (dfOlInverno["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdPrata")
    #  .sort_values(['QtdPrata'], ascending=False)
)
#########
#########Individual
PrataPaisInvernoIndividual = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Silver") & (dfOlInverno["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdPrata")
)

PrataPaisInverno = pd.concat(
    [PrataPaisInvernoColetivo, PrataPaisInvernoIndividual], ignore_index=True
)
# PrataPaisInverno.loc[(PrataPaisInverno['NOC'] == 'USA') & (PrataPaisInverno['Sport'] == 'Athletics') ]
#########

###############################################################Bronze
#########Coletivo
BronzePaisInvernoColetivo = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Bronze") & (dfOlInverno["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdBronze")
)

# BronzePaisInvernoColetivo
# BronzePaisInvernoColetivo.loc[(BronzePaisInvernoColetivo['Sport'] == 'Basketball') & (BronzePaisInvernoColetivo['NOC'] == 'USA')]
#########

#########Individual
BronzePaisInvernoIndividual = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Bronze") & (dfOlInverno["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdBronze")
)

BronzePaisInverno = pd.concat(
    [BronzePaisInvernoColetivo, BronzePaisInvernoIndividual], ignore_index=True
)
# BronzePaisInverno.loc[(BronzePaisInverno['NOC'] == 'USA') & (BronzePaisInverno['Sport'] == 'Athletics') ]
#########

# OuroPaisInverno.loc[(OuroPaisInverno['Sport'] == 'Basketball') & (OuroPaisInverno['NOC'] == 'USA')]
TotalPaisInverno = pd.concat([OuroPaisInverno, PrataPaisInverno, BronzePaisInverno])
TotalPaisInverno = TotalPaisInverno.fillna(0)
# TotalPaisInverno.loc[(TotalPaisInverno['Sport'] == 'Basketball') & (TotalPaisInverno['NOC'] == 'USA')]
TotalPaisInverno["Total"] = (
    TotalPaisInverno["QtdOuro"]
    + TotalPaisInverno["QtdPrata"]
    + TotalPaisInverno["QtdBronze"]
)
TotalPaisInverno.head(100)
TotalPaisInverno = (
    TotalPaisInverno[["NOC", "Year", "Total"]]
    .groupby(["NOC", "Year"])
    .sum()
    .reset_index()
)

# TotalPaisInverno
dfRes = TotalPaisInverno.merge(
    dim_indicadores,
    how="inner",
    left_on=["NOC", "Year"],
    right_on=["Country Code", "Time"],
)
dfRes = dfRes.sort_values(by=["Year"], ascending=True)
dfRes["Population, total [SP.POP.TOTL]"] = (
    dfRes["Population, total [SP.POP.TOTL]"] / 1000
)
# dfRes = dfRes.loc[dfRes['NOC'] == 'CHN']
fig = px.scatter(
    dfRes,
    x="GDP per capita (current US$) [NY.GDP.PCAP.CD]",
    y="Total",
    animation_frame="Year",
    animation_group="Country Name",
    size="Population, total [SP.POP.TOTL]",
    hover_name="Country Name",
    # color = 'Country Name',
    size_max=60,
    range_x=[0, 120000],
    range_y=[0, 100],
    # color_palette =
)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
st.subheader("Jogos Olímpicos de Inverno")
st.write("Quantidade de medalhas x Renda per capita - Jogos Olímpicos de Iverno")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig)
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")

##Obs: Acrescentar cor aos países faz alguns sumir

# Top 10 de países ganhadores de medalha total - (Guilherme) - Verão
# pd.set_option('display.max_rows', 300)


dfOlVerao = ft_Competicao.loc[
    (ft_Competicao["Season"] == "Summer") & (ft_Competicao["Year"] >= 1920)
]

###############################################################Ouro
#########Coletivo
OuroPaisVeraoColetivo = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Gold") & (dfOlVerao["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdOuro")
)

# OuroPaisVeraoColetivo
# OuroPaisVeraoColetivo.loc[(OuroPaisVeraoColetivo['Sport'] == 'Basketball') & (OuroPaisVeraoColetivo['NOC'] == 'USA')]
#########

#########Individual
OuroPaisVeraoIndividual = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Gold") & (dfOlVerao["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdOuro")
)

OuroPaisVerao = pd.concat(
    [OuroPaisVeraoColetivo, OuroPaisVeraoIndividual], ignore_index=True
)
# OuroPaisVerao.loc[(OuroPaisVerao['NOC'] == 'USA') & (OuroPaisVerao['Sport'] == 'Athletics') ]
#########

#############################################################################Prata
#########Coletivo
PrataPaisVeraoColetivo = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Silver") & (dfOlVerao["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdPrata")
    #  .sort_values(['QtdPrata'], ascending=False)
)
#########
#########Individual
PrataPaisVeraoIndividual = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Silver") & (dfOlVerao["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdPrata")
)

PrataPaisVerao = pd.concat(
    [PrataPaisVeraoColetivo, PrataPaisVeraoIndividual], ignore_index=True
)
# PrataPaisVerao.loc[(PrataPaisVerao['NOC'] == 'USA') & (PrataPaisVerao['Sport'] == 'Athletics') ]
#########

###############################################################Bronze
#########Coletivo
BronzePaisVeraoColetivo = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Bronze") & (dfOlVerao["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdBronze")
)

# BronzePaisVeraoColetivo
# BronzePaisVeraoColetivo.loc[(BronzePaisVeraoColetivo['Sport'] == 'Basketball') & (BronzePaisVeraoColetivo['NOC'] == 'USA')]
#########

#########Individual
BronzePaisVeraoIndividual = (
    dfOlVerao.loc[
        (dfOlVerao["Medal"] == "Bronze") & (dfOlVerao["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdBronze")
)

BronzePaisVerao = pd.concat(
    [BronzePaisVeraoColetivo, BronzePaisVeraoIndividual], ignore_index=True
)
# BronzePaisVerao.loc[(BronzePaisVerao['NOC'] == 'USA') & (BronzePaisVerao['Sport'] == 'Athletics') ]
#########

# OuroPaisVerao.loc[(OuroPaisVerao['Sport'] == 'Basketball') & (OuroPaisVerao['NOC'] == 'USA')]
TotalPaisVerao = pd.concat([OuroPaisVerao, PrataPaisVerao, BronzePaisVerao])
TotalPaisVerao = TotalPaisVerao.fillna(0)
# TotalPaisVerao.loc[(TotalPaisVerao['Sport'] == 'Basketball') & (TotalPaisVerao['NOC'] == 'USA')]
TotalPaisVerao["Total"] = (
    TotalPaisVerao["QtdOuro"] + TotalPaisVerao["QtdPrata"] + TotalPaisVerao["QtdBronze"]
)
TotalPaisVerao = (
    TotalPaisVerao[["NOC", "Total"]]
    .groupby("NOC")
    .sum()
    .reset_index()
    .nlargest(10, "Total")
)
sns.set_theme(style="darkgrid")

plt.figure(figsize=(20, 5))

fig = sns.barplot(data=TotalPaisVerao, x="NOC", y="Total")
fig.set(xlabel=None, ylabel=None)

sns.despine(left=True, bottom=True)

st.header("Os maiores medalhistas de todos os tempos")
st.subheader("Jogos Olímpicos de Verão")
st.write("Os 10 países que mais ganharam medalhas nos Jogos Olímpicos de Verão")
st.pyplot(plt.gcf())
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")

loading_bar.progress(70)

# Top 10 de países ganhadores de medalha total - (Guilherme) - Inverno
# pd.set_option('display.max_rows', 300)


dfOlInverno = ft_Competicao.loc[
    (ft_Competicao["Season"] == "Winter") & (ft_Competicao["Year"] >= 1920)
]

###############################################################Ouro
#########Coletivo
OuroPaisInverno = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Gold") & (dfOlInverno["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdOuro")
)

# OuroPaisInverno
# OuroPaisInverno.loc[(OuroPaisInverno['Sport'] == 'Basketball') & (OuroPaisInverno['NOC'] == 'USA')]
#########

#########Individual
OuroPaisInvernoIndividual = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Gold") & (dfOlInverno["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdOuro")
)

OuroPais = pd.concat([OuroPaisInverno, OuroPaisInvernoIndividual], ignore_index=True)
# OuroPais.loc[(OuroPais['NOC'] == 'USA') & (OuroPais['Sport'] == 'Athletics') ]
#########

#############################################################################Prata
#########Coletivo
PrataPaisInvernoColetivo = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Silver") & (dfOlInverno["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdPrata")
    #  .sort_values(['QtdPrata'], ascending=False)
)
#########
#########Individual
PrataPaisInvernoIndividual = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Silver") & (dfOlInverno["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdPrata")
)

PrataPaisInverno = pd.concat(
    [PrataPaisInvernoColetivo, PrataPaisInvernoIndividual], ignore_index=True
)
# PrataPaisInverno.loc[(PrataPaisInverno['NOC'] == 'USA') & (PrataPaisInverno['Sport'] == 'Athletics') ]
#########

###############################################################Bronze
#########Coletivo
BronzePaisInvernoColetivo = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Bronze") & (dfOlInverno["Esporte Coletivo"] == 1)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])
    .Sport.nunique()
    .reset_index(name="QtdBronze")
)

# BronzePaisInvernoColetivo
# BronzePaisInvernoColetivo.loc[(BronzePaisInvernoColetivo['Sport'] == 'Basketball') & (BronzePaisInvernoColetivo['NOC'] == 'USA')]
#########

#########Individual
BronzePaisInvernoIndividual = (
    dfOlInverno.loc[
        (dfOlInverno["Medal"] == "Bronze") & (dfOlInverno["Esporte Coletivo"] == 0)
    ][["NOC", "Medal", "Sport", "Year", "Sex"]]
    .groupby(["NOC", "Medal", "Sport", "Year", "Sex"])["Medal"]
    .count()
    .reset_index(name="QtdBronze")
)

BronzePaisInverno = pd.concat(
    [BronzePaisInvernoColetivo, BronzePaisInvernoIndividual], ignore_index=True
)
# BronzePaisInverno.loc[(BronzePaisInverno['NOC'] == 'USA') & (BronzePaisInverno['Sport'] == 'Athletics') ]
#########

# OuroPais.loc[(OuroPais['Sport'] == 'Basketball') & (OuroPais['NOC'] == 'USA')]
TotalPaisInverno = pd.concat([OuroPais, PrataPaisInverno, BronzePaisInverno])
TotalPaisInverno = TotalPaisInverno.fillna(0)
# TotalPaisInverno.loc[(TotalPaisInverno['Sport'] == 'Basketball') & (TotalPaisInverno['NOC'] == 'USA')]
TotalPaisInverno["Total"] = (
    TotalPaisInverno["QtdOuro"]
    + TotalPaisInverno["QtdPrata"]
    + TotalPaisInverno["QtdBronze"]
)
TotalPaisInverno = (
    TotalPaisInverno[["NOC", "Total"]]
    .groupby("NOC")
    .sum()
    .reset_index()
    .nlargest(10, "Total")
)
sns.set_theme(style="darkgrid")

plt.figure(figsize=(20, 5))

fig = sns.barplot(data=TotalPaisInverno, x="NOC", y="Total")
fig.set(xlabel=None, ylabel=None)

sns.despine(left=True, bottom=True)

st.subheader("Jogos Olímpicos de Inverno")
st.write("Os 10 países que mais ganharam medalhas nos Jogos Olímpicos de Inverno")
st.pyplot(plt.gcf())
st.caption("Fonte: dados retirados em https://www.sports-reference.com/")

st.header("A corrida pelas medalhas")
st.subheader("Jogos Olímpicos de Verão")

st.image("/home/vitor-mafra/Desktop/ufmg/2022_01/dataviz/streamlit_dataviz/Peek 2022-07-10 21-06.gif")

loading_bar.progress(80)
st.subheader("Jogos Olímpicos de Inverno")

st.image("/home/vitor-mafra/Desktop/ufmg/2022_01/dataviz/streamlit_dataviz/Peek 2022-07-10 21-08.gif")

loading_bar.progress(90)
ploting_state.empty()
loading_bar.progress(100)
warning.success("Tudo certo!")

time.sleep(2)
warning.empty()
loading_bar.empty()
