

# **Project Plan: Doctrinal Digitization and Operational Modeling for AI-Enabled Air Force Operations**

## **1\. Executive Summary**

The United States Air Force operates within an increasingly complex global security environment characterized by rapid technological proliferation, the re-emergence of great power competition, and the acceleration of warfare speeds imposed by autonomous systems and hypersonic capabilities. To maintain decision advantage in this environment, the Department of Defense (DoD) has initiated the Joint All-Domain Command and Control (JADC2) strategy, which seeks to connect sensors from all branches into a unified grid.1 However, a critical, often overlooked bottleneck threatens to stall these modernization efforts: the "analog" nature of Air Force doctrine.

Current Air Force doctrine—the fundamental set of principles, beliefs, and codified best practices that guide Service operations—exists primarily as static, unstructured text in Portable Document Format (PDF) files.3 While these documents, such as *Air Force Doctrine Publication (AFDP) 1: The Air Force* and *AFDP 3-0: Operations*, are accessible to human readers, they are opaque to the computational systems that increasingly underpin military operations.4 As the Service moves toward integrating Artificial Intelligence (AI) agents for functions ranging from logistics optimization to autonomous combat, the lack of a machine-readable model of doctrine creates a perilous gap. AI systems cannot currently "read" the commander's intent or the legal constraints embedded in doctrine, necessitating the hard-coding of rules that are brittle, difficult to update, and prone to misalignment with evolving operational concepts.

This report presents a comprehensive, exhaustive project plan to review, digitize, and model Air Force doctrine. The objective is to transform the doctrinal corpus from a passive reference library into an active, executable model—a "Digital Doctrinal DNA" that can be computationally analyzed and natively understood by AI agents.

The proposed methodology leverages a sophisticated convergence of technologies:

1. **Structural Digitization:** utilizing the **Akoma Ntoso/LegalDocML** standard to convert text into semantically tagged XML, capturing the hierarchical and normative structure of publications.6  
2. **Semantic Modeling:** Adopting the **Common Core Ontology (CCO)**, mandated by DoD for interoperability, to map doctrinal concepts to a rigorous logical framework.8  
3. **Logic Formalization:** employing **LegalRuleML** and Deontic Logic to mathematically express obligations, permissions, and prohibitions, allowing for automated compliance checking and conflict detection.10  
4. **Process Mining:** Analyzing operational logs against doctrinal models to identify inefficiencies and vulnerabilities to "reflexive control" information warfare strategies.12

By executing this plan, the Air Force will achieve two transformative capabilities. First, it will enable the automated analysis of the doctrine itself, identifying ambiguities, inconsistencies, and logical conflicts that currently require manual adjudication. Second, and perhaps more critically, it will provide the necessary "guardrails" for AI agents, ensuring that autonomous systems operate with a mathematically verifiable understanding of their roles, authorities, and constraints within the Mission Command framework.13 This report details the strategic imperative, the technical architecture, the analytical methodology, and the implementation roadmap required to achieve this vision of Executable Doctrine.

## **2\. Strategic Context and Operational Imperative**

### **2.1 The Digital-Doctrinal Gap in Modern Warfare**

The history of military innovation is often viewed through the lens of hardware—faster jets, stealthier bombers, and more precise munitions. However, the software of warfare—doctrine—is equally critical. Doctrine provides the "common operating system" for the human force, establishing a shared language and a unified conception of how to fight. In the current era, formalized in the *National Defense Strategy*, the Department of Defense is pivoting toward data-centric warfare.15 The Data Strategy emphasizes that data is a strategic asset and must be visible, accessible, understandable, linked, trustworthy, interoperable, and secure (VAULTIS).15

Despite this directive, Air Force doctrine remains trapped in the "document-centric" paradigm of the 20th century. A pilot or planner must manually read *AFDP 3-01 Counterair Operations* to understand the rules for integrating with surface-to-air missile defenses.5 If an automated battle management system is tasked with this integration, human engineers must manually translate those prose rules into if-then code statements. This translation process is slow, expensive, and error-prone. Worse, when doctrine changes—as it did significantly with the 2021 update to *AFDP 1* introducing "Mission Command"—the code does not automatically update.13 This creates a "synchronization latency" where the software governing the force is fighting according to outdated rules.

This disconnect is not merely an administrative inconvenience; it is an operational vulnerability. In a conflict with a peer adversary, the speed of adaptation will be decisive. If the Air Force updates its TTPs (Tactics, Techniques, and Procedures) to counter a new enemy capability, but its AI logistics and planning agents take six months of reprogramming to "learn" the new TTPs, the advantage is lost. A machine-readable doctrine allows for "over-the-air" updates to the organizational logic of the entire digital force, synchronizing human and machine understanding instantly.

### **2.2 Joint All-Domain Command and Control (JADC2)**

