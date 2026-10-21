import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import hmac

# ==========================================
# LOGIN CONFIGURATION
# ==========================================

# Demo credentials — change before using the app.
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "HHS@2026"

# Initialize login state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ==========================================
# ANIMATED LOGIN DESIGN
# ==========================================

st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --mint: #5cf2c2;
    --cyan: #48d9ff;
    --purple: #9875ff;
    --text: #f4f7ff;
    --muted: #9aaac3;
}

/* Animated background */
.stApp {
    background:
        radial-gradient(ellipse at 15% 15%, #143a49 0%, transparent 42%),
        radial-gradient(ellipse at 85% 80%, #292052 0%, transparent 40%),
        linear-gradient(135deg, #050914, #0a1222 50%, #07151c);
    background-size: 180% 180%;
    animation: backgroundFlow 16s ease infinite;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

@keyframes backgroundFlow {
    0%, 100% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
}

/* Subtle technical grid */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(130, 200, 255, .035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(130, 200, 255, .035) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: linear-gradient(to bottom, black, transparent 90%);
}

/* Soft animated glow */
.orb {
    position: fixed;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    filter: blur(85px);
    opacity: .25;
    pointer-events: none;
    z-index: 0;
    animation: orbFloat 10s ease-in-out infinite;
}

.orb-one {
    background: var(--mint);
    left: -100px;
    top: 10%;
}

.orb-two {
    background: var(--purple);
    right: -100px;
    bottom: 4%;
    animation-delay: -4s;
}

@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(35px, -35px) scale(1.13); }
}

/* Keep application content above the background */
[data-testid="stAppViewContainer"] > .main,
[data-testid="stSidebar"] {
    position: relative;
    z-index: 1;
}

/* Premium heading */
.login-badge {
    display: inline-block;
    color: var(--mint);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-align: center;
    width: 100%;
    margin-bottom: 18px;
    animation: fadeUp .7s ease both;
}

.login-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(32px, 4vw, 46px);
    line-height: 1.1;
    font-weight: 700;
    letter-spacing: -1.8px;
    text-align: center;
    color: #ffffff;
    margin-bottom: 12px;
    animation: fadeUp .8s ease both;
}

.login-subtitle {
    text-align: center;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 30px;
    animation: fadeUp .95s ease both;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(24px);
        filter: blur(5px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
        filter: blur(0);
    }
}

/* Glass login panel */
div[data-testid="stForm"] {
    position: relative;
    overflow: hidden;
    padding: 30px 28px 26px;
    border: 1px solid rgba(255, 255, 255, .13);
    border-radius: 24px;
    background: linear-gradient(
        145deg,
        rgba(255, 255, 255, .09),
        rgba(255, 255, 255, .025)
    );
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow:
        0 30px 80px rgba(0, 0, 0, .42),
        inset 0 1px 0 rgba(255, 255, 255, .09);
    animation: panelEnter 1s cubic-bezier(.2, .8, .2, 1) both;
}

div[data-testid="stForm"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 12%;
    width: 76%;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        var(--mint),
        var(--cyan),
        transparent
    );
    opacity: .9;
}

