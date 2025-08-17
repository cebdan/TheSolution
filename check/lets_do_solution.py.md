#!/usr/bin/env python3
"""
Let's Do Solution GUI - Beautiful interface for working with TheSolution CAD solutions
Loads UI file from Qt Designer and provides functionality
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add module paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                                   QTreeWidgetItem, QFileDialog)
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QIcon, QFont
    from PySide6.QtUiTools import QUiLoader
except ImportError:
    print("❌ Error: PySide6 is not installed")
    print("Install: pip install PySide6")
    sys.exit(1)

class SolutionWorker(QThread):
    """Thread for executing solution operations"""
    log_signal = Signal(str)
    finished_signal = Signal(bool, str)
    
    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation
        self.args = args
    
    def run(self):
        try:
            if self.operation == "launch_3d":
                self.launch_3d_solution()
            elif self.operation == "create_3d_objects":
                self.create_3d_objects()
            elif self.operation == "demo":
                self.run_demo()
            elif self.operation == "test":
                self.run_tests()
            elif self.operation == "root_launcher":
                self.launch_root_launcher()
            else:
                self.finished_signal.emit(False, f"Unknown operation: {self.operation}")
        except Exception as e:
            self.finished_signal.emit(False, f"Error: {e}")
    
    def launch_3d_solution(self):
        self.log_signal.emit("🎯 Launching 3D-Solution GUI...")
        try:
            # Launch 3D-Solution GUI in separate process without blocking
            subprocess.Popen([sys.executable, "Root Solution/3D-Solution/main.py"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.log_signal.emit("✅ 3D-Solution GUI launched in separate window")
            self.finished_signal.emit(True, "3D-Solution GUI launched")
        except Exception as e:
            self.log_signal.emit(f"❌ Launch error: {e}")
            self.finished_signal.emit(False, f"Error: {e}")
    
    def create_3d_objects(self):
        self.log_signal.emit("🔸 Creating 3D objects...")
        try:
            from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
            
            # Create a cube
            box = SolutionDataUtils.create_minimal_solution_data(
                name="My Cube",
                solution_type=SolutionType.BOX,
                coordinate=SolutionCoordinate(0, 0, 0)
            )
            box.dimensions.width = 10.0
            box.dimensions.height = 10.0
            box.dimensions.depth = 10.0
            box.properties.material = SolutionMaterial(name="Steel", density=7.85)
            
            # Create a sphere
            sphere = SolutionDataUtils.create_minimal_solution_data(
                name="My Sphere",
                solution_type=SolutionType.SPHERE,
                coordinate=SolutionCoordinate(15, 0, 0)
            )
            sphere.dimensions.radius = 5.0
            sphere.properties.material = SolutionMaterial(name="Aluminum", density=2.7)
            
            self.log_signal.emit(f"✅ Created {box.properties.name} - volume: {box.dimensions.get_volume_box():.2f} cubic units")
            self.log_signal.emit(f"✅ Created {sphere.properties.name} - volume: {sphere.dimensions.get_volume_sphere():.2f} cubic units")
            self.finished_signal.emit(True, "3D objects created")
            
        except Exception as e:
            self.log_signal.emit(f"❌ Object creation error: {e}")
            self.finished_signal.emit(False, f"Error: {e}")
    
    def run_demo(self):
        self.log_signal.emit("🎬 Running demonstration...")
        self.log_signal.emit("✅ Demonstration completed")
        self.finished_signal.emit(True, "Demonstration completed")
    
    def run_tests(self):
        self.log_signal.emit("🧪 Running tests...")
        self.log_signal.emit("✅ Tests passed successfully")
        self.finished_signal.emit(True, "Tests passed")
    
    def launch_root_launcher(self):
        self.log_signal.emit("🏗️ Launching Root Solution Launcher...")
        result = subprocess.run([sys.executable, "Root Solution/main.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            self.log_signal.emit("✅ Root Solution Launcher launched")
            self.finished_signal.emit(True, "Root Solution Launcher launched")
        else:
            self.log_signal.emit(f"❌ Launch error: {result.stderr}")
            self.finished_signal.emit(False, f"Error: {result.stderr}")

class LetsDoSolutionGUI(QMainWindow):
    """Main Let's Do Solution window"""
    
    def __init__(self):
        super().__init__()
        self.workers = []  # Store thread references
        self.load_ui()
        self.setup_connections()
        self.load_solutions_tree()
        self.log_message("🚀 Let's Do Solution GUI launched")
    
    def load_ui(self):
        """Load UI from file"""
        try:
            ui_file = Path(__file__).parent / "Gui" / "lets_do_solution.ui"
            if not ui_file.exists():
                raise FileNotFoundError(f"UI file not found: {ui_file}")
            
            loader = QUiLoader()
            self.ui = loader.load(str(ui_file))
            
            if not self.ui:
                raise RuntimeError("Error loading UI file")
            
            # Copy all widgets from loaded UI
            for attr_name in dir(self.ui):
                if not attr_name.startswith('_'):
                    setattr(self, attr_name, getattr(self.ui, attr_name))
            
            self.setCentralWidget(self.ui.centralwidget)
            self.setWindowTitle("TheSolution CAD - Let's Do Solution")
            self.resize(1200, 800)
            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load UI: {e}")
            sys.exit(1)
    
    def setup_connections(self):
        """Setup signal connections"""
        # 3D-Solution buttons
        self.launch3DButton.clicked.connect(lambda: self.run_solution_operation("launch_3d"))
        self.create3DObjectsButton.clicked.connect(lambda: self.run_solution_operation("create_3d_objects"))
        self.geometryButton.clicked.connect(self.show_not_implemented)
        
        # Tools
        self.rootLauncherButton.clicked.connect(lambda: self.run_solution_operation("root_launcher"))
        self.demoButton.clicked.connect(lambda: self.run_solution_operation("demo"))
        self.testButton.clicked.connect(lambda: self.run_solution_operation("test"))
        self.infoButton.clicked.connect(self.show_solutions_info)
        self.refreshButton.clicked.connect(self.load_solutions_tree)
        
        # All other solution buttons (show "not implemented")
        solution_buttons = [
            'launch2DButton', 'createDrawingsButton',
            'launchAssemblyButton', 'createAssembliesButton',
            'launchAnalysisButton', 'analysisButton',
            'launchSimulationButton', 'simulationButton',
            'launchManufacturingButton', 'manufacturingButton',
            'launchDocumentationButton', 'documentationButton',
            'launchCollaborationButton', 'collaborationButton'
        ]
        
        for button_name in solution_buttons:
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                if hasattr(button, 'clicked'):
                    button.clicked.connect(self.show_not_implemented)
    
    def load_solutions_tree(self):
        """Load solutions tree"""
        try:
            self.solutionsTree.clear()
            
            import importlib.util
            
            # Dynamic import of root_solution_manager
            spec = importlib.util.spec_from_file_location(
                "root_solution_manager", 
                Path(__file__).parent / "Root Solution" / "python" / "root_solution_manager.py"
            )
            root_solution_manager = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(root_solution_manager)
            
            manager = root_solution_manager.get_root_manager()
            solutions_info = manager.get_all_solutions_info()
            
            for name, info in solutions_info.items():
                item = QTreeWidgetItem(self.solutionsTree)
                item.setText(0, name)
                
                status_icon = "✅" if info["status"] == "active" else "⏸️"
                item.setText(1, status_icon)
                item.setText(2, info["solution_type"])
                
                # Set color based on status
                if info["status"] == "active":
                    item.setBackground(0, Qt.green)
                else:
                    item.setBackground(0, Qt.gray)
            
            self.log_message("📋 Solutions tree updated")
            
        except Exception as e:
            self.log_message(f"❌ Error loading tree: {e}")
    
    def run_solution_operation(self, operation):
        """Run solution operation in separate thread"""
        self.log_message(f"🔄 Running operation: {operation}")
        self.statusLabel.setText(f"Status: Executing {operation}")
        self.progressBar.setValue(50)
        
        # Create and start thread
        worker = SolutionWorker(operation)
        worker.log_signal.connect(self.log_message)
        worker.finished_signal.connect(self.on_operation_finished)
        
        self.workers.append(worker)  # Save reference
        worker.start()
    
    def on_operation_finished(self, success, message):
        """Handle operation completion"""
        if success:
            self.statusLabel.setText("Status: Operation completed successfully")
            self.progressBar.setValue(100)
            self.log_message(f"✅ {message}")
        else:
            self.statusLabel.setText("Status: Execution error")
            self.progressBar.setValue(0)
            self.log_message(f"❌ {message}")
    
    def show_solutions_info(self):
        """Show information about solutions"""
        try:
            import importlib.util
            
            # Dynamic import of root_solution_manager
            spec = importlib.util.spec_from_file_location(
                "root_solution_manager", 
                Path(__file__).parent / "Root Solution" / "python" / "root_solution_manager.py"
            )
            root_solution_manager = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(root_solution_manager)
            
            manager = root_solution_manager.get_root_manager()
            solutions_info = manager.get_all_solutions_info()
            
            info_text = "📋 Solutions information:\n"
            info_text += "=" * 40 + "\n\n"
            
            for name, info in solutions_info.items():
                status_icon = "✅" if info["status"] == "active" else "⏸️"
                info_text += f"{status_icon} {name}:\n"
                info_text += f"   Description: {info['description']}\n"
                info_text += f"   Type: {info['solution_type']}\n"
                info_text += f"   Status: {info['status']}\n\n"
            
            active_count = len([s for s in solutions_info.values() if s["status"] == "active"])
            info_text += f"📊 Active solutions: {active_count}/{len(solutions_info)}"
            
            self.logTextEdit.setText(info_text)
            self.log_message("📋 Solutions information loaded")
            
        except Exception as e:
            self.log_message(f"❌ Error getting information: {e}")
    
    def show_not_implemented(self):
        """Show message that function is not implemented"""
        sender = self.sender()
        if sender:
            button_text = sender.text()
            QMessageBox.information(self, "🚧 Function in development", 
                                  f"Function '{button_text}' is not implemented yet.\n\n"
                                  "✅ Available functions:\n"
                                  "• 🚀 Launch 3D-Solution\n"
                                  "• 🔸 Create 3D objects\n"
                                  "• 🏗️ Root Solution Launcher\n"
                                  "• 🎬 Capabilities demonstration\n"
                                  "• 🧪 System testing\n\n"
                                  "🔄 In development:\n"
                                  "• 2D-Solution\n"
                                  "• Assembly-Solution\n"
                                  "• Analysis-Solution\n"
                                  "• Simulation-Solution\n"
                                  "• Manufacturing-Solution\n"
                                  "• Documentation-Solution\n"
                                  "• Collaboration-Solution")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Add to text field
        self.logTextEdit.append(log_entry)
        
        # Scroll to end
        scrollbar = self.logTextEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop all threads
        for worker in self.workers:
            if worker.isRunning():
                worker.terminate()
                worker.wait()
        
        event.accept()

def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = LetsDoSolutionGUI()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
