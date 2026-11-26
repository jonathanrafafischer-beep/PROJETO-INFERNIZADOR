
# Projeto Integrador - 2º Ano
# Simulador da ação de Nanopartículas de Prata contra E. coli
# Versão: v0.0.4
# NOTA SOBRE O USO DE AI
# Ferramentas de Inteligência Artificial foram utilizadas exclusivamente como apoio 
# técnico para revisão de sintaxe, aprimoramento do texto e formatação de dados. 
# Toda a concepção científica, seleção bibliográfica, definição dos parâmetros 
# biológicos e validação dos resultados são de autoria integral do grupo.

import math
import csv
import os
import sys
import datetime

# Garante acentuação correta no terminal do Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --- Constantes calibradas com a literatura de microdiluição ---
MU_CRESCIMENTO = 0.60     # Taxa de replicação de E. coli (h^-1)
K_CAPACIDADE_MEIO = 1.0e9 # Capacidade de suporte típica do meio (CFU/mL)
K_MAX_MORTE = 1.35        # Taxa máxima de morte bactericida (h^-1)
IC50 = 8.00               # Concentração inibitória mediana dos artigos (ug/mL)
HILL_H = 1.60             # Coeficiente sigmoidal de Hill


def mostrar_aviso():
    print("=" * 68)
    print("  SIMULADOR DE EFICÁCIA DE AgNPs CONTRA Escherichia coli - v0.0.4")
    print("=" * 68)
    print("AVISO:")
    print("Este projeto foi desenvolvido por estudantes do 2º ano para fins acadêmicos.")
    print("Trata-se de uma modelagem computacional e NÃO substitui ensaios in vitro.")
    print("Pode conter variações inerentes a simplificações biológicas do modelo.")
    print("=" * 68)


