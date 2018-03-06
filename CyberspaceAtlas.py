# -*- coding: utf-8 -*-


from PyQt5.QtCore import QDir, Qt,pyqtSignal, QT_VERSION_STR, QRectF
#from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import *
#(QDialog, QAction, QApplication, QFileDialog, QLabel, QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy,QGridLayout,)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont
import cv2
from PIL import Image 
import numpy as np
#from functools import reduce
import sys
import os
import qimage2ndarray
import struct
from random import choice
import socket

def ip_strtoint(ipstr):
    """Convert an IPv4 address in dotted-decimal to an integer."""
    return reduce(lambda x,y: (x<<8)+y,
            map(lambda x: int(x),
                ipstr.split('.', 4)))

def ip_inttostr(ip):
    """Convert an integer to an IPv4 address in dotted-decimal."""
    #return '.'.join(map(lambda x: str(ord(str(x))), struct.pack('>L', ip)))
    return socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))

def d2xy(n, d):
	t=d
	s,rx,ry,x,y=1,0,0,0,0
	while(1):
		if s>=n:
			break
		rx=1&int((t/2))
		ry=1&int((int(t)^int(rx)))
		x,y=rot(s,x,y,rx,ry)
		x+=s*rx
		y+=s*ry
		t/=4
		s*=2
	return x,y
	
def xy2d(n, x, y):
	d,s,rx,ry=0,n/2,0,0
	while s>0:
		rx=(int(x)&int(s))>0;
		ry=(int(y)&int(s))>0;
		d+=s*s*((3*rx)^ry)
		x,y=rot(s,x,y,rx,ry)
		s/=2
	return d
	
def rot(n,x,y,rx,ry):
	if ry==0:
		if rx==1:
			x=n-1-x
			y=n-1-y
		t=x
		x=y
		y=t
	return x,y

def drawResult(img,solu,buffer_file,num):
#???????
	#alp=1900
	#red=255-1900*prob
    #red=2*int(asn%100)
	#blue=1900*prob
	#green=0
    #blue=2*int((asn%10000)/100)
    #green=2*int((asn/10000))
#???????
    #netIP=addr
    #ipnum=ip_strtoint(netIP)>>(32-solu)
    #side_length=2**(solu/2)
    #x,y=d2xy(side_length,ipnum)
	#b r g
	
    x_num=solu-15
    y_num=x_num+1
    for i in range(num):
        x = buffer_file[i][x_num]
        y = buffer_file[i][y_num]
        red = buffer_file[i][15]
        green = buffer_file[i][16]
        blue = buffer_file[i][17]
        img[y,x,0]=red
        img[y,x,1]=green
        img[y,x,2]=blue



		
	
