import streamlit as st

# ==============================
# Page config
# ==============================
st.set_page_config(page_title="CDS-A (Academic)", layout="centered")

st.title("Circular Development Score (CDS-A)")
st.caption("Academic mode — exact published methodology (JS, OR-logic SS, R-principles)")

st.markdown("---")

# ==============================
# Global weights (from paper)
# ==============================
W_JS = 0.53
W_SS = 0.47

W_SF = 0.47
W_NI = 0.53

NB_INDEX  = 1.00
OB_INDEX  = 0.61
NWB_INDEX = 0.43

R_WEIGHTS = {
    "Reduce": 0.43,
    "Renew":  0.28,
    "Replace":0.29
}

# ==============================
# Core functions (paper-faithful)
# ==============================
def need_importance(loi_score, loi_max=5):
    return loi_score / loi_max

def solution_fitness_no_build():
    return 1.0

def solution_fitness_build(POR, PDR, FGR):
    return (POR + PDR + FGR) / 3

def justification_score(SF, NI):
    return W_SF * SF + W_NI * NI

def sustainability_score(solution_type,
                          OB_score=None,
                          Reduce=None, Renew=None, Replace=None):
    if solution_type == "No-Build":
        return NB_INDEX
    elif solution_type == "Old-Build":
        if OB_score is None:
            raise ValueError("OB_score required for Old-Build")
        return OB_INDEX * OB_score
    elif solution_type == "New-Build":
        if None in (Reduce, Renew, Replace):
            raise ValueError("All R-principles required for New-Build")
        nwb = (
            R_WEIGHTS["Reduce"]  * Reduce +
            R_WEIGHTS["Renew"]   * Renew +
            R_WEIGHTS["Replace"]* Replace
        )
        return NWB_INDEX * nwb
    else:
        raise ValueError("Invalid solution type")

def cds_score(JS, SS):
    return W_JS * JS + W_SS * SS

def interpret(score):
    if score >= 0.80:
        return "🟢 Highly circular – proceed"
    elif score >= 0.65:
        return "🟢 Optimizable – strong circular potential"
    elif score >= 0.50:
        return "🟠 Vulnerable – redesign recommended"
    else:
        return "🔴 Linear-prone – reconsider build decision"

# ==============================
# Sidebar: Published case studies
# ==============================
st.sidebar.header("Published Case Studies")
case = st.sidebar.selectbox(
    "Load a case (optional)",
    ["— None —", "CS1: No-Build", "CS2: Old-Build", "CS3: New-Build", "CS3: New-Build (Optimized)"]
)

# Defaults
solution_type = "No-Build"
loi = 3
POR = PDR = FGR = 1.0
OB_score = 1.0
Reduce = Renew = Replace = 0.0

# Apply paper cases
if case == "CS1: No-Build":
    solution_type = "No-Build"
    loi = 3
elif case == "CS2: Old-Build":
    solution_type = "Old-Build"
    loi = 3
    POR, PDR, FGR = 0.90, 1.00, 1.10
    OB_score = 1.0
elif case == "CS3: New-Build":
    solution_type = "New-Build"
    loi = 3
    Reduce, Renew, Replace = 0.15, 0.25, 0.20
elif case == "CS3: New-Build (Optimized)":
    solution_type = "New-Build"
    loi = 3
    Reduce, Renew, Replace = 0.35, 0.45, 0.40

# ==============================
# UI: Inputs
# ==============================
st.subheader("1) Decision context")
solution_type = st.selectbox("Solution type", ["No-Build", "Old-Build", "New-Build"], index=["No-Build","Old-Build","New-Build"].index(solution_type))
loi = st.slider("Level of Importance (LoI)", 1, 5, int(loi))

st.subheader("2) Justification inputs")
if solution_type == "No-Build":
    SF = solution_fitness_no_build()
    st.info("No-Build selected → Solution Fitness (SF) = 1.00")
else:
    POR = st.slider("Past Occupancy Rate (POR)", 0.0, 1.2, float(POR), 0.05)
    PDR = st.slider("Present Demand Ratio (PDR)", 0.0, 1.2, float(PDR), 0.05)
    FGR = st.slider("Future Growth Ratio (FGR)", 0.0, 1.2, float(FGR), 0.05)
    SF = solution_fitness_build(POR, PDR, FGR)

NI = need_importance(loi)
JS = justification_score(SF, NI)

st.subheader("3) Sustainability inputs (OR-logic)")
if solution_type == "Old-Build":
    OB_score = st.slider("Old-Build sustainability score (normalized)", 0.0, 1.0, float(OB_score), 0.05)
elif solution_type == "New-Build":
    Reduce  = st.slider("Reduce (normalized)",  0.0, 1.0, float(Reduce),  0.05)
    Renew   = st.slider("Renew (normalized)",   0.0, 1.0, float(Renew),   0.05)
    Replace = st.slider("Replace (normalized)", 0.0, 1.0, float(Replace), 0.05)

SS = sustainability_score(
    solution_type,
    OB_score=OB_score if solution_type=="Old-Build" else None,
    Reduce=Reduce if solution_type=="New-Build" else None,
    Renew=Renew if solution_type=="New-Build" else None,
    Replace=Replace if solution_type=="New-Build" else None
)

CDS = cds_score(JS, SS)

# ==============================
# Results
# ==============================
st.markdown("---")
st.subheader("Result (Academic CDS)")

st.metric("Justification Score (JS)", f"{JS:.3f}")
st.metric("Sustainability Score (SS)", f"{SS:.3f}")
st.metric("Final CDS", f"{CDS:.3f}")

st.success(interpret(CDS))

st.caption("CDS-A reproduces the published methodology (JS, OR-logic SS, R-principle weights). Not a certification.")
