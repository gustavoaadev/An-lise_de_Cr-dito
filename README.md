# Análise de Carteira de Crédito Estruturado — Case de Dados.

## Objetivo
O objetivo foi realizar uma análise completa de uma carteira de crédito pessoal consignado, calculando métricas de performance, inadimplência e rentabilidade, e apresentando os resultados em uma apresentação institucional.

O case consiste em uma base de dados com cerca de 345 mil linhas contendo informações de contratos, parcelas, datas de vencimento, taxas mensais e pagamentos realizados. A partir disso, o desafio se propõe em quatro entregas principais: entender como a carteira está distribuída, calcular a taxa média ponderada, medir a inadimplência cash e, por fim, identificar onde está o problema que afeta a rentabilidade do fundo e quando ele começou.
A data-base adotada para todos os cálculos foi 31 de janeiro de 2026.

## Base de Dados
- ~345 mil linhas de Dados
- Período: 2022–2025
- Variáveis: valor, taxa, pagamentos

## Metodologia
- Tratamento de dados (datas e nulos)
- Cálculo de taxa média ponderada
- Cálculo de inadimplência (cash)
- Análise por tempo e convênio

## Principais Insights

- Inadimplência total de ~11%
- Volume total de R$ 99,3 milhões em parcelas
- Capital alocado de R$ 45,2 milhões
- Valor presente de R$ 71,5 milhões descontado a 31/01/2026.
- Taxa média ponderada de 1,84% ao mês.
- Deterioração da carteira a partir de 2025 (~35%)
- Concentração em convênios de maior risco (convênios 3 e 10)

## Estrutura
- carteira.csv (Base de dados)
- main.py (Tratamento e Análise dos Dados)
- apresentação.pptx (Apresentação construida com Lingugem Institucional)

## Como rodar
- Instale as dependências

```bash
pip install pandas numpy
```
- Com o carteira.csv na mesma pasta, execute:

```bash
python main.py
```

- Os resultados de cada etapa aparecem direto no terminal, organizados por seção.

## O que o código faz, etapa por etapa
- Etapa 1 — Distribuição da carteira:
O script agrupa os valores de parcela e de aquisição tanto por mês de aquisição quanto por convênio. Para o bônus do valor presente, foi criada uma função que calcula quantos meses cada parcela ainda tem até vencer a partir da data-base e desconta o valor usando a taxa mensal do próprio contrato.
- Etapa 2 — Taxa média ponderada:
A taxa foi ponderada pelo valor de aquisição de cada parcela, que representa o capital efetivamente alocado. Essa escolha dá uma visão mais precisa do retorno real sobre o investimento do que uma média simples entre as taxas.
- Etapa 3 — Inadimplência cash:
A fórmula usada foi 1 - (valor_pago / valor_a_receber), aplicada apenas sobre as parcelas já vencidas antes de 31/01/2026. Parcelas sem registro de pagamento foram tratadas como não pagas. O cálculo foi feito para a carteira total, por convênio e por mês de vencimento.
- Etapa 4 — Diagnóstico:
O spread estimado foi calculado como a diferença entre a taxa média e a inadimplência por convênio. Quando esse número fica negativo, significa que o custo do risco está consumindo mais do que o retorno contratado, o fundo está destruindo valor naquele grupo.

## Conclusão
Trabalhar nesse case foi uma experiência que misturou análise de dados com uma tentativa real de entender o que os números estavam dizendo sobre um negócio.  
  
A parte técnica em si foi relativamente direta: carregar e tratar os dados com pandas, construir as agregações certas, calcular valor presente parcela a parcela usando a taxa do próprio contrato. Mas o que exigiu mais atenção foi a escolha de como fazer cada cálculo e o porquê dessa escolha. Ponderar a taxa pelo valor de aquisição, por exemplo, não é a única forma de fazer, mas é a que reflete com mais honestidade o retorno sobre o capital real do fundo.  
  
O diagnóstico da Etapa 4 foi o momento mais interessante. Quando o spread estimado por convênio ficou pronto e os convênios 3 e 10 apareceram com números negativos superiores a 17 pontos percentuais, ficou claro que o problema não era ruído, era estrutural. A carteira estava sendo remunerada a uma taxa pensada para um nível de risco que não existe mais. A ruptura de agosto de 2025, onde a inadimplência triplicou em um mês, confirmou que as safras de 2024 já carregavam um perfil de crédito diferente desde a originação.  
  
No geral, o case reforçou algumas convicções que já tinha e criou outras. Dados sem contexto não dizem nada. Uma inadimplência de 11% é alta ou baixa dependendo da taxa que o fundo cobra e do perfil dos tomadores. O número sozinho não existe — ele só faz sentido em relação a outros números e a uma tese de risco. Aprender a construir esse contexto, e não apenas calcular as métricas, é o que torna uma análise de dados útil de verdade.
