# Trabalho de Linguagens e Automatos para conversão de AFND-Movimentos vazios para AFD lendo um arquivo de entrada.txt
# 1° Parte: Converter AFND (Com transiçoes vazia 'h') em AFD
# 2° Parte: Testar palavras AFD

from collections import defaultdict
from graphviz import Digraph

# ----------------------- Funções -----------------------


def verificar_existencia(conjunto, elemento):
    return elemento in conjunto  # Verfifica se o elemento já existe no conjunto#


def inserir_ordenado(conjunto, elemento):
    if elemento not in conjunto:  # Insere elemento no conjunto mantendo ordem e sem duplicados
        conjunto.append(elemento)
        conjunto.sort()


def compara_conjuntos(conjunto1, conjunto2):
    # Compara se dois conjuntos são iguais
    return sorted(conjunto1) == sorted(conjunto2)


def fecho_lambda(transicoes, estado):
    # Calcula o fecho λ (transicoes 'h') de um estado
    visitados = {estado}  # Conjunto de estadosjá alcançados
    pilha = [estado]  # Pilha para percorrer
    while pilha:
        atual = pilha.pop()
        for prox in transicoes[atual].get("h", []):  # Pega transiçoes vazias
            if prox not in visitados:
                visitados.add(prox)
                pilha.append(prox)
    return visitados


def mover(transicoes, estados, simbolo):
    # Dado um conjunto de estados, retorna os destinos pelo símbolo
    destinos = set()
    for e in estados:
        for prox in transicoes[e].get(simbolo, []):
            destinos.update(fecho_lambda(transicoes, prox))  # Inclui fecho λ
    return destinos


