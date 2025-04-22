import re
import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="Password Strength Analyzer",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .stApp {
            background-color: #34495e;
        }
        
        .main {
            color: #ffffff;
        }
        
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: #ffffff;
        }
        
        h1 {
            font-weight: 700 !important;
            font-size: 2.8rem !important;
            margin-bottom: 1.5rem !important;
            text-align: center;
            font-family: 'Poppins', sans-serif;
        }
        
        .subtitle {
            font-size: 1.3rem !important;
            margin-bottom: 1.5rem !important;
            text-align: center;
        }
        
        .password-container {
            margin-bottom: 20px;
        }
        
        .stTextInput > div > div > input {
            border: none !important;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 18px;
            background-color: #ecf0f1;
            color: #2c3e50;
        }
        
        .stButton > button {
            background-color: #3498db;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 12px 20px;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #2980b9;
        }
        
        .feedback-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            padding: 12px;
            border-radius: 8px;
            background-color: #2c3e50;
        }
        
        .feedback-icon {
            margin-right: 12px;
            font-size: 22px;
            color: #f39c12;
        }
        
        .progress-container {
            width: 100%;
            background-color: #2c3e50;
            border-radius: 8px;
            margin: 20px 0;
            height: 12px;
        }
        
        .progress-bar {
            height: 12px;
            border-radius: 8px;
            transition: width 0.5s ease-in-out;
        }
        
        .criteria-container {
            margin-top: 30px;
            background-color: #34495e;
            padding: 20px;
            border-radius: 8px;
        }
        
        .criteria-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .criteria-icon {
            margin-right: 12px;
            font-size: 22px;
            color: #2980b9;
        }
        
        .criteria-text {
            font-size: 16px;
        }
        
        .result-container {
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            text-align: center;
            font-weight: 600;
            font-size: 20px;
            animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #bdc3c7;
            font-size: 16px;
        }
        
        .stWarning {
            background-color: #2c3e50;
            color: #f39c12;
            padding: 12px;
            border-radius: 8px;
        }

        .enter-key-notice {
            color: #f1c40f;
            font-size: 16px;
            margin-top: 8px;
            margin-bottom: 15px;
            text-align: center;
            font-weight: 500;
            background-color: rgba(44, 62, 80, 0.7);
            padding: 8px;
            border-radius: 8px;
            display: block;
        }
    </style>
    
    <script>
        // Add event listener for the Enter key
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                const passwordInput = document.querySelector('input[type="password"]');
                if (passwordInput) {
                    passwordInput.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            const checkButton = document.querySelector('button.stButton');
                            if (checkButton) {
                                checkButton.click();
                            }
                        }
                    });
                }
            }, 1000); // Wait for Streamlit to render elements
        });
    </script>
    """, 
    unsafe_allow_html=True
)

# Initialize session state for password history and checking
if 'password_history' not in st.session_state:
    st.session_state.password_history = []

if 'check_triggered' not in st.session_state:
    st.session_state.check_triggered = False

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check for uppercase and lowercase
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Password should contain both uppercase and lowercase letters (A-Z, a-z).")
    
    # Check for numbers
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Password should contain at least one number (0-9).")
          
    # Check for special characters
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Password should contain at least one special character (!@#$%^&*).")

    return score, feedback

# Function to analyze password and show results
def analyze_password(password):
    if password:
        # Check if password is in the history
        if password in st.session_state.password_history:
            st.warning("This password has been used recently. Please choose a different password.")
        else:
            with st.spinner("Analyzing your password..."):
                time.sleep(1)
                
                score, feedback = check_password_strength(password)
                
                st.markdown("<div class='progress-container'>", unsafe_allow_html=True)
                
                progress_percentage = (score / 4) * 100
                progress_color = "#e74c3c" if score <= 1 else "#f39c12" if score <= 2 else "#2ecc71"
                
                st.markdown(
                    f"<div class='progress-bar' style='width: {progress_percentage}%; background-color: {progress_color};'></div>",
                    unsafe_allow_html=True
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Display result
                if score == 4:
                    st.markdown(
                        "<div class='result-container' style='background-color: rgba(46, 204, 113, 0.2); color: #2ecc71;'>Your password is strong! 🎉</div>",
                        unsafe_allow_html=True
                    )
                elif score == 3:
                    st.markdown(
                        "<div class='result-container' style='background-color: rgba(243, 156, 18, 0.2); color: #f39c12;'>Your password is moderate ⚠️</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div class='result-container' style='background-color: rgba(231, 76, 60, 0.2); color: #e74c3c;'>Your password is weak! ⛔</div>",
                        unsafe_allow_html=True
                    )
                
                # Display feedback
                if feedback:
                    st.markdown("<h4><span>⚠️</span> Improve Your Password:</h4>", unsafe_allow_html=True)
                    for item in feedback:
                        st.markdown(
                            f"<div class='feedback-item'><span class='feedback-icon'>⚠️</span>{item}</div>",
                            unsafe_allow_html=True
                        )
                
            # Add password to history
            st.session_state.password_history.append(password)
            if len(st.session_state.password_history) > 10:
                st.session_state.password_history.pop(0)
    else:
        st.warning("Please enter a password")

# App header
st.markdown("<h1><span>🔒</span> Password Strength Analyzer</h1>", unsafe_allow_html=True)

# Main container for spacing
st.markdown("<div class='password-container'>", unsafe_allow_html=True)

st.markdown("<p class='subtitle'><span>🔍</span> Check your password security and make it stronger</p>", unsafe_allow_html=True)

# Password input with proper label
password = st.text_input(
    label="Password Input",  # Provide a meaningful label
    type="password",
    placeholder="Enter your password",
    key="password_input",
    label_visibility="collapsed",  # Hides the label visually but keeps it for accessibility
    on_change=lambda: setattr(st.session_state, 'check_triggered', True) if st.session_state.password_input else None
)

# Display notice about Enter key functionality
st.markdown("<p class='enter-key-notice'>Press <strong>Enter</strong> to check password strength</p>", unsafe_allow_html=True)

# Display password criteria
st.markdown("<div class='criteria-container'>", unsafe_allow_html=True)
st.markdown("<h4><span>📋</span> Strong Password Criteria:</h4>", unsafe_allow_html=True)

criteria_items = [
    ("📏", "Minimum 8 characters"),
    ("🔠", "Uppercase and lowercase letters (A-Z, a-z)"),
    ("🔢", "At least one number (0-9)"),
    ("🔣", "At least one special character (!@#$%^&*)")
]

for icon, text in criteria_items:
    st.markdown(
        f"<div class='criteria-item'><span class='criteria-icon'>{icon}</span><span class='criteria-text'>{text}</span></div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# Check button with proper label
check_clicked = st.button(
    "Check Password Strength", 
    key="check_button"
)

# Analyze password when button is clicked or Enter is pressed
if check_clicked or st.session_state.check_triggered:
    analyze_password(password)
    # Reset the trigger after handling
    st.session_state.check_triggered = False

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    "<div class='footer'>© 2025 Password Strength Analyzer | Designed by <b>Shoaib Tahir</b></div>",
    unsafe_allow_html=True
)