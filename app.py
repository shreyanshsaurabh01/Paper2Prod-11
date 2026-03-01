import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Mathematical Model Implementation

def C(tau, gamma, k, sigma):
    """Function C(tau) from Eq. 13."""
    return (1 - np.exp(-k * tau)) / (1 - gamma) if gamma != 1 else np.log(1 + k * tau)

def D(tau, gamma, k, sigma):
    """Function D(tau) from Eq. 14."""
    return (1 - np.exp(-k * tau)) / (1 - gamma) if gamma != 1 else np.log(1 + k * tau)

def risk_aversion(gamma):
    """Risk aversion parameter from Eq. 12."""
    return gamma

def optimal_strategy(W_t, X_t, tau, gamma, k, sigma):
    """Optimal trading strategy from Eq. 16."""
    return -W_t * X_t * D(tau, gamma, k, sigma)

def value_function(W_t, X_t, tau, gamma, k, sigma):
    """Value function from Eq. 17."""
    return W_t ** (1 - gamma) / (1 - gamma) * (1 + C(tau, gamma, k, sigma) * X_t ** 2)

def simulate_ou_process(k, sigma, X0, T, dt):
    """Simulate OU process using Euler-Maruyama method."""
    n_steps = int(T / dt)
    X = np.zeros(n_steps + 1)
    X[0] = X0
    for i in range(1, n_steps + 1):
        X[i] = X[i-1] + k * (0 - X[i-1]) * dt + sigma * np.sqrt(dt) * np.random.normal()
    return X

# Streamlit App
st.title("Paper2Prod: Arbitrage under Power")

# Sidebar for parameter inputs
st.sidebar.header("Parameters")
gamma = st.sidebar.slider("Risk aversion (gamma)", -5.0, 0.99, 0.0)
log_utility = st.sidebar.checkbox("Log-utility mode", False)
k = st.sidebar.slider("Mean-reversion speed (k)", 0.1, 10.0, 1.0)
sigma = st.sidebar.slider("Volatility (sigma)", 0.1, 5.0, 1.0)
W0 = st.sidebar.slider("Initial wealth (W0)", 1, 1000, 100)
T = st.sidebar.slider("Time horizon (T)", 0.1, 5.0, 1.0)
X0 = st.sidebar.slider("Current spread (X0)", -5.0, 5.0, 0.0)
dt = 0.01  # Fixed time step for simulation

# Update gamma for log-utility mode
if log_utility:
    gamma = 0.0

# Main panel for visualizations
st.header("Optimal Trading Strategy")
tau = T  # Simplified for demonstration
X_t = np.linspace(-5, 5, 100)
alpha_t_star = optimal_strategy(W0, X_t, tau, gamma, k, sigma)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=X_t, y=alpha_t_star, mode='lines', name='Optimal Position'))
fig1.update_layout(title="Optimal Position \alpha_t^* vs. Spread X_t", xaxis_title="Spread X_t", yaxis_title="Optimal Position \alpha_t^*")
st.plotly_chart(fig1)

st.header("Value Function")
J = value_function(W0, X_t, tau, gamma, k, sigma)

fig2 = go.Figure(data=[go.Surface(z=J, x=X_t, y=X_t)])
fig2.update_layout(title="Value Function J(W_t, X_t, t) vs. Spread X_t", scene=dict(xaxis_title="Spread X_t", yaxis_title="Spread X_t", zaxis_title="Value Function J"))
st.plotly_chart(fig2)

st.header("Time Value B(\tau)")
tau_values = np.linspace(0.1, T, 100)
B_tau = np.exp(-k * tau_values)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=tau_values, y=B_tau, mode='lines', name='Time Value B(\tau)'))
fig3.update_layout(title="Time Value B(\tau) vs. Remaining Time \tau", xaxis_title="Remaining Time \tau", yaxis_title="Time Value B(\tau)")
st.plotly_chart(fig3)

st.header("Function D(\tau) vs. Remaining Time \tau")
D_tau = D(tau_values, gamma, k, sigma)

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=tau_values, y=D_tau, mode='lines', name='Function D(\tau)'))
fig4.update_layout(title="Function D(\tau) vs. Remaining Time \tau", xaxis_title="Remaining Time \tau", yaxis_title="Function D(\tau)")
st.plotly_chart(fig4)

st.header("Dynamic Simulation")
X_t_sim = simulate_ou_process(k, sigma, X0, T, dt)
time_steps = np.arange(0, T + dt, dt)
alpha_t_star_sim = optimal_strategy(W0, X_t_sim, T - time_steps, gamma, k, sigma)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=time_steps, y=X_t_sim, mode='lines', name='Spread X_t'))
fig5.add_trace(go.Scatter(x=time_steps, y=alpha_t_star_sim, mode='lines', name='Optimal Position \alpha_t^*'))
fig5.update_layout(title="Simulation of Spread X_t and Optimal Position \alpha_t^*", xaxis_title="Time", yaxis_title="Value")
st.plotly_chart(fig5)