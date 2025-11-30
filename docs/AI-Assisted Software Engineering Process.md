# **AI-Augmented Model-Based Systems Engineering: A Comprehensive Process Framework for Hybrid-Language Development**

## **1\. Introduction: The Convergence of AI, MBSE, and Hybrid Architectures**

The landscape of software and systems engineering is undergoing a seismic shift, driven by the simultaneous maturation of Generative Artificial Intelligence (GenAI), the evolution of Model-Based Systems Engineering (MBSE) standards like SysML v2, and the increasing necessity of hybrid-language development environments. This report defines a rigorous, end-to-end process framework designed to navigate this complexity. It addresses the specific requirement of transforming abstract concepts into hardened production systems using AI as an accelerant, SysML as the source of truth, and a synchronized implementation strategy spanning flexible prototyping languages (Python) and robust production environments (MATLAB/Simulink).

### **1.1 The Engineering Context and Problem Statement**

Modern complex systems—ranging from autonomous vehicles and aerospace control systems to medical devices—require a synthesis of high-level algorithmic intelligence and low-level deterministic control. This creates a "Two-Language Problem" in engineering. Data scientists and algorithm designers predominantly utilize Python for its rich ecosystem of machine learning libraries (PyTorch, TensorFlow, Scikit-learn) and rapid iteration capabilities. Conversely, safety-critical implementation and embedded deployment often necessitate languages like C, C++, or model-based environments like MATLAB/Simulink, which offer rigorous static analysis, code generation, and certification support (e.g., ISO 26262, DO-178C).  
The traditional "throw-over-the-wall" approach, where a Python prototype is manually rewritten into production code by a separate team, is fraught with risk. It introduces translation errors, desynchronization between the design intent and the implementation, and significant delays in the verification loop. Furthermore, the initial phase of requirements gathering is often plagued by ambiguity, leading to the "blank page problem" where teams struggle to translate vague stakeholder needs into testable technical specifications.

### **1.2 The Proposed Solution Architecture**

The process framework detailed in this report establishes a "Single Source of Truth" (SSoT) architecture rooted in **SysML v2**, effectively bridging the gap between the fluidity of AI-assisted elicitation and the rigidity of safety-critical production.

* **AI as the Architect's Assistant:** Large Language Models (LLMs) are employed not just for code generation, but for *cognitive automation* in the early lifecycle phases—transforming concepts into structured IEEE 830 requirements, generating Work Breakdown Structures (WBS), and drafting test plans.  
* **SysML v2 as the Digital Thread:** Unlike graphical-only predecessors, SysML v2’s textual notation and standardized API allow it to serve as a computational backbone. It acts as the immutable contract that both the Python prototype and the MATLAB production code must satisfy, enabling automated synchronization and requirements traceability.  
* **Hybrid Implementation Strategy:** The process supports a dual-path implementation.  
  * *Path A (Rapid Prototyping):* AI-accelerated Python development for algorithmic verification.  
  * *Path B (Production Hardening):* Automated transition to MATLAB/Simulink or optimized C++ for target deployment, verified via automated equivalence testing against the Python prototype.

This report is structured to guide engineering leaders through every phase of this advanced lifecycle, providing actionable process descriptions, best practices, and technical insights derived from current research.

## **2\. Phase I: Concept to Technical Requirements (The AI Transformation)**

The first phase of the lifecycle addresses the transformation of a nebulous user concept into a rigorous technical specification. Traditionally, this is a human-intensive process vulnerable to communication gaps. By leveraging AI agents with specific prompt engineering patterns, this phase can be accelerated while simultaneously increasing the structural quality of the requirements.

### **2.1 AI-Driven Requirements Elicitation**

The "Concept of Operations" (ConOps) provided by stakeholders is often unstructured. The goal is to utilize AI to parse this input, identify missing information, and structure it into a formal Software Requirements Specification (SRS).

#### **2.1.1 The "Interviewer" Agent Workflow**

Research suggests that a single-shot prompt is insufficient for complex requirements engineering. Instead, an "Agentic Workflow" is required, where an AI agent is assigned the persona of a Senior Requirements Analyst.  
**Workflow Steps:**

