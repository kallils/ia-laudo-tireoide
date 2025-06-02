
import streamlit as st

st.set_page_config(page_title="IA para Laudo de Tireoide com TI-RADS", layout="centered")

st.title("🧠 IA para Laudo de Tireoide com TI-RADS")
st.markdown("Preencha as características do nódulo tireoidiano abaixo. O laudo será gerado automaticamente com base nos critérios ACR TI-RADS.")

# Composição
st.header("Composição")
composicao = st.radio("Escolha uma opção:", [
    "Cístico ou quase totalmente cístico (0 pts)",
    "Espongiforme (0 pts)",
    "Misto (cístico e sólido) (1 pt)",
    "Sólido ou quase totalmente sólido (2 pts)"
])
comp_pontos = {"Cístico ou quase totalmente cístico (0 pts)": 0,
               "Espongiforme (0 pts)": 0,
               "Misto (cístico e sólido) (1 pt)": 1,
               "Sólido ou quase totalmente sólido (2 pts)": 2}[composicao]

# Ecogenicidade
st.header("Ecogenicidade")
eco = st.radio("Escolha uma opção:", [
    "Anecoico (0 pts)",
    "Hipoecogênico ou Isoecogênico (1 pt)",
    "Hipoecogênico (2 pts)",
    "Muito hipoecogênico (3 pts)"
])
eco_pontos = {"Anecoico (0 pts)": 0,
              "Hipoecogênico ou Isoecogênico (1 pt)": 1,
              "Hipoecogênico (2 pts)": 2,
              "Muito hipoecogênico (3 pts)": 3}[eco]

# Forma
st.header("Forma")
forma = st.radio("Escolha uma opção:", [
    "Mais larga que alta (0 pts)",
    "Mais alta que larga (3 pts)"
])
forma_pontos = {"Mais larga que alta (0 pts)": 0,
                "Mais alta que larga (3 pts)": 3}[forma]

# Margens
st.header("Margens")
margem = st.radio("Escolha uma opção:", [
    "Lisa (0 pts)",
    "Mal definida (0 pts)",
    "Lobulada ou irregular (2 pts)",
    "Com extensão extra-tireoidiana (3 pts)"
])
margem_pontos = {"Lisa (0 pts)": 0,
                 "Mal definida (0 pts)": 0,
                 "Lobulada ou irregular (2 pts)": 2,
                 "Com extensão extra-tireoidiana (3 pts)": 3}[margem]

# Focos ecogênicos
st.header("Focos Ecogênicos")
focos = st.multiselect("Selecione os focos presentes:", [
    "Nenhum ou artefatos comet tail (0 pts)",
    "Macrocalcificações (1 pt)",
    "Calcificações periféricas (2 pts)",
    "Microcalcificações (3 pts)"
])
foco_pontos = 0
if "Macrocalcificações (1 pt)" in focos: foco_pontos += 1
if "Calcificações periféricas (2 pts)" in focos: foco_pontos += 2
if "Microcalcificações (3 pts)" in focos: foco_pontos += 3

# Total de pontos
total = comp_pontos + eco_pontos + forma_pontos + margem_pontos + foco_pontos

def classificar_tirads(pontos):
    if pontos <= 1: return "TI-RADS 1 ou 2 – Benigno"
    elif pontos == 2: return "TI-RADS 3 – Levemente suspeito"
    elif 3 <= pontos <= 4: return "TI-RADS 4 – Moderadamente suspeito"
    else: return "TI-RADS 5 – Altamente suspeito"

if st.button("Gerar Laudo"):
    tirads = classificar_tirads(total)
    laudo = f"""
**ULTRASSONOGRAFIA DA TIREOIDE**

**Indicação:** Avaliação ultrassonográfica da glândula tireoide.

**Análise:**
Nódulo caracterizado por:
- Composição: {composicao}
- Ecogenicidade: {eco}
- Forma: {forma}
- Margens: {margem}
- Focos ecogênicos: {', '.join(focos) if focos else 'Nenhum'}

**Opinião:**
Classificação ACR {tirads} (Total de {total} pontos).
"""
    st.markdown("---")
    st.markdown("### 📝 Laudo Gerado")
    st.text_area("Laudo completo", laudo, height=350)
