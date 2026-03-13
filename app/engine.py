import numpy as np

def simular_monte_carlo(patrimonio_inicial, aporte_mensal, anos, gasto_mensal, perfil):
    """
    Simula 1000 cenários possíveis para o pratrimônio do cliente.
    """
    n_simulacoes = 1000
    meses = anos * 12

    #Configuração de risco baseada no perfil (Retorno anual médio e Volatilidade)
    perfis_config = {
        'Conservador': {"retorno": 0.09, "vol": 0.03}, #9% a.a, baixa varição
        'Moderador': {"retorno": 0.12, "vol": 0.08}, #12% a.a
        'Arrojado':  {"retorno": 0.15, "vol": 0.15}, #15% a.a, alta variação
    }

    config = perfis_config[perfil]
    #Converter retorno anual para mensal (simplificado)
    retorno_mensal_medio = (1 + config['retorno'])**(1/12) - 1
    vol_mensal = config['vol'] / np.sqrt(12)

    resultados = np.zeros((n_simulacoes, meses))

    for i in range(n_simulacoes):
        saldo = patrimonio_inicial
        for t in range(meses):
            #Retorno aleatório seguindo uma distribuição normal
            choque_mercado = np.random.normal(retorno_mensal_medio, vol_mensal)
            saldo = (saldo * (1 + choque_mercado)) + aporte_mensal - gasto_mensal

            if saldo < 0:
                saldo = 0
            resultados[i, t] = saldo
    return resultados