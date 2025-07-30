# Natural Selection and Ecological Process Simulator

## Synposis
The simulator will perform a complex modelling of natural selection and evolution similar to Earth's but with different species. Visualized with pygame, this simulator will be a state-of-the-art method to depict the complex workings of evolution, from predator-prey relationships, mutations, and speciation all the way to multiagent collaboration, symbiosis, and parasitism.

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

## **Phase 3: Ecological Interactions**

Objective: Introduce predator-prey and basic ecological dynamics.

### **Tasks**

* Add species distinction: prey vs. predator

* Predators seek and attack prey for energy

* Prey flee from nearby predators

* Fitness \= survival time \+ reproduction count

* Add competition for resources (limited food, push evolution)

* Implement carrying capacity (ecological bottlenecks)

* Introduce basic terrain/obstacles (affecting pathing)

---

## **Phase 4: Genetics and Speciation**

Objective: Model long-term evolutionary divergence.

### **Tasks**

* Calculate genetic distance between organisms

* Track lineages and ancestry (assign IDs)

* Introduce speciation:

  * Genetic distance \+ spatial isolation

  * Assign new species ID if conditions met

* Visual markers or coloring for different species

* Add reproduction strategies: random vs. preference-based (optional)

---

## **Phase 5: Environment & Weather Systems**

Objective: Add ecological variability and selection pressures from the environment.

### **Tasks**

* Implement:

  * Day/night cycle (light level affects vision or activity)

  * Temperature zones affecting survival or reproduction

  * Resource regen depending on weather

* Seasons (affect food availability, temperature)

* Organisms with traits adapted to environment

  * E.g., cold resistance, night vision

---

## **Phase 6: Behavioral Evolution**

Objective: Add adaptive behavior and evolving decision logic.

### **Tasks**

* State machines: idle, seek food, evade, seek mate, rest

* Perception system (field of view, cone or circle)

* Behavior driven by traits (vision, speed)

* Optional: evolve weights for decision making (neuroevolution)

* Optional: use NEAT or evolve behavior trees

---

## **Phase 7: Visualization and Data Analytics**

Objective: Enable analysis and interpretability.

### **Tasks**

* Stats dashboard in-game (population, species count, trait means)

* Plot graphs with `matplotlib` (live or saved):

  * Trait distributions over time

  * Fitness and population trends

* Implement pause, step, fast-forward, reset

* Export run data to CSV or JSON for later analysis

* Allow toggling overlays: species view, vision cones, fitness, etc.

---

## **Phase 8: Configuration, Persistence, UI**

Objective: Enable customization, reproducibility, and longer experiments.

### **Tasks**

* Config system (YAML, JSON, or CLI args)

  * Mutation rate, food regen, map size, initial traits

* Save/load simulation state (pickle or custom format)

* Seeded random number generation for repeatability

* Allow manual placing of food/organisms via mouse

* Optional: GUI menu to tweak parameters live

---

## **Phase 9: Advanced Features (Optional)**

Objective: Deepen realism or explore complex dynamics.

### **Tasks**

* Parasitism: organisms that steal energy

* Symbiosis: e.g., cleaners vs. host

* Disease model: pathogen with traits, spread rate, lethality

* Niche construction: scent trails, resource hoarding, shelters

* Culture/memetic evolution (e.g., flocking rules passed socially)

* Evolutionary arms races between predator and prey traits

---

## **Project Structure (Suggested)**
  
`evo_sim/`  
`├── main.py`  
`├── config.py`  
`├── organism.py`  
`├── species.py`  
`├── environment.py`  
`├── traits.py`  
`├── simulation.py`  
`├── ui/`  
`│   ├── visualizer.py`  
`│   └── dashboard.py`  
`├── data/`  
`│   ├── logs/`  
`│   └── saves/`  
`├── utils/`  
`│   ├── math_utils.py`  
`│   └── spatial_indexing.py`  
`└── assets/`

---

## **Usage**

### Running the Simulation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the simulation:
   ```bash
   python main.py
   ```

3. Run the Phase 2 demo (includes analysis):
   ```bash
   python demo_phase2.py
   ```

### Controls

- **Space**: Pause/Resume simulation
- **R**: Reset simulation
- **Escape**: Quit

### Features

- Real-time visualization of organisms with trait-based colors (red = fast, green = slow)
- DNA system with 6 traits: speed, vision, size, metabolism, reproduction_threshold, max_age
- Trait-to-behavior mapping: speed affects movement, vision affects food detection
- Asexual reproduction with gaussian mutation inheritance
- Death by energy depletion or age limit
- Comprehensive trait tracking and statistical analysis
- Food regeneration and energy-based survival
- Generation tracking and population dynamics

## **Tools & Libraries**

| Feature | Tool/Library |
| ----- | ----- |
| 2D Visualization | `pygame` |
| Plotting & analysis | `matplotlib`, `seaborn`, `pandas` |
| Genetic algorithms | `numpy`, `scipy`, optional `deap` |
| Save/load | `pickle`, `json` |
| Debugging | `cProfile`, `tqdm`, `logging` |
