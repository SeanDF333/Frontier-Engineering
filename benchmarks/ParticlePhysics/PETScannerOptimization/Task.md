# Particle Physics Engineering: PET Scanner Geometry and Cost Pareto Optimization

## 1. Task Background

Positron Emission Tomography (PET) is a crucial molecular imaging modality in nuclear medicine. Its core physical mechanism involves detecting positrons emitted by radioactive tracers (e.g., Fluorine-18) during $\beta^+$ decay. These positrons immediately undergo **antimatter annihilation** with surrounding electrons, releasing two **511 keV** gamma-ray photons traveling in almost exactly opposite directions (180°).



To capture these high-energy photons, a PET scanner is constructed with a ring of extremely expensive LYSO (Lutetium-yttrium oxyorthosilicate) scintillation crystals. When a pair of crystals detects photons within a nanosecond coincidence window, a Line of Response (LOR) is recorded.

## 2. The Engineering "Reality Gap" (The Impossible Triangle)

As the Chief Hardware Architect for a next-generation PET system, your task is to optimize the scanner's geometric dimensions to find the Pareto optimal solution among three conflicting physical and economic factors:

1. **System Sensitivity**:
   To stop highly penetrating 511 keV gamma rays, the crystals must be thick (large radial thickness $H$). Furthermore, extending the axial length $L$ and reducing the ring radius $R$ increases the solid angle coverage, capturing more photon pairs.
2. **Parallax Error and Spatial Resolution (DOI Effect)**:
   Thicker crystals (large $H$) combined with a smaller detector ring (small $R$) significantly increase the depth-of-interaction (DOI) uncertainty for obliquely incident gamma rays. 
   
   This effect causes severe spatial resolution degradation away from the center of the Field of View (FOV). Additionally, the single crystal cross-sectional width $W$ intrinsically limits the baseline spatial resolution.
3. **Strict Economic Budget (LYSO Cost)**:
   LYSO crystals are extremely expensive. Increasing $H$, $L$, or $R$ geometrically inflates the total LYSO crystal volume, quickly breaching the project's financial budget.

## 3. Decision Variables

The AI Agent must output a file named `solution.json` containing the following 4 continuous geometric variables (all units in millimeters, mm):

* `ring_radius` ($R$): Inner radius of the detector ring. (Search space: $300.0$ to $500.0$)
* `axial_length` ($L$): Axial length of the scanner. (Search space: $150.0$ to $300.0$)
* `crystal_thickness` ($H$): Radial thickness of the LYSO crystals. (Search space: $10.0$ to $30.0$)
* `crystal_width` ($W$): Cross-sectional width of a single crystal. (Search space: $2.0$ to $6.0$)

## 4. Physics Constraints & Scoring Logic

The evaluator script (`evaluator.py`) scores your design based on the following simplified physics model:

### A. Crystal Volume & Cost Penalty
The total crystal volume $V$ is approximated as an annular cylinder:
$$V = \pi \cdot ((R+H)^2 - R^2) \cdot L$$
If the total volume exceeds the budget constraint (e.g., $15,000,000 \text{ mm}^3$), a massive negative penalty is applied.

### B. Absolute Sensitivity Gain
According to the exponential attenuation law, the coincidence detection efficiency for a pair of 511 keV photons is $(1 - e^{-\mu H})^2$, where $\mu \approx 0.087 \text{ mm}^{-1}$ for LYSO.
Combined with the geometric solid angle approximation, the sensitivity score is proportional to:
$$S = \frac{L}{\sqrt{R^2 + (L/2)^2}} \cdot (1 - e^{-0.087 H})^2$$

### C. Spatial Resolution Penalty
The overall spatial resolution degradation $\Gamma$ is modeled by combining the intrinsic crystal width and the DOI parallax broadening:
$$\Gamma = \sqrt{W^2 + \left(200.0 \cdot \frac{H}{R}\right)^2}$$
A larger $\Gamma$ results in a heavier score deduction.

## 5. Output Format Requirement

The Agent must generate a valid `solution.json` in the current working directory, formatted as follows:

```json
{
  "ring_radius": 400.0,
  "axial_length": 200.0,
  "crystal_thickness": 20.0,
  "crystal_width": 3.0
}
```
**Goal**: Maximize the comprehensive score (Score = Sensitivity Gain - Resolution Penalty - Cost Penalty) without violating the total volume budget.