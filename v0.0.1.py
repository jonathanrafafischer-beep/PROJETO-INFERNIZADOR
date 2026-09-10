//O MAIN DO CODIGO, ONDE ELE VAI INICIAR TUDO, TEM AS FUNCOES DE INPUT DA FUNC DE INPUT
def main():
    print("SIMULAÇÃO DE AGLOMERAÇÃO AGNP's")
    waveLenght = ler_input("Comprimento de onda do pico de absorbancia(300nm<=x<=900nm) : ", float, validacao=lambda x: 300<=x<=900)
    fwhm = ler_input("Largura a meia altura(nm) : ", float) 
    naclconc = ler_input("Concentracao de sal do meio(%) : ", float) #EXEMPLO : (0.9%)
    iniciarsimulação = input("Dados coletados, pressione enter para iniciar a simulação")
    simulacao(waveLenght, fwhm, naclconc)


//PROTOTIPO DE SIMULAÇÃO
//NÃO É UMA SIMULAÇAO DE VERDADE E SO UM IF ELSE ELIF ELIF
def simulacao(waveLenght, fwhm, naclconc):
    pontos_de_risco = 0

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

    if pontos_de_risco <= 2:
        print("Resultado : Estavel")
        print("As AgNPs tem propiedades oticas excelentes e o meio tem salinidade estavel")
        print("Probabilidade de aglomeração na colônia: BAIXA.")
    elif pontos_de_risco <= 4:
        print("Resultado : Alerta")
        print("As partículas estão limítrofes ou o sal do meio vai forçar uma aglomeração parcial.")
        print("Probabilidade de aglomeração na colônia: MÉDIA.")
    else:
        print("Resultado : Instavel")
        print("O pico está muito largo, deslocado ou o sal destruirá a estabilidade eletrostática.")
        print("Probabilidade de aglomeração na colônia: ALTÍSSIMA.")


//FUNCAO PRA FACILITAR O INPUT, PQ VAI TER VARIADOS TIPOS DE ENTRADA, MENSAGEM SIGNIFICA O TEXTO, O TIPO É O TIPO DE DADO INT STRING ETC, VALIDACAO É POR EXEMPLO O INPUT SÓ VAI SE X > ALGUM VALOR Q VC QUISER
def ler_input(mensagem, tipo, validacao=lambda x: True):
    while True:
        entrada = input(mensagem)
        try:
            valor = tipo(entrada)
            if validacao(valor) == True:
                return valor
            print("Valor invalido, por favor insira um valor válido")

        except ValueError:
            print("Valor invalido, por favor insira um valor válido do tipo " + tipo.__name__)


if __name__ == "__main__":
    main()