The JADC2 initiative seeks to connect "sensors from all domains to shooters from all domains".1 This requires an unprecedented level of interoperability. Currently, interoperability is achieved through technical standards (like Link 16 for tactical data). However, JADC2 requires *semantic* interoperability—machines must understand the *meaning* of the data they exchange.

* **The Problem:** If an Army system requests "Close Air Support" (CAS) from an Air Force autonomous platform, both systems must share a precise, computable definition of what CAS entails, including the required check-in procedures, target verification steps, and abort criteria defined in *AFDP 3-03 Counterland Operations*.5  
* **The Solution:** By modeling Air Force doctrine using the **Common Core Ontology (CCO)**, which is also being adopted by the Army and other services, the Air Force ensures that its AI agents speak the same "logical language" as the rest of the Joint Force.8 This doctrinal digitization is therefore a prerequisite for the semantic coherence of JADC2.

### **2.3 The Threat of Reflexive Control and Information Warfare**

The imperative for this project extends beyond efficiency to defense. Adversaries, particularly Russia, have long employed the concept of "reflexive control"—conveying specially prepared information to an opponent to incline them to voluntarily make a predetermined decision.12 In the digital age, this manifests as information warfare attacks designed to exploit rigidities in organizational processes.

If Air Force doctrine contains predictable, rigid inefficiencies—for example, a mandatory 24-hour targeting cycle for certain asset classes—an adversary can exploit this by operating inside that decision loop. By using **Process Mining** techniques to analyze our own doctrine (as proposed in this plan), the Air Force can identify these "process vulnerabilities" before the enemy does.12 We can model how our doctrine dictates information flow and decision authority, identifying bottlenecks or predictable patterns that could be weaponized by an adversary. Thus, digitizing doctrine is also a counter-intelligence and force protection measure.

### **2.4 Enabling Mission Command for Artificial Intelligence**

The 2021 revision of *AFDP 1* enshrined **Mission Command** as the central philosophy of Air Force Command and Control (C2).13 Mission Command relies on "Centralized Command, Distributed Control, and Decentralized Execution" (CC-DC-DE). It requires subordinates to act on the *Commander's Intent* rather than detailed orders, enabling agility in contested environments where communications may be severed.

For AI agents to function as "digital subordinates" in this framework, they must be capable of:

1. **Interpreting Intent:** Understanding high-level goals (e.g., "Neutralize enemy air defenses in Sector 4") without needing turn-by-turn instructions.  
2. **Self-Constraint:** Adhering to Rules of Engagement (ROE) and Laws of Armed Conflict (LOAC) even when out of contact with human supervisors.16  
3. **Role Awareness:** Understanding their specific authority level (e.g., "I am a logistics agent; I can reroute fuel, but I cannot authorize a kinetic strike").16

Current AI paradigms (like pure Machine Learning) operate as "black boxes" that optimize for a reward function. They do not inherently "know" doctrine or law. A Reinforcement Learning agent might learn to bomb a hospital because it maximizes the "enemy neutralized" score, unless it is constrained by a formal model of *AFDP 3-60 Targeting* and *AFDP 3-84 Legal Support*.17 This project provides that explicit, auditable constraint layer.

## **3\. Doctrinal Architecture Analysis**

To create a model, we must first understand the structure of the data source. The Air Force doctrinal hierarchy is a complex, tiered system of publications that govern every aspect of operations.

### **3.1 The Hierarchy of Publications**

The Air Force doctrine library is organized into levels of precedence and specificity. A comprehensive review must ingest documents from all levels to create a complete model.

| Doctrine Level | Operational Focus | Key Publications & Examples | Modeling Challenge |
| :---- | :---- | :---- | :---- |
| **Capstone** | Broadest principles, Service culture, Command philosophy. | **AFDP 1:** *The Air Force* **AFDP 1-1:** *Mission Command* | High abstraction. Concepts like "Integrity" or "Trust" are difficult to formalize for AI. |
| **Operational** | Detailed organization of forces, specific mission sets (Keystone & Functional). | **AFDP 3-0:** *Operations* 19 **AFDP 2-0:** *Intelligence* **AFDP 3-01:** *Counterair Ops* **AFDP 4-0:** *Combat Support* | High complexity. Dense interconnectivity between functions (e.g., Intel driving Ops driving Logistics). |
| **Tactical (TTPs)** | Specific procedures, checklists, weapon employment. | **AFTTP 3-1 series** (e.g., specific aircraft tactics) **AFTTP 3-32:** *Civil Engineering* | High granularity. Very specific rules ("If X, do Y") that are easier to code but vast in volume. |
| **Doctrine Notes** | Emerging concepts, rapid updates. | **AFDN 1-21:** *Agile Combat Employment* **AFDN 25-1:** *Artificial Intelligence* 20 | Rapid change. These documents bridge the gap between static doctrine and new tech. |

**Key Insight:** The relationship between these documents is hierarchical but also cross-referential. *AFDP 3-01* (Counterair) relies on definitions of "Command Relationships" established in *AFDP 3-0* and *AFDP 3-0.1*. A change in the Capstone definition of "Supported Commander" ripples down to change the authorities in every functional publication. The digital model must capture these dependencies using a Knowledge Graph structure, preventing the "version mismatch" issues common in paper libraries.