class SettingDialog(QDialog): 
	
    def __init__(self, parent=None): 
        super(SettingDialog, self).__init__(parent) 
        self.initUI() 
        self.setWindowTitle("数据源设置") 
        self.resize(240, 100) 

    def initUI(self): 
        grid = QGridLayout() 
        grid.addWidget(QLabel("路径："), 0, 0) 
        self.pathLineEdit = QLineEdit() 
        self.pathLineEdit.setFixedWidth(200) 
        #self.pathLineEdit.setText(Global.path)
        grid.addWidget(self.pathLineEdit, 0, 1) 
        button = QPushButton("选择") 
        button.clicked.connect(self.changePath) 
        grid.addWidget(button, 0, 2) 
        grid.addWidget(QLabel("<font color='#ff0000'>请选择源文件，格式为txt</font>"), 1,0,1,3) 
        buttonBox = QDialogButtonBox() 
        buttonBox.setOrientation(Qt.Horizontal)  # 设置为水平方向
        buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel) 
        buttonBox.accepted.connect(self.accept)  # 确定
        buttonBox.rejected.connect(self.reject)  # 取消
        grid.addWidget(buttonBox, 2, 1) 
        self.setLayout(grid) 

    def changePath(self): 
        self.filename,_ = QFileDialog.getOpenFileName(self, "打开文件", QDir.currentPath(),"Source (*.txt  )")
        self.pathLineEdit.setText(self.filename) 
        print(self.filename)
		
    def closeEvent(self,event):
        reply = QtWidgets.QMessageBox.question(self,'确认退出','你确定要退出么？',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Image_Label(QLabel):
	
	# Mouse button signals emit image scene (x, y) coordinates.
    # !!! For image (row, column) matrix indexing, row = y and column = x.
    leftMouseButtonPressed = pyqtSignal(float, float)
    rightMouseButtonPressed = pyqtSignal(float, float)
    leftMouseButtonReleased = pyqtSignal(float, float)
    rightMouseButtonReleased = pyqtSignal(float, float)
    leftMouseButtonDoubleClicked = pyqtSignal(float, float)
    rightMouseButtonDoubleClicked = pyqtSignal(float, float)
   
	
    def __init__(self,sol):
        super(Image_Label,self).__init__()
        self.sol=sol
        self.pos_x=0
        self.pos_y=0
			
			
    def mousePressEvent(self, event):

        eventpos=str(event.pos())
        eventpos1=eventpos.split(',')
        eventpos2=eventpos1[0].split('(')
        eventpos3=eventpos1[1].split(')')
        self.pos_x=int(eventpos2[1])
        self.pos_y=int(eventpos3[0])
       
        # scenePos = self.mapToScene(event.pos())
        # print(scenePos)
        if event.button() == Qt.LeftButton:
            self.leftMouseButtonPressed.emit(self.pos_x, self.pos_y)
            print(self.pos_x)
            print(self.pos_y)
            # if self.canPan:
                # self.setDragMode(QGraphicsView.ScrollHandDrag)
            # self.leftMouseButtonPressed.emit(scenePos.x(), scenePos.y())
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPressed.emit(self.pos_x, self.pos_y)
            # if self.canZoom:
                # self.setDragMode(QGraphicsView.RubberBandDrag)
            # self.rightMouseButtonPressed.emit(scenePos.x(), scenePos.y())
        #QLabel.mousePressEvent(self, event)
		
    def mouseReleaseEvent(self, event):
        """ Stop mouse pan or zoom mode (apply zoom if valid).
        """
        QLabel.mouseReleaseEvent(self, event)
        #scenePos = self.mapToScene(event.pos())
        #if event.button() == Qt.LeftButton:
            #self.setDragMode(QGraphicsView.NoDrag)
            #self.leftMouseButtonReleased.emit(scenePos.x(), scenePos.y())
        # elif event.button() == Qt.RightButton:
            # if self.canZoom:
                # viewBBox = self.zoomStack[-1] if len(self.zoomStack) else self.sceneRect()
                # selectionBBox = self.scene.selectionArea().boundingRect().intersected(viewBBox)
                # self.scene.setSelectionArea(QPainterPath())  # Clear current selection area.
                # if selectionBBox.isValid() and (selectionBBox != viewBBox):
                    # self.zoomStack.append(selectionBBox)
                    # self.updateViewer()
            # self.setDragMode(QGraphicsView.NoDrag)
            # self.rightMouseButtonReleased.emit(scenePos.x(), scenePos.y())
    
    def mouseDoubleClickEvent(self, event):
        """ Show original image or go to the largest solution.
        """
        eventpos=str(event.pos())
        eventpos1=eventpos.split(',')
        eventpos2=eventpos1[0].split('(')
        eventpos3=eventpos1[1].split(')')
        self.pos_x=int(eventpos2[1])
        self.pos_y=int(eventpos3[0])

        if event.button() == Qt.LeftButton:
            self.leftMouseButtonDoubleClicked.emit(self.pos_x, self.pos_y)
        elif event.button() == Qt.RightButton:
            # if self.canZoom:
            #     self.zoomStack = []  # Clear zoom stack.
            #     self.updateViewer()
            self.rightMouseButtonDoubleClicked.emit(self.pos_x, self.pos_y)
		


class ImageViewer(QMainWindow):
	

	
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.printer = QPrinter()
        self.scaleFactor = 0.0
        self.sol=16
        self.isRightSingleClick = False
        self.isRightDoubleClick = False

        self.imageLabel = Image_Label(self.sol)
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.leftMouseButtonPressed.connect(self.cal_coordinates)
        self.imageLabel.rightMouseButtonPressed.connect(self.rightclick_movement)
        self.imageLabel.leftMouseButtonDoubleClicked.connect(self.returnto)
        self.imageLabel.rightMouseButtonDoubleClicked.connect(self.IP_Use)
		
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()
        self.createToolsbar()
        self.statusBar().showMessage("分辨率：255.255.255.255/"+str(self.sol)+"\n（注：不同颜色代表不同ASN）")
        self.setWindowTitle("网络空间地图")
        self.resize(400, 500)
        self.setWindowIcon(QtGui.QIcon(r'sample.PNG'))

        dialog = SettingDialog() 
        dialog.exec_()

#---------------------------------------------------------------
		
        file_1 = open(dialog.filename,'r')
        file_2 = file_1.readlines()
        self.col_num= len(file_2[0].split('	'))
        print(self.col_num)
        # if int(self.col_num) > 0:
        #     print(' The column number of sourcefile is not correct ! Exit! \n')
        #     sys.exit()
        print('The column number of file:')
        print(self.col_num)
        self.row_num = 0
        for line in file_2:
            self.row_num+=1
        print('The row number of file:')
        print(self.row_num)
        self.input_file = [[ 0 for i in range(18)] for i in range(self.row_num)]
        count =0
        for line in file_2:
            buffer = line.split('	')
            self.input_file[count][0] = buffer[0]
            for i in range(1,18):
                self.input_file[count][i] = int(buffer[i])
            count+=1
				
        broad=int(2**(self.sol/2))
        img = np.zeros((broad,broad,3), np.uint8)
        for i in range(broad):
            cv2.line(img,(i,0),(i,broad-1),(255,255,255),1)
        drawResult(img,self.sol,self.input_file,self.row_num)

        

#-----------------------------------------------
        self.q1=qimage2ndarray.array2qimage(img)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.q1))
		   
        self.scaleFactor = 1.0

        self.printAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()
