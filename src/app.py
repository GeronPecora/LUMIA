import json
import pandas as pd
import streamlit as st
from ollama import chat

# ── Configuração ──────────────────────────────────────────────
MODELO = "qwen3:latest"

# ── Carregar dados ────────────────────────────────────────────
perfil     = json.load(open('./data/perfil_investidor.json', encoding='utf-8'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico  = pd.read_csv('./data/historico_atendimento.csv')
produtos   = json.load(open('./data/produtos_financeiros.json', encoding='utf-8'))

# ── Contexto do cliente ───────────────────────────────────────
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ── System Prompt ─────────────────────────────────────────────
SYSTEM_PROMPT = f"""Você é a Lumia, uma educadora financeira amigável e didática.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

CONTEXTO DO CLIENTE:
{contexto}

REGRAS:
- NUNCA recomende investimentos específicos, apenas explique como funcionam;
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais.
  Quando ocorrer, responda lembrando o seu papel de educadora financeira;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para uma amiga;
- Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
"""

# ── Chamada à Ollama com histórico ────────────────────────────
def perguntar(historico_chat: list) -> str:
    try:
        response = chat(
            model=MODELO,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historico_chat
        )
        return response.message.content
    except Exception as e:
        return f"⚠️ Ocorreu um erro inesperado: {str(e)}"

# ── Interface Streamlit ───────────────────────────────────────
st.title("🎓 Lumia, sua Educadora Financeira")

# Inicializa histórico na sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
    st.chat_message("assistant").write(
        f"Olá, {perfil['nome']}! 👋 Sou a **Lumia**, sua educadora financeira. "
        "Pode me perguntar sobre orçamento, dívidas, investimentos ou qualquer dúvida financeira!"
    )

# Exibe histórico
for msg in st.session_state.mensagens:
    st.chat_message(msg["role"]).write(msg["content"])

# Nova mensagem
if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    with st.spinner("Lumia está pensando..."):
        resposta = perguntar(st.session_state.mensagens)

    st.chat_message("assistant").write(resposta)
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})