### **3.2 The Ambiguity Challenge in Natural Language**

A primary goal of this effort is to identify "ambiguous and inconsistent doctrine." Natural language is inherently fuzzy. Doctrinal texts use **deontic modalities**—words that define duty—in ways that vary in strictness.

* **"Must" / "Will":** Indicates a mandatory obligation. (e.g., "Commanders *must* ensure compliance with LOAC").  
* **"Should":** Indicates a recommendation or standard practice that can be deviated from with justification.  
* **"May":** Indicates permission or discretionary authority.  
* **"Can":** Indicates physical or functional capability.

The Analytical Problem:  
In AFDP 3-10 Force Protection, the text states: "The base perimeter is not the first line of defense... rather, in the context of...".3 This is a nuanced philosophical statement. However, a robotic sentry needs a binary definition: "Is the area 5 meters outside the fence 'Hostile' or 'Friendly'?" The review must identify where doctrine relies on "constructive ambiguity" (useful for humans) versus "destructive ambiguity" (fatal for machines).  
Furthermore, inconsistencies arise across the corpus. *AFDP 3-52 Airspace Control* might define the "coordinating altitude" between rotary and fixed-wing assets differently than the Army's corresponding doctrine, or even differently than an older version of *AFDP 3-03 Counterland*.5 Finding these contradictions requires parsing millions of words across hundreds of files—a task perfectly suited for the automated analysis proposed in Section 6\.

### **3.3 Target Audience and User Personas**

The "users" of this digitized doctrine are distinct, and the model must serve all of them:

1. **Doctrine Developers (LeMay Center):** They need tools to check for consistency and conflict when writing new drafts.  
2. **Operational Planners (AOC Strategy Division):** They need to query doctrine to validate plans (e.g., "Does this specialized targeting flow violate any constraints in *AFDP 3-60*?").  
3. **AI Agents (The Digital User):** They need an API to query their own "rules of the road" in real-time.

## **4\. Technological Framework: The Semantic Stack**

To convert PDF text into a "Detailed Model of Operations," we propose a specific technology stack. This is not a generic IT project; it requires specialized tools from the fields of Legal Informatics, Ontology Engineering, and Symbolic AI.

### **4.1 Structural Digitization: Akoma Ntoso / LegalDocML**

The first step is to move away from PDF (which is essentially a digital image of paper) to a format that understands the *structure* of regulations. We will standardize on **Akoma Ntoso**, also known as **LegalDocML** (OASIS standard).6

Why Akoma Ntoso?  
Developed originally for the United Nations to manage African parliamentary documents, Akoma Ntoso has become the global standard for legislative and normative XML.6 It provides a rigorous schema for describing:

* **Hierarchy:** Chapter, Section, Article, Clause.  
* **Metadata:** Lifecycle events (Drafted, Approved, Repealed), Authorship, Temporal applicability (e.g., "This rule is valid from 2021-01-01 to 2024-01-01").  
* **Semantics:** It allows inline tagging of concepts. We can tag the word "JFACC" not just as text, but as a specific entity type Role referring to a specific definition in the ontology.21

Implementation:  
We will utilize Python libraries such as Tulit or Bluebell, which are specialized parsers for Akoma Ntoso.22 These tools will ingest the raw text of AFDPs and wrap them in the LegalDocML XML structure. This ensures that every single sentence in Air Force doctrine has a unique, persistent identifier (URI), allowing an AI agent to cite the exact paragraph that justifies its action (e.g., urn:us:af:doc:afdp3-0:2021:chapter2:para14).

### **4.2 Semantic Foundation: Common Core Ontology (CCO)**

Structure is not enough; we need meaning. The **Common Core Ontology (CCO)** is a suite of eleven mid-level ontologies that extend the **Basic Formal Ontology (BFO)**.8 The DoD has mandated the use of BFO/CCO to ensure that data models are compatible across the Joint enterprise.9

Mapping Doctrine to CCO Modules:  
The project will map Air Force concepts to the specific CCO modules:

* **Agent Ontology:** Defines the hierarchy of actors. "Airman," "Commander," "Squadron," and "AI Agent" will all be subclasses of CCO:Agent.8 This allows the system to inherit properties—for example, knowing that an "AI Agent" acts on behalf of a "Organization" and thus inherits that Organization's liability or ROE.  
* **Information Entity Ontology:** Models the documents themselves. An "Air Tasking Order (ATO)" is an InformationContentEntity that *prescribes* a CCO:ActOfWarfare.8 This distinction is vital: the ATO is the plan; the airstrike is the event.  
* **Event Ontology:** Models the dynamic aspect of operations. "Air Interdiction," "Refueling," and "Reconnaissance" are types of Process. CCO allows us to define the *inputs* (fuel, ammo), *participants* (pilot, aircraft), and *outputs* (target destroyed) of these processes.25  
* **Geospatial Ontology:** Defines the spatial boundaries (e.g., "Kill Box," "No-Fly Zone") which are critical for deconfliction.8

