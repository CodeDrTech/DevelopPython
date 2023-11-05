from PyQt5.QtCore import QUrl
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.load(QUrl('Screen01.ui.qml'))

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec_())