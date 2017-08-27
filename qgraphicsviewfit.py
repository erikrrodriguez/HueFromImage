from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *

class QGraphicsViewFit(QGraphicsView):
  def __init__(self, Window):
      super().__init__(Window)

  def fitInView(self, rect, flags = Qt.IgnoreAspectRatio):
      if self.scene() is None or rect.isNull():
          return
      self.last_scene_roi = rect
      unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
      self.scale(1/unity.width(), 1/unity.height())
      viewRect = self.viewport().rect()
      sceneRect = self.transform().mapRect(rect)
      xratio = viewRect.width() / sceneRect.width()
      yratio = viewRect.height() / sceneRect.height()
      if flags == Qt.KeepAspectRatio:
          xratio = yratio = min(xratio, yratio)
      elif flags == Qt.KeepAspectRatioByExpanding:
          xratio = yratio = max(xratio, yratio)
      self.scale(xratio, yratio)
      self.centerOn(rect.center())