By translating doctrine into CCO, we create a Knowledge Graph (stored in a graph database like Neo4j) where:  
(Node: JFACC) \----\> (Node: AirAssets) \----\> (Node: CounterairOps).26

### **4.3 Logic Formalization: LegalRuleML**

While CCO defines the "nouns" (entities), we need a language for the "verbs" (rules). **LegalRuleML** is the OASIS standard for modeling legal and normative rules.10 It is specifically designed to handle the complexity of legal reasoning, which differs from standard computer logic.

**Key Capabilities for Doctrine:**

* **Deontic Logic:** Standard boolean logic involves True/False. Doctrine involves Obligations ("Must"), Permissions ("May"), and Prohibitions ("Must Not").27 LegalRuleML enables us to code: "If Target is Hostile, Engagement is *Permitted*." This is distinct from "Engagement is *True*."  
* **Defeasibility:** Doctrine is full of exceptions. "Do not fly below 5,000 feet *unless* in a TIC (Troops in Contact) situation." LegalRuleML handles **defeasible logic**, where a general rule holds until a specific exception overrides it.10 This is critical for preventing AI rigidity.  
* **Isomorphism:** LegalRuleML supports a direct link between the natural language text (in Akoma Ntoso) and the logical rule. This means if the text of *AFDP 3-60* changes, the system can flag exactly which logical rules are now "orphaned" or require update.28

## **5\. Methodology for Analysis and Modeling**

This section details the step-by-step methodology to execute the project, moving from raw text to analyzed insight.

### **5.1 Step 1: Automated Ingestion and NLP Extraction**

We will build a pipeline using Python-based Natural Language Processing (NLP) tools.

* **Corpus Collection:** Scrape and aggregate all PDFs from doctrine.af.mil.3  
* **Text Extraction:** Use OCR and PDF parsing (e.g., PyMuPDF) to extract raw text.  
* **Semantic Tagging:** Use **spaCy** or **LexNLP** (a library tuned for legal text) to perform Named Entity Recognition (NER).29  
  * *Custom Entity Models:* We will train the NLP model on military nomenclature. It must recognize that "C-17" is an Aircraft and "Suppression of Enemy Air Defenses (SEAD)" is a Mission.  
  * *Relation Extraction:* The model will identify Subject-Verb-Object triplets. "The JFACC (Subject) exercises (Verb) OPCON (Object)."

### **5.2 Step 2: Ambiguity and Inconsistency Detection**

Once the text is structured, we will apply analytical algorithms to identify the "ambiguous and inconsistent" areas requested by the user.

A. Logic Solver Analysis (ASP):  
We will translate the extracted rules into Answer Set Programming (ASP) using tools like CNL2ASP (Controlled Natural Language to ASP).31 ASP solvers (like Clingo) are powerful engines that can find logical contradictions in vast datasets.

* *Conflict Search:* We will query the solver: "Is there any situation where an agent is both prohibited and obligated to perform Action X?"  
* *Example:* If *AFDP 3-01* obligates a response to a threat, but *AFDP 3-84* prohibits engagement without specific clearances that are impossible to get in the timeframe, the solver will return "UNSATISFIABLE," highlighting a doctrinal conflict.

B. LLM-Based Ambiguity Scoring:  
We will use Large Language Models (LLMs) to scan for "semantic fuzziness."

* *Method:* The LLM will be prompted to identify vague quantifiers ("timely," "adequate," "appropriate") and generate an "Ambiguity Heatmap" of the corpus.  
* *Insight:* Sections with high ambiguity scores are candidates for rewriting. For automation purposes, "timely" must be defined (e.g., "within 10 minutes") or the AI cannot function.

### **5.3 Step 3: Process Mining for Efficiency Analysis**

Doctrine describes processes—sequences of actions. We can analyze these processes for inefficiencies.

* **Model Discovery:** We will use the text to generate "Ideal" process models (e.g., BPMN diagrams) of doctrinal workflows like the Joint Targeting Cycle (F2T2EA \- Find, Fix, Track, Target, Engage, Assess).17  
* **Conformance Checking:** We will compare these "Ideal" models against real-world "Actual" data logs (e.g., from AOC exercise logs or historical data). **Process Mining** algorithms (like those found in the ProM tool) will overlay the two.33  
* **Bottleneck Identification:** If the doctrine assumes the "Target" phase takes 30 minutes, but real-world logs show it takes 4 hours, the deviation highlights a friction point.  
* **Reflexive Control Analysis:** By mapping the decision loops, we can identify "predictable rigidities." If the process model shows that a specific input *always* triggers a specific, predictable response without deviation, this is a vulnerability to Russian-style reflexive control.12 The recommendation would be to introduce randomized variance or human-in-the-loop checks to break the predictability.

