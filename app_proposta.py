import streamlit as st
from datetime import date
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Simulador de Proposta", layout="centered")
st.title("🧾 Simulador de Proposta Comercial")

with st.form("proposta"):
    cliente = st.text_input("Nome do cliente")
    escopo = st.text_area("Escopo do projeto")
    valor_hora = st.number_input("Valor por hora (R$)", step=10.0, min_value=0.0)
    horas = st.number_input("Horas previstas", step=1, min_value=0)
    imposto_percentual = st.slider("Percentual estimado de impostos (%)", 0, 30, 15)
    submitted = st.form_submit_button("Gerar proposta")

if submitted:
    try:
        subtotal = valor_hora * horas
        impostos = subtotal * (imposto_percentual / 100)
        valor_total = subtotal - impostos

        doc = Document("modelo_proposta.docx")

        for p in doc.paragraphs:
            if p.text:
                p.text = p.text.replace("{{CLIENTE}}", cliente)
                p.text = p.text.replace("{{DATA}}", str(date.today()))
                p.text = p.text.replace("{{ESCOPO}}", escopo)
                p.text = p.text.replace("{{VALOR_HORA}}", f"{valor_hora:,.2f}")
                p.text = p.text.replace("{{HORAS}}", str(horas))
                p.text = p.text.replace("{{SUBTOTAL}}", f"{subtotal:,.2f}")
                p.text = p.text.replace("{{IMPOSTOS}}", f"{impostos:,.2f}")
                p.text = p.text.replace("{{VALOR_TOTAL}}", f"{valor_total:,.2f}")

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success("✅ Proposta gerada com sucesso!")
        st.download_button(
            label="📥 Baixar proposta",
            data=buffer.getvalue(),
            file_name=f"Proposta_{cliente}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Erro: {e}")