1. **Ingestion:** The AI ingests the raw concept text, diagrams, or voice transcripts.  
2. **Decomposition:** The agent decomposes the concept into functional and non-functional categories.  
3. **Gap Analysis (The "Critic"):** A secondary AI process (or a "Critic" node in the agent chain) analyzes the decomposed list for violations of the INVEST principles (Independent, Negotiable, Valuable, Estimable, Small, Testable) and the INCOSE Guide for Writing Requirements.  
4. **Clarification Loop:** The AI generates a list of clarifying questions for the human stakeholder (e.g., "You mentioned 'fast response,' can you quantify the maximum latency in milliseconds?"). This iterative loop continues until the ambiguity score drops below a defined threshold.

#### **2.1.2 Advanced Prompt Engineering Patterns**

To achieve high-fidelity results, specific prompt patterns must be employed.

* **Chain of Thought (CoT):** Instructing the model to "think step-by-step" helps in deriving complex dependencies. For example: "First, identify the user actors. Second, identify the external systems. Third, list the data flows between them. Finally, write the requirements for each data flow.".  
* **Persona Adoption:** "Act as a Systems Engineer specializing in ISO 26262 safety standards. Review the following concept for a braking controller and identify potential safety hazards that must be mitigated by software requirements.".  
* **Constraint-Based Generation:** The prompt must enforce the syntax of the output. "Generate requirements in the format: 'REQ-ID: The shall \[Action\]\[Object\] within \[Constraint\]'." This strict formatting is crucial for downstream parsing into MBSE tools.

### **2.2 Structuring the SRS (IEEE 830 / ISO 29148\)**

The output of the elicitation phase is a structured SRS document. AI tools can automatically populate standard templates, ensuring compliance with industry standards like IEEE 830-1998 or ISO/IEC/IEEE 29148:2018.  
**Table 1: Automated Mapping of Concept Elements to SRS Sections**

| SRS Section (ISO 29148\) | Source Information (Concept) | AI Transformation Task | Verification Criteria |
| :---- | :---- | :---- | :---- |
| **1\. Scope** | "Idea," "Vision," "Goal" | Summarize intent; define system boundaries (Context Diagram description). | Clarity, alignment with stakeholder vision. |
| **2\. User Characteristics** | "Who is this for?" | Create User Personas; define operator skill levels. | Completeness of stakeholder identification. |
| **3\. Functional Requirements** | "What does it do?" | Convert distinct features into atomic "shall" statements with unique IDs. | Atomicity, traceability, lack of ambiguity. |
| **4\. Interface Requirements** | "What does it connect to?" | Define APIs, hardware I/O, communication protocols (e.g., CAN bus, REST). | Consistency with SysML Interface definitions. |
| **5\. Quality Attributes** | "How well does it do it?" | Quantify performance, reliability, security (NFRs). | Measurability (e.g., " \< 50ms latency"). |
| **6\. Safety Requirements** | "What if it fails?" | Derive safety goals and ASIL/SIL levels based on hazard analysis. | Compliance with ISO 26262/IEC 61508\. |

### **2.3 Transitioning to Data-Centric Requirements (ReqIF)**

A critical best practice in this process is to move away from static Word/PDF documents immediately. The AI should be directed to output the requirements in a structured data format such as **JSON**, **XML**, or **ReqIF** (Requirements Interchange Format).  
This structured output allows for:

1. **Direct Import:** Seamless ingestion into requirements management tools (DOORS, Jama, Polarion) or directly into the SysML v2 model as requirement def elements.  
2. **Traceability:** Automatic generation of traceability links between requirements and subsequent test cases or architecture blocks.  
3. **Version Control:** Storing requirements as code/data enables Git-based versioning, allowing teams to track "Requirement Drift" over time.

## **3\. Phase II: AI-Generated Planning and Estimation**

Once the technical requirements are solidified, the process moves to planning. This phase leverages AI's ability to recognize patterns in historical data to generate realistic project plans, work breakdown structures (WBS), and test strategies.

### **3.1 Automated Work Breakdown Structure (WBS) Generation**

The SRS provides the "What"; the WBS provides the "How." AI agents can analyze the semantic content of the requirements to suggest a logical decomposition of tasks.  
**Mechanism of Action:** The AI parses the requirements and maps them to standard engineering activities based on a predefined domain ontology.

* *Requirement:* "The system shall implement a PID controller for the cooling fan."  
* *AI Decomposition:*  
  1. **Task 1.1:** Model fan plant dynamics (Python/Simulink).  
  2. **Task 1.2:** Design PID control law (SysML/Control Theory).  
  3. **Task 1.3:** Implement PID algorithm (Python Prototype).  
  4. **Task 1.4:** Implement PID algorithm (Simulink Production).  
  5. **Task 1.5:** Perform MIL (Model-in-the-Loop) testing.  
  6. **Task 1.6:** Generate C code and Integrate.