#----------------------------------------------------------------------

    def cal_coordinates(self,x,y):
        if self.isRightDoubleClick == False and self.isRightSingleClick == False:
            d=int(xy2d(2**(self.sol/2),x,y))
            buffer_d=(d<<(32-self.sol))
            ip=ip_inttostr(buffer_d)
            self.statusBar().showMessage("分辨率及IP："+str(ip)+"/"+str(self.sol))
        elif self.isRightDoubleClick == False and self.isRightSingleClick == True:
            d=int(xy2d(2**(self.sol/2),x,y))
            buffer_d=(d<<(32-self.sol))
            ip=ip_inttostr(buffer_d)
            self.statusBar().showMessage("分辨率及IP："+str(ip)+"/"+str(self.sol))
        elif self.isRightDoubleClick == True:
            d=int(xy2d(2**(self.sol/2),x,y))
            buffer_d=(d<<(32-self.sol))
            ip=ip_inttostr(buffer_d)
            self.statusBar().showMessage("分辨率及IP："+str(ip)+"/"+str(self.sol))

		
    def rightclick_movement(self,x,y):
        statu=False #statu为真，表示找到所属的色块，否则没有，不执行动作
        if self.isRightSingleClick == False and self.sol == 16:
            if self.isRightDoubleClick == False:
                bu_col=[255,255,255]
                for i in range(self.row_num):
                    if self.input_file[i][1] == int(x) and self.input_file[i][2] == int(y):
                        bu_col=[self.input_file[i][15],self.input_file[i][16],self.input_file[i][17]]
                        print(bu_col)
                        break       
                if bu_col == [61,145,64]:
                    file_1 = open('cache/transfer_data_3.txt','r')
                    statu=True
                elif bu_col == [250,51,153]:
                    file_1 = open('cache/transfer_data_4.txt','r')
                    statu=True

        if statu == True:
            self.isRightSingleClick = True
            self.sol=28
            broad=int(2**(20/2))
            img = np.zeros((broad,broad,3), np.uint8)
            for i in range(broad):
                cv2.line(img,(i,0),(i,broad-1),(255,255,255),1)
            for line in file_1:
                buffer = line.split(' ')          
                x = int(buffer[1])
                y = int(buffer[2])
                red = int(buffer[3])
                green = int(buffer[4])
                blue = int(buffer[5])
                img[y,x,0]=red
                img[y,x,1]=green
                img[y,x,2]=blue

            self.statusBar().showMessage("分辨率：255.255.255.255/"+str(self.sol)+"\n"+"（注：红色：清华校园网  青色：北邮校园网  黄色：公司A网络  紫色：公司B网络  嫩绿色：小区C网络）")
            self.q1=qimage2ndarray.array2qimage(img)
            self.imageLabel.setPixmap(QPixmap.fromImage(self.q1))
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def returnto(self):
        if self.isRightSingleClick == True or self.isRightDoubleClick == True: 
            self.sol=16
            broad=int(2**(self.sol/2))
            img = np.zeros((broad,broad,3), np.uint8)
            for i in range(broad):
                cv2.line(img,(i,0),(i,broad-1),(255,255,255),1)
            drawResult(img,self.sol,self.input_file,self.row_num)
    #-----------------------------------------------
            self.q1=qimage2ndarray.array2qimage(img)
            self.imageLabel.setPixmap(QPixmap.fromImage(self.q1))
               
            self.scaleFactor = 1.0
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()
            self.isRightSingleClick = False
            self.isRightDoubleClick = False

    def IP_Use(self):
        if self.isRightSingleClick == True:
            self.isRightDoubleClick = True
            # img = np.zeros((1080,1920,3), np.uint8)
            # col_list1=[(227,23,13),(255,128,0),(255,128,0),(255,128,0),(255,255,255),(255,255,255),(255,255,255),(64,224,208),(255,255,255),(255,255,255),(255,255,255)]
            # for a in range(1080):
            #     for b in range(1920):         
            #         img[a,b]=choice(col_list1)
            file_1 = open('cache/IP_Use_3.txt','r')
            self.sol=32
            broad=int(2**(22/2))
            img = np.zeros((broad,broad,3), np.uint8)
            for i in range(broad):
                cv2.line(img,(i,0),(i,broad-1),(255,255,255),1)
            for line in file_1:
                buffer = line.split(' ')          
                x = int(buffer[1])
                y = int(buffer[2])
                red = int(buffer[3])
                green = int(buffer[4])
                blue = int(buffer[5])
                img[y,x,0]=red
                img[y,x,1]=green
                img[y,x,2]=blue

            self.statusBar().showMessage("分辨率：255.255.255.255/"+str(32)+"\n"+"（注：镉红：Telnet  桔黄：Web  青绿：FTP  白色：未使用）")
            self.q1=qimage2ndarray.array2qimage(img)
            self.imageLabel.setPixmap(QPixmap.fromImage(self.q1))
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()
           



    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "选择新的数据源", QDir.currentPath(),"Source (*.txt *.csv )")

        file_1 = open(fileName,'r')
        file_2 = file_1.readlines()
        self.isRightSingleClick = False
        self.isRightDoubleClick = False
        self.col_num= len(file_2[0].split('	'))
        print('The column number of file:')
        print(self.col_num)
        self.row_num = 0
        for line in file_2:
            self.row_num+=1
        print('The row number of file:')
        print(self.row_num)
        self.input_file = [[ 0 for i in range(18)] for i in range(self.row_num)]
        count =0
        for line in file_2:
            buffer = line.split('	')
            self.input_file[count][0] = buffer[0]
            for i in range(1,18):
                self.input_file[count][i] = int(buffer[i])
            count+=1

        self.sol=16
        broad=int(2**(self.sol/2))
        img = np.zeros((broad,broad,3), np.uint8)
        for i in range(broad):
            cv2.line(img,(i,0),(i,broad-1),(255,255,255),1)
        drawResult(img,self.sol,self.input_file,self.row_num)

        self.statusBar().showMessage("分辨率：255.255.255.255/"+str(self.sol))
        self.q1=qimage2ndarray.array2qimage(img)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.q1))
        self.scaleFactor = 1.0

        self.printAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def save_(self):
        filepath,_ = QFileDialog.getSaveFileName(self, "保存图片",
                                                    "网络空间地图",
                                                    "Images (*.png *.jpg)")
        if filepath:
            img = self.q1
            img.save(filepath)

    def zoomIn(self):
        if self.isRightSingleClick == False and self.isRightDoubleClick == False:
            if self.sol == 28:
                self.statusBar().showMessage("分辨率：255.255.255.255/"+str(self.sol)+"  已放大至最大分辨率！")		
            else:
                self.sol=self.sol+2
                print(self.sol)
                broad=int(2**(self.sol/2))
                img = np.zeros((broad,broad,3), np.uint8)
                for i in range(broad):
                    cv2.line(img,(i,0),(i,broad-1),(255,255,255),1)
                drawResult(img,self.sol,self.input_file,self.row_num)

                self.q1=qimage2ndarray.array2qimage(img)
                self.imageLabel.setPixmap(QPixmap.fromImage(self.q1))

                self.scaleFactor = 1.0

                self.printAct.setEnabled(True)
                self.fitToWindowAct.setEnabled(True)
                self.updateActions()

                if not self.fitToWindowAct.isChecked():
                    self.imageLabel.adjustSize()
                self.statusBar().showMessage("分辨率：255.255.255.255/"+str(self.sol))
		
    def zoomOut(self):
        if self.isRightSingleClick == False and self.isRightDoubleClick == False:
            if self.sol == 16:
                self.statusBar().showMessage("分辨率：255.255.255.255/"+str(self.sol)+"  已缩小至最小分辨率！")		
            else:
                self.sol=self.sol-2
                print(self.sol)
                broad=int(2**(self.sol/2))
                img = np.zeros((broad,broad,3), np.uint8)
                for i in range(broad):
                    cv2.line(img,(i,0),(i,broad-1),(255,255,255),1)
                drawResult(img,self.sol,self.input_file,self.row_num)

                self.q1=qimage2ndarray.array2qimage(img)
                self.imageLabel.setPixmap(QPixmap.fromImage(self.q1))

                self.scaleFactor = 1.0

                self.printAct.setEnabled(True)
                self.fitToWindowAct.setEnabled(True)
                self.updateActions()

                if not self.fitToWindowAct.isChecked():
                    self.imageLabel.adjustSize()
                self.statusBar().showMessage("分辨率：255.255.255.255/"+str(self.sol))
			
    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About ASN-IP MAPPING",
                "<p>The <b>ASN-IP MAPPING</b> example is a simple example of a mapping application in cyberspace. "
                "<p>Copyright 2017 <b>@Jun Zhang  ZWW<b> "
                "<p>Any doubts please contact <b><font color='blue'>zhangjun32108@hotmail.com</font></b>. Thank you! "
                "</p>")

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P",
                enabled=False, triggered=self.print_)

        self.saveAct = QAction("&Save...",self, shortcut="Ctrl+S",
                enabled=True, triggered=self.save_)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.zoomInAct = QAction("Zoom &In ", self, shortcut="Ctrl+A",
                enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QAction("Zoom &Out ", self, shortcut="Ctrl+D",
                enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+N",
                enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False,
                checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                triggered=QApplication.instance().aboutQt)

        self.action1_tool = QAction(" + ",self,
                enabled=True, triggered=self.zoomIn)

        self.action2_tool = QAction(" - ", self,
                enabled=True, triggered=self.zoomOut)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def createToolsbar(self):
        toolbar = self.addToolBar("Tools")
        toolbar.addAction(self.action1_tool)
        toolbar.addAction(self.action2_tool)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 5.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))



    def closeEvent(self,event):
        reply = QtWidgets.QMessageBox.question(self,'确认退出','你确定要退出么？',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
			

	
			
            
if __name__ == '__main__':

    # def handleLeftClick(x, y):
        # row = int(y)
        # column = int(x)
        # print("Clicked on image pixel (row="+str(row)+", column="+str(column)+")")
			
    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    # imageViewer.leftMouseButtonPressed.connect(handleLeftClick)
    imageViewer.show()
    sys.exit(app.exec_())
