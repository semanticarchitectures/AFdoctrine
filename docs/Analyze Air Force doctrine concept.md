Based on the analysis of current Air Force doctrine from **doctrine.af.mil**, below is a comprehensive breakdown of **Agile Combat Employment (ACE)**, **Weather Operations**, and **Intelligence, Surveillance, and Reconnaissance (ISR)**.

To model operational activity effectively, you must understand that these three functions are not isolated. They are deeply interconnected: **ISR** defines the threat environment, **Weather** defines the physical environmental constraints and opportunities, and **ACE** is the scheme of maneuver used to survive and fight within those defined environments.

### **1\. Agile Combat Employment (ACE)**

**Primary Source:** *Air Force Doctrine Note (AFDN) 1-21*

Core Concept:  
ACE is an operational scheme of maneuver designed to solve the problem of highly contested environments where main bases are vulnerable to missile attacks. It shifts operations from large, centralized "Enduring Locations" (hubs) to a network of smaller, dispersed "Contingency Locations" (spokes).  
**Key Definitions & Operational Model:**

* **Scheme of Maneuver:** ACE operates on two types of maneuver:  
  * **Proactive Maneuver:** Moving forces *before* a threat materializes to assure allies, deter aggression, or gain a positional advantage.  
  * **Reactive Maneuver:** Moving forces *during* a conflict in response to an attack or threat indicator to complicate the enemy's targeting.  
* **Threat Timelines:** ACE is executed "within threat timelines." This means you must model the enemy's **Kill Chain** (Find, Fix, Track, Target, Engage, Assess). If the enemy takes 60 minutes to target a base, your ACE movements (launching, recovering, refueling, rearming, and moving) must occur faster than that cycle.  
* **Cluster Operations:** An "Enduring Location" commander typically commands a "cluster" of contingency locations. This requires a modeling of **Hub-and-Spoke** logistics.  
* **Multi-Capable Airmen (MCA):** To operate with small footprints at dispersed sites, personnel are trained in cross-functional skills (e.g., a weapons loader who also performs base defense or refueling).  
* **Mission Command (CC-DC-DE):** This is the C2 (Command and Control) philosophy required for ACE.  
  * **Centralized Command:** The Air Component Commander sets the intent.  
  * **Distributed Control:** Authority is delegated to lower-echelon commanders (e.g., at the Cluster level).  
  * **Decentralized Execution:** Small units at remote airfields execute the mission based on "Commander's Intent" even when communications with HQ are cut (Denied, Degraded, Intermittent, or Limited \- DDIL environments).

### **2\. Weather Operations**

**Primary Source:** *Air Force Doctrine Publication (AFDP) 3-59*

Core Concept:  
Weather operations are not just about "forecasting rain"; they are about Decision Advantage. The goal is to predict the environment's effect on operations to optimize friendly forces and degrade the enemy.  
**Operational Framework:**

* **Function 1: Analysis and Forecasting:** This is the centralized "science" part. Large centers (like Operational Weather Squadrons) ingest global data from satellites and sensors to produce a coherent picture of the atmosphere and space environment.  
* **Function 2: Mission Integration:** This is the tactical "art" part. Weather personnel (Staff Weather Officers) are embedded with flying units (Combat Air Forces) or Army units. Their job is to **Integrate** weather effects into the planning cycle (Joint Planning Process).  
  * *Example for Modeling:* It is not enough to say "low clouds." The model must translate that to "low clouds degrade enemy optical sensors, creating a window for friendly movement, but ground friendly Close Air Support platforms."  
* **Impact on ACE:** Weather is a critical variable in ACE. Dispersed locations may lack robust instrument landing systems, making accurate weather data vital for deciding *which* contingency location is viable for landing.

### **3\. Intelligence, Surveillance, and Reconnaissance (ISR)**

**Primary Source:** *Air Force Doctrine Publication (AFDP) 2-0* (and Annex 2-0)

Core Concept:  
ISR is an activity that synchronizes sensors, assets, and processing systems. It is treated as an "Integrated Whole" (Global Integrated ISR). It is distinct from "Intelligence" (the product) but is the primary feeder for it.  
Operational Cycle (The "PCPADE" Model):  
To model ISR accurately, you must simulate the Joint Intelligence Process:

1. **Planning and Direction:** What does the Commander need to know? (Priority Intelligence Requirements).  
2. **Collection:** Sensors (space, air, cyber, human) gather raw data.  
3. **Processing and Exploitation:** Raw data is converted into usable forms (e.g., decoding signals, interpreting images).  
4. **Analysis and Production:** All-source analysts fuse information to create "Intelligence" (actionable knowledge).  
5. **Dissemination:** Getting the intel to the decision-maker.  
6. **Evaluation and Feedback:** Did we answer the question?

**Key Operational Relationships:**

* **ISR Drives the Air Tasking Order (ATO):** ISR identifies targets. Without ISR, the "Strike" missions in your model have nothing to hit.  
* **Battlespace Characterization:** ISR provides the "Red Picture" (Enemy disposition) that allows ACE forces to know *when* and *where* to move.

### **Summary: How to Model the Interaction**

To build a comprehensive operational model using these three doctrines:

1. **Start with ISR (AFDP 2-0):** The model generates a threat warning (e.g., "Enemy missile battery detecting base X"). This establishes the **Threat Timeline**.  
2. **Apply Weather (AFDP 3-59):** The model checks environmental conditions. "Is the weather at Contingency Location Y suitable for our aircraft?" If yes, it becomes a viable option; if no, that node is closed.  
3. **Execute ACE (AFDN 1-21):** The force executes a **Reactive Maneuver**.  
   * Aircraft flush from the threatened Base X.  
   * They fly to Contingency Location Y (validated by Weather).  
   * **Mission Command** takes over: If comms are jammed (simulated DDIL), the unit commander at Location Y makes the decision to refuel and launch a counter-strike based on the last known "Commander's Intent," without waiting for permission from the Air Operations Center.