@keyframes panelEnter {
    from {
        opacity: 0;
        transform: translateY(28px) scale(.98);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Labels */
div[data-testid="stForm"] label {
    color: #dce8f8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* Input styling */
div[data-testid="stForm"] input {
    color: #ffffff !important;
    background: rgba(4, 12, 25, .68) !important;
    border: 1px solid rgba(166, 193, 230, .17) !important;
    border-radius: 12px !important;
    min-height: 44px;
    transition: border-color .25s ease, box-shadow .25s ease,
                background .25s ease;
}

div[data-testid="stForm"] input:focus {
    border-color: var(--mint) !important;
    box-shadow: 0 0 0 3px rgba(92, 242, 194, .10),
                0 0 22px rgba(92, 242, 194, .07) !important;
    background: rgba(4, 17, 29, .95) !important;
}

/* Main login button */
div[data-testid="stForm"] button[kind="primary"] {
    position: relative;
    overflow: hidden;
    min-height: 48px;
    margin-top: 12px;
    color: #06131b !important;
    background: linear-gradient(100deg, #5cf2c2, #48d9ff) !important;
    border: 0 !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    letter-spacing: .3px;
    box-shadow: 0 8px 25px rgba(72, 217, 255, .15);
    transition: transform .25s ease, box-shadow .25s ease,
                filter .25s ease;
}

div[data-testid="stForm"] button[kind="primary"]:hover {
    transform: translateY(-3px);
    filter: brightness(1.08);
    box-shadow: 0 14px 34px rgba(72, 217, 255, .28);
}

div[data-testid="stForm"] button[kind="primary"]:active {
    transform: translateY(0) scale(.99);
}

/* Checkbox */
div[data-testid="stForm"] [data-testid="stCheckbox"] label {
    color: #aebdd2 !important;
    font-size: 12px !important;
}

/* Footer */
.login-footer {
    color: #7f91aa;
    font-size: 10px;
    line-height: 2;
    letter-spacing: 1.5px;
    text-align: center;
    margin-top: 24px;
}

/* Hide Streamlit branding */
#MainMenu,
footer {
    visibility: hidden;
}

/* Mobile layout */
@media (max-width: 640px) {
    div[data-testid="stForm"] {
        padding: 23px 18px;
        border-radius: 18px;
    }

    .login-title {
        letter-spacing: -1px;
    }

    .orb {
        width: 190px;
        height: 190px;
    }
}

/* Respect reduced-motion accessibility */
@media (prefers-reduced-motion: reduce) {
    .stApp,
    .orb,
    .login-title,
    .login-subtitle,
    .login-badge,
    div[data-testid="stForm"] {
        animation: none !important;
    }

    * {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
    }
}
</style>

<div class="orb orb-one"></div>
<div class="orb orb-two"></div>
""", unsafe_allow_html=True)


# ==========================================
# LOGIN FORM
# ==========================================

def show_login():
    left, center, right = st.columns([1, 1.1, 1])

    with center:
        st.markdown("""
        <div class="login-badge">HHS • INTELLIGENCE PLATFORM</div>
        <div class="login-title">Welcome Back</div>
        <div class="login-subtitle">
            Sign in to your forecasting and capacity dashboard
        </div>
        """, unsafe_allow_html=True)

        with st.form("hhs_login_form"):
            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                placeholder="Enter your password",
                type="password"
            )

            remember = st.checkbox("Remember this session")

            submitted = st.form_submit_button(
                "Sign In →",
                use_container_width=True,
                type="primary"
            )

        if submitted:
            username_ok = hmac.compare_digest(
                username.strip(), DEMO_USERNAME
            )
            password_ok = hmac.compare_digest(
                password, DEMO_PASSWORD
            )

            if username_ok and password_ok:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.markdown("""
        <div class="login-footer">
            HHS CARE FORECASTING & CAPACITY PLANNING<br>
            Secure access • Predictive insights • Better planning
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# APPLICATION GATE
# ==========================================

if not st.session_state.authenticated:
    show_login()
    st.stop()

# Your existing HHS dashboard code goes below this line.
st.sidebar.success("Signed in successfully")

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()



# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="HHS Care Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f172a, #1d4ed8);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 1.05rem;
        opacity: 0.9;
    }

    .metric-card {
        padding: 18px;
        border-radius: 15px;
        background: white;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .risk-high {
        padding: 20px;
        border-radius: 15px;
        background: #fee2e2;
        border-left: 6px solid #dc2626;
        color: #991b1b;
    }

    .risk-normal {
        padding: 20px;
        border-radius: 15px;
        background: #dcfce7;
        border-left: 6px solid #16a34a;
        color: #166534;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIONS
# ============================================================
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        filename = uploaded_file.name.lower()

        if filename.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
    else:
        data_path = Path(__file__).resolve().parent / "data" / "sales.csv"

        if not data_path.exists():
            return None

        data = pd.read_csv(data_path)

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(
            data["Date"], errors="coerce"
        )

    return data




# ==========================================
# DATA CLEANING
# ==========================================

def clean_data(df):
    df = df.copy()

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Required HHS columns
    required_columns = [
        "Date",
        "Children in HHS Care",
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required HHS columns: {missing_columns}. "
            f"Available columns: {df.columns.tolist()}"
        )

    # Convert dates
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # Convert numeric columns, including comma-formatted values
    for col in df.columns:
        if col != "Date":
            df[col] = pd.to_numeric(
                df[col].astype(str)
                .str.replace(",", "", regex=False)
                .str.strip(),
                errors="coerce"
            )

    # Remove invalid dates and sort chronologically
    df = df.dropna(subset=["Date"])
    df = df.sort_values("Date")

    # Handle duplicate dates
    df = df.groupby("Date", as_index=False).last()

    # Use Date as the index
    df = df.set_index("Date")

    # Fill missing numeric values
    df = df.interpolate(method="linear")
    df = df.ffill().bfill()

    # Validate target data
    if df.empty:
        raise ValueError("No valid rows remain after cleaning.")

    if df["Children in HHS Care"].isna().all():
        raise ValueError(
            "'Children in HHS Care' contains no valid numeric values."
        )

    return df


# ==========================================
# FEATURE ENGINEERING
# ==========================================

def create_features(df):
    df = df.copy()

    target = "Children in HHS Care"
    transfers = "Children transferred out of CBP custody"
    discharges = "Children discharged from HHS Care"

    required_columns = [target, transfers, discharges]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot create features. Missing columns: {missing_columns}"
        )

    # Historical target values
    df["lag1"] = df[target].shift(1)
    df["lag7"] = df[target].shift(7)
    df["lag14"] = df[target].shift(14)

    # Rolling averages
    df["rolling7"] = df[target].rolling(
        window=7, min_periods=7
    ).mean()

    df["rolling14"] = df[target].rolling(
        window=14, min_periods=14
    ).mean()

    # Transfers minus discharges
    df["Net_Pressure"] = df[transfers] - df[discharges]

    # Calendar features
    df["month"] = df.index.month
    df["dayofweek"] = df.index.dayofweek

    # Remove rows without enough historical data
    df = df.dropna()

    if len(df) < 10:
        raise ValueError(
            "Not enough rows to train the forecasting models. "
            "Use a dataset with more historical observations."
        )

    return df


# ==========================================
# MODEL TRAINING AND EVALUATION
# ==========================================

def train_models(df):
    features = [
        "lag1",
        "lag7",
        "lag14",
        "rolling7",
        "rolling14",
        "Net_Pressure",
        "month",
        "dayofweek"
    ]

    target = "Children in HHS Care"

    # Check required columns
    required = features + [target]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing model features: {missing}. "
            "Run create_features(df) first."
        )

    # Remove infinite or missing values
    model_df = df[required].replace(
        [np.inf, -np.inf], np.nan
    ).dropna()

    if len(model_df) < 10:
        raise ValueError(
            "Not enough valid observations for model training."
        )

    # Chronological train/test split
    train_size = int(len(model_df) * 0.8)

    train = model_df.iloc[:train_size]
    test = model_df.iloc[train_size:]

    if train.empty or test.empty:
        raise ValueError(
            "Insufficient data for train/test split."
        )

    X_train = train[features]
    y_train = train[target]

    X_test = test[features]
    y_test = test[target]

    # Random Forest
    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    # Gradient Boosting
    gb = GradientBoostingRegressor(
        random_state=42,
        n_estimators=100,
        learning_rate=0.05,
        max_depth=3
    )

    # Train models
    rf.fit(X_train, y_train)
    gb.fit(X_train, y_train)

    # Predictions
    rf_pred = rf.predict(X_test)
    gb_pred = gb.predict(X_test)

    # Evaluation
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

    gb_mae = mean_absolute_error(y_test, gb_pred)
    gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))

    return {
        "rf": rf,
        "gb": gb,
        "features": features,
        "test": test,
        "y_test": y_test,
        "rf_pred": rf_pred,
        "gb_pred": gb_pred,
        "rf_mae": rf_mae,
        "rf_rmse": rf_rmse,
        "gb_mae": gb_mae,
        "gb_rmse": gb_rmse
    }

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <h1>📊 HHS Care Forecasting</h1>
    <p>
        Interactive Machine Learning Dashboard for forecasting
        Children in HHS Care
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:

    st.header("⚙️ Controls")

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "📋 Data Overview",
            "📈 Trend Analysis",
            "🤖 ML Forecasting",
            "🔍 Feature Importance",
            "⚠️ Capacity Risk",
            "📥 Export"
        ]
    )

    st.divider()

    st.caption(
        "HHS Care Forecasting • Random Forest + Gradient Boosting"
    )


