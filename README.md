# Natural Selection and Ecological Process Simulator - Enhanced

## Synopsis
The Enhanced Natural Selection Simulator performs complex modeling of natural selection and evolution with unprecedented realism. This state-of-the-art simulator depicts the complex workings of evolution, from predator-prey relationships and mutations to speciation, multiagent collaboration, symbiosis, and advanced behavioral evolution.

## Major Enhancements (Latest Version)

### **Enhanced Trait System (30+ Traits)**
- **Movement Traits**: speed, vision, stamina
- **Behavioral Traits**: intelligence, social_behavior, exploration_rate, memory_capacity
- **Protective Traits**: camouflage, toxicity, armor, warning_signals, group_cohesion
- **Hunting Traits**: hunting_strategy, patience, cooperation, learning_rate
- **Weather Adaptation**: cold_resistance, heat_resistance, night_vision
- **Enhanced Traits**: efficiency, adaptability, resilience, specialization, innovation

### **Realistic Trait Interactions**
- **Trait Synergies**: Complementary traits provide bonuses (e.g., speed + stamina)
- **Trait Conflicts**: Opposing traits create penalties (e.g., aggression vs caution)
- **Adaptation Scoring**: Overall fitness based on trait combinations
- **Energy Efficiency**: Traits affect energy consumption and efficiency

### **Enhanced Evolutionary Pressure**
- **Realistic Energy Costs**: Movement, attacks, reproduction, and social behavior cost energy
- **Environmental Stress**: Temperature and weather affect survival
- **Resource Competition**: Limited food creates realistic competition
- **Territorial Behavior**: Organisms defend territories and compete for resources
- **Population Dynamics**: Natural growth and decline based on environmental conditions

### **Advanced Behavioral Evolution**
- **State Machines**: 8 behavioral states with realistic transitions
- **Learning Systems**: Organisms learn from experience and adapt strategies
- **Memory Systems**: Remember past events and successful strategies
- **Social Learning**: Share information with group members
- **Innovation**: Develop new strategies based on environmental challenges

### **Realistic Physics and Interactions**
- **Collision Detection**: Realistic organism interactions
- **Momentum Conservation**: Physics-based movement
- **Friction and Gravity**: Realistic environmental effects
- **Territorial Conflicts**: Competition for space and resources

### **Enhanced Environmental Systems**
- **Dynamic Weather**: Day/night cycles, temperature zones, seasons
- **Environmental Stress**: Weather affects organism survival and behavior
- **Resource Scarcity**: Realistic food availability and competition
- **Adaptation Tracking**: Monitor how well organisms adapt to environment

### **Advanced Visualization**
- **Energy Bars**: Visual energy levels on organisms
- **Trait Indicators**: Color coding for key traits
- **Behavioral States**: Visual indicators for current behavior
- **Evolutionary Pressure**: Warning indicators for high pressure
- **Environmental Effects**: Visual weather and temperature effects

## Roadmap

## **Phase 1: Core Infrastructure & Simulation Loop** ✅

Objective: Build a basic, functioning simulation loop with rudimentary agents in a 2D environment.

### **Tasks** ✅

* Project scaffolding and module structure ✅

  * `main.py`, `environment.py`, `organism.py`, `sim_config.py`, etc. ✅

* Initialize Pygame window and event loop ✅

* Create 2D world grid or continuous space (define coordinate system) ✅

* Add time steps and simulation tick control ✅

* Base `Organism` class with: ✅

  * Position ✅

  * Movement (random walk) ✅

  * Basic energy system ✅

* Basic food resources (as stationary points with regen) ✅

* Organism eats food to gain energy, dies if energy reaches 0 ✅

* Visualize organisms and food in Pygame ✅

---

## **Phase 2: Heredity and Reproduction** ✅

Objective: Implement reproduction and trait inheritance with mutation.

### **Tasks** ✅

* Add `DNA` (genome) to organisms: dict or list of traits ✅

  * Traits: speed, vision, size, metabolism, reproduction_threshold, max_age ✅

* Add trait-to-behavior mapping (phenotype mapping) ✅

* Asexual reproduction ✅

  * Reproduce when energy threshold met ✅

  * Child inherits DNA with mutation (Gaussian variation) ✅

* Death by age/energy ✅

* Visualize trait differences (color = speed) ✅

* Track and log trait distributions over time ✅

---

## **Phase 3: Ecological Interactions** ✅

Objective: Introduce predator-prey and basic ecological dynamics.

### **Tasks** ✅

* Add species distinction: prey vs. predator ✅

* Predators seek and attack prey for energy ✅

* Prey flee from nearby predators ✅

* Fitness = survival time + reproduction count ✅

* Add competition for resources (limited food, push evolution) ✅

* Implement carrying capacity (ecological bottlenecks) ✅

* Introduce basic terrain/obstacles (affecting pathing) ✅

---

## **Phase 4: Genetics and Speciation** ✅

Objective: Model long-term evolutionary divergence.

### **Tasks** ✅

* Calculate genetic distance between organisms ✅

