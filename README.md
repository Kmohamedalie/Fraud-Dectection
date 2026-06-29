---

# 🚨 Real-Time Fraud Monitoring Dashboard

An interactive, high-velocity Streamlit application built to simulate, detect, and analyze fraudulent financial transactions in real-time. This application features live metric tracking, risk anomaly mapping, and geo-location breakdown of suspicious activities.


<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/572dd15a-5c96-476f-a30c-5bc365adea58" /><br/> Image credits Gemini


---

## 🚀 Features

* **Live Data Streaming:** Simulates a real-time feed of credit card transactions with customizable stream velocity.
* **Heuristic Fraud Detection Engine:** Instantly evaluates incoming transaction metadata (amounts, risk scores, and locations) to flag anomalies.
* **Interactive Dynamic Metrics:** Updates key performance indicators (KPIs) like total volume, alert count, and current fraud rates on-the-fly.
* **Advanced Visualizations:** Uses Plotly Express to render real-time scatter plots for anomaly clusters and geographical risk distribution charts.
* **Isolated User Sessions:** Built using Streamlit's structural session state, allowing multiple external users to interact with the dashboard simultaneously without cross-interfering.


---

### Application Logical Flow

The sequential execution follows this order:

1. **User Connection Initialization:** An external user accesses the Streamlit web server. The server instantly establishes an isolated workspace (`st.session_state`) dedicated purely to that user's session.
2. **Configuration Load:** The application checks the sidebar configuration values (e.g., whether the live stream is active and the speed delay setting).
3. **Data Generation Loop:**
* A simulated background transactional engine creates a dummy transaction payload.
* A heuristic evaluator inspects the payload using predetermined risk factors (such as suspicious geolocation or abnormally high withdrawal limits).
* Transactions crossing these thresholds are tagged as anomalies (`Is_Fraud = 1`) and assigned a high risk coefficient score.


4. **State Storage Sync:** The newest transaction is prepended to the user's historical state tracking table (`df`). To prevent memory leaks during long browsing sessions, the historical cache automatically limits its capacity to the most recent 100 activities.
5. **UI & Layout Compilation:** The calculation engine sums up total volumes, averages fraud alert rates, and pipes the active state table through Plotly Express to redraw the metric widgets, time-series clusters, and geographical distribution pie charts.
6. **Thread Sleep & Re-trigger:** The script sleeps for the designated fraction of a second chosen by the user and then programmatically issues an internal `st.rerun()` statement to restart the cycle from Step 2 seamlessly.
---

## 🛠️ Tech Stack

* **Frontend/Dashboard Framework:** Streamlit
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Plotly Express
* **Environment Containerization:** Docker


## 🏗️ Application Architecture

The application uses an efficient, single-process stream simulation loop. Because Streamlit naturally isolates memory spaces for different connections, multiple external users can interact with the app concurrently without impacting each other's live dashboards.

[ User Browser ] <---> 
[ Streamlit Server Instance ]

                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
       [ User A Session ]            [ User B Session ]
        (st.session_state)            (st.session_state)
               │                             │
    ┌──────────┴──────────┐       ┌──────────┴──────────┐
    ▼                     ▼       ▼                     ▼
    [Mock Generator] ──► [UI Engine] [Mock Generator] ──► [UI Engine]
    (6% Fraud Bias)      (Plotly)    (6% Fraud Bias)      (Plotly)

---

## 📦 Local Installation & Setup

### Prerequisites

Make sure you have Python 3.9+ installed on your machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fraud-monitoring-dashboard.git
cd fraud-monitoring-dashboard

```

### 2. Install Dependencies

It is highly recommended to use a virtual environment:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

```

*(Note: Your `requirements.txt` should contain at least: `streamlit`, `pandas`, `numpy`, and `plotly`)*

### 3. Run the Application

```bash
streamlit run app.py

```

The dashboard will automatically launch in your default browser at `http://localhost:8501`.

---

## 🐳 Docker Deployment (For External Users)

To deploy this application to cloud platforms (AWS, GCP, DigitalOcean, Render) so external users can access it, you can package it using the provided `Dockerfile`.

### Build the Docker Image:

```bash
docker build -t fraud-dashboard:latest .

```

### Run the Container Locally:

```bash
docker run -p 8501:8501 fraud-dashboard:latest

```

Now, users on your network can access the application via your machine's IP address on port `8501`.

---

## 🤝 Credits & Acknowledgments

This application was conceptualized and developed by **Gemini**, an AI collaborator, in tandem with engineering insights for real-time stream simulation and modern analytical UI design.

---

## 📝 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