**Parametric Estimation:** By integrating with historical project databases (e.g., Jira archives), the AI can estimate the effort (person-hours) for each task based on complexity factors (e.g., "Safety Critical" tag increases effort by 3x). This moves estimation from "gut feel" to "data-driven," significantly reducing planning risk.

### **3.2 Generating the Master Test Plan (IEEE 829\)**

A robust engineering process adopts a "Test-First" mentality. The AI is tasked with generating the Software Test Plan (STP) concurrently with the development plan.  
**Test Case Generation:** Using the "shall" statements from the SRS, the AI generates detailed test cases.

* **Input:** "REQ-001: System shall stop motor if temp \> 90°C."  
* **AI Output:**  
  * *Test Case ID:* TC-001  
  * *Pre-condition:* Motor running, Temp \= 89°C.  
  * *Action:* Inject Temp \= 91°C signal.  
  * *Expected Result:* Motor RPM \= 0 within 200ms.  
  * *Test Type:* Boundary Value Analysis.

**Traceability Matrix Construction:** The AI automatically constructs the **Requirement Traceability Matrix (RTM)**, linking every Requirement ID to one or more Test Case IDs. This ensures 100% test coverage from the outset and facilitates impact analysis during change requests. Tools like TestRail or Xray can import these AI-generated test definitions.

### **3.3 Risk Management Plan**

AI analysis of the requirements can also highlight potential risks. For example, if the SRS mentions "new, unproven sensor hardware," the AI can flag this as a "Technical Risk" and suggest mitigation strategies (e.g., "Procure dev kit early," "allocate extra buffer for driver development").

## **4\. Phase III: The Architectural Core (SysML v2 System Model)**

The central pillar of this process framework is the **SysML v2 System Model**. In traditional processes, the "design" is often a collection of Visio diagrams and wiki pages. In this AI-augmented process, the design is a formal, computable model that serves as the **Single Source of Truth (SSoT)**. This model bridges the gap between the textual requirements and the executable code.

### **4.1 The SysML v2 Advantage**

The shift from SysML v1 to v2 is critical for this workflow. SysML v2 introduces a textual notation (KerML-based) that is both human-readable and machine-writable. This allows LLMs to generate valid architectural models directly as code, which can then be parsed, validated, and visualized by MBSE tools.

* **Infrastructure as Code (IaC) for Systems:** SysML v2 models can be stored in Git repositories, allowing for diffs, merges, and pull requests—workflows familiar to software engineers but previously difficult for systems engineers using binary model files.  
* **Standardized API:** The SysML v2 API allows external scripts (Python, MATLAB) to query the model programmatically. This is the mechanism that keeps the prototype and production code in sync.

### **4.2 AI-Assisted Architecture Generation**

An AI agent, fed with the structured SRS from Phase I, generates the initial SysML v2 textual code. This is a "text-to-model" transformation.  
**Example Prompt Interaction:**  
*User:* "Create a SysML v2 architecture for the Cooling System based on the SRS. Define a block for the Controller, a block for the Sensor, and the interfaces between them."  
*AI Output:*  
`package CoolingSystem {`  
    `import ScalarValues::*;`  
      
    `part def Controller {`  
        `port tempInput : TemperatureIn;`  
        `port pwmOutput : PWMOut;`  
          
        `attribute maxTemp : Real = 90.0;`  
    `}`  
      
    `part def Sensor {`  
        `port tempOutput : TemperatureOut;`  
    `}`  
      
    `connect Controller.tempInput to Sensor.tempOutput;`  
`}`

The generated code is then imported into a SysML v2 compliant tool (e.g., Cameo, PTC Modeler, or the OpenMBEE environment) for visualization and refinement by human architects.

### **4.3 Defining the Hybrid Interface Contracts**

To support the requirement of having *both* a Python prototype and a production version (MATLAB or other), the SysML model must explicitly define the **contracts** that both implementations must fulfill.

