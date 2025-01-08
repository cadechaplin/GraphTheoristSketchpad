

# GraphTheoristSketchpad

GraphTheoristSketchpad is an interactive application for creating, editing, and analyzing graph structures. It provides a user-friendly interface for visualizing nodes and edges, running graph algorithms, and viewing matrix representations of graphs.

---

## Features

### Nodes
- **Creating Nodes:**  
  Use the `Create Node` button in the Control tab. New nodes are blue by default, named "vx" (where `x` is the lowest available non-negative number), and have no initial edges.
  
- **Editing Nodes:**  
  When a node is selected, you can:  
  - **Change Name:** Enter a label in the textbox and click `Change Name` to save.  
  - **Choose Color:** Open a color picker with the `Choose Color` button.  
  - **Adjust Size:** Use the slider to resize the node.  
  - **Delete Node:** Deletes the node and all connected edges.  

- **Node Selection:**  
  Double-click a node, use the node drop-down menu, or select "None" to unselect. Selected nodes have a red outline.

- **Moving Nodes:**  
  Drag nodes to reposition them. Connected edges automatically adjust.

---

### Edges
- **Creating Edges:**  
  Use the `Create Edge` button in the Control tab, then select two nodes. New edges are black by default, named "edge x" (where `x` is the lowest available non-negative number). You can set edges as directional.

- **Editing Edges:**  
  When an edge is selected, you can:  
  - **Change Name:** Enter a new label and click `Change Name`.  
  - **Choose Color:** Open a color picker with the `Choose Color` button.  
  - **Toggle Directionality:** Use the checkbox to toggle directionality.  
  - **Delete Edge:** Removes the edge from the graph.

- **Edge Selection:**  
  Double-click an edge, use the edge drop-down menu, or select "None" to unselect. Selected edges are highlighted.

---

### Algorithms
- **Running Algorithms:**  
  Access the `Algorithms` tab, select an algorithm, and click `Run` to execute. Results and visualizations appear in the application.

- **Available Algorithms:**  
  - **Breadth-First Search (BFS):** Layer-by-layer graph traversal.  
  - **Depth-First Search (DFS):** Explores branches to their limits before backtracking.  
  - **Dijkstra's Algorithm:** Finds the shortest paths in weighted graphs.  
  - **Topological Sort:** Linear ordering for Directed Acyclic Graphs (DAGs).  
  - **Custom Algorithms:** Additional options may be available.

---

### Matrices
- **Viewing Matrices:**  
  The `Matrix` tab displays adjacency, incidence, or other relevant graph matrices.

- **Interacting with Matrices:**  
  - **Edit Connections:** Modify matrix entries to add/remove edges. Changes update the graph.  
  - **Analyze Graph Properties:** Calculate properties like node degrees and connectivity.

---

### Additional Features
- **Saving and Loading Graphs:**  
  - **Save:** Use the `Save Graph` option in the File menu.  
  - **Load:** Open saved graphs with the `Load Graph` option.  

- **Exporting Graphs:**  
  - **Export as Image:** Save the current graph as a PNG, JPEG, or SVG file.  

- **User Interface Overview:**  
  - **Control Tab:** Create/edit nodes and edges.  
  - **Zooming and Panning:** Use the scroll wheel to zoom and right-click drag to pan.  

- **Keyboard Shortcuts:**  
  - `Ctrl + Z`: Undo  
  - `Ctrl + Y`: Redo  

---

### Preferences and Settings
- **Customization:**  
  Adjust default colors, node sizes, and more in the Settings menu.  

- **Auto-Save:**  
  Enable auto-save to periodically save progress and prevent data loss.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/GraphTheoristSketchpad.git
   cd GraphTheoristSketchpad
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

---

## Contributing

1. Fork the repository.  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add AmazingFeature"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Support

For assistance or advanced features, refer to the Help section in the application or visit the official documentation.

---