## ==========================================
# LOAD + CLEAN
# ==========================================

uploaded_file = st.sidebar.file_uploader(
    "Upload HHS Dataset",
    type=["csv", "xlsx"]
)

try:
    if uploaded_file is None:
        st.info("Please upload your HHS dataset to continue.")
        st.stop()

    # Load CSV or Excel file
    if uploaded_file.name.lower().endswith(".xlsx"):
        raw_df = pd.read_excel(uploaded_file)
    else:
        raw_df = pd.read_csv(uploaded_file)

    if raw_df.empty:
        st.error("The uploaded dataset is empty.")
        st.stop()

    st.success("Dataset loaded successfully!")

    # Show column names to help verify the dataset
    st.write("Dataset columns:", raw_df.columns.tolist())

    # Clean data
    df = clean_data(raw_df)

    # Create model features
    model_df = create_features(df)

except Exception as e:
    st.error("Unable to load or process the dataset.")
    st.exception(e)
    st.stop()


# ============================================================
# DASHBOARD
# ============================================================
if page == "🏠 Dashboard":

    st.subheader("Executive Dashboard")

    target = "Children in HHS Care"

    latest = float(df[target].iloc[-1])
    average = float(df[target].mean())
    maximum = float(df[target].max())
    minimum = float(df[target].min())

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Current HHS Care",
            f"{latest:,.0f}"
        )

    with c2:
        st.metric(
            "Average",
            f"{average:,.0f}"
        )

    with c3:
        st.metric(
            "Maximum",
            f"{maximum:,.0f}"
        )

    with c4:
        st.metric(
            "Minimum",
            f"{minimum:,.0f}"
        )

    st.divider()

    st.subheader("HHS Care Trend")

    fig = px.line(
        df.reset_index(),
        x="Date",
        y=target,
        markers=True,
        title="Children in HHS Care Over Time"
    )

    fig.update_layout(
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Latest Records")
        st.dataframe(
            df.tail(10),
            use_container_width=True
        )

    with col2:
        st.subheader("Correlation")

        corr = df.corr(
            numeric_only=True
        )

        fig_corr = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix"
        )

        st.plotly_chart(
            fig_corr,
            use_container_width=True
        )


