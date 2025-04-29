import streamlit as st
import re
import random
import string

st.set_page_config(page_title="Password Strength Meter", page_icon="🔒", layout="centered")

# --- Professional Dark Blue Theme CSS with improved input field ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #232946 0%, #121629 100%) !important;
    }
    # .glass-card {
    #     background: rgba(36, 41, 61, 0.92);
    #     box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.18);
    #     backdrop-filter: blur(8px);
    #     -webkit-backdrop-filter: blur(8px);
    #     border-radius: 18px;
    #     border: 1.5px solid rgba(200, 220, 255, 0.08);
    #     padding: 2.2rem 2rem 2rem 2rem;
    #     max-width: 410px;
    #     margin: 2rem auto;
    # }
    .strength-bar-outer {
        width: 100%;
        background: #1a1f36;
        border-radius: 8px;
        height: 16px;
        margin-bottom: 10px;
        margin-top: 10px;
        overflow: hidden;
        border: 1px solid #232946;
    }
    .strength-bar-inner {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s;
        background: linear-gradient(90deg, #6c63ff, #00bfae 80%);
        box-shadow: 0 0 8px #00bfae55;
    }
    .feedback-list {
        margin: 0.5rem 0 1rem 0;
        padding-left: 1.2rem;
        font-size: 1.01rem;
        color: #b8c1ec;
    }
    .gen-btn, .copy-btn {
        background: linear-gradient(90deg, #6c63ff 0%, #00bfae 100%);
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        cursor: pointer;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: background 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 8px #6c63ff33;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .gen-btn:hover, .copy-btn:hover {
        background: linear-gradient(90deg, #00bfae 0%, #6c63ff 100%);
        box-shadow: 0 4px 16px #00bfae55;
    }
    /* --- IMPROVED INPUT FIELD --- */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1.5px solid #6c63ff;
        padding: 0.5rem;
        background: #f5f6fa !important;
        color: #232946 !important;
        font-size: 1.08rem;
        transition: border 0.2s;
    }
    .stTextInput>div>div>input:focus {
        border: 2px solid #00bfae;
        outline: none;
        background: #fff !important;
    }
    .stTextInput>label {
        color: #6c63ff !important;
        font-weight: 600;
    }
    .stCheckbox>label {
        color: #b8c1ec !important;
    }
    .stButton>button {
        font-size: 1.05rem;
    }
    .icon {
        font-size: 1.2em;
        vertical-align: middle;
    }
    h2 {
        color: #eebbc3 !important;
        letter-spacing: 1px;
        font-weight: 700;
    }
    @media (max-width: 600px) {
        .glass-card { padding: 1.2rem 0.5rem 1rem 0.5rem; }
    }
    </style>
""", unsafe_allow_html=True)

def password_strength(password):
    length = len(password)
    lower = re.search(r"[a-z]", password)
    upper = re.search(r"[A-Z]", password)
    digit = re.search(r"\d", password)
    special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

    score = 0
    feedback = []
    if length >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")
    if lower:
        score += 1
    else:
        feedback.append("Add lowercase letters")
    if upper:
        score += 1
    else:
        feedback.append("Add uppercase letters")
    if digit:
        score += 1
    else:
        feedback.append("Add numbers")
    if special:
        score += 1
    else:
        feedback.append("Add special characters (!@#$...)")

    if score <= 2:
        return "Weak", "#ff7675", 20, feedback, "🔴"
    elif score == 3 or score == 4:
        return "Medium", "#fdcb6e", 60, feedback, "🟡"
    else:
        return "Strong", "#00bfae", 100, feedback, "🟢"

def generate_password(length=14):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        if (re.search(r"[a-z]", password) and re.search(r"[A-Z]", password) and
            re.search(r"\d", password) and re.search(r"[!@#$%^&*()]", password)):
            return password

# Glassmorphism card start
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>🔒 Password Strength Meter</h2>", unsafe_allow_html=True)

# Show/hide password toggle with icon
col1, col2 = st.columns([8,2])
with col1:
    password = st.text_input("🔑 Enter your password", type="password" if "show" not in st.session_state else "default", key="password_input")
with col2:
    if st.button("👁️" if "show" not in st.session_state else "🙈", key="showhide_btn", help="Show/Hide Password"):
        if "show" in st.session_state:
            del st.session_state["show"]
        else:
            st.session_state["show"] = True

# Password strength analysis
if password:
    strength, color, percent, feedback, icon = password_strength(password)
    st.markdown(
        f'''
        <div class="strength-bar-outer">
            <div class="strength-bar-inner" style="width:{percent}%;"></div>
        </div>
        ''', unsafe_allow_html=True
    )
    st.markdown(
        f"<b>Strength:</b> <span style='color:{color}; font-weight:bold'>{icon} {strength}</span>",
        unsafe_allow_html=True
    )
    if feedback:
        st.markdown("<ul class='feedback-list'>" + "".join([f"<li>{f}</li>" for f in feedback]) + "</ul>", unsafe_allow_html=True)
    if strength == "Weak":
        st.info("Try making your password stronger using the suggestions above.")
    elif strength == "Medium":
        st.warning("Good! But you can make it even stronger.")
    else:
        st.success("Great! Your password is strong.")
else:
    st.markdown(
        f'''
        <div class="strength-bar-outer">
            <div class="strength-bar-inner" style="width:0%;"></div>
        </div>
        ''', unsafe_allow_html=True
    )
    st.write("Please enter a password to check its strength.")

# Password generator and copy to clipboard
st.markdown("---")
st.markdown("<b>Need a strong password?</b>", unsafe_allow_html=True)
colg1, colg2 = st.columns([2,1])
with colg1:
    if st.button("✨ Generate Strong Password", key="gen_btn", help="Generate a random strong password"):
        gen_pass = generate_password()
        st.session_state['gen_pass'] = gen_pass
with colg2:
    if 'gen_pass' in st.session_state:
        st.text_input("Generated Password", st.session_state['gen_pass'], key="gen_pass_input")
        st.button("📋 Copy", key="copy_btn", help="Copy generated password", on_click=st.write, args=("Copied!",))

st.markdown("""
    <div style='text-align:center; color:#b8c1ec; margin-top:1.5rem; font-size:0.95rem;'>
        <span>Made with <span style="color:#eebbc3;">&#10084;</span> using <b>Streamlit</b></span>
    </div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