* **Interface Definitions:** The port and interface definitions in SysML act as the "API spec" for the system. Whether implemented in Python or C++, the component must accept the inputs and produce the outputs defined in the SysML model.  
* **Constraint Modeling:** Requirements such as "Response time \< 50ms" are modeled as SysML constraints. These constraints are passed to the verification environment to automatically check if the implementation meets the spec.  
* **Variant Modeling:** SysML v2 supports variant modeling. The system can define an abstract Controller part, with two specific realizations:  
  * variant part controller\_proto : PythonPrototype  
  * variant part controller\_prod : MatlabImplementation This explicitly acknowledges the dual-path nature of the development within the architecture itself.

## **5\. Phase IV: Rapid Prototyping (The Python Path)**

With the architecture defined, the team enters the prototyping phase. Python is selected for this stage due to its agility and the vast availability of "off-the-shelf" algorithms for vision, AI, and data processing. This allows for rapid validation of the *logic* and *behavior* before committing to the rigorous effort of safety-critical implementation.

### **5.1 Automated Skeleton Generation**

Using the SysML v2 API, a "Scaffolding Script" (written in Python) queries the system architecture and automatically generates the Python class structure.  
**Transformation Logic:**

* **SysML Block** \\rightarrow **Python Class**  
* **SysML Attribute** \\rightarrow **Class Property** (with type hints)  
* **SysML Port** \\rightarrow **Interface Method**  
* **SysML Requirement** \\rightarrow **Docstring/Comment**

This automation ensures that the prototype structure is mathematically identical to the architectural intent. It prevents the common issue where the prototype diverges from the architecture because the developer "took a shortcut".

### **5.2 AI-Assisted Implementation (Copilot Integration)**

Developers use AI coding assistants (e.g., GitHub Copilot, CodeWhisperer) to fill in the business logic within the generated skeletons. Crucially, the "context window" provided to the AI includes the SysML-derived constraints and the SRS requirements. This "Context-Aware Coding" significantly reduces logic errors.

* *Example:* If the SysML model defines max\_speed \= 120, the AI, seeing this in the generated class structure or docstring, is more likely to generate code that clamps the speed variable to 120\.

### **5.3 Verification of the Prototype**

The test cases generated in Phase II are converted (again, by AI agents) into executable **pytest** scripts. The Python prototype is then validated against the functional requirements. This provides early confidence in the algorithmic logic (Concept Validation) before any production code is written.  
**Feedback Loop:** If the prototype fails or if the developers discover that a requirement is physically impossible to meet, they update the SysML model (or request a change), which then propagates back to the requirements. This "Soft Loop" iteration is fast and cheap.

## **6\. Phase V: Production Hardening (The MATLAB/Simulink Path)**

While Python is excellent for prototyping, safety-critical systems (automotive, aerospace, medical) often require deterministic, real-time guarantees that standard Python cannot provide due to the Global Interpreter Lock (GIL) and dynamic memory management. Therefore, the process defines a rigorous transition to a hardened production environment, typically **MATLAB/Simulink** or **Embedded C/C++**.

### **6.1 Transition Strategy: Architecture-Driven Construction**

To ensure the production code matches the prototype, we do *not* manually translate Python code line-by-line. Instead, we use the **MBSE Architecture** as the bridge.

* **System Composer Integration:** Tools like MathWorks' **System Composer** can import the SysML v2 model (or an intermediary format) to generate the skeleton of the Simulink model. This ensures that the Simulink blocks have the exact same ports, interfaces, and hierarchy as the SysML model and the Python prototype.  
* **Algorithmic Implementation:**  
  * *Control Logic:* Implemented using Simulink blocks and Stateflow charts, which are ideal for safety-critical state machines.  
  * *Complex Algorithms:* If the Python prototype used complex math, this is re-implemented using MATLAB code blocks or DSP System Toolbox blocks, which support automatic C code generation.

### **6.2 Handling Deep Learning Models**

If the Python prototype includes a Deep Learning model (e.g., a neural network trained in PyTorch), re-implementing it in C code manually is impossible.

* **ONNX Bridge:** The standard workflow is to export the Python model to the **ONNX** (Open Neural Network Exchange) format.  
* **MATLAB Import:** MATLAB's Deep Learning Toolbox imports the ONNX model.  
* **Code Generation:** GPU Coder or Embedded Coder then generates optimized, standalone C/C++ or CUDA code from the imported model, which is traceable and verifiable.

### **6.3 Pure Python Production (The "Non-Safety" Branch)**

It is important to note that not all systems are safety-critical. For IT systems, data analytics pipelines, or non-real-time components, the Python prototype *can* evolve directly into production code.

