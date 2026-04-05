Linguagens Formais e Autômatos – Trabalho 1B

Parte 1: Converter um AFND (com movimentos vazios) em um AFD.
Alfabeto: {0,1}

Entrada: um arquivo com a tabela do AFND.

Formato do arquivo de entrada:

Linha 0: a sequência de estados separados por espaço. Exemplo: A B C D E F

Linha 1: estado inicial

Linha 2: estados finais separados por espaço (se houver mais de um estado final)

Linha 3 em diante: estado atual, espaço, caractere lido, espaço, próximo estado

Observação: representar a transição vazia por h.

Saída: um arquivo com a tabela do AFD.
Formato do arquivo de saída: o mesmo do arquivo de entrada.

Usar o JFLAP e desenhar os dois autômatos: o de entrada e o de saída.

Para saber se a conversão funcionou corretamente, será implementada a parte 2 a fim de testar palavras que são reconhecidas pelo AFND antes da conversão. Depois de converter, as mesmas palavras devem ser reconhecidas pelo AFD equivalente.

Parte 2: Dado um conjunto de palavras, determinar se a palavra é reconhecida ou não pelo AFD equivalente gerado na parte 1.
Alfabeto: {0,1}

Entrada: um arquivo com as palavras a serem reconhecidas.

Uma palavra por linha.

Saída: um arquivo com todas as palavras e, na frente de cada palavra, “aceito” ou “não aceito” (reconhecido ou não reconhecido).

Uma palavra por linha.

Exemplo:

Linha 1: qwefr aceito

Linha 2: abder não aceito

Linguagem de programação: Python
