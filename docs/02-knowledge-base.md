# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve a Lumia? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores, ou seja, dar continuidade ao atendimento de forma mais eficiente. |
| `perfil_investidor.json` | JSON | Personalizar as explicações sobre as dúvidas e necessidades de aprendizado do cliente. |
| `produtos_financeiros.json` | JSON | Conhecer os produtos disponíveis para que eles possam ser ensinados ao cliente. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar essas informações de forma didática. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

O produto Fundo Imobiliário (FII) substituiu o Fundo Multimercado, pois pessoalmente me sinto mais confiante em usar apenas produtos financeiros que eu conheço. Assim, poderei validar as respostas da Lumia de forma mais assertiva.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas abordagens possíveis: injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregá-los via código, como demonstrado no exemplo abaixo:

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos “injetar” os dados diretamente no prompt, garantindo que o agente tenha o melhor contexto possível. No entanto, em soluções mais robustas, o ideal é que essas informações sejam carregadas de forma dinâmica, proporcionando maior flexibilidade e escalabilidade.

```text
DADOS DO CLIENTE E PERFIL (data/perfil_investidor.json):
{
  "nome": "Geron Pécora",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "gastos_mensais": 3000.00,
  "valor_disponivel_para_investir": 2000.00,
  "dividas": 0.00,
  "tem_reserva_suficiente": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}

TRANSACOES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida
2025-10-28,Padaria,alimentacao,35.00,saida
2025-11-01,Salário,receita,5000.00,entrada
2025-11-02,Aluguel,moradia,1200.00,saida
2025-11-03,Supermercado,alimentacao,420.00,saida
2025-11-05,Spotify,lazer,34.90,saida
2025-11-06,Farmácia,saude,65.00,saida
2025-11-08,Restaurante,alimentacao,95.00,saida
2025-11-10,Uber,transporte,60.00,saida
2025-11-12,Conta de Luz,moradia,175.00,saida
2025-11-15,Internet,moradia,120.00,saida
2025-11-18,Academia,saude,99.00,saida
2025-11-20,Combustível,transporte,230.00,saida
2025-11-22,Cinema,lazer,40.00,saida
2025-11-25,Padaria,alimentacao,28.00,saida
2025-12-01,Salário,receita,5000.00,entrada
2025-12-02,Aluguel,moradia,1200.00,saida
2025-12-03,Supermercado,alimentacao,480.00,saida
2025-12-05,Netflix,lazer,55.90,saida
2025-12-06,Farmácia,saude,72.00,saida
2025-12-08,Restaurante,alimentacao,130.00,saida
2025-12-10,Uber,transporte,50.00,saida
2025-12-12,Conta de Luz,moradia,190.00,saida
2025-12-15,Internet,moradia,120.00,saida
2025-12-18,Academia,saude,99.00,saida
2025-12-20,Combustível,transporte,260.00,saida
2025-12-22,Presente,lazer,150.00,saida
2025-12-25,Ceia de Natal,alimentacao,300.00,saida
2025-12-28,Padaria,alimentacao,32.00,saida
2026-01-01,Salário,receita,5000.00,entrada
2026-01-02,Aluguel,moradia,1200.00,saida
2026-01-03,Supermercado,alimentacao,410.00,saida
2026-01-05,Spotify,lazer,34.90,saida
2026-01-07,Farmácia,saude,80.00,saida
2026-01-10,Restaurante,alimentacao,110.00,saida
2026-01-12,Uber,transporte,55.00,saida
2026-01-15,Conta de Luz,moradia,185.00,saida
2026-01-18,Academia,saude,99.00,saida
2026-01-20,Combustível,transporte,240.00,saida

HISTORICO DE ATENDIMENTO DO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim
2025-10-28,chat,CDB,Cliente comparou CDB com poupança,sim
2025-11-02,telefone,Problema no app,Erro ao fazer login foi reportado,sim
2025-11-05,chat,Tesouro Selic,Cliente quis saber sobre liquidez diária,sim
2025-11-10,email,Metas financeiras,Cliente revisou planejamento mensal,sim
2025-11-15,chat,Investimentos,Cliente pediu orientação geral sobre investimentos,sim
2025-11-20,telefone,Problema no app,Aplicativo apresentou lentidão,sim
2025-11-25,email,Atualização cadastral,Cliente alterou endereço,sim
2025-12-01,chat,CDB,Cliente perguntou sobre rendimento líquido,sim
2025-12-05,chat,Tesouro Selic,Cliente questionou segurança do investimento,sim
2025-12-10,email,Metas financeiras,Cliente ajustou meta de economia,sim
2025-12-15,telefone,Problema no app,Erro ao acessar saldo foi resolvido,sim
2025-12-20,chat,Investimentos,Cliente quis entender diversificação,sim
2025-12-22,email,Atualização cadastral,Cliente atualizou dados pessoais,sim
2025-12-28,chat,CDB,Cliente perguntou sobre prazo mínimo,sim
2026-01-03,telefone,Problema no app,Erro intermitente no sistema,sim

PRODUTOS DISPONIVEIS PARA ENSINO (data/produtos_financeiros.json):
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Imobiliário (FII)",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "Dividend Yield (DY) costuma ficar entre 6% a 12% ao ano",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil moderado que busca diversificação e renda recorrente mensal"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  },
  {
    "nome": "Tesouro IPCA+",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "IPCA + taxa prefixada",
    "aporte_minimo": 30.00,
    "indicado_para": "Proteção contra inflação no longo prazo"
  },
  {
    "nome": "CDB Prefixado",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "Taxa fixa anual definida no momento da aplicação",
    "aporte_minimo": 500.00,
    "indicado_para": "Quem acredita na queda da taxa de juros"
  },
  {
    "nome": "Tesouro Prefixado",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "Taxa fixa definida na compra",
    "aporte_minimo": 30.00,
    "indicado_para": "Planejamento financeiro com retorno previsível"
  },
  {
    "nome": "Fundos Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "Variável conforme estratégia do fundo",
    "aporte_minimo": 100.00,
    "indicado_para": "Investidores que buscam diversificação com gestão ativa"
  },
  {
    "nome": "Ações",
    "categoria": "variavel",
    "risco": "alto",
    "rentabilidade": "Variável conforme mercado",
    "aporte_minimo": 50.00,
    "indicado_para": "Investidores com perfil arrojado e foco no longo prazo"
  },
  {
    "nome": "ETFs",
    "categoria": "variavel",
    "risco": "medio",
    "rentabilidade": "Acompanha índices de mercado",
    "aporte_minimo": 50.00,
    "indicado_para": "Quem busca diversificação com baixo custo"
  },
  {
    "nome": "Debêntures",
    "categoria": "renda_fixa",
    "risco": "medio",
    "rentabilidade": "Pode ser prefixada, pós-fixada ou híbrida",
    "aporte_minimo": 1000.00,
    "indicado_para": "Investidores que aceitam maior risco em troca de maior retorno"
  }
]
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto apresentado abaixo é baseado nos dados originais da base de conhecimento, porém foi sintetizado para manter apenas as informações mais relevantes, otimizando o consumo de tokens. Ainda assim, é importante destacar que, mais do que economizar tokens, o essencial é garantir que todas as informações relevantes estejam disponíveis no contexto.

```
DADOS DO CLIENTE:
- Nome: Geron Pécora
- Perfil: Moderado
- Objetivo: Construir reserva de emergência
- Reserva atual: R$ 10.000 (meta: R$ 15.000)

RESUMO DE GASTOS:
- Moradia: R$ 1.442,50
- Alimentação: R$ 652,50
- Transporte: R$ 297,50
- Saúde: R$ 175,50
- Lazer: R$ 92,68
- Total de saídas: R$ 2.660,68

PRODUTOS DISPONÍVEIS PARA EXPLICAR:
- Tesouro Selic (risco baixo)
- CDB Liquidez Diária (risco baixo)
- LCI/LCA (risco baixo)
- Fundo Imobiliário - FII (risco médio)
- Fundo de Ações (risco alto)
- Tesouro IPCA+ (risco baixo)
- CDB Prefixado (risco baixo)
- Tesouro Prefixado (risco baixo)
- Fundos Multimercado (risco médio)
- Ações (risco alto)
- ETFs (risco médio)
- Debêntures (risco médio)
```