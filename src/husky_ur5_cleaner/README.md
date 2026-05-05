# 🤖 Solar PV Non-Water Cleaning Cobot

**ROS 2 Jazzy | Ubuntu 24.04**

---

## 📌 Project Vision

This project develops a **collaborative robot (cobot) system** designed for **waterless cleaning of solar photovoltaic (PV) panels** in large-scale solar farms.

The core idea is simple but impactful: solar panels degrade in efficiency significantly due to dust and particulate accumulation. Traditional cleaning methods consume high number of human labour and enormous volumes of water — a scarce resource in most high-solar-irradiance regions. This project explores a **dry, autonomous robotic alternative**.

The system pairs a **Clearpath Husky A200** ground mobile platform with a **Universal Robots UR5** manipulator arm to form an integrated cleaning cobot capable of:

1. **Autonomously navigating** a solar farm environment
2. **Reaching and cleaning** solar panel surfaces without water
3. **Operating from a simulation-first, hardware-ready** design paradigm

The project aims to follow a layered development approach:

1. **Robot modeling & environment simulation (current phase)**
2. Mobile base navigation & localization
3. Manipulator arm control & panel interaction
4. Full autonomous cleaning mission execution


---

## 🧱 Scope of This Repository

⚠️ **This repository currently covers the robot description, simulation environment, and basic mobility validation.**

It includes:
- ✅ Husky A200 and UR5 URDF/Xacro robot description
- ✅ Custom solar farm world for Gazebo simulation
- ✅ RViz2 visualization configuration
- ✅ Launch files for simulation bringup
- ✅ Husky A200 base navigation (teleoperation validated in Gazebo)

It does **not yet** include:
- ❌ UR5 arm motion planning or control
- ❌ Autonomous navigation stack (Nav2)
- ❌ Panel detection or cleaning path planning
- ❌ Sensor fusion or localization pipelines

> In short: **the robot exists in the world — now we teach it to move purposefully through it.**

---

## 🏗️ System Architecture

### 🦾 Robot Platform — Husky A200 and UR5

| Component | Details |
|---|---|
| **Mobile Base** | Clearpath Husky A200 |
| **Manipulator** | Universal Robots UR5 (6-DOF) |
| **Integration** | Custom URDF/Xacro cobot description |
| **Middleware** | ROS 2 Jazzy |
| **OS** | Ubuntu 24.04 LTS |
| **Simulator** | Gazebo (via `ros_gz`) |
| **Visualizer** | RViz2 |

### 🌍 Simulation Environment

The Gazebo world models a representative **solar farm layout** with:
- Arrayed PV panel structures at realistic geometry and spacing
- Ground terrain suitable for wheeled robot navigation
- A GeoTIFF overhead map for localization reference



## 📂 Repoo Structure

```text
husky_ur5_ws/                          (ROS 2 Workspace Root)
│
├── .gitattributes                     (Git LFS/Attributes)
├── .gitignore                         (Git ignore rules)         
├── images/                            (images and media of the project)         
├── README.md                          (project documentation)
│
└── src/
    └── husky_ur5_cleaner/             (Main ROS 2 Package)
        ├── urdf/                      (Robot Description Files)
        │   ├── a200/                  (Husky-specific URDF parts)
        │   ├── ur5/                   (UR5-specific URDF parts)
        │   ├── huskyur5.urdf.xacro    (Main Top-level Xacro)
        │   ├── joints.xacro
        │   ├── links.xacro
        │   └── materials.xacro
        │
        ├── launch/                    (ROS 2 Launch Files)
        │   ├── solar_farm_research.launch.py
        │   └── view_robot.launch.py
        │
        ├── worlds/                    (Gazebo World Definitions)
        │   └── solar_farm.sdf         (Custom environment definition)
        │
        ├── meshes/                    (3D Mesh Assets)
        │   ├── a200/
        │   ├── accessories/
        │   ├── solar_farm/
        │   └── ur5/
        │
        ├── config/                    (Controller & Parameter Configs)
        │   ├── a200/
        │   └── ur5/
        │
        ├── rviz/                      (RViz2 Configuration)
        │   └── view.rviz
        │
        ├── geotif/                    (Geospatial Map Data)
        │
        ├── README.md
        ├── CMakeLists.txt
        └── package.xml
```