* **Hardening Python:** This involves adding type enforcement (Pydantic), extensive error handling, logging, and containerization (Docker).  
* **Limitations:** The report acknowledges that this path is generally unsuitable for ASIL-D/DAL-A applications due to the lack of certified Python runtimes for safety-critical microcontrollers.

### **6.4 Automated Equivalence Testing (Back-to-Back Testing)**

The most critical step in a hybrid workflow is verifying that the Production Code (MATLAB/C) behaves *exactly* like the validated Prototype (Python). This is achieved through **Automated Equivalence Testing**.

1. **Test Vectors:** A set of input data (vectors) is generated.  
2. **Execution:** The vectors are fed into the Python prototype and the Simulink model (via SIL \- Software-in-the-Loop).  
3. **Comparison:** The outputs are compared. Any deviation beyond a defined floating-point tolerance (epsilon) triggers a regression failure.  
4. **Root Cause:** If they differ, either the production implementation is wrong, or the prototype relied on undefined behavior.

## **7\. Phase VI: Synchronization and The Digital Thread**

The "Digital Thread" is the connected data flow that links requirements, architecture, prototype, and production code. Maintaining this thread is the primary defense against complexity.

### **7.1 The API Synchronization Mechanism**

The SysML v2 API acts as the "clearinghouse" for system parameters.

* **Parameter Database:** Critical values (e.g., MAX\_RPM, PID\_GAINS) are stored in the SysML model.  
* **Pull Mechanism:** Both the Python build pipeline and the MATLAB init scripts are configured to query the SysML API to fetch these values at runtime/compile time.  
* **Prevention of "Magic Numbers":** Hard-coding values in Python or MATLAB is strictly prohibited by the process. All configuration data must originate from the SysML model.

### **7.2 Change Management Workflow**

When a requirement changes (e.g., "Increase max speed"):

1. **Impact Analysis:** AI tools traverse the SysML graph to identify all downstream components (Python classes, Simulink blocks, Test Cases) linked to that requirement.  
2. **Alerts:** The owners of the Python and MATLAB subsystems are automatically notified via the CI/CD system.  
3. **Resynchronization:** The parameters are updated in SysML. The automated equivalence tests run. If the Python code passes but the MATLAB code fails (or vice versa), the pipeline halts until synchronization is restored.

## **8\. Process Description Document (PDD)**

This section provides the formal **Process Description Document** required for organizational adoption. It is structured to be compliant with **ISO/IEC 12207:2017** (Software Life Cycle Processes).

### **8.1 Process Identification**

* **Process Name:** AI-Augmented Hybrid-Language Systems Engineering (AHL-SE).  
* **Process ID:** PROC-SE-001.  
* **Version:** 1.0.  
* **Owner:** Chief Systems Engineer / AI Transformation Lead.

### **8.2 Process Purpose**

To transform loose stakeholder concepts into verified, validated, and safety-compliant production software using a synchronized workflow that leverages AI for acceleration and SysML v2 for architectural governance.

### **8.3 Entry and Exit Criteria**

* **Entry Criteria:** A Stakeholder Concept Document (SCD) or Statement of Work (SOW) is approved.  
* **Exit Criteria:** Production Source Code is generated, verified against requirements, and passes all Equivalence Tests; all Certification Artifacts (traceability matrices) are generated.

### **8.4 Process Roles**

* **AI Architect:** Configures LLM agents, manages prompt libraries, and ensures AI governance (HITL gates).  
* **Systems Modeler:** Owns the SysML v2 model, defines interfaces, and manages the "Single Source of Truth."  
* **Prototype Engineer:** Implements algorithms in Python; validates concepts.  
* **Safety/Embedded Engineer:** Implements production models in Simulink; manages code generation and safety compliance.

### **8.5 Detailed Activity Definitions**

**Table 2: Process Activities and Tasks**

