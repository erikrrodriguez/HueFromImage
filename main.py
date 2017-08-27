import sys
from threading import Timer, Thread
from random import randint
from gui import Ui_Window
from hue import HueLights
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Window()
        self.ui.setupUi(self)

        self.scene = QGraphicsScene()
        self.ui.imageView.setScene(self.scene)

        self.colorOneScene = QGraphicsScene()
        self.colorTwoScene = QGraphicsScene()
        self.colorThreeScene = QGraphicsScene()
        self.ui.colorOneView.setScene(self.colorOneScene)
        self.ui.colorTwoView.setScene(self.colorTwoScene)
        self.ui.colorThreeView.setScene(self.colorThreeScene)

        #Vars
        self.pixmap = None
        self.img = None
        self.circle_one = CircleIndicator()
        self.circle_two = CircleIndicator()
        self.circle_three = CircleIndicator()
        self.circles = [self.circle_one, self.circle_two, self.circle_three]
        self.ellipses = [0, 0, 0]
        self.running = False
        self.width = 0
        self.height = 0
        self.speed = 5
        self.run_timer = RepeatedTimer(self, self.speed, self.run) #interval, function

        #connect buttons
        self.ui.speedSlider.valueChanged.connect(self.change_speed)
        self.ui.openButton.clicked.connect(self.open_file)
        self.ui.startStopButton.clicked.connect(self.start_stop)

        #Setup Hue
        self.hue = HueLights()

        self.show()

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File','','Images (*.png *.jpg *.bmp)')
        if file_name[0]:
            self.scene.clear()
            self.ellipses = [0, 0, 0]
            self.pixmap = QPixmap(file_name[0])
            self.scene.addPixmap(self.pixmap)
            self.scene.update()
            self.resize_view()

    def resizeEvent(self, event):
        if self.pixmap:
            self.resize_view()
            # print("------------------------------------")
            # print('GraphicsView: width:{}    height:{}'.format(self.ui.imageView.size().width(), self.ui.imageView.size().height()))
            # print('GraphicsPort: width:{}    height:{}'.format(self.ui.imageView.viewport().width(), self.ui.imageView.viewport().height()))
            # print('Pixmap:       width:{}    height:{}'.format(self.pixmap.width(), self.pixmap.height()))
            # print('Image:        width:{}    height:{}'.format(self.img.width(), self.img.height()))
            if not self.running:
                for circle in self.circles:
                    circle.xpos = randint(0, self.ui.imageView.width())
                    circle.ypos = randint(0, self.ui.imageView.height())

    def resize_view(self):
        img_aspect_ratio =  float(self.pixmap.width() / self.pixmap.height()) 
        width = self.ui.imageView.size().width()
        self.ui.imageView.setFixedHeight( width / img_aspect_ratio)
        self.ui.imageView.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.img = self.pixmap.toImage()
        CircleIndicator.diameter = int(self.img.width()*.07) #7% of imgl width

    def start_stop(self):
        if self.running:
            self.run_timer.stop()
            self.running = False
        else:
            self.run_timer.interval = 0
            self.run_timer.start()
            self.run_timer.interval = self.speed
            self.running = True

    def run(self):
        for i, circle in enumerate(self.circles):
            circle.advance(self.pixmap.width(), self.pixmap.height())
            circle.color = QColor(self.img.pixel(circle.xpos, circle.ypos))
        # print('--------------------------')
        # print('Circle1: xpos:{}    ypos:{}'.format(self.circle_one.xpos, self.circle_one.ypos))
        # print('Circle2: xpos:{}    ypos:{}'.format(self.circle_two.xpos, self.circle_two.ypos))
        # print('Circle3: xpos:{}    ypos:{}'.format(self.circle_three.xpos, self.circle_three.ypos))
    
    def update_gui(self):
        for ellipse in self.ellipses:
            if not ellipse is 0:
                self.scene.removeItem(ellipse)
        for i, circle in enumerate(self.circles):
            self.ellipses[i] = self.scene.addEllipse(circle.xpos, circle.ypos, circle.diameter, circle.diameter, pen=QPen(Qt.white), brush=QBrush(circle.color))
        self.colorOneScene.setBackgroundBrush(QBrush(self.circle_one.color))
        self.colorTwoScene.setBackgroundBrush(QBrush(self.circle_two.color))
        self.colorThreeScene.setBackgroundBrush(QBrush(self.circle_three.color))
        self.send_colors_to_hue()
        # self.hue.change_all_lights(self.circles, self.speed)

    # @threaded
    def send_colors_to_hue(self):
        for i, circle in enumerate(self.circles):
            r, g, b, a = circle.color.getRgb()
            self.hue.change_light_xy(bulb=i+1, r=r/255, g=g/255, b=b/255, transitiontime=self.speed*10) #transtime in ms

    def change_speed(self):
        self.speed = self.scale_val(self.ui.speedSlider.value(), 1, 99, 5, .3) #~ 10 commands per second with 3 lights
        self.run_timer.interval = self.speed
    
    def scale_val(self, val, oldmin, oldmax, newmin, newmax):
        return (((val - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin

class RepeatedTimer(QObject):
    
    signal = pyqtSignal()

    def __init__(self, parent, interval, function, *args, **kwargs):
        super().__init__()
        self.parent     = parent
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.signal.connect(parent.update_gui)
        # self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
        self.signal.emit()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.daemon = True #thread will exit when main app exits
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class CircleIndicator:
    diameter = 40
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.xvel = randint(-5,5)
        self.yvel = randint(-5,5)
        self.color = None #Qcolor object

    def advance(self, width, height):
        self.xpos += self.xvel
        self.ypos += self.yvel
        if self.xpos >= width-CircleIndicator.diameter or self.xpos <= abs(self.xvel):
            self.xvel = self.xvel * -1
        if self.ypos >= height-CircleIndicator.diameter or self.ypos <= abs(self.yvel):
            self.yvel = self.yvel * -1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = AppWindow()
    sys.exit(app.exec_())



