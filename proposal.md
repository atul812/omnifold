# GSoC 2026 Proposal  
## Publication of OmniFold Weights


## 1. Personal Information

**Name:** Atul Kumar  
**University:** RNS Institute of Technology, Bengaluru  
**Degree:** B.E. in Information Science and Engineering  
**Year:** Third Year  

---

## 2. About Me

I am Atul Kumar, a third year undergraduate student pursuing B.E. in Information Science and Engineering at RNS Institute of Technology, Bengaluru. I am deeply interested in Machine Learning and Software Engineering, with a growing focus on building systems that are scalable, interpretable, and useful in real world scenarios.

My primary programming language is Python. I am comfortable working with tools such as NumPy, Pandas, and Jupyter notebook. I have experience building and experimenting with machine learning algorithms. Alongside this, I have a good knowledge of web technologies such as HTML, CSS, and JavaScript, which I have used to build user interfaces for projects.

I have actively participated in hackathons which has helped me improve my problem solving skills and ability to work on practical, time bound projects. I am also involved in multiple developer communities on Discord.

I have also gained experience through open source contributions, where I have worked on debugging, improving existing codebases, and understanding real world project structures. This has helped me to develop skills in reading and understanding unfamiliar code, following contribution guidelines, and writing maintainable code.

What particularly interests me about this project is the intersection of machine learning and scientific software design. This project aligns strongly with my interest as it focuses on standardization, data design, and usability in a scientific context.

I am eager to learn more about high energy physics workflows and contribute meaningfully by building tools that improve the usability and reproducibility of modern analysis techniques.


---

## 3. Abstract

Modern unfolding techniques such as OmniFold use machine learning to produce per-event weights instead of traditional binned histograms. While this enables flexible reinterpretation of results, it also introduces challenges in standardizing how results are stored, documented, and shared.

Currently, there is no consistent framework for publishing OmniFold outputs in a way that ensures reproducibility and usability. This project aims to design a structured and standardized system for representing OmniFold results, including per-event weights, metadata, and optional model information.

The project will define data and metadata specifications, implement a reference Python API for loading and applying weights, and provide validation and example workflows. The final outcome will enable seamless reuse and reinterpretation of OmniFold-based analyses and facilitate integration with HEPData.

---

## 4. Benefits to the Community

This project addresses a critical gap in the publication of machine-learning–based physics results.

Key benefits include:

- **Reproducibility:** Clear metadata ensures that results can be understood and reused correctly.
- **Standardization:** Establishes a consistent format across analyses and experiments.
- **Usability:** Provides tools for physicists to easily apply weights and compute observables.
- **Interoperability:** Enables compatibility with HEPData for broader accessibility.
- **Future-proofing:** Supports evolving ML-based workflows in high-energy physics.

---

## 5. Deliverables

By the end of the project, the following deliverables will be produced:

- A **standardized schema** (YAML) for OmniFold metadata
- A **defined structure** for per-event weight storage (HDF5-based)
- A **Python package or API** to:
  - Load OmniFold outputs
  - Apply weights to datasets
  - Compute observables
  - Generate plots
- A **validation framework** for checking correctness
- **End-to-end examples** demonstrating:
  - Publication
  - Reuse
  - Reinterpretation
- Initial **HEPData integration guidelines** (stretch goal)

---

## 6. Technical Approach

### 6.1 Problem Understanding

From the evaluation task, I observed that current OmniFold outputs:

- Contain large datasets with many weight columns
- Lack clear separation between observables and weights
- Do not include sufficient metadata
- Have inconsistent structures across different files

This makes reuse difficult and introduces ambiguity.

The core objective is to define a system that ensures:

- Clear structure
- Minimal ambiguity
- Ease of reuse

---

### 6.2 Data & Metadata Specification

A YAML-based metadata schema will be designed to describe:

- Dataset provenance (generator, simulation, selection)
- Observable definitions (name, meaning, units)
- Weight definitions (nominal and systematic)
- Normalization and scaling information

The schema will distinguish between:

- **Required fields** (for reinterpretation)
- **Optional fields** (for full reproducibility)

---

### 6.3 Per-Event Weight Format

A standardized structure for storing weights will be defined using HDF5:

- Consistent naming conventions:
  - `weights_nominal`
  - `weights_<systematic_name>`
- Alignment of indices across observables and weights
- Support for systematic variations

The design will ensure scalability to large datasets.

---

### 6.4 Model & Training Metadata

A minimal set of model-related metadata will be included:

- OmniFold version
- Number of iterations

Optional extensions may include:

- Architecture details
- Training parameters

This ensures a balance between lightweight reuse and full reproducibility.

---

### 6.5 User-Facing Python API

A lightweight Python interface will be developed to:

- Load OmniFold outputs and metadata
- Apply weights to event data
- Compute histograms and observables
- Handle systematic variations

The API will prioritize simplicity and usability.

---

### 6.6 Validation Framework

Standard validation procedures will be implemented:

- Normalization checks
- Stability across systematic variations
- Basic consistency checks

These tools will help ensure correctness of published results.

---

### 6.7 HEPData Integration (Stretch Goal)

If time permits:

- Define mapping of OmniFold outputs to HEPData format
- Provide submission templates
- Demonstrate example integration

---

## 7. Timeline (175 Hours)

The project will be executed over ~16 weeks with incremental deliverables.

---

### Phase 1: Familiarization & Requirement Analysis (Weeks 1–2)

- Study OmniFold workflow and repository
- Analyze existing weight files
- Refine gap analysis

**Output:** Clear requirements and problem definition

---

### Phase 2: Metadata & Schema Design (Weeks 3–4)

- Design YAML metadata schema
- Define required and optional fields

**Output:** metadata specification and documentation

---

### Phase 3: Data Format Standardization (Weeks 5–6)

- Define HDF5 structure for weights
- Establish naming conventions

**Output:** Standardized format specification

---

### Phase 4: Prototype Implementation (Weeks 7–9)

- Implement utilities to load and apply weights
- Extend histogram functionality

**Output:** Initial working prototype

---

### Phase 5: API Development (Weeks 10–12)

- Build user-facing Python API
- Add plotting and analysis support

**Output:** Functional API with examples

---

### Phase 6: Validation Framework (Weeks 13–14)

- Implement validation checks
- Provide example validation workflows

**Output:** Validation tools

---

### Phase 7: Documentation & Examples (Weeks 15–16)

- Create end-to-end examples
- Write documentation

**Output:** Complete usage guide and examples

---

## 8. Previous Work

As part of the evaluation task, I have:

- Explored OmniFold output files
- Identified gaps in structure and metadata
- Designed a metadata schema
- Implemented a weighted histogram function with validation

---

## 9. Post GSoC 

I intend to continue contributing to this project beyond the GSoC period, particularly in refining and extending the proposed standard based on usage and feedback.

I have planned to:
- Incorporate feedback from users and mentors to improve the metadata schema and data format
- Extend the Python API with more advanced analysis features and better usability
- Improve documentation and examples to support wider adoption

I would be interested to continue to open source contributions in this area and collaborate with the community to further improve reproducibility and usability in ML based scientific workflows.

--- 

## 10. Conclusion

I am excited about the opportunity to contribute to work closely with the mentors to build an impactful solution. The project aims to define a structured and practical framework for publishing OmniFold results. By focusing on standardization, usability, and reproducibility, it will enable broader adoption and reuse of machine learning based unfolding techniques.
