# Paper2Prod: Arbitrage under Power

Interactive dashboard for the optimal trading strategy described in "Arbitrage under Power" by Boguslavsky & Boguslavskaya.

## Mathematical Model
- **Price Process**: Ornstein-Uhlenbeck (OU) process for spread $X_t$:
  $$dX_t = -k X_t dt + \sigma dB_t$$
- **Optimal Strategy**: $\alpha_t^* = -W_t X_t D(\tau)$, where:
  - $\tau = T - t$ (time left),
  - $D(\tau) = \frac{C'(\tau)}{C(\tau)}$
- **Value Function**: $J(W_t, X_t, t) = \frac{W_t^{1-\gamma}}{1-\gamma} (1 + C(\tau) X_t^2)$

## How to Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## How to Deploy on Replit
1. Create a new Replit project with Python template.
2. Upload the `app.py`, `requirements.txt`, and `README.md` files.
3. Install dependencies in the Shell:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```