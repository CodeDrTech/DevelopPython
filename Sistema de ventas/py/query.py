from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Importar QWebEngineView
from PyQt5.QtCore import QUrl  # Importar QUrl desde QtCore

class ReportViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear un componente WebEngineView para mostrar el informe HTML
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

    def show_report(self, html_file):
        # Cargar el archivo HTML en el WebEngineView
        self.webview.setUrl(QUrl.fromLocalFile(html_file))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    viewer = ReportViewer()
    viewer.show_report("informe.html")  # Reemplaza "informe.html" con la ubicación de tu archivo HTML
    viewer.show()
    sys.exit(app.exec_())