---

## 👁️ Visuals & Simulation Previews

> 📁 All images and media are stored in the `/images` directory.

### 🟦 RViz2 — Robot Visualization
Full cobot model (Husky A200 + UR5) loaded and visualized with joint states, TF frames, and robot description.

![RViz2 Cobot Visualization](images/husky_ur5_rviz_visualization.png)

---

### 🟦 Gazebo — Simulation Environment
The Husky A200 + UR5 cobot spawned inside the custom solar farm Gazebo world.

![Gazebo Simulation](images/husky_ur5_gazebo_simulation.png)

---

### 🟦 GeoTIFF — Solar Environment Overhead Map
Top-down geospatial map of the solar farm environment used as a localization reference layer.

![Solar Environment GeoTIFF](images/geotif_solar_environment.png)

---

## 🛠️ Tools & Technologies

| Category | Stack |
|---|---|
| **Robot OS** | ROS 2 Jazzy Jalisco |
| **Operating System** | Ubuntu 24.04 LTS |
| **Simulation** | Gazebo (ros_gz bridge) |
| **Visualization** | RViz2 |
| **Robot Description** | URDF / Xacro |
| **Build System** | Colcon / CMake |
| **Version Control** | Git & GitHub |

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/abdulmumeen-abdullahi/Solar-PV-Non-Water-Cleaning-Cobot.git
```
then:
```bash
cd Solar-PV-Non-Water-Cleaning-Cobot
```

### 2. Install Dependencies

Ensure ROS 2 Jazzy and required dependencies are installed. Then run:

```bash
rosdep update
```
then:
```bash
rosdep install --from-paths src --ignore-src -r -y
```

### 3. Build the Workspace

```bash
colcon build
```
then:
```bash
source install/setup.bash
```

> 💡 **Tip:** Add `source ~/Projects/husky_ur5_ws/install/setup.bash` to your `~/.bashrc` to avoid repeating this step every session.

---

## 🚀 Running the System

### 4. Visualize the Robot in RViz2

Launch the Husky A200 + UR5 cobot model for inspection and debugging:

```bash
ros2 launch husky_ur5_cleaner view_robot.launch.py
```

This loads:
- Full robot description (URDF/Xacro)
- TF tree
- Preconfigured RViz2 visualization layout

### 5. Launch the Simulation (Gazebo)

Start the solar farm simulation environment:

```bash
ros2 launch husky_ur5_cleaner solar_farm_research.launch.py
```

This initializes:
- Husky A200 mobile base
- UR5 manipulator arm
- Custom solar farm Gazebo world
- Controllers and simulation interfaces

### 6. Teleoperate the Robot

In a **new terminal**:
```bash
source install/setup.bash
```
then:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r /cmd_vel:=/model/husky_ur5_cobot/cmd_vel
```

This remaps velocity commands directly to the simulated Husky base.

---

## 📝 Notes

- 📦 Large assets (meshes) are managed via **Git LFS**

---

## 🚀 Development Roadmap

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Robot modeling (URDF) + Environment setup | ✅ Complete |
| **Phase 1** | Husky A200 base teleoperation in Gazebo | ✅ Validated |
| **Phase 2** | UR5 arm motion planning (MoveIt 2) | 🔄 In Progress |
| **Phase 3** | Autonomous navigation with Nav2 | ⏳ Planned |
| **Phase 4** | Panel detection & cleaning path planning | ⏳ Planned |
| **Phase 5** | Full autonomous mission integration | ⏳ Planned |

---

## 🤝 Contributing

This is an active personal R&D project. If you work in agricultural robotics, solar energy automation, or ROS 2 development and want to collaborate or share feedback, feel free to open an issue or reach out directly.

---

## 🧠 Summary

> *Before a robot can clean a solar farm, it must first learn to exist in one — and then move through it with intent.*