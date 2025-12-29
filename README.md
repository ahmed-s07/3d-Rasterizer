# PyRaster: Software 3D Rendering Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active_Development-orange)

**PyRaster** is a 3D graphics engine built from first principles in Python. Unlike standard graphics projects that rely on OpenGL or DirectX APIs, this engine implements the **programmable graphics pipeline** entirely in software.

The goal of this project is to simulate how a GPU handles vertex processing, primitive assembly, and rasterization at a low level. `Pygame` is utilized solely for the final frame buffer display (blitting pixels to the window); all 3D logic is custom-written.

## 📸 Demo
<img width="746" height="746" alt="Screenshot 2025-12-29 at 1 30 45 AM" src="https://github.com/user-attachments/assets/4d1c6ca6-f166-49de-bc7d-fb63808b976a" />


## 🧠 Core Features & Architecture

### 1. The Graphics Pipeline
The engine follows a standard fixed-function pipeline architecture:
1.  **Vertex Processing:** 3D World Coordinates $\rightarrow$ Camera Space.
2.  **Projection:** Perspective division to transform 3D coordinates to 2D screen space.
3.  **Rasterization:** Converting geometric primitives (triangles/lines) into fragments (pixels).

### 2. Mathematical Implementation
The engine relies heavily on Linear Algebra concepts without using vector libraries like GLM.

**Perspective Projection:**
To simulate depth, vertices are projected onto the 2D view plane by dividing by the $Z$ coordinate (depth).
$$x_{screen} = \frac{x_{world} \cdot f}{z_{world}}$$
*Where $f$ is the focal length (field of view).*

**Scanline Rasterization:**
The engine implements a **Scanline Triangle Filling Algorithm**. It:
* Sorts vertices by Y-coordinate.
* Interpolates X-coordinates along the edges (DDA Algorithm).
* Fills horizontal spans (scanlines) between the left and right edges.
* *Feature in progress:* Gouraud Shading via color interpolation along scanlines.

## 🛠 Tech Stack
* **Language:** Python
* **Dependencies:** `pygame` (Display driver only), `numpy` (planned for matrix optimizations)

## 🚀 Getting Started

### Prerequisites
You need Python installed. This project uses `pygame` for the window management.

```bash
pip install pygame