## **6\. Operational Application: AI Agents and Mission Command**

The ultimate deliverable is not just a report, but a model that enables effective automation. This section describes how the "Executable Doctrine" integrates with AI agents.

### **6.1 The "Digital Commander's Intent"**

*AFDP 1-1 Mission Command* emphasizes the "Understanding of Commander's Intent".13 Currently, "intent" is conveyed via voice or slide deck. For an AI, intent must be a mathematical object.

* **Machine-Readable Intent (MRI):** We will define a standard schema for Intent that includes:  
  1. **End State:** The desired outcome state (modeled in CCO).  
  2. **Constraints:** The boundaries (from LegalRuleML rules).  
  3. **Risk Tolerance:** A variable parameter (e.g., 0.0 to 1.0) governing how much doctrinal deviation is permitted in pursuit of the objective.

### **6.2 Compliance by Design (The "Doctrinal Governor")**

We will implement a "Doctrinal Governor" module for AI agents. This is a software wrapper that sits between the AI's decision engine and its effectors.

* **Mechanism:** Before the AI executes an action (e.g., firing a missile), the Governor queries the Knowledge Graph: "Is Action A permitted given Current State S and Rules R?"  
* **Neuro-Symbolic AI:** This combines the flexibility of Neural Networks (for perception and strategy) with the rigidity of Symbolic Logic (for compliance). The Neural Network suggests the action; the Symbolic Logic validates it against doctrine.34  
* **Benefit:** This solves the "Black Box" trust issue. Commanders can trust the AI because its compliance mechanism is explicit, deterministic, and derived directly from approved Service doctrine.

### **6.3 The "Digital Twin" of Air Force Operations**

By ingesting the entirety of doctrine, we effectively create a **Digital Twin** of the Air Force's organizational logic.

* **Simulation:** We can run thousands of Monte Carlo simulations using this Digital Twin. We can test "What if we change the command relationship in *AFDP 3-0* from OPCON to TACON for this asset?" The simulation will reveal the cascading effects on logistics and decision speed before any doctrine is actually rewritten.  
* **Wargaming:** This allows for "Doctrinal Wargaming." We can pit our doctrinal model against a model of adversary doctrine (derived from intelligence) to see which organizational structure reacts faster.1

## **7\. Implementation Roadmap**

This project is ambitious and should be executed in phases to manage risk and demonstrate value.

### **7.1 Phase 1: The "Targeting" Pilot (Months 1-6)**

* **Focus:** **AFDP 3-60 Targeting**. This publication is highly process-driven (Joint Targeting Cycle) and rule-heavy (ROE, Collateral Damage Estimation), making it the perfect candidate for automation.17  
* **Deliverables:**  
  * Digitized XML version of AFDP 3-60.  
  * LegalRuleML model of the targeting constraints.  
  * A prototype "Targeting Compliance Agent" that can check a proposed target list against the digitized constraints.  
* **Techniques:** Use **LexNLP** to extract ROE rules; use **Process Mining** to map the F2T2EA cycle.

### **7.2 Phase 2: The "Logistics" Expansion (Months 7-12)**

* **Focus:** **AFDP 4-0 Combat Support** and **AFDP 3-36 Air Mobility Operations**.5  
* **Rationale:** Logistics is the backbone of operations and a primary domain for AI optimization.  
* **Deliverables:**  
  * Ontology of supply classes and transport assets.  
  * Integration of Logistics constraints into the Phase 1 Targeting model (e.g., "Can we support this strike plan logistically?").  
  * Demonstration of **Process Mining** to find supply chain bottlenecks.

### **7.3 Phase 3: The "Mission Command" Capstone (Months 13-18)**

* **Focus:** **AFDP 1** and **AFDP 1-1**.  
* **Deliverables:**  
  * Formalization of abstract command relationships (OPCON/TACON/ADCON) in the **Agent Ontology**.  
  * Deployment of the "Doctrinal Governor" wrapper for a generic AI agent in a simulated environment.  
  * Policy recommendations for rewriting doctrine to be "born digital."

### **7.4 Policy and Workforce Recommendations**

* **Update DAFPD 10-13:** The policy directive governing doctrine development should be updated to mandate that all new doctrine be published in **LegalDocML** format alongside PDF.18  
* **Rules as Code:** Adopt a "Rules as Code" approach where doctrine writers work side-by-side with ontologists. The code *is* the doctrine, not a translation of it.36  
* **Open Architecture:** Ensure the Doctrinal Knowledge Graph is accessible via an open API to industry partners, preventing vendor lock-in and enabling the "App Store" model of JADC2 development.37

## **8\. Conclusion**

The transition to an AI-enabled Air Force is not merely a hardware upgrade; it is an ontological shift. We cannot run a 21st-century digital force on 20th-century analog rules. The current disconnect between the speed of algorithmic warfare and the static nature of text-based doctrine creates a "compliance gap" that hinders the deployment of autonomous systems and exposes the force to inefficiencies and information warfare vulnerabilities.

