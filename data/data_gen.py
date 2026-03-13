import pandas as pd
import numpy as np
import os

if not os.path.exists('data'):
    os.mkdir('data')

def gerar_base_clientes(n_clientes=50):
    np.random.seed(42) #para os dados serem sempre os mesmos

    data = {
        'ID_Cliente': range(1, n_clientes + 1 ),
        'Nome': [f'Cliente {i}' for i in range(1, n_clientes + 1)],
        'Idade': np.random.randint(30, 65, n_clientes),
        'Idade_Aposentadoria': np.random.randint(65, 75, n_clientes),
        'Patrimonio_Inicial': np.random.uniform(500_000, 10_000_000, n_clientes).round(2),
        'Aporte_Mensal': np.random.uniform(2_000, 50_000, n_clientes).round(2),
        'Gasto_Mensal_Desejado': np.random.uniform(10_000, 40_000, n_clientes).round(2),
        'Perfil_Risco': np.random.choice(['Conversador', 'Moderado', 'Arrojado'], n_clientes),
        'Expectativa_Vida': [90] * n_clientes
    }

    df = pd.DataFrame(data)
    df.to_csv('data/simulacao_clientes.csv', index=False)
    print("Base de Dados 'simulacao_clientes.csv' gerada com sucesso!")

if __name__ == '__main__':
    gerar_base_clientes()