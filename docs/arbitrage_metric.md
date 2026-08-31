# Spoilage Arbitrage Metric Mathematical Formulation

The **Spoilage Arbitrage Metric** converts environmental sensor drift (temperature, humidity, vibration) into a real-time financial decision signal for commodities traders.

---

## 1. Temperature & Micro-Climate Drift Penalty

Let $T_{\text{curr}}$ be the current internal container temperature, $T_{\text{min}}$ and $T_{\text{max}}$ be safe commodity boundaries:

$$\Delta T = \max(0, T_{\text{curr}} - T_{\text{max}}) + \max(0, T_{\text{min}} - T_{\text{curr}})$$

Vibration shock penalty ($V_{\text{curr}}$ in G-force):

$$P_V = \begin{cases} (V_{\text{curr}} - 0.5) \times 1.5 & \text{if } V_{\text{curr}} > 0.5 \\ 0 & \text{otherwise} \end{cases}$$

---

## 2. Compound Degradation Rate & Time to Spoilage

The Degradation Rate Multiplier $M_{\text{deg}}$ scales baseline shelf life $H_{\text{base}}$:

$$M_{\text{deg}} = 1.0 + (\Delta T \times 0.45) + P_V$$

$$\text{TTS}_{\text{hours}} = \max\left(0.5, \frac{H_{\text{base}}}{M_{\text{deg}}}\right)$$

$$\text{Spoilage Probability } P_{\text{spoil}} = \min\left(1.0, \max\left(0.0, 1.0 - \frac{\text{TTS}_{\text{hours}}}{H_{\text{base}}}\right)\right)$$

---

## 3. Haversine Distance to Candidate Markets

Let $(\phi_1, \lambda_1)$ be current container coordinates and $(\phi_2, \lambda_2)$ be target market coordinates:

$$d = 2 R \arcsin\left(\sqrt{\sin^2\left(\frac{\phi_2 - \phi_1}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\lambda_2 - \lambda_1}{2}\right)}\right)$$

Where $R = 6371\text{ km}$. Transit travel hours:

$$t_{\text{transit}} = \frac{d}{60.0} + 1.0\text{ (handling buffer)}$$

---

## 4. Net Spoilage Arbitrage Profit Formula

$$\text{Reroute Transport Cost } C_{\text{reroute}} = d \times 45.0\text{ (₹/km)}$$

$$\text{Expected Spoilage Loss } L_{\text{spoil}} = \begin{cases} V_{\text{cargo}} \times 0.75 & \text{if Risk = HIGH or CRITICAL} \\ V_{\text{cargo}} \times 0.30 & \text{if Risk = MEDIUM} \\ 0 & \text{otherwise} \end{cases}$$

$$\text{Net Arbitrage Profit } \Pi_{\text{net}} = (L_{\text{spoil}} \times 0.90) + \left(V_{\text{cargo}} \times \frac{P_{\text{target}} - P_{\text{orig}}}{P_{\text{orig}}}\right) - C_{\text{reroute}}$$

---

## 5. Arbitrage Decision Signal

An arbitrage opportunity exists IF:

$$t_{\text{transit}} < \text{TTS}_{\text{hours}} \quad \text{AND} \quad \Pi_{\text{net}} > 0 \quad \text{AND} \quad \text{Risk Level} \in \{\text{HIGH}, \text{CRITICAL}\}$$
