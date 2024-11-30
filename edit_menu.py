from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QGraphicsView, QInputDialog, QSlider, QColorDialog, QCheckBox, QComboBox, QTabWidget, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from node import Node
from edge import Edge



class EditMenu(QWidget):
        


    def __init__(self):
        super().__init__()
        self.graph = None

        # Create a QTabWidget
        self.tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        


        # Create a QWidget for the Controls tab
        controls_widget = QWidget()
        self.controls_layout = QVBoxLayout()
        controls_widget.setLayout(self.controls_layout)

        # Create NodeMenu and EdgeMenu layouts
        self.NodeMenu = QVBoxLayout()
        self.EdgeMenu = QVBoxLayout()
        self.selectionMenu = QVBoxLayout()

        # Common controls
        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.color_button = QPushButton("Choose Color")
        self.delete_button = QPushButton("Delete")

        # Selection menu controls
        self.selection_label = QLabel("Selection:")
        self.selection_label_Node = QLabel("Node:")
        self.selectNode = QComboBox()
        self.selectNode.currentTextChanged.connect(self.onNodeSelection)
        self.selection_label_Edge = QLabel("Edge:")
        self.selectEdge = QComboBox()
        self.selectEdge.currentTextChanged.connect(self.onEdgeSelection)

        # Add widgets to selectionMenu
        self.selectionMenu.addWidget(self.selection_label)
        self.selectionMenu.addWidget(self.selection_label_Node)
        self.selectionMenu.addWidget(self.selectNode)
        self.selectionMenu.addWidget(self.selection_label_Edge)
        self.selectionMenu.addWidget(self.selectEdge)

        # Node-specific controls
        self.size_label = QLabel("Size:")
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(10, 100)

        # Edge-specific controls
        self.toggleDirectionalCheckbox = QCheckBox("Directional")
        self.toggleDirectionalCheckbox.stateChanged.connect(self.updateDirectional)

        # Add controls to NodeMenu
        self.NodeMenu.addWidget(self.name_label)
        self.NodeMenu.addWidget(self.name_edit)
        self.NodeMenu.addWidget(self.color_button)
        self.NodeMenu.addWidget(self.size_label)
        self.NodeMenu.addWidget(self.size_slider)
        self.NodeMenu.addWidget(self.delete_button)

        # Add controls to EdgeMenu
        self.EdgeMenu.addWidget(self.name_label)
        self.EdgeMenu.addWidget(self.name_edit)
        self.EdgeMenu.addWidget(self.color_button)
        self.EdgeMenu.addWidget(self.toggleDirectionalCheckbox)
        self.EdgeMenu.addWidget(self.delete_button)

        # Add layouts to the controls_layout
        self.controls_layout.addLayout(self.selectionMenu)
        self.controls_layout.addLayout(self.NodeMenu)
        self.controls_layout.addLayout(self.EdgeMenu)

        # Add Node and Edge buttons
        self.add_node_button = QPushButton("Add Node")
        self.add_edge_button = QPushButton("Add Edge")
        self.controls_layout.addWidget(self.add_node_button)
        self.controls_layout.addWidget(self.add_edge_button)

        # Add the controls widget as a tab
        self.tabs.addTab(controls_widget, "Controls")

        # Connect signals
        self.color_button.clicked.connect(self.choose_color)
        self.name_edit.textChanged.connect(self.update_name)
        self.size_slider.valueChanged.connect(self.update_size)
        self.delete_button.clicked.connect(self.delete)
        self.add_node_button.clicked.connect(self.add_node)
        self.add_edge_button.clicked.connect(self.add_edge)

        # Initialize visibility
        self.hide_edge_controls()

        # Variable to store the currently selected item
        self.selected_item = None
        
        #example for adding new tab
        new_tab_widget = QWidget()
        new_tab_layout = QVBoxLayout()
        new_tab_widget.setLayout(new_tab_layout)
        # Add widgets to new_tab_layout as needed
        self.tabs.addTab(new_tab_widget, "New Tab")
        
    def bind_graph(self, graph):
        self.graph = graph
        graph.SelectionChanged.update.append(self.updateSelectionMenu)
        graph.nodes.onSelectionChanged.update.append(self.updateSelectionMenu)  # Handle node selection change

    def add_node(self):
        name = f"v{self.graph.node_counter}"
        node_count = self.graph.node_counter
        while name in [node.name for node in self.graph.nodes]:
            node_count += 1
            name = f"v{node_count}"
        self.graph.node_counter += 1
        pos = QPoint(100 + len(self.graph.nodes) * 50, 300)
        self.graph.add_node(name, pos)
        
        self.updateSelectionMenu()

    def add_edge(self):
        if len(self.graph.nodes) < 1:
            return

        node_names = [node.name for node in self.graph.nodes]
        node1_name, ok1 = QInputDialog.getItem(self, "Add Edge", "Select first node:", node_names)
        if not ok1 or not node1_name:
            return

        node2_name, ok2 = QInputDialog.getItem(self, "Add Edge", "Select second node:", node_names)
        if not ok2 or not node2_name:
            return

        from_node = next(node for node in self.graph.nodes if node.name == node1_name)
        to_node = next(node for node in self.graph.nodes if node.name == node2_name)
        
        self.graph.add_edge(from_node, to_node, "edge " + str(self.graph.edge_counter), True)
        self.graph.edge_counter += 1
        self.updateSelectionMenu()
    
    def choose_color(self):
        if self.selected_item:
            color = QColorDialog.getColor()
            if color.isValid():
                if isinstance(self.selected_item, Node):
                    # Update node color
                    self.selected_item.viewModel.dColor = color
                    self.selected_item.viewModel.hoverColor = color.lighter(125)
                elif isinstance(self.selected_item, Edge):
                    # Edge color handling if needed
                    pass
                self.update_item()

    
        
        
        
    
    def updateSelectionMenu(self, change_selection=False):
        # Block all signals during selection updates
        self.selectNode.blockSignals(True)
        self.selectEdge.blockSignals(True)
        self.name_edit.blockSignals(True)
    
        self.selectNode.clear()
        self.selectEdge.clear()
        
        # Add items to selection menus
        self.selectNode.addItem("None")
        for node in self.graph.nodes:
            self.selectNode.addItem(node.name)
        self.selectEdge.addItem("None")
        for edge in self.graph.edges:
            self.selectEdge.addItem(edge.name)
        
        # Reset both selections
        self.selectNode.setCurrentText("None")
        self.selectEdge.setCurrentText("None")
        self.selected_item = None
        
        # Update based on current selection
        if self.graph.nodes.selected and isinstance(self.graph.nodes.selected, Node):
            self.selectNode.setCurrentText(self.graph.nodes.selected.name)
            self.show_node_controls()
            self.name_edit.setText(self.graph.nodes.selected.name)
            self.selected_item = self.graph.nodes.selected
        elif self.graph.selected and isinstance(self.graph.selected, Edge):
            self.selectEdge.setCurrentText(self.graph.selected.name)
            self.show_edge_controls()
            self.name_edit.setText(self.graph.selected.name)
            self.selected_item = self.graph.selected
        else:
            self.show_node_controls()  # Default to node controls
            self.name_edit.clear()
        
        # Re-enable signals
        self.selectNode.blockSignals(False)
        self.selectEdge.blockSignals(False)
        self.name_edit.blockSignals(False)
    
        
        
    def onNodeSelection(self, text):
        # Block all signals during selection change
        self.name_edit.blockSignals(True)
        self.selectEdge.blockSignals(True)
        
        if text == "None":
            self.graph.nodes.setSelected(None)
        else:
            # Properly deselect edge first
            if self.graph.selected:
                old_edge = self.graph.selected
                self.graph.selected = None
                old_edge.viewModel.update()
            
            for node in self.graph.nodes:
                if node.name == text:
                    self.graph.nodes.setSelected(node)
                    break
        
        # Reset edge selection UI
        self.selectEdge.setCurrentText("None")
        
        # Update the editor UI
        self.updateSelection(self.graph.nodes.selected)
        
        # Re-enable signals
        self.name_edit.blockSignals(False)
        self.selectEdge.blockSignals(False)
        
        self.graph.update()
        
    def onEdgeSelection(self, text=None):
        if text == "None":
            if self.graph.selected:
                old_edge = self.graph.selected
                self.graph.selected = None
                old_edge.viewModel.selected = False
                old_edge.viewModel.update()
        else:
            self.graph.nodes.deselect()  # Deselect the currently selected node
            
            # Clear old edge selection if exists
            if self.graph.selected:
                old_edge = self.graph.selected
                old_edge.viewModel.selected = False
                old_edge.viewModel.update()
                self.graph.selected = None
                    
            for edge in self.graph.edges:
                if edge.name == text:
                    self.graph.selected = edge
                    edge.viewModel.selected = True
                    edge.viewModel.update()
                    break
        
        self.selectNode.blockSignals(True)
        self.selectNode.setCurrentText("None")
        self.selectNode.blockSignals(False)
        
        # Update selection with the selected edge
        self.updateSelection(self.graph.selected)
        
        # Ensure the edge selection menu displays the selected edge
        self.selectEdge.blockSignals(True)
        self.selectEdge.setCurrentText(text)
        self.selectEdge.blockSignals(False)
        
        self.graph.update()
        
    def delete(self):
        #self.graph.deleteSelected()
        if self.selected_item:
            if isinstance(self.selected_item, Node):
                self.removeItem(self.selected_item)
                removeList = []
                for item in self.graph.edges:
                    if item.from_node == self.selected_item or item.to_node == self.selected_item:
                        removeList.append(item)
                for item in removeList:
                    self.removeItem(item)     
            elif isinstance(self.selected_item, Edge):
                self.removeItem(self.selected_item)
            self.selected_item = None
            self.update_item()
            self.updateSelectionMenu()
        self.update()
        return
    def removeItem(self,item):
        if isinstance(item, Node):
            self.graph.nodes.remove(item)
        else:
            self.graph.edges.remove(item)
        item.onDelete.trigger()
    
    def update_name(self, text):                
        if self.selected_item:
            if isinstance(self.selected_item, Node):
                if text in [node.name for node in self.graph.nodes]:
                    QMessageBox.warning(
                        self,
                        "Duplicate Name",
                        "Duplicate node names are not allowed.",
                        QMessageBox.Ok
                    )
                    # Reset name edit to original name
                    self.name_edit.blockSignals(True)
                    self.name_edit.setText(self.selected_item.name)
                    self.name_edit.blockSignals(False)
                    return
            self.selected_item.name = text
            self.update_item()
            self.updateSelectionMenu()  # Refresh the selection menu to reflect the new name
            if isinstance(self.selected_item, Edge):
                self.selectEdge.setCurrentText(self.graph.selected.name)


    def update_size(self, value):
        if self.selected_item and isinstance(self.selected_item, Node):
            self.selected_item.updateSize(value)
            self.update_item()
            
    def updateDirectional(self, value):
        if self.selected_item and isinstance(self.selected_item, Edge):
            self.selected_item.directional = value
            self.selected_item.viewModel.update()
            self.update_item()

    def update_item(self):
        # Redraw the graph after any change
        self.graph.update()

    def updateSelection(self, item):
        self.selected_item = item
        if isinstance(item, Node):
            # Show Node controls
            self.show_node_controls()

            # Set values for Node editing
            self.name_edit.setText(item.name)
            self.size_slider.setValue(item.getSize())

        elif isinstance(item, Edge):
            # Show Edge controls
            self.show_edge_controls()

            
            self.toggleDirectionalCheckbox.blockSignals(True)
            self.toggleDirectionalCheckbox.setChecked(item.directional)
            self.toggleDirectionalCheckbox.blockSignals(False)
            
            # Set values for Edge editing
            self.name_edit.setText(item.name)

        else:
            # Show node controls to maintain spacing
            
            self.show_node_controls()  
            self.hide_edge_controls()
            self.name_edit.clear()
            self.size_slider.setValue(10)
            self.toggleDirectionalCheckbox.setChecked(False)
            self.selected_item = None

        self.update()

    def show_node_controls(self):
        # Show all Node controls
        self.name_label.show()
        self.name_edit.show()
        self.color_button.show()
        self.size_label.show()
        self.size_slider.show()
        self.delete_button.show()

    def hide_node_controls(self):
        # Hide all Node controls
        self.name_label.hide()
        self.name_edit.hide()
        self.color_button.hide()
        self.size_label.hide()
        self.size_slider.hide()
        self.delete_button.hide()

    def show_edge_controls(self):
        # Show all Edge controls
        self.name_label.show()
        self.name_edit.show()
        self.color_button.show()
        self.size_label.hide()  # Edge does not need size control
        self.size_slider.hide()  # Edge does not need size control
        self.toggleDirectionalCheckbox.show()
        self.delete_button.show()

    def hide_edge_controls(self):
        # Hide all Edge controls
        self.name_label.hide()
        self.name_edit.hide()
        self.color_button.hide()
        self.toggleDirectionalCheckbox.hide()
        self.delete_button.hide()
