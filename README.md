# Agentic Aerial Swarms

This project develops an **intelligent formation control framework for aerial drone swarms** using ROS/ROS2. It extends a classical leader–follower architecture into the next generation of Agentic Aerial Swarms by integrating **Generative AI** and **adaptive formation strategies**.

At its core, the framework enables a Leader drone to receive **natural language mission commands** from the user and translate them into executable swarm missions. The leader coordinates multiple Follower drones, guiding them into dynamically selected formations such as line, flock, or helical patterns. Unlike static swarm controllers, this framework incorporates **LLM-powered mission planning** and **context-aware formation adaptation**, allowing swarms to reason, reconfigure, and execute missions with greater autonomy and resilience.

---

## ✨ Key Features
- **Leader–Follower Swarm Control**  
  One leader drone orchestrates multiple follower drones through ROS topics and services.  

- **Natural Language Mission Interface (LLM-powered)**  
  Mission commands can be given in plain English (e.g., *“Survey the north field in line formation at 30m altitude”*). A lightweight open-source **Large Language Model (LLM)** (e.g., LLaMA, Mistral, Falcon) converts these commands into structured mission plans (waypoints, formations, safety constraints).  

- **Adaptive Formation Switching**  
  Swarm formations can adapt automatically in response to **environmental conditions**, **mission intent**, or **safety constraints** (e.g., switching to a line in a narrow passage, or tightening flock cohesion in high wind).  

- **Multiple Formation Modes**  
  - **Line Formation** for corridor navigation  
  - **Flock Formation** for cohesive group behavior  
  - **Helical Formation** for perimeter or volumetric surveillance  

- **Mission Execution Modes**  
  - **MANUAL**: User controls leader via RC, followers mirror formation  
  - **GUIDED**: User sends a waypoint; swarm moves autonomously to target  
  - **AUTO**: User uploads a full mission plan (series of waypoints), executed automatically by the swarm  

- **Safety and Resilience**  
  Includes geofencing, minimum separation enforcement, dynamic spacing, and optional ORCA-based collision avoidance.  

- **Simulation & Real-world Ready**  
  Designed for **ArduPilot SITL** and **Gazebo** testing, with support for real drone hardware via MAVROS.  

---

## 🚀 Why This Project Matters
The ability to command swarms of aerial robots in natural language and have them adapt their formation intelligently represents a major step toward human–swarm teaming, autonomous aerial robotics, and agentic multi-robot systems.

Traditional swarm control relies on rigid leader–follower rules and pre-programmed missions. Such systems struggle in dynamic environments, require expert configuration, and lack adaptability. By integrating Generative AI and agentic reasoning, this project enables swarms to:
- Interpret high-level intent directly from humans, reducing operator workload.
- Reconfigure adaptively in uncertain or constrained environments. 
- Provide a scalable foundation for future applications such as search & rescue operations, environmental monitoring & agriculture, disaster response, perimeter surveillance & security and infrastructure inspection.

In today’s world of increasing demand for **autonomous, resilient, and scalable drone operations**, this framework provides a much-needed step toward **trustworthy and adaptive aerial swarms**.

---
## 🛠️ Tech Stack
- **Robotics Middleware**: ROS Noetic (ROS 2 Humble ready)  
- **Flight Control Integration**: MAVROS, ArduPilot SITL  
- **Generative AI**: Open-source LLMs (LLaMA, Mistral, Falcon, Qwen) via Ollama / GPT4All / HuggingFace  
- **Swarm Algorithms**: Leader–Follower Control, Formation Geometry, ORCA (RVO2) Collision Avoidance  
- **Safety & Adaptation**: Geofencing, min-separation checks, dynamic spacing, formation FSM  
- **Simulation**: Gazebo Classic / Ignition  

---

## 📌 Roadmap
- [x] Leader–Follower swarm architecture (ROS + MAVROS)  
- [x] Mission execution in MANUAL / GUIDED / AUTO modes  
- [x] Basic line, flock, and helical formations  
- [ ] LLM-powered natural language interface for mission planning  
- [ ] Adaptive formation switching based on environmental context  
- [ ] Safety manager with geofencing & separation enforcement  
- [ ] End-to-end demo in PX4 SITL + Gazebo  
- [ ] Paper-ready experimental results  

---

## 🌍 Open Research & Collaboration
This project is part of ongoing research in **multi-robot systems, embodied intelligence, and agentic swarms**. The goal is to push forward the boundary of what is possible with **free, open-source AI and robotics tools**. Contributions and collaborations are welcome — whether in **ROS development**, **Generative AI integration**, or **experimental validation**.  