| Activity ID | Activity Name | Inputs | Tasks | Outputs | Tools |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **ACT-01** | **Concept Decomposition** | Concept Doc | 1.1 Ingest concept into AI Agent. 1.2 Generate IEEE 830 SRS draft. 1.3 Semantic Gap Analysis. 1.4 Human Review (HITL Gate). | Baseline SRS (ReqIF) | GenAI Agent, Requirements Tool |
| **ACT-02** | **Planning & Estimation** | SRS | 2.1 AI generates WBS & estimates. 2.2 AI generates IEEE 829 Test Plan. 2.3 Risk Assessment. | SDP, STP, WBS | GenAI Project Agent, Jira |
| **ACT-03** | **Architectural Design** | SRS | 3.1 Generate SysML v2 code from SRS. 3.2 Define Interfaces & Variants. 3.3 Verify Logical Consistency. | SysML v2 Model | SysML Tool, Compiler |
| **ACT-04** | **Prototyping (Python)** | SysML Model | 4.1 Generate Python Skeletons. 4.2 AI-Assisted Coding. 4.3 Pytest execution. | Verified Python Prototype | Python, Copilot, Pytest |
| **ACT-05** | **Production Hardening** | SysML Model, Python Code | 5.1 Import Arch to System Composer. 5.2 Implement in Simulink/Stateflow. 5.3 Import ONNX (if ML). 5.4 Generate C Code. | Production C Code, Simulink Model | MATLAB, Simulink, Embedded Coder |
| **ACT-06** | **Verification & Sync** | Prototype, Prod Code | 6.1 Execute Back-to-Back Tests. 6.2 Check Parameter Sync. 6.3 Generate RTM. | Verification Report, RTM | CI/CD Pipeline, Test Automation |

### **8.6 Tailoring Guidelines**

* **For Non-Safety Projects:** Skip ACT-05 (Hardening). Deploy Python Prototype directly (ACT-04) using containerization.  
* **For Pure Software Projects:** SysML may be replaced by UML, provided the API synchronization mechanism is maintained.

## **9\. Best Practices and Recommendations**

Implementing this advanced process requires adherence to specific best practices to avoid "AI hallucination" risks and "Hybrid Language" synchronization hell.

### **9.1 AI Governance and Human-in-the-Loop**

AI is a probabilistic tool, not a deterministic one. It *will* generate errors.

* **The "Two-Person" Rule (Human \+ AI):** No AI-generated artifact (requirement, plan, code) typically bypasses human review. AI generates the *draft*; a human provides the *approval*. This "Review Gate" must be formally logged in the version control system.  
* **Prompt Management:** Treat prompts as engineering assets. Store them in a version-controlled "Prompt Library." Do not allow ad-hoc prompting for critical tasks; use validated, pre-tested prompt templates to ensure consistent outputs.  
* **Hallucination Check:** Use the SysML model as a constraint. If an AI coding assistant suggests code that violates the interface defined in SysML, the linter/compiler should flag it immediately.

### **9.2 Managing the Hybrid Environment**

* **Data Serialization:** Never copy-paste constants between Python and MATLAB. Use a build script that exports SysML values to a common format (JSON or YAML). Both the Python \_\_init\_\_.py and the MATLAB init.m scripts should load from this single file.  
* **Containerized Build Environments:** To prevent "it works on my machine" issues, specifically with Python library versions and MATLAB toolboxes, use Docker containers for the build and test pipelines. This ensures that the "Reference Python Environment" is identical for all developers.

### **9.3 SysML v2 Implementation**

* **Text-First Mindset:** Encourage systems engineers to embrace the textual notation of SysML v2. It allows for proper diffing in Git, which is essential for reviewing AI-generated architectural changes. Graphical views should be treated as *projections* of the text, not the source.  
* **Granularity:** Do not model internal algorithms in SysML. Use SysML for *Structure, Interfaces, and Contracts*. Leave the *Behavioral Implementation* to Python and Simulink. Trying to model detailed logic in SysML creates redundancy and synchronization burden.

### **9.4 Testing Strategy**

* **Shift-Left Verification:** Use the Python prototype to verify requirements *before* the expensive hardware design or embedded coding begins. If the logic is flawed, catch it in Python, not in C.  
* **Automated Traceability:** Rely on the AI to maintain the traceability matrix. Manual linking is error-prone and rarely kept up to date. The AI should scan the code for "tag annotations" (e.g., @implements REQ-123) and update the RTM automatically.

## **10\. Conclusion**

