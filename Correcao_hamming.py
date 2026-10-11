#!/usr/bin/env python3

"""
Nome: Camila de Oliveira Gomes

Exercício 08 / parte 3 - Correção do Hamming 
"""

POSICOES_PARIDADE = [1, 2, 4, 8, 16]
TOTAL_BITS = 31
BITS_DADOS = 26


def validar_entrada(dado: str) -> bool:
    "Verifica se a entrada possui exatamente 26 números binários entre 0 e 1"
    return len(dado) == BITS_DADOS and all(c in "01" for c in dado)


def codificar_hamming(dados_26: str) -> list[int]:
    "Recebe uma string com 26 bits de dados e devolve uma lista com a palavra Hamming"
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
    print("Detalhamento do cálculo de Paridade")

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

def verificar_e_corrigir(palavra_recebida: list[int]) -> tuple[list[int], int, dict[int, int]]:
    "Calcula a síndrome, identifica o bit incorreto e efetua a correção"
    sindrome_decimal = 0
    bits_sindrome = {}
    palavra_corrigida = list(palavra_recebida)

    for p in POSICOES_PARIDADE:
        paridade_calculada = 0
        for pos in range(1, TOTAL_BITS + 1):
            if (pos & p) != 0:
                paridade_calculada ^= palavra_recebida[pos]
        bits_sindrome[p] = paridade_calculada
        if paridade_calculada != 0:
            sindrome_decimal += p

    if sindrome_decimal != 0:
        palavra_corrigida[sindrome_decimal] ^= 1

    return palavra_corrigida, sindrome_decimal, bits_sindrome


def main():
    print("  ")
    print("Codificador Hamming (31, 26)\n")
    print("  ")
    entrada = input("Digite uma sequência binária de 26 bits: ").strip()

    while not validar_entrada(entrada):
        print("Entrada inválida! Certifique-se de digitar exatamente 26 dígitos binários (0 ou 1)")
        entrada = input("Digite novamente: ").strip()

    palavra_original = codificar_hamming(entrada)
    palavra_codificada_str = palavra_para_string(palavra_original)

    print("\nResultado da Codificação")
    print(f" - Entrada original (26 bits)  : {entrada}")
    print(f" - Palavra codificada (31 bits): {palavra_codificada_str}")

    print("\nPosições dos bits de paridade:")
    for p in POSICOES_PARIDADE:
        print(f"  Posição {p:>2}: {palavra_original[p]}")

    exibir_detalhes_paridade(palavra_original)

    print("\nTeste de Detecção e Correção de Erro")
    resposta = input("Deseja simular a alteração de um bit? (s/n): ").strip().lower()

    if resposta == "s":
        pos_erro = int(input("Informe a posição do bit a ser alterado (1 a 31): ").strip())
        while pos_erro < 1 or pos_erro > 31:
            pos_erro = int(input("Posição inválida! Escolha um valor entre 1 e 31: ").strip())

        palavra_com_erro = list(palavra_original)
        palavra_com_erro[pos_erro] ^= 1
        palavra_com_erro_str = palavra_para_string(palavra_com_erro)

        print("\n--- Resultados do Teste de Erro ---")
        print(f"- Palavra Correta  : {palavra_codificada_str}")
        print(f"- Palavra com Erro : {palavra_com_erro_str}")
        print(f"- Bit alterado     : Posição {pos_erro} (invertido de {palavra_original[pos_erro]} para {palavra_com_erro[pos_erro]})")

        palavra_corrigida, sindrome, bits_s = verificar_e_corrigir(palavra_com_erro)
        palavra_corrigida_str = palavra_para_string(palavra_corrigida)

        sindrome_bin = f"{bits_s[16]}{bits_s[8]}{bits_s[4]}{bits_s[2]}{bits_s[1]}"
        print(f"\nSíndrome Calculada:")
        print(f" - Bits da síndrome (s16 s8 s4 s2 s1): {sindrome_bin}")
        print(f" - Valor decimal da síndrome         : {sindrome}")

        print(f"\nResultado da Correção:")
        print(f" - Posição identificada com erro: {sindrome}")
        print(f" - Palavra após correção        : {palavra_corrigida_str}")
        print(f" - Correção bem-sucedida?       : {'SIM' if palavra_corrigida_str == palavra_codificada_str else 'NÃO'}")
        print("=" * 70)


if __name__ == "__main__":
    main()