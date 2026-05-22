# PitWall Build Roadmap

## 1. Exploratory Data Analysis
- [x ] Inspect each DataFrame (lap_times, pit_stops, cautions, lead_changes, results)
- [x ] Plot lap-time distributions — green-flag laps cluster around one peak, pit-stop and caution laps form a long right tail
- [x ] Plot a full lap-time-by-lap timeline to see the race shape (cautions, pit cycles, lead battles)
- [ ] Identify outliers, nulls, weird values — note them
- [ ] Build a "data dictionary" for your future self: what each column means in your terms, not pynascar's

## 2. Build Foundational Sub-Models
Each becomes a probability distribution that feeds into the Monte Carlo engine.

### 2.1 Tire Degradation Model
- [ ] Fit lap-time-as-function-of-tire-age using clean green-flag laps only
- [ ] Linear or exponential; pick the simpler one that fits the data
- [ ] Capture both mean degradation rate AND variance around it
- [ ] Stretch: per-driver variance (better drivers preserve tires)

### 2.2 Fuel Consumption Model
- [ ] Compute average laps per tank at this track from observed pit cycles
- [ ] Identify the fuel window — max laps before a car HAS to pit
- [ ] Deterministic is fine for v0.1

### 2.3 Pit Stop Time Model
- [ ] From pit_stops DataFrame: distribution of total durations
- [ ] Mean and standard deviation
- [ ] Distinguish 4-tire vs 2-tire vs fuel-only if data supports

### 2.4 Caution Probability Model (Bayesian Piece)
- [ ] Use PyMC (or simple frequency counts for v0.1)
- [ ] Model P(caution in next N laps | current lap, race stage, cautions so far)
- [ ] Start with a flat prior per track, update with observed cautions
- [ ] Hardest and most interesting piece — the JD's bullseye

### 2.5 Caution Duration Model
- [ ] Distribution of caution lengths (short tracks average 5-7 laps)
- [ ] Simple normal or empirical sampling

### 2.6 Position-After-Pit Model
- [ ] When you pit and others don't, where do you cycle back to?
- [ ] Computed from gap-to-leader and field spacing
- [ ] Simplified for v0.1: positions cycle by stop order

## 3. Build the Monte Carlo Engine

### 3.1 Race State Representation
- [ ] A struct/class with: current_lap, fuel_level, tire_age, position, gap_to_leader, on_pit_road, last_pit_lap, flag_state

### 3.2 Single-Race Simulation (Inner Loop)
- [ ] For each lap: roll random variables, update state, compute lap time
- [ ] Trigger pit stops when strategy dictates
- [ ] When cautions fire, handle the open pit window and position cycling
- [ ] Continue until race ends, return final position

### 3.3 Outer Loop
- [ ] Wrap inner loop in `for _ in range(N)` where N = 10,000
- [ ] Collect all final positions
- [ ] Aggregate into distribution

### 3.4 Output Format
- [ ] Mean position, std dev, percentiles
- [ ] P(top 5), P(top 10), P(top 15)
- [ ] Best/worst case finishes

## 4. Strategy Decision Layer

### 4.1 Define What a "Strategy" Is
- [ ] Planned pit laps (e.g., pit on 120, 240, 360)
- [ ] Tire choice per stop (4-tire vs 2-tire vs fuel-only)
- [ ] Optional reactive rules ("pit on next caution after lap X")

### 4.2 Generate Candidate Strategies
- [ ] Hand-coded set of 3-5 reasonable strategies for v0.1
- [ ] Later: programmatic generation across a parameter grid

### 4.3 Decision Logic
- [ ] Run Monte Carlo for each candidate strategy
- [ ] Compare distributions
- [ ] Pick best by expected finish OR risk-adjusted (e.g., highest 25th percentile)

## 5. Visualization

### 5.1 Race Trace
- [ ] Lap times by lap; mark cautions, pit stops, lead changes

### 5.2 Strategy Comparison
- [ ] Box plot or violin plot of finishing position per strategy

### 5.3 Decision Dashboard
- [ ] Current race state + recommended strategy
- [ ] Probability table per strategy
- [ ] Risk metrics side by side

## 6. Validation

### 6.1 Replay Historical Race
- [ ] Feed in the actual strategies drivers used
- [ ] Check whether predicted finish distributions cover the actual finishes
- [ ] Iterate model until predictions are reasonable

### 6.2 Sanity Checks
- [ ] Average simulated lap times match reality
- [ ] Caution frequency matches reality
- [ ] No absurd outputs (negative positions, positions > field size)

## 7. Polish & Ship

### 7.1 Repo Hygiene
- [ ] README with project description, methodology, results, charts
- [ ] Examples folder with a runnable demo
- [ ] Tests for the core simulation engine
- [ ] Requirements/environment pinned (`requirements.txt` or `pyproject.toml`)

### 7.2 Writeup
- [ ] Medium post or expanded GitHub README
- [ ] Lead with the most interesting finding
- [ ] Explain the Bayesian caution model in plain English
- [ ] Include charts and a sample strategy comparison

### 7.3 Outreach
- [ ] LinkedIn post with #motorsports #montecarlo
- [ ] Connect with TRD engineers; share with a thoughtful note
- [ ] Optional: direct email to hiring manager with the repo link

## Future (v2) Expansion
- [ ] Per-driver competitor models (Hamlin manages tires differently than Reddick)
- [ ] Full-field simulation (not just one car against an abstract field)
- [ ] Real-time mode (consume live timing data during a race)
- [ ] Rust hot loop via PyO3 (the JD signal)
- [ ] Multi-track training (generalize the caution model across short tracks, intermediates, superspeedways)

---

**Scope markers:**
- Phases 1–3 = v0.1 (minimum viable simulator)
- Phases 4–5 = v1 (decision-quality output)
- Phase 6 = makes it credible (don't skip)
- Phase 7 = makes it visible