# ============================================================
# DATA OVERVIEW
# ============================================================
elif page == "📋 Data Overview":

    st.subheader("📋 Dataset Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        f"{len(df):,}"
    )

    c2.metric(
        "Columns",
        f"{len(df.columns):,}"
    )

    c3.metric(
        "Missing Values",
        f"{int(df.isnull().sum().sum()):,}"
    )

    st.divider()

    st.subheader("Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    st.subheader("Descriptive Statistics")

    st.dataframe(
        df.describe().T,
        use_container_width=True
    )


# ============================================================
# TREND ANALYSIS
# ============================================================
elif page == "📈 Trend Analysis":

    st.subheader("📈 Trend Analysis")

    available_numeric = df.select_dtypes(
        include="number"
    ).columns.tolist()

    selected_columns = st.multiselect(
        "Select metrics",
        available_numeric,
        default=["Children in HHS Care"]
        if "Children in HHS Care" in available_numeric
        else available_numeric[:1]
    )

    if selected_columns:

        fig = px.line(
            df.reset_index(),
            x="Date",
            y=selected_columns,
            title="Selected Metrics Over Time"
        )

        fig.update_layout(
            height=550,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("📊 Intake vs Discharge")

    intake = "Children apprehended and placed in CBP custody*"
    discharge = "Children discharged from HHS Care"

    if intake in df.columns and discharge in df.columns:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[intake],
                mode="lines",
                name="Intake"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[discharge],
                mode="lines",
                name="Discharge"
            )
        )

        fig.update_layout(
            title="Intake vs Discharge",
            height=500,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("📅 Day-of-Week Analysis")

    dow = (
        model_df
        .groupby("dayofweek")["Children in HHS Care"]
        .mean()
        .reset_index()
    )

    dow["Day"] = dow["dayofweek"].map({
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    })

    fig = px.bar(
        dow,
        x="Day",
        y="Children in HHS Care",
        title="Average HHS Care by Day"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# ML FORECASTING
# ============================================================
elif page == "🤖 ML Forecasting":

    st.subheader("🤖 Machine Learning Forecasting")

    with st.spinner("Training Random Forest and Gradient Boosting..."):
        results = train_models(model_df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "RF MAE",
        f"{results['rf_mae']:,.2f}"
    )

    c2.metric(
        "RF RMSE",
        f"{results['rf_rmse']:,.2f}"
    )

    c3.metric(
        "GB MAE",
        f"{results['gb_mae']:,.2f}"
    )

    c4.metric(
        "GB RMSE",
        f"{results['gb_rmse']:,.2f}"
    )

    st.divider()

    model_choice = st.selectbox(
        "Select Model",
        [
            "Random Forest",
            "Gradient Boosting",
            "Compare Both"
        ]
    )

    test = results["test"]
    y_test = results["y_test"]

    if model_choice == "Random Forest":

        prediction = results["rf_pred"]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=test.index,
                y=y_test,
                mode="lines",
                name="Actual"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=test.index,
                y=prediction,
                mode="lines",
                name="Random Forest"
            )
        )

        fig.update_layout(
            title="Actual vs Random Forest Prediction",
            height=550,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif model_choice == "Gradient Boosting":

        prediction = results["gb_pred"]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=test.index,
                y=y_test,
                mode="lines",
                name="Actual"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=test.index,
                y=prediction,
                mode="lines",
                name="Gradient Boosting"
            )
        )

        fig.update_layout(
            title="Actual vs Gradient Boosting Prediction",
            height=550,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=test.index,
                y=y_test,
                mode="lines",
                name="Actual"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=test.index,
                y=results["rf_pred"],
                mode="lines",
                name="Random Forest"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=test.index,
                y=results["gb_pred"],
                mode="lines",
                name="Gradient Boosting"
            )
        )

        fig.update_layout(
            title="Model Comparison",
            height=550,
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Model Performance")

    performance = pd.DataFrame({
        "Model": [
            "Random Forest",
            "Gradient Boosting"
        ],
        "MAE": [
            results["rf_mae"],
            results["gb_mae"]
        ],
        "RMSE": [
            results["rf_rmse"],
            results["gb_rmse"]
        ]
    })

    st.dataframe(
        performance,
        use_container_width=True
    )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================
elif page == "🔍 Feature Importance":

    st.subheader("🔍 Feature Importance")

    results = train_models(model_df)

    importance = pd.DataFrame({
        "Feature": results["features"],
        "Importance": results["rf"].feature_importances_
    })

    importance = importance.sort_values(
        "Importance",
        ascending=False
    )

    fig = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Random Forest Feature Importance"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        importance,
        use_container_width=True
    )