* Track lineages and ancestry (assign IDs) ✅

* Introduce speciation: ✅

  * Genetic distance \+ spatial isolation ✅

  * Assign new species ID if conditions met ✅

* Visual markers or coloring for different species ✅

* Add reproduction strategies: random vs. preference-based (optional) ✅

---

## **Phase 5: Environment & Weather Systems** ✅

Objective: Add ecological variability and selection pressures from the environment.

### **Tasks** ✅

* Implement:

  * Day/night cycle (light level affects vision or activity) ✅

  * Temperature zones affecting survival or reproduction ✅

  * Resource regen depending on weather ✅

* Seasons (affect food availability, temperature) ✅

* Organisms with traits adapted to environment ✅

  * E.g., cold resistance, night vision ✅

---

## **Phase 6: Behavioral Evolution** ✅

Objective: Add adaptive behavior and evolving decision logic.

### **Tasks** ✅

* State machines: idle, seek food, evade, seek mate, rest ✅

* Perception system (field of view, cone or circle) ✅

* Behavior driven by traits (vision, speed) ✅

* Optional: evolve weights for decision making (neuroevolution) ✅

* Optional: use NEAT or evolve behavior trees ✅

* Prey protective features beyond simple fleeing ✅
  - Camouflage: reduces detection by predators
  - Toxicity: damages attacking predators
  - Armor: provides physical protection
  - Warning signals: alerts nearby prey
  - Group cohesion: protective group behavior

* Predator hunting strategies ✅
  - Ambush hunting: wait and strike
  - Cooperative hunting: coordinate with other predators
  - Pursuit hunting: standard chase and attack

* Social behavior and information sharing ✅

* Memory-based decision making and learning ✅

* Visual behavioral state indicators ✅

---

## **Phase 7: Enhanced Evolution & Realism** ✅

Objective: Create a balanced and realistic simulation with advanced evolutionary mechanisms.

### **Tasks** ✅

* **Enhanced Trait System**: 30+ traits with realistic interactions ✅
  - Trait synergies and conflicts
  - Adaptation scoring
  - Energy efficiency calculations

* **Realistic Energy Costs**: Movement, attacks, reproduction cost energy ✅
  - Speed affects energy consumption
  - Size affects energy requirements
  - Metabolism affects energy decay

* **Enhanced Evolutionary Pressure**: Stronger selection pressures ✅
  - Environmental stress
  - Resource competition
  - Population density effects

* **Territorial Behavior**: Organisms defend territories ✅
  - Territory establishment
  - Territorial conflicts
  - Resource claiming

* **Advanced Learning Systems**: Memory and experience-based learning ✅
  - Experience memory
  - Strategy learning
  - Behavioral adaptation

* **Realistic Physics**: Collision detection and momentum ✅
  - Collision detection
  - Momentum conservation
  - Friction and gravity effects

* **Population Dynamics**: Natural growth and decline ✅
  - Extinction thresholds
  - Recovery mechanisms
  - Population diversity tracking

---

## **Phase 8: Visualization and Data Analytics** ✅

Objective: Enable analysis and interpretability.

### **Tasks** ✅

* Stats dashboard in-game (population, species count, trait means) ✅

* Plot graphs with `matplotlib` (live or saved): ✅

  * Trait distributions over time ✅

  * Fitness and population trends ✅

* Implement pause, step, fast-forward, reset ✅

* Export run data to CSV or JSON for later analysis ✅

* Allow toggling overlays: species view, vision cones, fitness, etc. ✅

* Enhanced visualization features: ✅
  - Energy bars on organisms
  - Trait-based color indicators
  - Behavioral state indicators
  - Environmental effect visualization
  - Evolutionary pressure indicators

---

## **Phase 9: Configuration, Persistence, UI** ✅

Objective: Enable customization, reproducibility, and longer experiments.

### **Tasks** ✅

* Config system (YAML, JSON, or CLI args) ✅

  * Mutation rate, food regen, map size, initial traits ✅

* Save/load simulation state (pickle or custom format) ✅

* Seeded random number generation for repeatability ✅

* Allow manual placing of food/organisms via mouse ✅

* Optional: GUI menu to tweak parameters live ✅

---

## **Phase 10: Advanced Features (Optional)**

Objective: Deepen realism or explore complex dynamics.

### **Tasks**

* Parasitism: organisms that steal energy

* Symbiosis: e.g., cleaners vs. host

* Disease model: pathogen with traits, spread rate, lethality

* Niche construction: scent trails, resource hoarding, shelters

* Culture/memetic evolution (e.g., flocking rules passed socially)

* Evolutionary arms races between predator and prey traits

---

## **Project Structure**
  
`naturalselection/`  
`├── main.py`  
`├── sim_config.py`  
`├── organism.py`  
`├── environment.py`  
`├── weather_system.py`  
`├── simulation.py`  
`├── trait_analyzer.py`  
`├── demo_enhanced.py`  
`├── requirements.txt`  
`└── README.md`

---

## **Usage**

