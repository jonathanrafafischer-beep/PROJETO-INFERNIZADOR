import math
pi = 3.14159265358979


def main():
    waveLenght = ler_input("Comprimento de onda do pico de absorbancia (300nm<=x<=900nm): ", float, validacao=lambda x: 300 <= x <= 900)
    fwhm = ler_input("Largura a meia altura - FWHM (nm): ", float, validacao=lambda x: x > 0)
    naclconc = ler_input("Concentracao de sal do meio (%): ", float, validacao=lambda x: x >= 0)
    concentracao_agnp = ler_input("Concentracao de AgNP (ug/mL): ", float, validacao=lambda x: x > 0)
    bacterias_iniciais = ler_input("Quantidade inicial de E. coli (CFU/mL): ", float, validacao=lambda x: x > 0)
    tempo = ler_input("Tempo de exposicao (horas): ", float, validacao=lambda x: x > 0)

    input("Pressione enter pra iniciar a simulação")

    simulacao(waveLenght, fwhm, naclconc, concentracao_agnp, bacterias_iniciais, tempo)


def simulacao(waveLenght, fwhm, naclconc, concentracao_agnp, bacterias_iniciais, tempo):

    pontos_de_risco = 0

    #parte da v0.1
    if waveLenght > 430:
        pontos_de_risco += 2
    elif waveLenght > 415:
        pontos_de_risco += 1

    if fwhm > 80:
        pontos_de_risco += 3
    elif fwhm > 50:
        pontos_de_risco += 1

    if naclconc >= 0.9:
        pontos_de_risco += 3
    elif naclconc > 0.1:
        pontos_de_risco += 1

    # coisa da 0.2

    # o risco de aglomeracao transformado em atividade
    # valor provisorios
    # precisa ser ajustado

    if pontos_de_risco <= 2:
        estado = "ESTAVEL"
        atividade_relativa = 1.0

    elif pontos_de_risco <= 4:
        estado = "ALERTA"
        atividade_relativa = 0.6

    else:
        estado = "INSTAVEL"
        atividade_relativa = 0.25

    print("\nestago agnps")

    print("Pontos de risco:", pontos_de_risco)
    print("Estado:", estado)
    print(f"Atividade relativa estimada: {atividade_relativa * 100:.0f}%")

    # Numero 0.01 NAO e uma constante universal
    # E apenas um parametro inicial do modelo
    # que devera ser calibrado posteriormente

    K_BASE = 0.01

    k = K_BASE * atividade_relativa * concentracao_agnp

    print("\nsimulação")

    print(f"Quantidade inicial: {bacterias_iniciais:.2e} CFU/mL")
    print(f"Constante de efeito k: {k:.4f}")

    # N(t) = N0 * e^(-k*t)
    # N0 = bacterias no inicio
    # N(t) = bacterias depois de certo tempo
    # k = intensidade do efeito
    # t = tempo

    bacterias_finais = (bacterias_iniciais * math.exp(-k * tempo)
    )

    sobrevivencia = (bacterias_finais / bacterias_iniciais ) * 100

    print(f"\nTempo de exposicao: {tempo:.1f} h")
    print(f"Quantidade de bacterias finais: {bacterias_finais:.2e} CFU/mL")
    print(f"Quantidade de sobreviventes: {sobrevivencia:.2f}%")

    print("\n--- RESULTADO ---")

    if sobrevivencia < 10:
        print("EFEITO  ALTO")

    elif sobrevivencia < 50:
        print("EFEITO MODERADO")

    else:
        print("EFEITO BAIXO")


def ler_input(mensagem, tipo, validacao=lambda x: True):

    while True:

        entrada = input(mensagem)

        try:
            valor = tipo(entrada)

            if validacao(valor):
                return valor

            print("Valor invalido.")

        except ValueError:
            print("Valor invalido. Insira um valor do tipo " + tipo.__name__)


if __name__ == "__main__":
    main()
