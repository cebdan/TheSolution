#!/usr/bin/env python3
"""
3D Visualization Dialog for TheSolution CAD
"""

import sys
import os
from typing import Dict, Any, Optional, Tuple
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                               QGroupBox, QFormLayout, QComboBox, QSlider,
                               QPushButton, QLabel, QSpinBox, QDoubleSpinBox,
                               QCheckBox, QListWidget, QColorDialog, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

from visualization_3d import (Visualization3D, LineStyle, GradientType, 
                             MaterialType, ColorScheme, VisualizationPresets)

class VisualizationDialog(QDialog):
    """Dialog for configuring 3D visualization settings"""
    
    # Signals
    settings_changed = Signal(dict)  # Emitted when settings are applied
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("3D Visualization Settings")
        self.setModal(True)
        self.resize(600, 700)
        
        # Initialize visualization system
        self.visualization = Visualization3D()
        
        # Current settings
        self.current_settings = {
            'material_type': MaterialType.METAL,
            'transparency': 0.0,
            'base_color': (0.8, 0.8, 0.9),
            'gradient_type': GradientType.NONE,
            'gradient_intensity': 50,
            'line_style': LineStyle.SOLID,
            'line_width': 1.0,
            'line_color': (0.8, 0.8, 0.8),
            'show_edges': True,
            'show_vertices': False,
            'wireframe_mode': False,
            'color_scheme': ColorScheme.CLASSIC,
            'show_grid': True,
            'grid_spacing': 1.0,
            'grid_size': 20.0,
            'show_axes': True,
            'show_labels': True
        }
        
        self.setup_ui()
        self.setup_connections()
        self.load_current_settings()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Materials & Colors tab
        self.setup_materials_tab()
        
        # Line Styles tab
        self.setup_lines_tab()
        
        # Presets tab
        self.setup_presets_tab()
        
        # Environment tab
        self.setup_environment_tab()
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.preview_button = QPushButton("Preview")
        self.reset_button = QPushButton("Reset to Default")
        self.cancel_button = QPushButton("Cancel")
        self.apply_button = QPushButton("Apply")
        self.ok_button = QPushButton("OK")
        
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def setup_materials_tab(self):
        """Setup Materials & Colors tab"""
        materials_widget = QTabWidget()
        
        # Material Properties group
        material_group = QGroupBox("Material Properties")
        material_layout = QFormLayout()
        
        self.material_type_combo = QComboBox()
        self.material_type_combo.addItems([mt.value for mt in MaterialType])
        material_layout.addRow("Material Type:", self.material_type_combo)
        
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.setValue(0)
        material_layout.addRow("Transparency:", self.transparency_slider)
        
        self.color_button = QPushButton("Choose Color")
        material_layout.addRow("Base Color:", self.color_button)
        
        material_group.setLayout(material_layout)
        
        # Gradient Settings group
        gradient_group = QGroupBox("Gradient Settings")
        gradient_layout = QFormLayout()
        
        self.gradient_type_combo = QComboBox()
        self.gradient_type_combo.addItems([gt.value for gt in GradientType])
        gradient_layout.addRow("Gradient Type:", self.gradient_type_combo)
        
        self.gradient_intensity_slider = QSlider(Qt.Horizontal)
        self.gradient_intensity_slider.setRange(0, 100)
        self.gradient_intensity_slider.setValue(50)
        gradient_layout.addRow("Gradient Intensity:", self.gradient_intensity_slider)
        
        gradient_group.setLayout(gradient_layout)
        
        # Add to tab
        materials_layout = QVBoxLayout()
        materials_layout.addWidget(material_group)
        materials_layout.addWidget(gradient_group)
        materials_layout.addStretch()
        
        materials_widget.setLayout(materials_layout)
        self.tab_widget.addTab(materials_widget, "Materials & Colors")
    
    def setup_lines_tab(self):
        """Setup Line Styles tab"""
        lines_widget = QTabWidget()
        
        # Line Properties group
        line_group = QGroupBox("Line Properties")
        line_layout = QFormLayout()
        
        self.line_style_combo = QComboBox()
        self.line_style_combo.addItems([ls.value for ls in LineStyle])
        line_layout.addRow("Line Style:", self.line_style_combo)
        
        self.line_width_spin = QSpinBox()
        self.line_width_spin.setRange(1, 10)
        self.line_width_spin.setValue(1)
        line_layout.addRow("Line Width:", self.line_width_spin)
        
        self.line_color_button = QPushButton("Choose Color")
        line_layout.addRow("Line Color:", self.line_color_button)
        
        line_group.setLayout(line_layout)
        
        # Edge Display group
        edge_group = QGroupBox("Edge Display")
        edge_layout = QVBoxLayout()
        
        self.show_edges_check = QCheckBox("Show Edges")
        self.show_edges_check.setChecked(True)
        edge_layout.addWidget(self.show_edges_check)
        
        self.show_vertices_check = QCheckBox("Show Vertices")
        self.show_vertices_check.setChecked(False)
        edge_layout.addWidget(self.show_vertices_check)
        
        self.wireframe_check = QCheckBox("Wireframe Mode")
        self.wireframe_check.setChecked(False)
        edge_layout.addWidget(self.wireframe_check)
        
        edge_group.setLayout(edge_layout)
        
        # Add to tab
        lines_layout = QVBoxLayout()
        lines_layout.addWidget(line_group)
        lines_layout.addWidget(edge_group)
        lines_layout.addStretch()
        
        lines_widget.setLayout(lines_layout)
        self.tab_widget.addTab(lines_widget, "Line Styles")
    
    def setup_presets_tab(self):
        """Setup Presets tab"""
        presets_widget = QTabWidget()
        
        presets_layout = QVBoxLayout()
        
        info_label = QLabel("Choose a predefined visualization preset:")
        presets_layout.addWidget(info_label)
        
        self.presets_list = QListWidget()
        self.presets_list.addItems([
            "Metal Preset",
            "Glass Preset", 
            "Wood Preset",
            "Plastic Preset",
            "Technical Preset",
            "Artistic Preset"
        ])
        presets_layout.addWidget(self.presets_list)
        
        preset_buttons_layout = QHBoxLayout()
        self.apply_preset_button = QPushButton("Apply Preset")
        self.save_preset_button = QPushButton("Save as Preset")
        
        preset_buttons_layout.addWidget(self.apply_preset_button)
        preset_buttons_layout.addWidget(self.save_preset_button)
        
        presets_layout.addLayout(preset_buttons_layout)
        presets_widget.setLayout(presets_layout)
        
        self.tab_widget.addTab(presets_widget, "Presets")
    
    def setup_environment_tab(self):
        """Setup Environment tab"""
        environment_widget = QTabWidget()
        
        environment_layout = QVBoxLayout()
        
        # Color Scheme group
        scheme_group = QGroupBox("Color Scheme")
        scheme_layout = QFormLayout()
        
        self.color_scheme_combo = QComboBox()
        self.color_scheme_combo.addItems([cs.value for cs in ColorScheme])
        scheme_layout.addRow("Background Scheme:", self.color_scheme_combo)
        
        scheme_group.setLayout(scheme_layout)
        environment_layout.addWidget(scheme_group)
        
        # Grid Settings group
        grid_group = QGroupBox("Grid Settings")
        grid_layout = QFormLayout()
        
        self.show_grid_check = QCheckBox()
        self.show_grid_check.setChecked(True)
        grid_layout.addRow("Show Grid:", self.show_grid_check)
        
        self.grid_spacing_spin = QDoubleSpinBox()
        self.grid_spacing_spin.setRange(0.1, 10.0)
        self.grid_spacing_spin.setValue(1.0)
        self.grid_spacing_spin.setSingleStep(0.1)
        grid_layout.addRow("Grid Spacing:", self.grid_spacing_spin)
        
        self.grid_size_spin = QDoubleSpinBox()
        self.grid_size_spin.setRange(5.0, 100.0)
        self.grid_size_spin.setValue(20.0)
        self.grid_size_spin.setSingleStep(1.0)
        grid_layout.addRow("Grid Size:", self.grid_size_spin)
        
        grid_group.setLayout(grid_layout)
        environment_layout.addWidget(grid_group)
        
        # Coordinate Axes group
        axes_group = QGroupBox("Coordinate Axes")
        axes_layout = QVBoxLayout()
        
        self.show_axes_check = QCheckBox("Show Coordinate Axes")
        self.show_axes_check.setChecked(True)
        axes_layout.addWidget(self.show_axes_check)
        
        self.show_labels_check = QCheckBox("Show Axis Labels")
        self.show_labels_check.setChecked(True)
        axes_layout.addWidget(self.show_labels_check)
        
        axes_group.setLayout(axes_layout)
        environment_layout.addWidget(axes_group)
        
        environment_layout.addStretch()
        environment_widget.setLayout(environment_layout)
        
        self.tab_widget.addTab(environment_widget, "Environment")
    
    def setup_connections(self):
        """Setup signal connections"""
        # Buttons
        self.preview_button.clicked.connect(self.preview_settings)
        self.reset_button.clicked.connect(self.reset_to_default)
        self.cancel_button.clicked.connect(self.reject)
        self.apply_button.clicked.connect(self.apply_settings)
        self.ok_button.clicked.connect(self.accept_and_apply)
        
        # Color buttons
        self.color_button.clicked.connect(self.choose_base_color)
        self.line_color_button.clicked.connect(self.choose_line_color)
        
        # Preset buttons
        self.apply_preset_button.clicked.connect(self.apply_preset)
        self.save_preset_button.clicked.connect(self.save_preset)
        
        # Preset list
        self.presets_list.itemDoubleClicked.connect(self.apply_preset)
    
    def load_current_settings(self):
        """Load current settings into UI"""
        # Material settings
        self.material_type_combo.setCurrentText(self.current_settings['material_type'].value)
        self.transparency_slider.setValue(int(self.current_settings['transparency'] * 100))
        self.gradient_type_combo.setCurrentText(self.current_settings['gradient_type'].value)
        self.gradient_intensity_slider.setValue(self.current_settings['gradient_intensity'])
        
        # Line settings
        self.line_style_combo.setCurrentText(self.current_settings['line_style'].value)
        self.line_width_spin.setValue(self.current_settings['line_width'])
        
        # Display settings
        self.show_edges_check.setChecked(self.current_settings['show_edges'])
        self.show_vertices_check.setChecked(self.current_settings['show_vertices'])
        self.wireframe_check.setChecked(self.current_settings['wireframe_mode'])
        
        # Environment settings
        self.color_scheme_combo.setCurrentText(self.current_settings['color_scheme'].value)
        self.show_grid_check.setChecked(self.current_settings['show_grid'])
        self.grid_spacing_spin.setValue(self.current_settings['grid_spacing'])
        self.grid_size_spin.setValue(self.current_settings['grid_size'])
        self.show_axes_check.setChecked(self.current_settings['show_axes'])
        self.show_labels_check.setChecked(self.current_settings['show_labels'])
    
    def get_current_settings(self) -> Dict[str, Any]:
        """Get current settings from UI"""
        settings = {}
        
        # Material settings
        settings['material_type'] = MaterialType(self.material_type_combo.currentText())
        settings['transparency'] = self.transparency_slider.value() / 100.0
        settings['base_color'] = self.current_settings['base_color']  # Keep current color
        settings['gradient_type'] = GradientType(self.gradient_type_combo.currentText())
        settings['gradient_intensity'] = self.gradient_intensity_slider.value()
        
        # Line settings
        settings['line_style'] = LineStyle(self.line_style_combo.currentText())
        settings['line_width'] = self.line_width_spin.value()
        settings['line_color'] = self.current_settings['line_color']  # Keep current color
        
        # Display settings
        settings['show_edges'] = self.show_edges_check.isChecked()
        settings['show_vertices'] = self.show_vertices_check.isChecked()
        settings['wireframe_mode'] = self.wireframe_check.isChecked()
        
        # Environment settings
        settings['color_scheme'] = ColorScheme(self.color_scheme_combo.currentText())
        settings['show_grid'] = self.show_grid_check.isChecked()
        settings['grid_spacing'] = self.grid_spacing_spin.value()
        settings['grid_size'] = self.grid_size_spin.value()
        settings['show_axes'] = self.show_axes_check.isChecked()
        settings['show_labels'] = self.show_labels_check.isChecked()
        
        return settings
    
    def choose_base_color(self):
        """Choose base color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_settings['base_color'] = (color.redF(), color.greenF(), color.blueF())
            self.color_button.setStyleSheet(f"background-color: {color.name()}")
    
    def choose_line_color(self):
        """Choose line color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_settings['line_color'] = (color.redF(), color.greenF(), color.blueF())
            self.line_color_button.setStyleSheet(f"background-color: {color.name()}")
    
    def apply_preset(self):
        """Apply selected preset"""
        current_item = self.presets_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a preset first.")
            return
        
        preset_name = current_item.text()
        
        if "Metal" in preset_name:
            preset = VisualizationPresets.get_metal_preset()
        elif "Glass" in preset_name:
            preset = VisualizationPresets.get_glass_preset()
        elif "Wood" in preset_name:
            preset = VisualizationPresets.get_wood_preset()
        elif "Plastic" in preset_name:
            preset = VisualizationPresets.get_plastic_preset()
        elif "Technical" in preset_name:
            preset = VisualizationPresets.get_technical_preset()
        elif "Artistic" in preset_name:
            preset = VisualizationPresets.get_artistic_preset()
        else:
            QMessageBox.warning(self, "Warning", "Unknown preset.")
            return
        
        # Apply preset to UI
        self.material_type_combo.setCurrentText(preset['material_type'].value)
        self.transparency_slider.setValue(int(preset['transparency'] * 100))
        self.gradient_type_combo.setCurrentText(preset['gradient_type'].value)
        self.line_style_combo.setCurrentText(preset['line_style'].value)
        self.line_width_spin.setValue(preset['line_width'])
        
        # Update colors
        self.current_settings['base_color'] = preset['color']
        self.current_settings['line_color'] = preset['color']
        
        QMessageBox.information(self, "Success", f"Applied {preset_name}")
    
    def save_preset(self):
        """Save current settings as preset"""
        # This would typically save to a configuration file
        QMessageBox.information(self, "Info", "Preset saving functionality will be implemented.")
    
    def preview_settings(self):
        """Preview current settings"""
        settings = self.get_current_settings()
        self.settings_changed.emit(settings)
        QMessageBox.information(self, "Preview", "Settings preview applied to 3D view.")
    
    def reset_to_default(self):
        """Reset to default settings"""
        reply = QMessageBox.question(self, "Reset", 
                                   "Are you sure you want to reset to default settings?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.current_settings = {
                'material_type': MaterialType.METAL,
                'transparency': 0.0,
                'base_color': (0.8, 0.8, 0.9),
                'gradient_type': GradientType.NONE,
                'gradient_intensity': 50,
                'line_style': LineStyle.SOLID,
                'line_width': 1.0,
                'line_color': (0.8, 0.8, 0.8),
                'show_edges': True,
                'show_vertices': False,
                'wireframe_mode': False,
                'color_scheme': ColorScheme.CLASSIC,
                'show_grid': True,
                'grid_spacing': 1.0,
                'grid_size': 20.0,
                'show_axes': True,
                'show_labels': True
            }
            self.load_current_settings()
    
    def apply_settings(self):
        """Apply current settings"""
        settings = self.get_current_settings()
        self.settings_changed.emit(settings)
        QMessageBox.information(self, "Success", "Settings applied successfully.")
    
    def accept_and_apply(self):
        """Accept dialog and apply settings"""
        self.apply_settings()
        self.accept()
    
    def get_visualization_settings(self) -> Dict[str, Any]:
        """Get visualization settings for external use"""
        return self.get_current_settings()