The "AI-Augmented Hybrid-Language Software Engineering Process" defined in this report represents a fundamental restructuring of the engineering lifecycle. It moves away from document-heavy, siloed workflows toward a data-driven, model-centric approach.  
By positioning **SysML v2** as the immutable digital thread, we solve the synchronization problem between Python prototyping and MATLAB hardening. By injecting **AI Agents** into the requirements and planning phases, we solve the "blank page" problem and accelerate the early lifecycle by 40-60%.  
This process does not replace the engineer. Instead, it elevates the engineer from a "generator of boilerplate" to an "architect of systems," verifying the outputs of AI and ensuring the safety and integrity of the final product. For organizations developing complex, safety-critical systems in the modern era, this hybrid, rigorous, and AI-enabled pathway is not just an option—it is the future standard.  
*End of Report.*  
*Disclaimer: The implementation of this process requires access to SysML v2 compliant tools (e.g., Keyhole Markup Language parsers, API clients) and GenAI enterprise instances. Regulatory compliance (ISO 26262, DO-178C) remains the responsibility of the human safety officers, utilizing the artifacts generated by this process.*

#### **Works cited**

1\. Bridging MATLAB and Python: Seamless Workflows and Engineering Solutions \- MathWorks, https://www.mathworks.com/company/events/webinars/upcoming/bridging-ml-python-seamless-workflows-eng-solutions-4879950.html 2\. Functional Safety and Standards \- MATLAB & Simulink \- MathWorks, https://www.mathworks.com/solutions/functional-safety.html 3\. Streamline Systems Engineering Workflows with AI Requirements Management, https://resources.altium.com/p/systems-engineering-workflows-ai-requirement-insights 4\. As a programmer asked to convert his entire Python codebase to MATLAB, my frustration is unfathomable. : r/ProgrammerHumor \- Reddit, https://www.reddit.com/r/ProgrammerHumor/comments/b2tvsz/as\_a\_programmer\_asked\_to\_convert\_his\_entire/ 5\. How AI is Transforming Requirements Gathering and Documentation \- Copilot4DevOps, https://copilot4devops.com/ai-in-requirements-gathering-and-documentation/ 6\. AI Software Documentation Generator | Create with AI \- Miro, https://miro.com/ai/software-development/ai-software-documentation/ 7\. Generative AI app developer workflow \- Azure Databricks | Microsoft Learn, https://learn.microsoft.com/en-us/azure/databricks/generative-ai/tutorials/ai-cookbook/genai-developer-workflow 8\. Automating SRS Creation with Agentic Workflows: Unlocking Seamless Consistency and Productivity Gains \- K G Aravinda Kumar, https://aravindakumar.medium.com/automating-srs-creation-with-agentic-workflows-unlocking-seamless-consistency-and-productivity-f2aff2efc861 9\. SysML Connector \- MATLAB & Simulink \- MathWorks, https://www.mathworks.com/products/sysml.html 10\. SysML® v2 Specification — Next-Generation MBSE Modeling | Object Management Group, https://www.omg.org/sysml/sysmlv2/ 11\. Embedded Coder for Production Code Generation \- MATLAB & Simulink \- MathWorks, https://www.mathworks.com/learn/training/embedded-coder-for-production-code-generation.html 12\. Developing, Verifying, and Validating IEC 62304 Compliant Code with MATLAB \- YouTube, https://www.youtube.com/watch?v=PPCBFnDJs98 13\. Code Generation — How Agentic Workflows Transform Requirements into Code, https://aravindakumar.medium.com/code-generation-how-agentic-workflows-transform-requirements-into-code-61aecd683cbb 14\. Digital requirements engineering with an INCOSE-derived SysML meta-model \- arXiv, https://arxiv.org/html/2410.21288v1 15\. Prompt Engineering Guide, https://www.promptingguide.ai/ 16\. Leveraging Graph-RAG and Prompt Engineering to Enhance LLM-Based Automated Requirement Traceability and Compliance Checks \- arXiv, https://arxiv.org/html/2412.08593v1 17\. Prompt engineering \- OpenAI API, https://platform.openai.com/docs/guides/prompt-engineering 18\. Using LLMs in Software Requirements Specifications: An Empirical Evaluation \- arXiv, https://arxiv.org/html/2404.17842v1 19\. The Engineering Blueprint for an AI-Augmented SDLC \- V2Solutions, https://www.v2solutions.com/whitepapers/ai-augmented-sdlc-whitepaper/ 20\. Using generative AI to create test cases for software requirements | AWS for Industries, https://aws.amazon.com/blogs/industries/using-generative-ai-to-create-test-cases-for-software-requirements/ 21\. Work Breakdown Structure (WBS) Software for Projects \- Galorath, https://galorath.com/seer/use-case/work-breakdown-structure-wbs/ 22\. AI-Based Accelerators Series: AI for Effortless Work Breakdown Structures (WBS), https://mobilelive.ai/blog/ai-based-accelerators-series-ai-for-effortless-work-breakdown-structures-wbs 23\. How Model-Based Systems Engineering Can Help Drive R\&D Innovation \- Rescale, https://rescale.com/blog/how-model-based-systems-engineering-can-help-drive-rd-innovation/ 24\. Simplify Software Testing with AI-Driven Test Case and Assertion Tools, https://kailash-pathak.medium.com/simplify-software-testing-with-ai-driven-test-case-and-assertion-tools-092097a10ea3 25\. AI-Driven Test Management Software by TestRail, https://www.testrail.com/ 26\. Model-Based Systems Engineering (MBSE) \- SEBoK, https://sebokwiki.org/wiki/Model-Based\_Systems\_Engineering\_(MBSE) 27\. Modeling Languages for Model-Based Systems Engineering (MBSE), https://www.sei.cmu.edu/blog/modeling-languages-for-model-based-systems-engineering-mbse/ 28\. Has anyone seriously tried the textual notation in SysML v2? Thoughts? \- Reddit, https://www.reddit.com/r/systems\_engineering/comments/1kyxvwf/has\_anyone\_seriously\_tried\_the\_textual\_notation/ 29\. Creating Integrated Digital Environments with SysML v2 \- NCSI, https://www.ncsi.com/wp-content/uploads/2023/05/1400-ARA-Creating-Integrated-Digital-Environments-with-SysML-v2.pdf 30\. Interoperability Live \- SysML v2 API in Action \- Model Based Systems Engineering 4 You, https://mbse4u.com/2025/01/14/interoperability-live-sysml-v2-api-in-action/ 31\. SysTemp: A Multi-Agent System for Template-Based Generation of SysML v2 \- arXiv, https://arxiv.org/html/2506.21608v1 32\. SysML v2 Tools \- Object Management Group, https://www.omg.org/sysml/sysmlv2/sysml-tool/ 33\. Leveraging the Python-to-MATLAB Framework for Embedded Target Platform Integration, https://www.cyient.com/blog/leveraging-the-python-to-matlab-framework-for-embedded-target-platform-integration 34\. DAF-Digital-Transformation-Office/PySysML2: PySysML2 is a Python-based parser for the SysML 2.0 textual modeling language. Its main purpose is to parse a SysML 2.0 textual model into a Python object, and then transform that model into various data structures useful for data science and analysis. \- GitHub, https://github.com/DAF-Digital-Transformation-Office/PySysML2 35\. Set Up Now for AI to Augment Software Development \- Gartner, https://www.gartner.com/en/articles/set-up-now-for-ai-to-augment-software-development 36\. Create Test Cases using AI | Use Generative AI in Software Testing, https://www.youtube.com/watch?v=x432efxE6QA 37\. \#9 \- How To Generate End-to-End Automation Test With AI Using TestRigor, https://www.youtube.com/watch?v=GGinNM87WL0 38\. Python coding standard for Safety Critical Applications \- Stack Overflow, https://stackoverflow.com/questions/69673807/python-coding-standard-for-safety-critical-applications 39\. Using MATLAB with Python \- MathWorks, https://www.mathworks.com/help/comm/using-matlab-with-python.html?s\_tid=CRUX\_lftnav 40\. Incorporating Machine Learning Models into Safety-Critical Systems \- MathWorks, https://www.mathworks.com/company/events/webinars/upcoming/incorporating-machine-learning-models-safety-critical-sys-4785150.html 41\. Import Python Code to Simulink Using Python Importer Wizard \- MATLAB & Simulink, https://www.mathworks.com/help/simulink/ug/import-python-code-using-python-importer.html 42\. Automating Model Based Systems Engineering with AI \- ThunderGraph Blog, https://www.thundergraph.ai/blog/automating-mbse 43\. What Is Human In The Loop (HITL)? \- IBM, https://www.ibm.com/think/topics/human-in-the-loop 44\. Why do people still pay and use matlab having python numpy and matplotlib? \- Reddit, https://www.reddit.com/r/Python/comments/u6bcgc/why\_do\_people\_still\_pay\_and\_use\_matlab\_having/ 45\. Best practices for using generative AI in software development \- AWS Prescriptive Guidance, https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-accelerate-software-dev-lifecycle-gen-ai/best-practices.html