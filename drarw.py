from json import tool
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QLabel, QApplication,QMainWindow


class Canvas(QLabel):
    def __init__(self,height, width, background_color=QColor('#FFFFFF')):
        super().__init__()
        qpixmap = QPixmap(int(height), int(width))
        qpixmap.fill(background_color)
        self.setPixmap(qpixmap)
        self.cavas = qpixmap
        self.backcol = background_color
        self.pen_color = QColor('#000000')
        self.pointspassed = []
        self.redocapacity = []
        self.movesiteration = 0
        self.laststep = []
       

    def set_pen_color(self, color):
        self.pen_color = QtGui.QColor(color)

    def draw_point(self, x, y):
        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPoint(x, y)
        painter.end()
        self.update()

    def draw_line(self, x0, y0, x1, y1):
        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(x0, y0, x1, y1)
        painter.end()
        self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.draw_point(e.x(), e.y())
        self.prev_point = (e.x(), e.y())
        

    def mouseMoveEvent(self, e):
        self.draw_line(self.prev_point[0], self.prev_point[1], e.x(), e.y())
        self.prev_point = (e.x(), e.y())
        self.pointspassed.append(self.prev_point)
        # print(self.redocapacity)

    def mouseReleaseEvent(self, e):
        self.prev_point = tuple()
        self.redocapacity.append(0)
        self.redocapacity[self.movesiteration]=self.pointspassed
        self.pointspassed = []
        self.movesiteration+=1
        # limiting 5 moves for the redo action
        if self.movesiteration>4:
            print("you cannot go more")
        # print(self.redocapacity)

    def undo(self, e):
        if self.movesiteration > 0:
            self.cavas.fill(self.backcol)
            # drawing from first to the last-1 line
            for i in range(0,len(self.redocapacity)-1):
                # going throgh lines to get them and draw them
                for j in range(self.redocapacity[i][j]-1):
                    # drawing lines
                    self.draw_line(self.redocapacity[i][j](0),self.redocapacity[i][j](0),self.redocapacity[i][j+1](0),self.redocapacity[i][+1j](1))
                
            else:
                print("you cannot undo the job")               




class PaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(32, 32))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color + "border-radius : 15; ")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.colors = [
            '#000002', '#868687', '#900124', '#ed2832', '#2db153', '#13a5e7', '#4951cf',
            '#fdb0ce', '#fdca0f', '#eee3ab', '#9fdde8', '#7a96c2', '#cbc2ec', '#a42f3b',
            '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#dbcfc2',
        ]
        app = QApplication.instance()
        screen = app.primaryScreen()
        geometry = screen.availableGeometry()
        self.canvas = Canvas(geometry.width()*0.60, geometry.height()*0.7)
        
        w = QtWidgets.QWidget()
        w.setStyleSheet("background-color: #313234")
        l = QtWidgets.QVBoxLayout()  # vertical layout
        w.setLayout(l)
        l.addWidget(self.canvas)

        palette = QtWidgets.QHBoxLayout()  # horizontal layout
        self.add_palette_button(palette)
        l.addLayout(palette)

        self.setCentralWidget(w)
         # creating satatus bar
        mainmenu =self.menuBar()
        fileMenu = mainmenu.addMenu("File")
        redoaction = QtWidgets.QAction("undo",self)
        fileMenu.addAction(redoaction)
        redoaction.triggered.connect(Canvas.undo(self,))

    def add_palette_button(self, palette):
        for c in self.colors:
            item = PaletteButton(c)
            item.pressed.connect(self.set_canvas_color)
            palette.addWidget(item)

    def set_canvas_color(self):
        sender = self.sender()
        self.canvas.set_pen_color(sender.color)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
window.show()
app.exec_()

# Window dimensions