By executing this project plan—digitizing the text with **Akoma Ntoso**, modeling the meaning with **Common Core Ontology**, and formalizing the logic with **LegalRuleML**—the Air Force will transform its doctrine into a strategic asset. This "Executable Doctrine" will empower AI agents to operate with the agility of Mission Command while remaining tethered to the ethical and legal values of the Service. It will allow the Air Force to analyze its own operations with mathematical precision, identifying and eliminating the inefficiencies that an adversary might otherwise exploit. In doing so, the Service will ensure that its intellectual foundation is as advanced as its technological edge.

---

## **9\. Appendix: Technical Architecture & Standards**

The following table summarizes the proposed technical stack for the Doctrinal Modeling Project, selected to maximize interoperability with DoD and Industry standards.

| Component Layer | Function | Proposed Standard/Tool | Rationale | Reference |
| :---- | :---- | :---- | :---- | :---- |
| **Data Layer** | Structured Document Format | **Akoma Ntoso (LegalDocML)** | OASIS standard for normative text; supports rich metadata and hierarchy. | 6 |
| **Semantic Layer** | Domain Ontology | **Common Core Ontology (CCO)** | DoD-mandated mid-level ontology extending BFO; ensures Joint interoperability. | 8 |
| **Logic Layer** | Rule Representation | **LegalRuleML** | OASIS standard for legal/normative rules; handles Defeasibility and Deontic Logic. | 10 |
| **Extraction Layer** | NLP / Text Mining | **spaCy** \+ **LexNLP** | Open-source Python libraries with strong NER and legal text capabilities. | 29 |
| **Reasoning Layer** | Conflict Detection & Compliance | **Clingo (ASP Solver)** | Answer Set Programming solver capable of handling complex combinatorial constraints. | 31 |
| **Translation Layer** | Natural Language to Logic | **CNL2ASP** | Tool to bridge Controlled Natural Language (human readable) and ASP (machine code). | 32 |
| **Analysis Layer** | Process Efficiency | **ProM** (Process Mining) | Leading open-source framework for process discovery and conformance checking. | 33 |
| **Storage Layer** | Knowledge Graph | **Neo4j** | Graph database optimized for storing highly interconnected relationship data. | 26 |
| **Interface Layer** | Human-Machine Interaction | **Neuro-Symbolic Wrapper** | Hybrid AI approach combining LLM fluidity with Symbolic Logic rigidity. | 34 |

**Note on Standards:** The selection of OASIS standards (LegalDocML, LegalRuleML) and DoD-mandated Ontologies (BFO/CCO) is deliberate to ensure that this project does not become a proprietary "stovepipe" but rather a foundational infrastructure layer for the entire Department of Defense.

#### **Works cited**

