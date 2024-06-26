import sys
import cv2
import time
import rospy
import threading
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QDialog, QMessageBox
from lab_config_proxy import LabConfigProxy
from ui import *
import add_color_dialog
from sensor_msgs.msg import Image

class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        rospy.init_node('lab_node')
        self.last_range_max = [999, 999, 999]
        self.last_range_min = [999, 999, 999]
        ip = "127.0.0.1"
        image_org_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_org_callback)
        image_lab_sub = rospy.Subscriber('/lab_config_manager/image_result', Image, self.image_lab_callback)        
        self.lab_config_proxy = LabConfigProxy(host=ip, port=9090)
        self.lab_config_proxy.enter_func()

        self.comboBox_color.currentTextChanged.connect(self.set_slider_by_combobox)
        self.horizontalSlider_LMax.valueChanged.connect(lambda value: self.label_LMax.setNum(value))
        self.horizontalSlider_LMin.valueChanged.connect(lambda value: self.label_LMin.setNum(value))
        self.horizontalSlider_AMax.valueChanged.connect(lambda value: self.label_AMax.setNum(value))
        self.horizontalSlider_AMin.valueChanged.connect(lambda value: self.label_AMin.setNum(value))
        self.horizontalSlider_BMax.valueChanged.connect(lambda value: self.label_BMax.setNum(value))
        self.horizontalSlider_BMin.valueChanged.connect(lambda value: self.label_BMin.setNum(value))
        self.pushButton_labWrite.clicked.connect(self.save_ranges_to_disk)
        self.pushButton_AddColor.clicked.connect(self.add_color)
        self.update_color_names()
        self.range_update_timer = threading.Timer(0.05, self.update_current_range)
        self.range_update_timer.setDaemon(True)
        self.range_update_timer.start()
    
    def image_org_callback(self, ros_image):
        frame = np.ndarray(shape=(ros_image.height, ros_image.width, 3), dtype=np.uint8, buffer=ros_image.data)
        image = cv2.resize(frame, (400, 300), interpolation=cv2.INTER_NEAREST) 
        qimage = QImage(image.data, 400, 300, QImage.Format_RGB888)
        self.label_orign.setPixmap(QPixmap.fromImage(qimage))

    def image_lab_callback(self, ros_image):
        frame = np.ndarray(shape=(ros_image.height, ros_image.width, 3), dtype=np.uint8, buffer=ros_image.data)
        qimage = QImage(frame.data, 400, 300, QImage.Format_RGB888)
        self.label_process.setPixmap(QPixmap.fromImage(qimage))

    # 窗口退出
    def closeEvent(self, e):        
        result = QMessageBox.question(self,
                                    "关闭窗口提醒",
                                    "exit?",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if result == QMessageBox.Yes:
            self.lab_config_proxy.exit_func()
            QWidget.closeEvent(self, e)
        else:
            e.ignore()

    def apply_current_range(self):
        rsl = self.lab_config_proxy.apply_current_range(self.comboBox_color.currentText())
        if rsl['success']:
            QMessageBox.information(self, "Apply color range", "Successed!")
        else:
            QMessageBox.information(self, "Apply color range", "Failed")

    def save_ranges_to_disk(self):
        self.lab_config_proxy.apply_current_range(self.comboBox_color.currentText())
        rsl = self.lab_config_proxy.save_ranges_to_disk()
        if rsl['success']:
            QMessageBox.information(self, "Save to disk", "Successed!")
        else:
            QMessageBox.information(self, "Save to disk", "Failed")

    def add_color(self):
        dialog = QDialog()
        dialog_ui = add_color_dialog.Ui_Dialog()
        dialog_ui.setupUi(dialog)

        def get_color_name():
            color_name = dialog_ui.lineEdit.text()
            self.lab_config_proxy.apply_current_range(color_name)
            self.comboBox_color.addItem(color_name)
            self.comboBox_color.setCurrentText(color_name)
            dialog.close()

        dialog_ui.pushButton_ok.clicked.connect(get_color_name)
        dialog_ui.pushButton_cancel.clicked.connect(dialog.close)
        dialog.exec_()

    def update_current_range(self):
        range_max = list((int(n) for n in (self.label_LMax.text(), self.label_AMax.text(), self.label_BMax.text())))
        range_min = list((int(n) for n in (self.label_LMin.text(), self.label_AMin.text(), self.label_BMin.text())))
        if not (range_max == self.last_range_max and range_min == self.last_range_min):
            self.lab_config_proxy.set_current_range(range_min, range_max)
            self.last_range_max = range_max
            self.last_range_min = range_min
        self.range_update_timer = threading.Timer(0.05, self.update_current_range)
        self.range_update_timer.start()

    def update_color_names(self):
        names = self.lab_config_proxy.get_all_color_name()
        names.sort()
        self.comboBox_color.addItems(names)

    def set_slider_states(self, range_min, range_max):
        self.horizontalSlider_LMin.setSliderPosition(range_min[0])
        self.horizontalSlider_AMin.setSliderPosition(range_min[1])
        self.horizontalSlider_BMin.setSliderPosition(range_min[2])
        self.horizontalSlider_LMax.setSliderPosition(range_max[0])
        self.horizontalSlider_AMax.setSliderPosition(range_max[1])
        self.horizontalSlider_BMax.setSliderPosition(range_max[2])

    def set_slider_by_combobox(self, msg):
        rsl = self.lab_config_proxy.get_range_by_name(msg)
        self.set_slider_states(rsl['min'], rsl['max'])
        self.lab_config_proxy.set_current_range(rsl['min'], rsl['max'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
