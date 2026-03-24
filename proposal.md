# GSoC 2026 Proposal
## Publication of OmniFold Weights
**Organization:** CERN-HSF

---

## 1. Basic Information

### 1.1 Personal Details

| Field | Details |
|---|---|
| **Name** | Atul Kumar |
| **Major** | Information Science and Engineering |
| **Degree** | Bachelor of Engineering |
| **Year** | Third Year |
| **Institute** | RNS Institute of Technology, Bengaluru, India |
| **Resume** | [View Resume](https://drive.google.com/file/d/1xb9fnzsN9kn2UHB9gpcw4bhz2DN18lx8/view?usp=sharing) |
| **GitHub** | [github.com/atul812](https://github.com/atul812) |
| **Evaluation Task** | [github.com/atul812/omnifold](https://github.com/atul812/omnifold) |
| **Time Zone** | Indian Standard Time (UTC +5:30) |

---

### 1.2 About Me

I am Atul Kumar. I'm a third year undergraduate student at RNS Institute of Technology, Bengaluru, pursuing a Bachelor of Engineering in Information Science and Engineering.

My primary language is Python. I work with it for data processing, structured file handling, and algorithm design. I am comfortable with libraries including NumPy, Pandas, h5py, and Matplotlib, and I have used Jupyter notebooks for exploratory analysis. I have a working understanding of YAML and JSON for structured data representation, and have basic familiarity with HTML, CSS, and JavaScript for web related tasks.

My interest in machine learning led me to this project. I have explored how ML models are trained and how their outputs can be consumed by downstream systems. This interest in the intersection of ML and reusable outputs is what drew me toward OmniFold when I got to know that it is a system where the ML output is the scientific result itself.

For the evaluation task, I loaded and inspected the three provided HDF5 files (`multifold.h5`, `multifold_sherpa.h5`, `multifold_nonDY.h5`), performed a structural gap analysis, designed a YAML metadata schema, and implemented a self contained `weighted_histogram()` function with edge case tests. This work gave me a good understanding of what the project needs to solve.

I actively participate in hackathons and have contributed to open source projects which has improved my ability to read, adapt, and contribute meaningfully to existing codebases. I am comfortable working asynchronously with mentors across time zones and prefer clear documentation and regular check-ins.

---

## 2. Project

### 2.1 Abstract

The OmniFold algorithm uses machine learning to perform unfolding in high energy physics. Unlike traditional methods that produce fixed binned histograms, OmniFold outputs per-event weights which is one weight per event that encode the correction from detector level measurements back to particle level. This flexibility enables users to reinterpret results for any observable, not just those published by the original analysis.

However, this flexibility comes with a significant practical problem: there is currently no standard for how these weights should be stored, documented, or shared. From analyzing the evaluation task files, I found that the nominal file (`multifold.h5`) contains 418,014 events with 200 columns —> 25 observable columns and 175 weight columns, yet contains no metadata whatsoever. There is no information about which generator was used, how many OmniFold iterations were run, what the systematic variations mean physically, or how the weights should be normalized. The other two files (`multifold_sherpa.h5` and `multifold_nonDY.h5`) have entirely different column counts, making cross-file usage ambiguous without external documentation.

This project addresses that gap by defining a standardized system for publishing OmniFold results. The outcome will be a Python package that allows any physicist to load, apply, validate, and reinterpret OmniFold weights without needing access to the original analysis team or codebase.

---

### 2.2 Motivation

The publication of scientific results is not just about sharing numbers, it is about sharing them in a form that others can actually use. In traditional high energy physics analyses, a binned histogram is self-contained: it has values, uncertainties, and axis labels. A physicist can pick it up and use it immediately.

Per-event weights are fundamentally different. They are meaningless without knowing what observable they belong to, how they were produced, what systematic variations they encode, and how they should be normalized. The evaluation task made this concrete for me: a file with 175 weight columns and no metadata is effectively unusable for anyone outside the original team.

I am motivated by the problem of making ML based scientific outputs reproducible and reusable. This requires thinking carefully about what information a user needs, how it should be structured, and what tools make it easy to consume. That combination of software design thinking and scientific usefulness is exactly what drew me to this project.

Additionally, as someone interested in machine learning, I find it meaningful that OmniFold is a case where ML is not a black box but a tool whose output directly feeds scientific publications. Standardizing how that output is shared ensures that the benefits of ML in physics can be multiplied across the community, not isolated within individual experiments.

---

### 2.3 Why CERN-HSF?

CERN has been a long term aspiration for me. Tim Berners Lee invented the World Wide Web at CERN. It is a technology that now underlies virtually all of modern software. CERN is a place where rigorous scientific thinking and cutting edge software engineering coexist and reinforce each other. That is the environment I want to learn and grow in.

CERN-HSF specifically addresses the software infrastructure that makes modern physics experiments possible. The fact that HSF projects are practical, open, and community driven makes it the right place to contribute as a student. I am not just contributing to a codebase but I am contributing to the infrastructure that physicists worldwide depend on.

This project in particular is a good fit for where I am now. It requires me to code, but more importantly, it requires me to think about what information matters, how it should be structured, and how a physicist, who did not run the original analysis would interact with the result. That kind of design thinking with real scientific needs is exactly the kind of work I want to do at CERN.

---

### 2.4 Proposed Deliverables

By the end of the project, the following will be produced:

1. **Metadata Specification** — A formal, versioned YAML schema describing OmniFold results, with clear distinction between required and optional fields, and documentation of every field's purpose.

2. **Per-Event Weight Format** — A standardized HDF5 (and Parquet) structure for storing nominal weights, systematic variations, and bootstrap replicas, with enforced naming conventions and indexing alignment.

3. **Python Package (`omnifold-pub`)** — A user-facing library providing:
   - `OmniFoldResult.load()` — load weights and metadata from HDF5/Parquet + YAML
   - `get_weights(variation="nominal")` — retrieve weight arrays by name
   - `histogram(observable, bins, weights)` — compute weighted histograms
   - `plot(...)` — generate publication-quality figures
   - Uncertainty propagation across systematic variations

4. **Validation Framework** — Standardized checks including normalization verification, closure tests, cross-file consistency, and iteration stability.

5. **Observable Definition Format** — A structured way to describe physics observables including their physical meaning, units, phase-space restrictions, and binning.

6. **End-to-End Jupyter Notebooks** — Demonstrating the full workflow: publish → load → apply weights → compute observables → plot → validate.

7. **HEPData Integration Guidelines** *(stretch goal)* — Mapping OmniFold outputs to HEPData submission format, with templates and an example submission.

---

### 2.5 Plan of Action

This section describes the technical approach for each component of the project, with concrete design decisions and implementation details.

---

#### 2.5.1 Data and Metadata Specification

**The Problem:**
From my analysis of the evaluation task files, the core issue is the complete absence of metadata. A physicist loading `multifold.h5` sees 175 columns with names like `weights_theoryPSjet` or `weights_trackPtScale` but there is no information about:
- Which generator produced the events (MG5 vs. Sherpa vs. Pythia)
- How many OmniFold iterations were run
- What each weight column physically represents
- Whether weights are multiplicative or additive
- What event selections were applied
- What normalization convention is used

**The Solution:**
A YAML metadata schema that accompanies every published weight file. The schema will have two tiers: **required fields** needed for basic reinterpretation, and **optional fields** for full reproducibility.

Below is a concrete draft of the schema, designed around the actual structure of the evaluation task files:

```yaml
omnifold_metadata:
  schema_version: "1.0"

  dataset:
    name: "Z+jets pseudodata (ATLAS-style)"
    description: "OmniFold unfolding of Z+jets events at 13 TeV"
    generator: "MadGraph5_aMC@NLO"
    detector_simulation: "Delphes"
    selection: "pT_Z > 20 GeV, |eta_jet| < 2.5, at least 2 jets"
    n_events: 418014

  omnifold:
    version: "0.1.0"
    n_iterations: 5
    weight_column_nominal: "weights_nominal"

  observables:
    - name: "pT_jet1"
      description: "Leading jet transverse momentum"
      units: "GeV"
    - name: "eta_jet1"
      description: "Leading jet pseudorapidity"
      units: "dimensionless"
    - name: "mjj"
      description: "Dijet invariant mass"
      units: "GeV"

  systematics:
    - name: "weights_theoryPSjet"
      description: "Parton shower scale variation (jet)"
      type: "weight_variation"
      file: "multifold.h5"
    - name: "weights_trackPtScale"
      description: "Track pT scale uncertainty"
      type: "weight_variation"
      file: "multifold.h5"
    - name: "multifold_sherpa"
      description: "Alternative generator (Sherpa) systematic"
      type: "alternative_sample"
      file: "multifold_sherpa.h5"
    - name: "multifold_nonDY"
      description: "Alternative sample composition (EW Zjj + diboson)"
      type: "alternative_sample"
      file: "multifold_nonDY.h5"

  normalization:
    cross_section_pb: 831.76
    luminosity_ifb: 137.0
    convention: "per_event_weight"
```

This schema was designed around three decisions I made during the evaluation task:
- Separating column-level systematics (within a single file) from file-level alternative samples (the Sherpa and nonDY files) because these have different column structures and should be treated differently
- Including `schema_version` to allow future evolution without breaking backward compatibility
- Keeping normalization explicit, since the evaluation files provided no indication of whether weights are already normalized or require cross-section scaling

---

#### 2.5.2 Per-Event Weight Format

**HDF5 Structure:**

The current structure (a single flat Pandas DataFrame stored under key `"df"`) makes it difficult to distinguish observables from weights programmatically, and provides no logical grouping. The standardized structure will use HDF5 groups:

```
omnifold_output.h5
├── metadata/          # JSON-serialized metadata (mirrors YAML)
├── observables/
│   ├── pT_jet1        # shape: (N_events,), dtype: float32
│   ├── eta_jet1
│   ├── phi_jet1
│   ├── mjj
│   └── ...            # all 25 kinematic columns
└── weights/
    ├── nominal        # shape: (N_events,), dtype: float64
    ├── theoryPSjet    # systematic variations
    ├── theoryPSsoft
    ├── theoryPDF
    ├── trackPtScale
    ├── lumi
    └── ...            # all systematic weight columns
```

**Parquet Alternative:**

For users working in environments where Parquet is preferred (e.g., Spark-based workflows or cloud storage), a Parquet format will also be supported. The Parquet output will use a flat column structure with a `__group__` prefix convention (`obs__pT_jet1`, `weights__nominal`) along with a sidecar metadata JSON file.

**Naming Conventions:**
- Observables: plain physics names (`pT_jet1`, `eta_jet1`)
- Nominal weight: always `nominal`
- Systematic weights: short descriptive names matching the metadata YAML
- No spaces, no ambiguity between observables and weights (enforced by group separation in HDF5)

---

#### 2.5.3 Python API Design

The user-facing API will prioritize simplicity. A physicist should be able to load and use results in 5 lines of code.

```python
from omnifold_pub import OmniFoldResult

# Load weights + metadata
result = OmniFoldResult.load("multifold.h5", metadata="metadata.yaml")

# Get nominal weights
weights = result.get_weights(variation="nominal")

# Compute and plot a weighted histogram
hist, edges = result.histogram("pT_jet1", bins=20, weights=weights)
result.plot("pT_jet1", bins=20, label="Unfolded (nominal)", show_systematics=True)
```

**Internal structure of the API:**

```
omnifold_pub/
├── __init__.py
├── loader.py         # OmniFoldResult.load() — handles HDF5/Parquet + YAML
├── weights.py        # get_weights(), list_variations(), apply_selection()
├── histogram.py      # histogram(), compute_observable()
├── plotting.py       # plot(), plot_ratio(), plot_systematics()
├── validation.py     # normalization_check(), closure_test(), stability_check()
└── schema.py         # YAML schema validation using jsonschema or pydantic
```

**Uncertainty propagation:**
For systematic variations, the API will compute envelope uncertainties by default:
```python
result.plot("pT_jet1", show_systematics=True)
# Internally: computes histogram for each systematic, takes max deviation as band
```

---

#### 2.5.4 Validation Framework

Three standard validation checks will be implemented:

1. **Normalization Check** : Verify that the sum of nominal weights matches the expected total (cross-section × luminosity). A configurable tolerance will be used (default: 1%).

2. **Closure Test** : Apply the unfolded weights to the generator level truth and verify that known observables are reproduced within statistical uncertainty.

3. **Iteration Stability** : For analyses that publish multi iteration weights, verify that weights stabilize across iterations and flag anomalous divergence.

Each check will produce a structured pass/fail report with numerical diagnostics, not just a boolean.

---

#### 2.5.5 Observable Definitions

A companion YAML format for describing observables will be defined, separating observable metadata from weight metadata:

```yaml
observables:
  - name: "pT_jet1"
    description: "Transverse momentum of the leading jet"
    units: "GeV"
    phase_space: "pT > 20 GeV, |eta| < 2.5"
    default_bins: [20, 40, 60, 80, 100, 130, 160, 200, 260, 320, 400]
    log_scale: true
```

Reference Python implementations will be provided for computing each observable from raw four-momentum inputs, enabling users to apply the published weights to their own datasets.

---

#### 2.5.6 HEPData Integration *(Stretch Goal)*

If time allows after completing the core deliverables, I will work on:
- Mapping the standardized OmniFold HDF5 output to HEPData's submission YAML format
- Providing a submission template
- Demonstrating an example upload using public ATLAS Z+jets data

This is listed as a stretch goal in the project description and will only be attempted after all primary deliverables are complete and tested.

---

### 2.6 Timeline

**Total hours:** 175  
**Availability:** 20–30 hours/week (see Section 3 for constraints)  
**Coding period:** June 2 – September 29, 2026

> **Note:** My 6th semester final exams end on **June 12, 2026**. During Weeks 1–2 of the coding period, I will be limited to approximately 10 hours/week. From June 13 onward, I will be available for 20–25 hours/week dedicated to GSoC.

---

#### Community Bonding Period (May 8 – June 1)

*No coding. Full study and setup.*

- Complete reading of the OmniFold paper (arXiv:1911.09107) and the MultiFold extension
- Explore the `omnifold` PyPI package in depth —> understand the iterative two-step reweighting procedure
- Study HEPData submission format and existing YAML conventions
- Set up development environment, finalize milestones with mentors
- Identify any open questions about the evaluation task files to discuss with mentors: Tanvi and Benjamin

---

#### Phase 1: Deep Analysis and Specification Design (Weeks 1–3 | ~30 hours)

*Weeks 1-2 limited to 10 hrs/week due to exams; Week 3 full pace.*

| Task | Hours |
|---|---|
| Extend gap analysis: document all ambiguities across the three evaluation files | 5 |
| Finalize YAML metadata schema with mentor feedback | 8 |
| Define HDF5 group structure and naming conventions | 7 |
| Write formal specification documents for both formats | 10 |

**Output:** Finalized `metadata_spec.md`, `weight_format_spec.md`, and validated YAML schema

---

#### Phase 2: Core Data Format Implementation (Weeks 4–6 | ~35 hours)

| Task | Hours |
|---|---|
| Implement HDF5 writer: convert flat DataFrame to structured group format | 10 |
| Implement HDF5 reader with schema validation | 8 |
| Implement Parquet writer and reader with sidecar metadata | 10 |
| Write unit tests for all I/O functions | 7 |

**Output:** Stable, tested I/O layer. Any published weights can be converted to/from the standardized format.

---

#### Phase 3: Python API Development (Weeks 7–9 | ~40 hours)

| Task | Hours |
|---|---|
| Implement `OmniFoldResult` class with `load()`, `get_weights()`, `list_variations()` | 12 |
| Implement `histogram()` with proper weight handling, extending evaluation task function | 8 |
| Implement `plot()` with uncertainty bands and systematic envelopes | 10 |
| Implement `apply_selection()` for phase-space filtering | 5 |
| Write integration tests using evaluation task files | 5 |

**Output:** Functional API, importable as `omnifold_pub`, covering all core use cases.

---

#### Phase 4: Validation Framework (Weeks 10–11 | ~25 hours)

| Task | Hours |
|---|---|
| Implement normalization check with configurable tolerance | 8 |
| Implement closure test procedure | 8 |
| Implement iteration stability diagnostic | 5 |
| Write structured report output (JSON + human-readable summary) | 4 |

**Output:** `omnifold_pub.validation` module with documented pass/fail criteria.

---

#### Phase 5: Observable Definitions and Plotting Polish (Weeks 12–13 | ~20 hours)

| Task | Hours |
|---|---|
| Define observable YAML format and implement parser | 6 |
| Provide reference Python implementations for key Z+jets observables | 6 |
| Polish plotting utilities: ratio panels, systematic bands, publication style | 8 |

**Output:** Observable definition format + polished, publication-quality plots.

---

#### Phase 6: End-to-End Examples and Documentation (Weeks 14–15 | ~15 hours)

| Task | Hours |
|---|---|
| Write Jupyter notebook: publication workflow (produce → format → validate) | 5 |
| Write Jupyter notebook: reinterpretation workflow (load → apply → new observable) | 5 |
| Write API reference documentation (docstrings + Sphinx or MkDocs) | 5 |

**Output:** Complete usage guide with runnable notebooks.

---

#### Phase 7: Buffer, Review, and Stretch Goal (Week 16 | ~10 hours)

| Task | Hours |
|---|---|
| Address mentor feedback and fix open issues | 5 |
| Begin HEPData integration template (stretch goal) | 5 |

**Output:** Final polished package, ready for community use.

---

**Hours Summary:**

| Phase | Weeks | Hours |
|---|---|---|
| Community Bonding | Pre-Week 1 | — |
| Phase 1: Analysis & Specification | 1–3 | 30 |
| Phase 2: Data Format Implementation | 4–6 | 35 |
| Phase 3: Python API Development | 7–9 | 40 |
| Phase 4: Validation Framework | 10–11 | 25 |
| Phase 5: Observable Definitions | 12–13 | 20 |
| Phase 6: Examples & Documentation | 14–15 | 15 |
| Phase 7: Buffer & Stretch Goal | 16 | 10 |
| **Total** | | **175** |

---

## 3. Commitments

I am a third year undergraduate student with the following concurrent commitments during the GSoC period (June–October 2026):

| Commitment | Hours/Week | Notes |
|---|---|---|
| **GSoC — this project** | 20–25 hrs | Primary commitment from June 13 |
| **6th semester exams** | — | End June 12, 2026 |
| **7th semester coursework** | — | Begins July 2026; manageable alongside GSoC |
| **College major project** | ~11 hrs | Submission deadline Nov–Dec 2026; no conflict |
| **Research work (under guide)** | ~7–8 hrs | Publication timeline flexible; no fixed deadline |

My 6th semester final exams conclude on **June 12, 2026**. For the first two weeks of the coding period (June 2–12), I will contribute approximately 10 hours/week. From June 13 onward, I will dedicate 20–25 hours per week exclusively to GSoC. The timeline in Section 2.6 accounts for this constraint.

My major project and research work have no critical deadlines before November 2026, and neither involves full-time commitment. I have successfully managed parallel technical work before and am confident in my ability to maintain consistent GSoC progress throughout the summer.

I am available on email, and video calls during Indian Standard Time business hours and I am comfortable adjusting to mentor availability in US time zones for scheduled meetings.

---

## 4. Contributions

### 4.1 Evaluation Task

As part of applying for this project, I completed all three parts of the evaluation task provided by the mentors at [github.com/wamorkart/omnifold-hepdata](https://github.com/wamorkart/omnifold-hepdata).

**My solution:** [github.com/atul812/omnifold](https://github.com/atul812/omnifold)

The repository contains:

---

**`gap_analysis.md` — Structural Exploration and Gap Identification**

I loaded all three HDF5 files and documented their structure:

| File | Rows | Columns |
|---|---|---|
| `multifold.h5` (nominal) | 418,014 | 200 (25 observables + 175 weights) |
| `multifold_sherpa.h5` | 326,430 | 51 |
| `multifold_nonDY.h5` | 433,397 | 26 |

Key gaps I identified:
- **No metadata** in any file : no generator information, no OmniFold version, no iteration count
- **No semantic labeling** : columns named `weights_theoryPSjet` contain no indication of whether they are multiplicative, what the variation means physically, or whether they should be applied together
- **Inconsistent structure across files** : the three files have entirely different column counts, making programmatic cross-file analysis impossible without external documentation
- **No normalization information** : no cross-section or luminosity values embedded anywhere
- **No event selection documentation** : a downstream user cannot reproduce the phase-space cuts that were applied

---

**`metadata.yml` and `schema_design.md` — Schema Design**

I designed a YAML metadata schema that addresses the gaps above, with a justification document explaining:
- Why I separated systematic types (column-level vs. file-level alternative samples)
- Why `schema_version` is a required field for future compatibility
- What fields a user who did not run the original analysis would need to interact with the result correctly

---

**`weighted_histogram.py` — Coding Exercise**

I implemented a self-contained `weighted_histogram()` function that:
- Accepts a Pandas DataFrame, an observable column name, and a weight column name
- Uses `sqrt(N)` as a sensible default binning strategy
- Produces a matplotlib plot when `plot=True`
- Returns `(hist, bin_edges)` for programmatic use

I included four test cases covering the most important edge cases:
1. **Basic unweighted case** : verify histogram integrates to total event count
2. **Weighted sum verification** : confirm that weights are actually applied and summed correctly
3. **Missing column error handling** : ensure a `ValueError` is raised (not a silent failure) when the observable or weight column does not exist
4. **Empty DataFrame handling** : ensure a `ValueError` is raised before any computation on an empty input



---

## 5. Post GSoC

My intention is to continue contributing to this project after the GSoC period ends.

The most immediate next step would be working toward formal adoption of the metadata schema. A specification is only useful if it is used consistently, and the right path for that is getting feedback from physicists who publish OmniFold results and iterating on the schema based on real use cases.

Specifically, I plan to:
- Refine the YAML schema based on feedback from the broader ATLAS and CMS communities
- Extend Parquet support for cloud-native and distributed analysis workflows
- Contribute toward HEPData integration if it was not completed during GSoC
- Improve documentation and add more worked examples to support wider adoption

I see this project as a starting point, not a fixed deliverable. Standardization work is iterative by nature, the schema will need to evolve as new use cases emerge. I am interested in staying involved in that process and in continuing to collaborate with the CERN-HSF community beyond this summer.

---

*Thank you for reviewing my proposal. I am happy to answer questions or provide additional detail on any section.*
