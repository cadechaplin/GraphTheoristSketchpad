import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from graph import GraphWidget
from edit_menu import EditMenu

    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Edge Graph")
        self.setGeometry(100, 100, 800, 600)

        self.graph_widget = GraphWidget()
        
        self.setCentralWidget(self.graph_widget)


        # Create a QDockWidget for the buttons
        dock_widget = QDockWidget("Controls", self)
        dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        button_widget = QWidget()
        button_layout = QVBoxLayout()

        self.EditMenu = EditMenu()  # Save reference to node edit menu
        self.EditMenu.bind_graph(self.graph_widget)

        button_layout.addWidget(self.EditMenu)
        button_widget.setLayout(button_layout)

        dock_widget.setWidget(button_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
        self.graph_widget.SelectionChanged.update.append(self.updateSelection)

    def updateSelection(self):
        self.EditMenu.updateSelection(self.graph_widget.selected)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())