1. Joint All-Domain Command and Control for Modern Warfare: An Analytic Framework for Identifying and Developing Artificial Intelli \- RAND, accessed November 24, 2025, [https://www.rand.org/content/dam/rand/pubs/research\_reports/RR4400/RR4408z1/RAND\_RR4408z1.pdf](https://www.rand.org/content/dam/rand/pubs/research_reports/RR4400/RR4408z1/RAND_RR4408z1.pdf)  
2. Summary of the Joint All-Domain Command and Control Strategy \- DoD, accessed November 24, 2025, [https://media.defense.gov/2022/Mar/17/2002958406/-1/-1/1/SUMMARY-OF-THE-JOINT-ALL-DOMAIN-COMMAND-AND-CONTROL-STRATEGY.pdf](https://media.defense.gov/2022/Mar/17/2002958406/-1/-1/1/SUMMARY-OF-THE-JOINT-ALL-DOMAIN-COMMAND-AND-CONTROL-STRATEGY.pdf)  
3. Air Force Doctrine Smart Book, accessed November 24, 2025, [https://www.doctrine.af.mil/Portals/61/documents/SmartBook/AFDoctrineSmartBook.pdf](https://www.doctrine.af.mil/Portals/61/documents/SmartBook/AFDoctrineSmartBook.pdf)  
4. U.S. Air Force Doctrine \> Home, accessed November 24, 2025, [https://www.doctrine.af.mil/](https://www.doctrine.af.mil/)  
5. Air Force Doctrine Publications, accessed November 24, 2025, [https://www.doctrine.af.mil/Operational-Level-Doctrine/](https://www.doctrine.af.mil/Operational-Level-Doctrine/)  
6. Akoma Ntoso \- Wikipedia, accessed November 24, 2025, [https://en.wikipedia.org/wiki/Akoma\_Ntoso](https://en.wikipedia.org/wiki/Akoma_Ntoso)  
7. Akoma Ntoso | Akoma Ntoso Site, accessed November 24, 2025, [http://akomantoso.info/](http://akomantoso.info/)  
8. CommonCoreOntology/CommonCoreOntologies: The ... \- GitHub, accessed November 24, 2025, [https://github.com/CommonCoreOntology/CommonCoreOntologies](https://github.com/CommonCoreOntology/CommonCoreOntologies)  
9. \[2311.10505\] CNL2ASP: converting controlled natural language sentences into ASP \- arXiv, accessed November 24, 2025, [https://arxiv.org/abs/2311.10505](https://arxiv.org/abs/2311.10505)  
10. LegalRuleML Core Specification Version 1.0 \- Index of / \- OASIS Open, accessed November 24, 2025, [https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html](https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html)  
11. LegalRuleML Core Specification V1.0 OASIS Standard published, accessed November 24, 2025, [https://www.oasis-open.org/2021/09/08/legalruleml-core-specification-v1-0-oasis-standard-published/](https://www.oasis-open.org/2021/09/08/legalruleml-core-specification-v1-0-oasis-standard-published/)  
12. Process Mining: The Missing Piece in Information Warfare \- ResearchGate, accessed November 24, 2025, [https://www.researchgate.net/publication/331744765\_Process\_Mining\_The\_Missing\_Piece\_in\_Information\_Warfare](https://www.researchgate.net/publication/331744765_Process_Mining_The_Missing_Piece_in_Information_Warfare)  
13. AFDP 3-0.1, Command and Control \- Air Force Doctrine, accessed November 24, 2025, [https://www.doctrine.af.mil/Portals/61/documents/AFDP\_3-0\_1/AFDP3-0.1CommandandControl.pdf](https://www.doctrine.af.mil/Portals/61/documents/AFDP_3-0_1/AFDP3-0.1CommandandControl.pdf)  
14. MISSION COMMAND \- Air Force Doctrine, accessed November 24, 2025, [https://www.doctrine.af.mil/Portals/61/documents/AFDP\_1-1/AFDP%201-1%20Mission%20Command.pdf](https://www.doctrine.af.mil/Portals/61/documents/AFDP_1-1/AFDP%201-1%20Mission%20Command.pdf)  
15. DOD Data Strategy, accessed November 24, 2025, [https://media.defense.gov/2020/Oct/08/2002514180/-1/-1/0/DOD-DATA-STRATEGY.PDF](https://media.defense.gov/2020/Oct/08/2002514180/-1/-1/0/DOD-DATA-STRATEGY.PDF)  
16. AI Agents in Military: Next-Gen Defense Technology \- Creole Studios, accessed November 24, 2025, [https://www.creolestudios.com/ai-agent-military-use/](https://www.creolestudios.com/ai-agent-military-use/)  
17. Air Force Doctrine Publication 3-60, Targeting, accessed November 24, 2025, [https://www.doctrine.af.mil/Portals/61/documents/AFDP\_3-60/3-60-AFDP-TARGETING.pdf](https://www.doctrine.af.mil/Portals/61/documents/AFDP_3-60/3-60-AFDP-TARGETING.pdf)  
18. INFORMATION IN AIR FORCE OPERATIONS, accessed November 24, 2025, [https://www.doctrine.af.mil/Portals/61/documents/AFDP\_3-13/3-13-AFDP-INFO-OPS.pdf](https://www.doctrine.af.mil/Portals/61/documents/AFDP_3-13/3-13-AFDP-INFO-OPS.pdf)  
19. Air Force Doctrine Publication 3-0, Operations, accessed November 24, 2025, [https://www.doctrine.af.mil/Portals/61/documents/AFDP\_3-0/AFDP3-0Operations.pdf](https://www.doctrine.af.mil/Portals/61/documents/AFDP_3-0/AFDP3-0Operations.pdf)  
20. Air Force Doctrine Note 25-1, Artificial Intelligence (AI), accessed November 24, 2025, [https://www.doctrine.af.mil/Portals/61/documents/AFDN\_25-1/AFDN%2025-1%20Artificial%20Intelligence.pdf](https://www.doctrine.af.mil/Portals/61/documents/AFDN_25-1/AFDN%2025-1%20Artificial%20Intelligence.pdf)  
21. Akoma Ntoso Version 1.0. Part 1: XML Vocabulary \- Index of / \- OASIS Open, accessed November 24, 2025, [https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html)  
22. Welcome to tulit's documentation\! \- Read the Docs, accessed November 24, 2025, [https://tulit-docs.readthedocs.io/en/latest/](https://tulit-docs.readthedocs.io/en/latest/)  
23. laws-africa/bluebell: Bluebell is a generic Akoma Ntoso 3 parser. \- GitHub, accessed November 24, 2025, [https://github.com/laws-africa/bluebell](https://github.com/laws-africa/bluebell)  
24. DODAF Formal Ontology \- DoD CIO \- Department of War, accessed November 24, 2025, [https://dodcio.defense.gov/Library/DoD-Architecture-Framework/dodaf20\_ontology1/](https://dodcio.defense.gov/Library/DoD-Architecture-Framework/dodaf20_ontology1/)  
25. The Common Core Ontologies \- University of Twente, accessed November 24, 2025, [https://www.utwente.nl/en/eemcs/fois2024/resources/papers/jensen-et-al-the-common-core-ontologies.pdf](https://www.utwente.nl/en/eemcs/fois2024/resources/papers/jensen-et-al-the-common-core-ontologies.pdf)  
26. Ten Questions Defense Leaders Must Ask About Knowledge Graphs \- Altair, accessed November 24, 2025, [https://altair.com/blog/executive-insights/deploying-knowledge-graphs-in-defense](https://altair.com/blog/executive-insights/deploying-knowledge-graphs-in-defense)  
27. Deontic Logic \- Stanford Encyclopedia of Philosophy, accessed November 24, 2025, [https://plato.stanford.edu/entries/logic-deontic/](https://plato.stanford.edu/entries/logic-deontic/)  
28. RAWE: A Web Editor for Rule Markup in LegalRuleML \- CEUR-WS.org, accessed November 24, 2025, [https://ceur-ws.org/Vol-1004/paper4.pdf](https://ceur-ws.org/Vol-1004/paper4.pdf)  
29. spaCy · Industrial-strength Natural Language Processing in Python, accessed November 24, 2025, [https://spacy.io/](https://spacy.io/)  
30. LexNLP \- Open Source Legal, accessed November 24, 2025, [https://opensource.legal/projects/LexNLP](https://opensource.legal/projects/LexNLP)  
31. Towards Automatic Composition of ASP Programs from Natural Language Specifications \- IJCAI, accessed November 24, 2025, [https://www.ijcai.org/proceedings/2024/0685.pdf](https://www.ijcai.org/proceedings/2024/0685.pdf)  
32. CNL2ASP: Converting Controlled Natural Language Sentences into ASP | Theory and Practice of Logic Programming \- Cambridge University Press & Assessment, accessed November 24, 2025, [https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/cnl2asp-converting-controlled-natural-language-sentences-into-asp/AF5901FADC579E49C583CFD5A10C0192](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/cnl2asp-converting-controlled-natural-language-sentences-into-asp/AF5901FADC579E49C583CFD5A10C0192)  
33. Process Mining, accessed November 24, 2025, [https://www.processmining.org/](https://www.processmining.org/)  
34. Knowledge graphs for AI agents: The architectural backbone of next-generation intelligence, accessed November 24, 2025, [https://blog.hellord.com/knowledge-graphs-for-ai-agents-the-architectural-backbone-of-next-generation-intelligence-3878d02ca8f8](https://blog.hellord.com/knowledge-graphs-for-ai-agents-the-architectural-backbone-of-next-generation-intelligence-3878d02ca8f8)  
35. The Future of Mission-Readiness: Knowledge Graphs and Contextual AI for Defense, accessed November 24, 2025, [https://medium.com/@ValkyrieAI/the-future-of-mission-readiness-knowledge-graphs-and-contextual-ai-for-defense-0566078369a5](https://medium.com/@ValkyrieAI/the-future-of-mission-readiness-knowledge-graphs-and-contextual-ai-for-defense-0566078369a5)  
36. Rules \- DoD Open Government, accessed November 24, 2025, [https://open.defense.gov/Regulatory-Program/Rules/](https://open.defense.gov/Regulatory-Program/Rules/)  
37. Acquiring Machine-Readable Data \> JAG Reporter \> Article View Post, accessed November 24, 2025, [https://www.jagreporter.af.mil/Post/Article-View-Post/Article/3216144/acquiring-machine-readable-data/](https://www.jagreporter.af.mil/Post/Article-View-Post/Article/3216144/acquiring-machine-readable-data/)  
38. Implementing a Modular Open Systems Approach in Department of Defense Programs \- USD(R\&E), accessed November 24, 2025, [https://www.cto.mil/wp-content/uploads/2025/03/MOSA-Implementation-Guidebook-27Feb2025-Cleared.pdf](https://www.cto.mil/wp-content/uploads/2025/03/MOSA-Implementation-Guidebook-27Feb2025-Cleared.pdf)  
39. CNL2ASP: Converting Controlled Natural Language Sentences into ASP \- Cambridge University Press & Assessment, accessed November 24, 2025, [https://www.cambridge.org/core/services/aop-cambridge-core/content/view/AF5901FADC579E49C583CFD5A10C0192/S1471068423000388a.pdf/cnl2asp\_converting\_controlled\_natural\_language\_sentences\_into\_asp.pdf](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/AF5901FADC579E49C583CFD5A10C0192/S1471068423000388a.pdf/cnl2asp_converting_controlled_natural_language_sentences_into_asp.pdf)  
40. From Legal Documents to Knowledge Graphs | by Tomaz Bratanic | Neo4j Developer Blog, accessed November 24, 2025, [https://medium.com/neo4j/from-legal-documents-to-knowledge-graphs-ccd9cb062320](https://medium.com/neo4j/from-legal-documents-to-knowledge-graphs-ccd9cb062320)