### Running the Enhanced Simulation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the enhanced simulation:
   ```bash
   python demo_enhanced.py
   ```

3. Run the basic simulation:
   ```bash
   python main.py
   ```

### Controls

- **Space**: Pause/Resume simulation
- **R**: Reset simulation
- **Escape**: Quit
- **1**: Toggle energy bars
- **2**: Toggle trait indicators
- **3**: Toggle behavioral state indicators
- **4**: Toggle evolutionary pressure indicators
- **5**: Toggle vision radius
- **6**: Toggle species colors
- **7**: Toggle day/night cycle
- **8**: Toggle temperature zones
- **9**: Toggle season indicator

### Features

#### **Enhanced Trait System**
- **30+ traits** with realistic interactions and evolution
- **Trait synergies**: Complementary traits provide bonuses
- **Trait conflicts**: Opposing traits create penalties
- **Adaptation scoring**: Overall fitness based on trait combinations
- **Energy efficiency**: Traits affect energy consumption

#### **Realistic Evolution**
- **Enhanced evolutionary pressure**: Stronger selection pressures
- **Environmental stress**: Weather affects survival and behavior
- **Resource competition**: Limited food creates realistic competition
- **Population dynamics**: Natural growth and decline
- **Territorial behavior**: Organisms defend territories

#### **Advanced Behavioral Systems**
- **8 behavioral states**: idle, seek_food, evade, hunt, rest, explore, group_behavior, seek_mate
- **Learning systems**: Memory and experience-based learning
- **Social behavior**: Information sharing and group coordination
- **Innovation**: Develop new strategies based on environment

#### **Realistic Physics**
- **Collision detection**: Realistic organism interactions
- **Momentum conservation**: Physics-based movement
- **Friction and gravity**: Realistic environmental effects

#### **Enhanced Environmental Systems**
- **Dynamic weather**: Day/night cycles, temperature zones, seasons
- **Environmental stress**: Weather affects organism survival
- **Resource scarcity**: Realistic food availability
- **Adaptation tracking**: Monitor environmental adaptation

#### **Advanced Visualization**
- **Energy bars**: Visual energy levels on organisms
- **Trait indicators**: Color coding for key traits
- **Behavioral states**: Visual indicators for current behavior
- **Evolutionary pressure**: Warning indicators for high pressure
- **Comprehensive analysis**: 9-panel plots with multiple metrics

#### **Comprehensive Analysis**
- **Real-time statistics**: Population, species, traits, fitness
- **Trait evolution tracking**: Monitor trait changes over time
- **Speciation analysis**: Track species formation and divergence
- **Environmental analysis**: Monitor stress and competition levels
- **Behavioral analysis**: Track learning and innovation rates

#### **Enhanced Data Export**
- **Comprehensive plots**: 9-panel analysis with multiple metrics
- **Trait interaction heatmap**: Visualize trait relationships
- **Speciation timeline**: Track species formation over time
- **CSV export**: Detailed data for external analysis

## **Tools & Libraries**

| Feature | Tool/Library |
| ----- | ----- |
| 2D Visualization | `pygame` |
| Plotting & analysis | `matplotlib`, `seaborn`, `pandas` |
| Genetic algorithms | `numpy`, `scipy`, optional `deap` |
| Save/load | `pickle`, `json` |
| Debugging | `cProfile`, `tqdm`, `logging` |

## **Key Improvements in Enhanced Version**

### **Balanced and Realistic Simulation**
- **Reduced mutation rates**: More stable evolution
- **Realistic energy costs**: Movement, attacks, reproduction cost energy
- **Enhanced selection pressure**: Stronger environmental and competitive pressures
- **Population balance**: Better predator-prey dynamics
- **Resource scarcity**: More realistic food competition

### **Advanced Trait Interactions**
- **Trait synergies**: Speed + stamina, vision + intelligence, etc.
- **Trait conflicts**: Aggression vs caution, efficiency vs innovation
- **Adaptation scoring**: Overall fitness based on trait combinations
- **Energy efficiency**: Traits affect energy consumption patterns

### **Enhanced Evolutionary Mechanisms**
- **Environmental adaptation**: Weather affects survival and reproduction
- **Territorial behavior**: Organisms compete for space and resources
- **Learning systems**: Memory and experience-based adaptation
- **Innovation**: Develop new strategies based on environmental challenges

### **Realistic Physics and Interactions**
- **Collision detection**: Realistic organism interactions
- **Momentum conservation**: Physics-based movement
- **Friction and gravity**: Realistic environmental effects
- **Territorial conflicts**: Competition for space and resources

### **Advanced Visualization and Analysis**
- **Energy bars**: Visual energy levels on organisms
- **Trait indicators**: Color coding for key traits
- **Behavioral states**: Visual indicators for current behavior
- **Evolutionary pressure**: Warning indicators for high pressure
- **Comprehensive analysis**: 9-panel plots with multiple metrics

This enhanced version creates a much more realistic and balanced simulation where all features can be mutated and evolved, with strong selection pressures driving meaningful evolutionary change.
