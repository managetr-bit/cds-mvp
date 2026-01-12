import streamlit as st

st.set_page_config(page_title="Circular Development Score (CDS) – MVP", layout="centered")

# ---- Title ----
st.title("Circular Development Score (CDS)")
st.caption("Pre-feasibility circularity decision support | MVP v1")
st.markdown("---")

# ---- Weights ----
WEIGHTS = {
    "Justification (Refuse)": 0.33,
    "No-Build / Rethink": 0.20,
    "Reuse / Repurpose": 0.15,
    "Reduce": 0.15,
    "Renew": 0.10,
    "Replace": 0.07,
}

# ---- Archetypes ----
ARCHETYPES = {
    "No-Build Archetype": {
        "Justification (Refuse)": 85,
        "No-Build / Rethink": 95,
        "Reuse / Repurpose": 90,
        "Reduce": 85,
        "Renew": 80,
        "Replace": 70,
    },
    "Reuse Archetype": {
        "Justification (Refuse)": 75,
        "No-Build / Rethink": 55,
        "Reuse / Repurpose": 85,
        "Reduce": 70,
        "Renew": 65,
        "Replace": 60,
    },
    "New-Build Archetype": {
        "Justification (Refuse)": 60,
        "No-Build / Rethink": 10,
        "Reuse / Repurpose": 15,
        "Reduce": 45,
        "Renew": 55,
        "Replace": 50,
    },
    "Best Case": {
        "Justification (Refuse)": 100,
        "No-Build / Rethink": 100,
        "Reuse / Repurpose": 95,
        "Reduce": 95,
        "Renew": 90,
        "Replace": 80,
    },
    "Worst Case": {
        "Justification (Refuse)": 30,
        "No-Build / Rethink": 0,
        "Reuse / Repurpose": 5,
        "Reduce": 20,
        "Renew": 15,
        "Replace": 10,
    },
}

# ---- Session state ----
if "scores" not in st.session_state:
    st.session_state.scores = {k: 50 for k in WEIGHTS.keys()}

# ---- Archetype buttons ----
st.subheader("Quick scenarios")
cols = st.columns(5)
for i, name in enumerate(ARCHETYPES.keys()):
    if cols[i].button(name):
        st.session_state.scores = ARCHETYPES[name].copy()

st.markdown("---")

# ---- Sliders ----
st.subheader("Input scores (0–100)")
for dim in WEIGHTS.keys():
    st.session_state.scores[dim] = st.slider(
        dim,
        0,
        100,
        int(st.session_state.scores[dim]),
        key=dim
    )

# ---- CDS Calculation ----
cds = sum(st.session_state.scores[d] * WEIGHTS[d] for d in WEIGHTS)

# ---- Interpretation ----
def interpret(score):
    if score >= 80:
        return "🟢 Highly circular – proceed", "#1b5e20"
    elif score >= 65:
        return "🟢 Optimizable – strong circular potential", "#2e7d32"
    elif score >= 50:
        return "🟠 Vulnerable – redesign recommended", "#f9a825"
    else:
        return "🔴 Linear-prone – reconsider build decision", "#c62828"

message, color = interpret(cds)

st.markdown("---")
st.subheader("Result")

st.markdown(
    f"""
    <div style="padding:20px;border-radius:10px;border:2px solid {color};text-align:center;">
        <h1 style="color:{color};">CDS = {cds:.1f}</h1>
        <h3>{message}</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Disclaimer: CDS MVP v1 – decision support tool. Not a certification.")
