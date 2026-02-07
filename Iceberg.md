# Project TANS: Tactical Arctic Navigation System

**Tagline:** *Tactical Decision Support for the 50km Arctic Navigation Gap*

---

## 1. The Problem: The "Tactical Gap"

Arctic navigation is currently split between **Macro-Scale satellite charts** (12–24 hours old) and **Micro-Scale human lookouts** (2km visibility). There is no reliable tool for the **5km to 50km "Tactical Window."** 

In this range, icebergs move like drifting minefields, making it impossible for ships like the RCN's Harry DeWolf-class to plot safe 6-12 hour tactical paths. TANS provides decision support with periodic SAR updates, enabling predictive navigation in this critical zone.

---

## System Architecture

TANS consists of three integrated modules that work together to provide real-time Arctic navigation intelligence:

---

## Module A: The Eyes (ML Classification)

**Objective:** Distinguish between ships and icebergs in low-visibility environments.

### The Technical Stack
- **Input:** Dual-polarization SAR backscatter (HH/HV bands) from RADARSAT Constellation Mission (RCM) for operational deployment; Sentinel-1 for proof-of-concept demonstration
- **Model Architecture:** CNN (Inception-v3 or YOLOv11) trained on Statoil/C-CORE iceberg dataset

### The Deep Tech
- **Polarimetric Signature:** Ships exhibit high specular reflection; icebergs show mixed surface/volume scattering. Classification uses HV/HH backscatter ratios
- **Sub-Resolution Detection:** For targets smaller than pixel resolution (~10-40m), sub-aperture analysis detects speckle divergence patterns indicating sub-pixel scatterers (growlers, fragmentation fields)

---

## Module B: The Brain (Predictive Drift Engine)

**Objective:** Propagate the iceberg's position forward in time based on environmental forces.

### The Technical Stack
- **Library:** OpenDrift (OpenBerg module)
- **Environmental Data:** Copernicus Marine (CMEMS) for ocean currents and wind vectors
- **Uncertainty Tracking:** Kalman filtering for position uncertainty propagation over prediction horizon

### The Math: The Momentum Balance

Assuming open-water conditions, the engine solves:

$$M \frac{d\vec{V}_i}{dt} = \vec{F}_{air} + \vec{F}_{water} + \vec{F}_{coriolis}$$

- **Air/Water Drag:** Quadratic drag law:

$$F = \frac{1}{2} \rho C_d A |V - V_i|(V - V_i)$$

where $\rho$ is fluid density, $C_d$ is drag coefficient, and $A$ is cross-sectional area.

- **Coriolis Force:** Accounts for Earth's rotation, causing icebergs to drift at ~30° right of wind direction in Northern Hemisphere.

---

## Module C: The Hands (Path Planning)

**Objective:** Find a path that minimizes risk while moving through a dynamic environment.

### The Technical Stack
- **Algorithm:** Time-Varying A* with maritime dynamics constraints
- **Implementation:** Custom Python path planner with COLREGs awareness
- **Grid:** Spatio-temporal costmap with 500m resolution, 1-hour time steps

### The Deep Tech

**Dynamic Cost Function:**

$$f(n) = g(n) + h(n) + R(t)$$

where $g(n)$ is path cost, $h(n)$ is heuristic distance to goal, and $R(t)$ is time-varying risk from predicted iceberg positions.

**Uncertainty-Aware Risk:** Grid cell costs use Gaussian distributions centered on predicted iceberg positions. Risk bubbles expand with prediction horizon (e.g., ±500m at 6 hours, ±2km at 24 hours) to account for drift model uncertainty.

**Maritime Constraints:** Planner respects ship dynamics (turning radius, momentum) and COLREGs rules when encountering other vessels.

---

## Validation Strategy

TANS is validated using historical data:

1. **Detection Validation:** Statoil/C-CORE labeled SAR dataset for classification accuracy
2. **Drift Validation:** Canadian Ice Service iceberg tracking data (2020-2025) to compare predicted vs. actual positions over 6-24 hour windows
3. **Path Validation:** Simulated scenarios with actual iceberg distributions from Baffin Bay and Davis Strait

**Target Metrics:** Detection recall >85% for icebergs >50m, position prediction RMSE <2km at 24 hours.

---

## Why This Matters

TANS bridges the critical gap in Arctic maritime navigation, enabling:
- **Tactical decision support** for 6-12 hour planning windows in the 5-50km range
- **Physics-based drift prediction** accounting for wind, currents, and Coriolis effects
- **Risk-aware path planning** for Arctic patrol vessels and commercial shipping
- **Maritime compliance** with COLREGs for multi-vessel scenarios

---

## Technical Highlights

- 🛰️ **SAR Processing:** Dual-polarization analysis for object classification
- 🧠 **Physics-Based Prediction:** Multi-force momentum balance modeling
- 🗺️ **Dynamic Path Planning:** Time-varying risk-aware navigation
- ⚓ **Maritime Compliance:** COLREGs-aware routing algorithms

---

*Developed for QHacks 2026*