def menu():
    while True:
        print("\n" + "=" * 50)
        print("                 MENU PRINCIPAL                  ")
        print("=" * 50)
        print("  [1] Iniciar Simulação")
        print("  [2] Sair")
        print("=" * 50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            rodar_simulacao()
        elif opcao == "2":
            print("\nEncerrando o programa... Até mais!")
            break
        else:
            print("Opção inválida. Digite 1 para simular ou 2 para sair.")


def avaliar_uvvis(waveLength, fwhm):
    # Avaliação coloidal baseada no UV-Vis (deslocamento SPR e FWHM)
    pontos_de_risco = 0

    if waveLength > 460:
        pontos_de_risco += 2
    elif waveLength > 440:
        pontos_de_risco += 1

    if fwhm > 90:
        pontos_de_risco += 2
    elif fwhm > 70:
        pontos_de_risco += 1

    # Classificação do estado e atividade relativa
    if pontos_de_risco <= 1:
        estado = "ESTÁVEL (Monodisperso)"
        atividade = 1.00  # 100% de atividade de superfície
    elif pontos_de_risco == 2:
        estado = "ALERTA LEVE (Leve Polidispersão)"
        atividade = 0.85  # 85% de atividade
    elif pontos_de_risco <= 4:
        estado = "ALERTA (Agregação Parcial)"
        atividade = 0.65  # 65% de atividade
    else:
        estado = "INSTÁVEL (Forte Aglomeração)"
        atividade = 0.30  # 30% de atividade

    return pontos_de_risco, estado, atividade


def rodar_simulacao():
    print("\n--- ENTRADA DE PARÂMETROS ---")
    
    waveLength = ler_numero("Comprimento de onda do pico de absorbância (300 a 900 nm): ", float, 300, 900)
    fwhm = ler_numero("Largura a meia altura - FWHM (nm): ", float, 1)
    concentracao_agnp = ler_numero("Concentração de AgNP (ug/mL): ", float, 0)
    bacterias_iniciais = ler_numero("Quantidade inicial de E. coli (CFU/mL, ex: 1e6): ", float, 1)
    tempo = ler_numero("Tempo de exposição (horas, ex: 6, 18 ou 24): ", float, 0.1)

    print("\nProcessando a simulação...")

    # 1. Avaliação do estado das nanopartículas
    pontos_risco, estado, atividade = avaliar_uvvis(waveLength, fwhm)
    conc_efetiva = concentracao_agnp * atividade

    # 2. Taxa de morte induzida pela cinética de Hill
    if conc_efetiva > 0:
        k_kill = K_MAX_MORTE * (conc_efetiva ** HILL_H) / ((IC50 ** HILL_H) + (conc_efetiva ** HILL_H))
    else:
        k_kill = 0.0

    # 3. Resolução numérica da EDO pelo Método de Euler
    # A equação calcula a taxa de nascimentos e mortes. Como não da pra calcular o final direto de uma vez, o metodo de Euler resolve dando passinhos pequenos ao longo do tempo
    dt = 0.01  # passo de 0.01h (36 segundos) para precisão
    t = 0.0
    N = float(bacterias_iniciais)
    
    # Amostragem da curva temporal para exportar em CSV
    historico = []
    passo_amostra = tempo / 50  # registra 50 pontos ao longo do tempo
    proxima_amostra = 0.0

    historico.append((0.0, N, (N / bacterias_iniciais) * 100))

    while t < tempo:
        if N <= 0:
            N = 0.0
            break

        crescimento = MU_CRESCIMENTO * N * (1.0 - (N / K_CAPACIDADE_MEIO))
        morte = k_kill * N
        dN = (crescimento - morte) * dt
        N = max(0.0, N + dN)
        t += dt

        if t >= proxima_amostra:
            historico.append((round(t, 2), N, (N / bacterias_iniciais) * 100))
            proxima_amostra += passo_amostra

    bacterias_finais = N
    sobrevivencia = (bacterias_finais / bacterias_iniciais) * 100

    # 4. Apresentação técnica e detalhada dos resultados
    print("\n" + "-" * 50)
    print(">>> CARACTERIZAÇÃO DAS AgNPs")
    print(f"Pontos de risco de agregação: {pontos_risco}/4")
    print(f"Estado coloidal: {estado}")
    print(f"Atividade relativa estimada: {atividade * 100:.0f}%")
    print(f"Concentração efetiva de AgNP: {conc_efetiva:.2f} ug/mL")
    print("-" * 50)

    print("\n>>> RESULTADOS DA SIMULAÇÃO")
    print(f"População inicial: {bacterias_iniciais:.2e} CFU/mL")
    print(f"Tempo decorrido: {tempo:.1f} h")
    print(f"Taxa de morte induzida (k_kill): {k_kill:.4f} h^-1")
    print(f"Taxa de replicação bacteriana (mu): {MU_CRESCIMENTO:.4f} h^-1")
    print(f"População final estimada: {bacterias_finais:.2e} CFU/mL")
    print(f"Sobrevivência relativa: {sobrevivencia:.2f}%")

    print("\n--- AVALIAÇÃO DO EFEITO ---")
    if conc_efetiva == 0:
        diagnostico = "CONTROLE NEGATIVO: Sem AgNPs ativas, as bactérias se multiplicam normalmente."
    elif k_kill > MU_CRESCIMENTO * 1.5:
        diagnostico = "EFEITO BACTERICIDA ELEVADO (Morte rápida supera amplamente o crescimento)."
    elif k_kill >= MU_CRESCIMENTO * 0.85:
        diagnostico = "EFEITO BACTERIOSTÁTICO / INIBITÓRIO (Taxa de morte em equilíbrio ou ligeiramente superior à de crescimento)."
    else:
        diagnostico = "EFEITO INSUFICIENTE / SUB-INIBITÓRIO (A replicação bacteriana supera a ação das AgNPs)."
    
    print(diagnostico)
    print("=" * 68)

    # 5. Opção de exportação para CSV
    salvar = input("\nDeseja salvar a curva em um arquivo CSV para gerar gráficos? (s/n): ").strip().lower()
    if salvar in ["s", "sim"]:
        salvar_csv(historico, conc_efetiva, tempo, diagnostico)


def salvar_csv(historico, conc_efetiva, tempo, diagnostico):
    nome_padrao = "resultado_simulacao.csv"
    nome = input(f"Nome do arquivo CSV [aperte Enter para '{nome_padrao}']: ").strip()
    if not nome:
        nome = nome_padrao
    if not nome.endswith(".csv"):
        nome += ".csv"

    try:
        with open(nome, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f, delimiter=";")
            escritor.writerow(["# Simulador AgNP vs E. coli - Projeto Integrador"])
            escritor.writerow(["# Data", datetime.datetime.now().strftime("%d/%m/%Y %H:%M")])
            escritor.writerow(["# Concentracao Efetiva (ug/mL)", f"{conc_efetiva:.2f}"])
            escritor.writerow(["# Tempo (horas)", f"{tempo:.1f}"])
            escritor.writerow(["# Diagnostico", diagnostico])
            escritor.writerow([])
            escritor.writerow(["Tempo (h)", "Populacao (CFU/mL)", "Sobrevivencia (%)"])
            
            for t, pop, sob in historico:
                escritor.writerow([f"{t:.2f}".replace(".", ","), f"{pop:.2e}", f"{sob:.2f}".replace(".", ",")])

        print(f"\n[Sucesso] Arquivo '{nome}' salvo com sucesso! Você pode abrir no Excel para plotar a curva de decaimento.")
    except Exception as e:
        print(f"\n[Erro] Falha ao salvar arquivo: {e}")


def ler_numero(mensagem, tipo, minimo=None, maximo=None):
    while True:
        entrada = input(mensagem).strip()
        try:
            valor = tipo(entrada)
            if minimo is not None and valor < minimo:
                print(f"O valor não pode ser menor que {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"O valor não pode ser maior que {maximo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite apenas números válidos.")


if __name__ == "__main__":
    mostrar_aviso()
    menu()
