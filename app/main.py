import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from engine import simular_monte_carlo

#Configuração da página
st.set_page_config(page_title="WealthPath - Adivisor", layout="wide")

st.title("📊 WealthPath: Simulador de Independência Financeira")
st.markdown('---')

#Sidebar para inputs do cliente
st.sidebar.header('📝 Dados do Planejamento')

#Carregar base para exemplo (input manual primeiro)
patrimonio = st.sidebar.number_input('Patrimonio Atual (R$)', value=1000000, step=50000)
aporte = st.sidebar.number_input('Aporte Mensal (R$)', value=5000, step=500)
gasto = st.sidebar.number_input('Gasto Mensal Desejado (R$)', value=10000, step=500)
idade_atual = st.sidebar.slider('Idade Atual', 18, 80, 35)
idade_aposentadoria = st.sidebar.slider('Idade de Aposentadoria', 45, 90, 65)
perfil = st.sidebar.selectbox('Perfil de Investidor', ['Conservador', 'Moderado', 'Arrojado'])

tempo_simulacao = idade_aposentadoria - idade_atual

if st.sidebar.button('Simular Cenários'):
    #Chamar engine
    resultados = simular_monte_carlo(patrimonio, aporte, tempo_simulacao, gasto, perfil)

    #Cálculos de métricas
    meses = tempo_simulacao * 12
    eixo_x = np.arange(meses) / 12 #converte meses para anos

    #criar gráfico
    fig = go.Figure()

    #plotar primeiras 50 simulações
    for i in range(50):
        fig.add_trace(go.Scatter(x=eixo_x, y=resultados[i], mode='lines',
                                 line=dict(width=1), opacity=0.1, showlegend=False))

    #Plotar mediana
    mediana = np.median(resultados, axis=0)
    fig.add_trace(go.Scatter(x=eixo_x, y=mediana, mode='lines',
                             name='Cenário Provável (Mediana)', line=dict(color='gold', width=4)))

    fig.update_layout(title='Projeção da Evolução Patrimonial (Monte Carlo)',
        xaxis_title='Anos a partir de agora',
        yaxis_title='Patrimônio (R$)',
        template='plotly_dark')

    #Exibir métricas em colunas
    col1, col2, col3 = st.columns(3)
    sucesso = (resultados[:, -1] > 0).mean() * 100

    col1.metric('Probabilidade de Sucesso', f'{sucesso}%')
    col2.metric('Saldo Estimado (Mediana)', f'R$ {mediana[-1]:,.2f}')
    col3.metric('Tempo de Simulação', f'{tempo_simulacao} anos')

    st.plotly_chart(fig, use_container_width=True)

    #Insight Automático
    st.subheader('💡 Diagnóstico do Consultor')
    if sucesso > 80:
        st.success('O plano é sólido! A probabilidade de manter o padrão de vida é alta.')
    elif sucesso > 50:
        st.warning('Atenção: O plano possui riscos moderados. Considere aumentar aportes ou rever o perfil de risco.')
    else:
        st.error('Risco Crítico: Grande chance de descapitalização antes da idade alvo. É necessário ajuste imediato.')

else:
    st.info('Ajuste os dados na barra lateral e clique em "Simular Cenários" para começar.')