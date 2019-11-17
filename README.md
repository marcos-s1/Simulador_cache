# cache
Cache memory simulator project developed for computer architecture and organization 2019.4 - Federal University of Pará - Telecommunications Engineering

O projeto usa traços de memoria como entradas e interage com o usuario acerca das configuraçes da memoria cache a ser utilizada

1- Escolha  o tamanho da memoria cache:

2- escolha o tipo de mapeamento

    1-Direto 2-Associativo 3-Associativo Conjunto
    
3-Escolha a politica de escrita

    1-Write throught 2-Write back
    

Caso a política de escrita seja do tipo associativa ou associativa conjunto sera necessário fornecer uma política de substituição e,
alem disso, caso a politica seja associativo conjunto, sera necessario fornecer o numero de conjuntos.

3-Escolha a politica de substituição

  1-RANDOM  2-FIFO

4-Escolha a quantidade de conjuntos:

A saida exibira as informaçes de acordo com a configuração escolhida pelo usuario

Exemplo:

    Mapeamento Direto
  
    Politica de escrita:1
  
    Total de escritas na memoria principal: 596
  
    Total de memórias acessadas: 596
  
    Total HIT: 451
  
    Total MISS: 145
  
    Taxa de Cache HIT: 75.67%
  
    Tempo de execução: 0.0 dias, 0.0 horas, 0.0 minutos e 0.084 segundos.
  
  