def ler_afnd(arquivo):
    # Le o arquivo AFND:
    # Linha 0: Estados separados por espaço
    # Linha 1: Estado inicial
    # Linha 2: Estados finais separados por espaço
    # Linha 3+: Transiçoes (estado simbolo próximo_estado)

    with open(arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    # Linha 0: estados
    estados = linhas[0].split()

    # Linha 1: inicial
    inicial = linhas[1].strip()

    # Linha 2: finais
    finais = linhas[2].split()

    # Linhas de transicoes (entre { ... })
    transicoes = defaultdict(lambda: defaultdict(list))
    for linha in linhas[3:]:
        origem, simbolo, destino = linha.split()
        transicoes[origem][simbolo].append(destino)

    return estados, inicial, finais, transicoes


def converter_afnd_para_afd(estados, inicial, finais, transicoes, alfabeto):
    # Constroi o AFD equivalente usando o metodo dos conjuntos
    inicial_fecho = fecho_lambda(transicoes, inicial)  # Fecho λ do inicial
    novos_estados = [frozenset(inicial_fecho)]  # Lista de estados a explorar
    afd_transicoes = {}
    finais_afd = set()
    visitados = set()

    while novos_estados:
        atual = novos_estados.pop()
        if atual in visitados:
            continue
        visitados.add(atual)

        nome_atual = "_".join(sorted(atual))  # Nome do estado composto
        afd_transicoes[nome_atual] = {}

        if any(e in finais for e in atual):  # Se contém estado final do AFND
            finais_afd.add(nome_atual)

        for simbolo in alfabeto:
            destino = mover(transicoes, atual, simbolo)
            if destino:
                nome_destino = "_".join(sorted(destino))
                afd_transicoes[nome_atual][simbolo] = nome_destino
                if frozenset(destino) not in visitados:
                    novos_estados.append(frozenset(destino))

    inicial_afd = "_".join(sorted(inicial_fecho))
    return list(afd_transicoes.keys()), inicial_afd, list(finais_afd), afd_transicoes


def salvar_afd(arquivo, estados, inicial, finais, transicoes):
    # Salva o AFD em arquivo txt
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(" ".join(estados) + "\n")
        f.write(inicial + "\n")
        f.write(" ".join(finais) + "\n")
        for origem in transicoes:
            for simbolo, destino in transicoes[origem].items():
                f.write(f"{origem} {simbolo} {destino}\n")


def reconhecer_palavras_AFND_AFD(arquivo_palavras, arquivo_saida, inicial_afnd, finais_afnd, transicoes_afnd, inicial_afd, finais_afd, transicoes_afd):
    # Parte 2: Testar palavra
    # Testar palavras que são reconhecidas pelo AFND antes da conversão.
    # Depois de converter as mesmas palavras devem ser reconhecidas pelo AFD equivalente.
    with open(arquivo_palavras, "r", encoding="utf-8") as f:
        palavras = [linha.strip() for linha in f if linha.strip()]

    resultados = []

    for palavra in palavras:
        # ---- Teste no AFND ----
        # Conjunto de estados possíveis, começando pelo fecho λ do inicial
        estados_possiveis = fecho_lambda(transicoes_afnd, inicial_afnd)

        for simbolo in palavra:
            novos_estados = set()
            for estado in estados_possiveis:
                for prox in transicoes_afnd[estado].get(simbolo, []):
                    novos_estados.update(fecho_lambda(transicoes_afnd, prox))
                estados_possiveis = novos_estados

        aceito_afnd = any(e in finais_afnd for e in estados_possiveis)

        # ---- Teste no AFD ----
        estado = inicial_afd
        for simbolo in palavra:
            if simbolo in transicoes_afd[estado]:
                estado = transicoes_afd[estado][simbolo]
            else:
                estado = None
                break
        aceito_afd = estado in finais_afd if estado else False

        resultados.append(
            f"{palavra} | AFND: {'aceito' if aceito_afnd else 'não aceito'} | AFD: {'aceito' if aceito_afd else 'não aceito'}")

    # Salva os resultados em arquivo
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for r in resultados:
            f.write(r + "\n")


def desenhar_afnd(estados, inicial, finais, transicoes, arquivo="afnd.png"):
    # Desenha o AFND em PNG usando Graphviz
    dot = Digraph(comment="AFND", format="png")
    dot.attr(rankdir="LR")  # Estilo do jflap: esquerda -> direita

    # Adiciona estados
    for estado in estados:
        if estado == inicial:
            dot.node(estado, shape="circle", style="bold", color="blue")
        elif estado in finais:
            dot.node(estado, shape="doublecircle", color="red")
        else:
            dot.node(estado, shape="circle")

    # Adiciona transicoes
    for origem in transicoes:
        for simbolo, destinos in transicoes[origem].items():
            for destino in destinos:
                label = "λ" if simbolo == "h" else simbolo
                dot.edge(origem, destino, label=label)
    dot.render(arquivo, cleanup=True)


def desenhar_afd(estados, inicial, finais, transicoes, arquivo="afd.png"):
    # Desenha o AFND em PNG usando Graphviz
    dot = Digraph(comment="AFD", format="png")
    dot.attr(rankdir="LR")

    # Adiciona estados
    for estado in estados:
        if estado == inicial:
            dot.node(estado, shape="circle", style="bold", color="blue")
        elif estado in finais:
            dot.node(estado, shape="doublecircle", color="red")
        else:
            dot.node(estado, shape="circle")

    # Adiciona transicoes
    for origem in transicoes:
        for simbolo, destino in transicoes[origem].items():
            dot.edge(origem, destino, label=simbolo)

    dot.render(arquivo, cleanup=True)

# ---------------------------- Main ----------------------------


if __name__ == "__main__":
    # Parte 1: Converter AFND para AFD

    # Lê AFND do arquivo
    estados, inicial, finais, transicoes = ler_afnd("entrada_afnd.txt")
    alfabeto = ["0", "1"]

    # Converte AFND para AFD
    estados_afd, inicial_afd, finais_afd, transicoes_afd = converter_afnd_para_afd(
        estados, inicial, finais, transicoes, alfabeto)

    # Salva AFD em arquivo txt
    salvar_afd("saida_afd.txt", estados_afd,
               inicial_afd, finais_afd, transicoes_afd)

    # Cria a imagem PNG do dois autômatos
    desenhar_afnd(estados, inicial, finais, transicoes, "afnd")
    desenhar_afd(estados_afd, inicial_afd, finais_afd, transicoes_afd, "afd")

    # Parte 2: Reconhecer palavras

    # Testa as palavras e salva resultado
    reconhecer_palavras_AFND_AFD("palavras.txt", "resultado.txt",
                                 inicial, finais, transicoes, inicial_afd, finais_afd, transicoes_afd)

    print("Conversão concluída. Arquivos gerados: saida_afd.txt e resultado.txt")
