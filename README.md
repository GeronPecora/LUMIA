# 🎓 Lumia — Educadora Financeira com IA
 
Agente conversacional de educação financeira desenvolvido com Python, Streamlit e LLM local via Ollama. A Lumia usa dados reais do cliente (perfil, transações e histórico de atendimento) para explicar conceitos financeiros de forma personalizada e didática.
 
---
 
## 💡 O que eu aprendi com este projeto
 
### 1. Como montar um agente de IA do zero
 
Um agente de IA vai muito além de "chamar uma API". Aprendi que um agente bem construído precisa de:
 
- **Persona definida**: nome, tom de voz, comportamentos esperados e limitações claras
- **System prompt estruturado**: com regras do que fazer, o que não fazer e edge cases
- **Contexto injetado**: dados do cliente passados diretamente no prompt para personalizar as respostas
- **Histórico de conversa**: o modelo não tem memória entre chamadas, então é preciso enviar todo o histórico a cada requisição
### 2. Engenharia de Prompt
 
Esta foi uma das maiores lições do projeto. Um prompt mal escrito gera respostas imprevisíveis, especialmente em modelos menores (como o Qwen3 via Ollama). Aprendi que:
 
- **Regras vagas geram comportamentos vagos**: "responda de forma simples" não é suficiente. É preciso dar exemplos concretos do que é certo e errado
- **Proibições precisam de exemplos negativos**: para evitar markdown vazando na resposta, não basta dizer "não use markdown" — é preciso mostrar `ERRADO: **texto**` e `CERTO: texto`
- **Modelos locais exigem prompts mais rígidos**: GPT e Claude toleram ambiguidades melhor do que modelos menores. Com Qwen3, cada instrução precisa ser explícita
- **Edge cases devem estar no system prompt**: colocar os casos limite só nos exemplos não é suficiente; os mais críticos precisam estar nas regras principais
### 3. Estrutura de dados para agentes
 
Aprendi a diferença entre injetar os dados **diretamente no prompt** (mais simples, bom para protótipos) versus carregar **dinamicamente via código** (mais escalável para produção). Neste projeto usei a abordagem direta com Python + pandas:
 
```python
perfil     = json.load(open('./data/perfil_investidor.json', encoding='utf-8'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico  = pd.read_csv('./data/historico_atendimento.csv')
produtos   = json.load(open('./data/produtos_financeiros.json', encoding='utf-8'))
```
 
### 4. Segurança e Anti-Alucinação
 
Um agente educativo que inventa informações é pior do que um que admite não saber. Implementei estratégias para reduzir alucinações:
 
- O agente só usa dados fornecidos no contexto, nunca extrapola
- Instruções explícitas para admitir incerteza: *"Não tenho essa informação, mas posso explicar como funciona..."*
- Distinção clara entre fatos e exemplos ilustrativos
- Bloqueio de recomendações diretas de produtos ou instituições financeiras
### 5. Diferenças entre LLMs
 
Testei o mesmo system prompt em ChatGPT, Claude e Qwen3 (via Ollama) e observei comportamentos distintos:
 
| Modelo | Comportamento |
|--------|--------------|
| Claude | Seguiu as regras com precisão, respostas bem calibradas |
| ChatGPT | Performou bem, mas falhou em um edge case de escopo |
| Qwen3 (Ollama) | Mais literal, precisa de instruções mais rígidas e exemplos concretos |
 
---
 
## 🗂️ Estrutura do Projeto
 
```
lumia/
├── app.py                        # Aplicação principal (Streamlit + Ollama)
├── data/
│   ├── perfil_investidor.json    # Perfil e metas do cliente
│   ├── produtos_financeiros.json # Produtos disponíveis para ensino
│   ├── transacoes.csv            # Histórico de transações do cliente
│   └── historico_atendimento.csv # Histórico de atendimentos anteriores
└── docs/
    ├── 01-agent-documentation.md # Documentação do agente (persona, arquitetura)
    ├── 02-knowledge-base.md      # Base de conhecimento e estratégia de dados
    ├── 03-prompts.md             # System prompt, exemplos e edge cases
    └── 04-metrics.md             # Métricas de avaliação e resultados de testes
```
 
---
 
## ⚙️ Como rodar o projeto
 
### Pré-requisitos
 
- Python 3.10+
- [Ollama](https://ollama.com/) instalado localmente
- Modelo Qwen3 baixado: `ollama pull qwen3`
### Instalação
 
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/lumia-agente-financeiro
cd lumia-agente-financeiro
 
# Instale as dependências
pip install streamlit ollama pandas
 
# Rode a aplicação
streamlit run app.py
```
 
---
 
## 🧠 Arquitetura
 
```
Usuário → Streamlit (interface) → System Prompt + Contexto + Histórico → Ollama (Qwen3) → Resposta
```
 
Os dados do cliente são carregados na inicialização e injetados diretamente no system prompt. A cada nova mensagem, o histórico completo da conversa é enviado junto ao modelo, garantindo continuidade.
 
---
 
## 📏 Métricas de Avaliação
 
| Métrica | Descrição |
|---------|-----------|
| Assertividade | A resposta foi direta e dentro do escopo? |
| Segurança | O agente evitou inventar informações ou recomendar produtos? |
| Coerência | A linguagem foi adequada ao perfil do cliente? |
 
---
 
## ⚠️ Limitações
 
- Não faz recomendação de investimentos
- Não acessa dados bancários reais
- Não substitui um profissional certificado (CFP, planejador financeiro)
- Os dados são mockados — em produção, deveriam ser carregados dinamicamente de uma fonte confiável
---
 
## 🛠️ Possíveis melhorias futuras
 
- Carregamento dinâmico de dados via banco de dados ou API
- Suporte a múltiplos perfis de usuário (iniciante, moderado, avançado)
- Avaliação automática das respostas com LLM como juiz
- Memória persistente entre sessões
- Deploy em nuvem com autenticação
---
 
## 📚 Tecnologias utilizadas
 
- [Streamlit](https://streamlit.io/) — interface web
- [Ollama](https://ollama.com/) — execução local do LLM
- [Qwen3](https://ollama.com/library/qwen3) — modelo de linguagem
- [pandas](https://pandas.pydata.org/) — manipulação dos dados CSV
- Python 3.10+