#!/usr/bin/env python3

"""
Nome: Camila de Oliveira Gomes

Exercício 08 / parte 1 - Hamming 
"""

POSICOES_PARIDADE = [1, 2, 4, 8, 16]
TOTAL_BITS = 31
BITS_DADOS = 26


def validar_entrada(dado: str) -> bool:
    "Verifica se a entrada possui exatamente 26 números binários entre 0 e 1"
    return len(dado) == BITS_DADOS and all(c in "01" for c in dado)


def codificar_hamming(dados_26: str) -> list[int]:
    "Recebe uma string com 26 bits de dados e devolve uma lista de 32 inteiros"
    if not validar_entrada(dados_26):
        raise ValueError("A entrada deve conter exatamente 26 bits binários.")

    palavra = [0] * (TOTAL_BITS + 1)

    idx_dado = 0
    for pos in range(1, TOTAL_BITS + 1):
        if pos not in POSICOES_PARIDADE:
            palavra[pos] = int(dados_26[idx_dado])
            idx_dado += 1

    "Calcula cada bit de paridade (paridade par)"
    for p in POSICOES_PARIDADE:
        soma = 0
        for pos in range(1, TOTAL_BITS + 1):
            "Se a posição contém o bit de paridade 'p' na sua representação binária"
            if pos != p and (pos & p) != 0:
                soma ^= palavra[pos]
        palavra[p] = soma

    return palavra


def palavra_para_string(palavra: list[int]) -> str:
    return "".join(str(palavra[i]) for i in range(1, TOTAL_BITS + 1))


def exibir_detalhes_paridade(palavra: list[int]):
    print("  ")
    print("Detalhamento do cálculo de Pariedade")

    for p in POSICOES_PARIDADE:
        cobertos = [pos for pos in range(1, TOTAL_BITS + 1) if pos != p and (pos & p) != 0]
        
        posicoes_str = ", ".join(f"{pos:>2}" for pos in cobertos)
        equacao_rotulos = " + ".join(f"D{pos}" for pos in cobertos)
        equacao_valores = " + ".join(str(palavra[pos]) for pos in cobertos)
        
        qtd_uns = sum(palavra[pos] for pos in cobertos)
        tipo_paridade = "par" if qtd_uns % 2 == 0 else "ímpar"

        print(f"\nP{p:<2} - Bit de Paridade na Posição {p:>2}")
        print(f" - Posições verificadas: [{posicoes_str}]")
        print(f" - Fórmula: P{p} = {equacao_rotulos}")
        print(f" - Cálculo: P{p} = {equacao_valores}")
        print(f" - Total  : {qtd_uns} ({tipo_paridade}), ou seja, P{p} = {palavra[p]}")
    
    print("\n" + "=" * 70)

def verificar_e_corrigir(palavra_com_erro: list[int]) -> tuple[list[int], int]:
    sindrome = 0
    palavra_corrigida = list(palavra_com_erro)

    for p in POSICOES_PARIDADE:
        paridade_calculada = 0
        for pos in range(1, TOTAL_BITS + 1):
            if (pos & p) != 0:
                paridade_calculada ^= palavra_com_erro[pos]
        if paridade_calculada != 0:
            sindrome += p

    if sindrome != 0:
        palavra_corrigida[sindrome] ^= 1

    return palavra_corrigida, sindrome


def main():
    print("  ")
    print("Codificador Hamming (31, 26)")
    print("  ")
    entrada = input("Digite uma sequência binária de 26 bits: ").strip()

    while not validar_entrada(entrada):
        print("Entrada inválida! Certifique-se de digitar exatamente 26 dígitos binários (0 ou 1)")
        entrada = input("Digite novamente: ").strip()

    palavra = codificar_hamming(entrada)
    palavra_str = palavra_para_string(palavra)

    print("\nResultado da Codificação")
    print(f" - Entrada original (26 bits): {entrada}")
    print(f" - Palavra codificada (31 bits): {palavra_str}")
    
    print("\nPosições dos bits de paridade:")
    for p in POSICOES_PARIDADE:
        print(f"  Posição {p:>2}: {palavra[p]}")

    exibir_detalhes_paridade(palavra)


if __name__ == "__main__":
    main()