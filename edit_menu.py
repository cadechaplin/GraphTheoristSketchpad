from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QSlider, QColorDialog, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from node import Node
from edge import Edge



class EditMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create NodeMenu and EdgeMenu layouts
        self.NodeMenu = QVBoxLayout()
        self.EdgeMenu = QVBoxLayout()
        self.selectionMenu = QVBoxLayout()

        # Common controls
        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.color_button = QPushButton("Choose Color")
        self.delete_button = QPushButton("Delete")
        
        #selection menu controls
        self.selection_label = QLabel("Selection:")
        self.selection_label_Node = QLabel("Node:")
        self.selectNode = QComboBox()
        self.selectNode.currentTextChanged.connect(self.onNodeSelection)
        self.selection_label_Edge = QLabel("Edge:")
        self.selectEdge = QComboBox()
        self.selectEdge.currentTextChanged.connect(self.onEdgeSelection)
        
        self.selectionMenu.addWidget(self.selection_label)
        self.selectionMenu.addWidget(self.selection_label_Node)
        self.selectionMenu.addWidget(self.selectNode)
        self.selectionMenu.addWidget(self.selection_label_Edge)
        self.selectionMenu.addWidget(self.selectEdge)

        # Node-specific controls
        self.size_label = QLabel("Size:")
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(10, 100)  # Adjust range as needed for node size

        # Edge specific controls
        self.toggleDirectionalCheckbox = QCheckBox("Directional")
        
        
        
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

        # Add layouts to the main layout
        self.layout.addLayout(self.selectionMenu)
        self.layout.addLayout(self.NodeMenu)
        self.layout.addLayout(self.EdgeMenu)
        

        # Initially hide all controls
        self.hide_node_controls()
        self.hide_edge_controls()

        # Variable to store the currently selected item (Node or Edge)
        self.selected_item = None

        # Connect signals
        self.color_button.clicked.connect(self.choose_color)
        self.name_edit.textChanged.connect(self.update_name)
        self.size_slider.valueChanged.connect(self.update_size)
        self.delete_button.clicked.connect(self.delete)

    def choose_color(self):
        if self.selected_item:
            color = QColorDialog.getColor()
            if color.isValid():
                self.selected_item.fill_color = color  # Assume Node and Edge both have a 'color' attribute
                self.update_item()

    def bind_graph(self, graph):
        self.graph = graph
        graph.SelectionChanged.update.append(self.updateSelectionMenu)
        
        
        
    
    def updateSelectionMenu(self, change_selection = False):
        #Stops events from menu selection from triggering updateSelection
        self.selectNode.blockSignals(True)
        self.selectEdge.blockSignals(True)
    
        self.selectNode.clear()
        self.selectEdge.clear()
        
        
        
        self.selectNode.addItem("None")
        for node in self.graph.nodes:
            self.selectNode.addItem(node.name)
        self.selectEdge.addItem("None")
        for edge in self.graph.edges:
            self.selectEdge.addItem(edge.name)
        
        if self.graph.selected:
            if isinstance(self.graph.selected, Node):
                self.selectNode.setCurrentText(self.graph.selected.name)
            elif isinstance(self.graph.selected, Edge):
                self.selectEdge.setCurrentText(self.graph.selected.name)
        
        #Re-enables events
        self.selectNode.blockSignals(False)
        self.selectEdge.blockSignals(False)
        
    def onNodeSelection(self, text):
        
        for node in self.graph.nodes:
            if node.name == text:
                self.graph.selected = node
                break
            
        self.selectEdge.blockSignals(True)
        self.selectEdge.setCurrentText("None")
        self.selectEdge.blockSignals(False)
        
        self.updateSelection(self.graph.selected)
        
        self.graph.update()
        
    def onEdgeSelection(self, text = None):
        
        for edge in self.graph.edges:
                if edge.name == text:
                    self.graph.selected = edge
                    break
        
        self.selectNode.blockSignals(True)
        self.selectNode.setCurrentText("None")
        self.selectNode.blockSignals(False)
        
        self.updateSelection(self.graph.selected)
        
        self.graph.update()
        
    def delete(self):
        #self.graph.deleteSelected()
        if self.selected_item:
            if isinstance(self.selected_item, Node):
                self.graph.nodes.remove(self.selected_item)
                removeList = []
                for item in self.graph.edges:
                    if item.from_node == self.selected_item or item.to_node == self.selected_item:
                        removeList.append(item)
                for item in removeList:
                    self.graph.edges.remove(item)
            elif isinstance(self.selected_item, Edge):
                self.graph.edges.remove(self.selected_item)
            self.selected_item = None
            self.update_item()
            self.updateSelectionMenu()
        return
    
    def update_name(self, text):
        if self.selected_item:
            self.selected_item.name = text
            self.update_item()

    def update_size(self, value):
        if self.selected_item and isinstance(self.selected_item, Node):
            self.selected_item.size = value
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
            self.size_slider.setValue(item.size)

        elif isinstance(item, Edge):
            # Show Edge controls
            self.show_edge_controls()

            self.toggleDirectionalCheckbox.setChecked(item.directional)
            self.toggleDirectionalCheckbox.stateChanged.connect(self.update_item)
            # Set values for Edge editing
            self.name_edit.setText(item.name)

        else:
            # Hide all controls when no item is selected
            self.hide_node_controls()
            self.hide_edge_controls()

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
