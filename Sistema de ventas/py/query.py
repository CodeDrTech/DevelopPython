import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLineEdit, QDateEdit, QPushButton
from PyQt5.QtCore import Qt

def toggle_widgets_state():
    # Función para activar/desactivar los widgets
    state = not combo_box.isEnabled()
    
    combo_box.setEnabled(state)
    line_edit.setEnabled(state)
    date_edit.setEnabled(state)
    push_button.setEnabled(state)
    
app = QApplication(sys.argv)
app.setStyle("Fusion")  # Usar el estilo Fusion para poder aplicar hojas de estilo
window = QWidget()
window.setWindowTitle("Ejemplo de Activar/Desactivar Widgets")
layout = QVBoxLayout()

# Crear los widgets
combo_box = QComboBox()
combo_box.addItems(["Opción 1", "Opción 2", "Opción 3"])
layout.addWidget(combo_box)

line_edit = QLineEdit()
line_edit.setPlaceholderText("Escribe algo ok")
layout.addWidget(line_edit)

date_edit = QDateEdit()
layout.addWidget(date_edit)

push_button = QPushButton("Botón")
new_var = push_button
layout.addWidget(new_var)

toggle_button = QPushButton("Activar/Desactivar Widgets")
toggle_button.clicked.connect(toggle_widgets_state)
layout.addWidget(toggle_button)

# Establecer un estilo de hoja de estilo para widgets deshabilitados
style = """
QComboBox:disabled,
QLineEdit:disabled,
QDateEdit:disabled,
QPushButton:disabled {
    background-color: #D3D3D3;  /* Color de fondo gris claro para indicar deshabilitado */
    color: #888888;  /* Color de texto gris claro */
}
"""
app.setStyleSheet(style)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