# ============================================================
# CAPACITY RISK
# ============================================================
elif page == "⚠️ Capacity Risk":

    st.subheader("⚠️ Capacity Risk Analysis")

    target = "Children in HHS Care"

    threshold_method = st.selectbox(
        "Risk Threshold",
        [
            "Historical Average",
            "75th Percentile",
            "90th Percentile"
        ]
    )

    if threshold_method == "Historical Average":
        threshold = df[target].mean()

    elif threshold_method == "75th Percentile":
        threshold = df[target].quantile(0.75)

    else:
        threshold = df[target].quantile(0.90)

    latest = df[target].iloc[-1]

    st.metric(
        "Risk Threshold",
        f"{threshold:,.0f}"
    )

    st.metric(
        "Current HHS Care",
        f"{latest:,.0f}"
    )

    if latest > threshold:

        st.markdown(
            f"""
            <div class="risk-high">
                <h3>🚨 HIGH CAPACITY RISK</h3>
                <p>
                Current HHS Care ({latest:,.0f}) is above
                the selected threshold ({threshold:,.0f}).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="risk-normal">
                <h3>✅ NORMAL CAPACITY</h3>
                <p>
                Current HHS Care ({latest:,.0f}) is below
                the selected threshold ({threshold:,.0f}).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    risk_df = df[[target]].copy()

    risk_df["Risk"] = np.where(
        risk_df[target] > threshold,
        "High Risk",
        "Normal"
    )

    fig = px.scatter(
        risk_df.reset_index(),
        x="Date",
        y=target,
        color="Risk",
        title="Capacity Risk Over Time"
    )

    fig.add_hline(
        y=threshold,
        line_dash="dash",
        annotation_text="Risk Threshold"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# EXPORT
# ============================================================
elif page == "📥 Export":

    st.subheader("📥 Export Forecast Results")

    with st.spinner("Preparing forecast data..."):
        results = train_models(model_df)

    export_df = model_df.copy()

    test_index = results["test"].index

    export_df.loc[
        test_index,
        "RF_Prediction"
    ] = results["rf_pred"]

    export_df.loc[
        test_index,
        "GB_Prediction"
    ] = results["gb_pred"]

    threshold = export_df[
        "Children in HHS Care"
    ].mean()

    export_df["Capacity_Risk"] = np.where(
        export_df["Children in HHS Care"] > threshold,
        "High Risk",
        "Normal"
    )

    export_df = export_df.reset_index()

    st.dataframe(
        export_df.tail(20),
        use_container_width=True
    )

    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Forecast CSV",
        data=csv_data,
        file_name="HHS_Forecasting_Final.csv",
        mime="text/csv"
    )

    # Excel download
    import io

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        export_df.to_excel(
            writer,
            index=False,
            sheet_name="Forecast"
        )

        pd.DataFrame({
            "Model": [
                "Random Forest",
                "Gradient Boosting"
            ],
            "MAE": [
                results["rf_mae"],
                results["gb_mae"]
            ],
            "RMSE": [
                results["rf_rmse"],
                results["gb_rmse"]
            ]
        }).to_excel(
            writer,
            index=False,
            sheet_name="Model Performance"
        )

    st.download_button(
        label="📊 Download Excel Report",
        data=excel_buffer.getvalue(),
        file_name="HHS_Forecasting_Final.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success(
        "Your forecast report is ready to download."
    )


# ============================================================
# FOOTER
# ============================================================
st.divider()

st.caption(
    "HHS Care Forecasting | Interactive Streamlit ML Dashboard"
)



