import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
#from datetime import datetime
from os import listdir
import xml.etree.ElementTree as ET


class Note_Window(QDialog):

    BG_Color = "\#000000"
    FG_Color = "\#ffffff"
    Title = "Note"

    def Get_Settings(self):
        location = os.environ['HOME'] + '/Python/General CLI/'
        filename = 'Get_Settings2.xml'
        filepath = location + filename

        print("File to open: " + filename )
        print("Open: " +  filepath + "\n ")

        File_Handle = open( filepath, 'r')
        File_Contents = str(File_Handle.read())

        tree = ET.fromstring( File_Contents )
        lst = tree.findall('note')
        print('Note count:', len(lst))

        for item in lst:
            print('Id', item.find('id').text)
            print('Name', item.find('name').text)
            print('Position:', item.find('Position_x').text, item.find('Position_y').text)
            print('Size_x', item.find('Size_x').text)
            print('Size_y', item.find('Size_y').text)
            print('BG_Color', item.find('BG_Color').text)
            print('FG_Color', item.find('FG_Color').text)
            print('Note_Contents', item.find('Note_Contents').text)

        Position_x = int(lst[1].find('Position_x').text)
        print(str(Position_x))


    def reset_text(self):
        Cursor_Position = self.Note_Area.textCursor().position()
        #print(self.Note_Area.textCursor())
        print(Cursor_Position)
        #self.Note_Area.setTextCursor( Cursor_Position ) # This...
        self.Note_Area.setPlainText( self.Note_Area.toPlainText() )
        self.Note_Area.setStyleSheet(f"QWidget {{'border: none; background-color: {self.parent.BG_Color}; color: {self.parent.FG_Color};}}")




    def __init__(self):
        super(Note_Window, self).__init__()
        self.Main_Layout  = QVBoxLayout()
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.setWindowTitle("MacTest")
        self.setWindowOpacity(0.9)
        self.Main_Layout.addWidget( MyBar( self ) )

        # Trying to only accept plain text without colors or any other formatting, but when pasting on Mac, it puts whatever color it starts as, which means black text on black
        self.Note_Area = QTextEdit("Enter text here.")
        self.Note_Area.acceptRichText = False
        self.Main_Layout.addWidget( self.Note_Area )
        self.Note_Area.setStyleSheet('border: none;')
        self.Note_Area.textChanged.connect(self.reset_text)
        self.setLayout(self.Main_Layout)
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.Main_Layout.addStretch(-1)
        self.setMinimumSize(200,100)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f'QWidget {{background-color: {self.BG_Color}; font-size: 14pt; color: {self.FG_Color};}}')
        self.pressing = False
        self.Get_Settings()

class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.Bar_Layout = QHBoxLayout()
        self.Bar_Layout.setContentsMargins(0,0,0,0)
        self.title = QLabel(" ")

        btn_size = 10

        self.Menu_Button = QPushButton("X", flat=True)   #("Ξ")
        self.Menu_Button.clicked.connect(self.Menu_Button_clicked)
        self.Menu_Button.setFixedSize(btn_size,btn_size)
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

        self.Restore_btn = QPushButton("o", flat=True)
        self.Restore_btn.clicked.connect(self.Restore_btn_clicked)
        self.Restore_btn.setFixedSize(btn_size, btn_size)
        self.Restore_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

        self.Roll_Up_btn = QPushButton("-", flat=True)
        self.Roll_Up_btn.clicked.connect(self.change_background)
        self.Roll_Up_btn.setFixedSize(btn_size,btn_size)
        self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

        self.btn_max = QPushButton("O", flat=True)
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

        self.title.setFixedHeight(btn_size)
        self.title.setAlignment(Qt.AlignCenter)
        self.Bar_Layout.addWidget(self.Menu_Button)
        self.Bar_Layout.addWidget(self.title)
        self.Bar_Layout.addWidget(self.Roll_Up_btn)
        self.Bar_Layout.addWidget(self.Restore_btn)
        self.Bar_Layout.addWidget(self.btn_max)

        self.title.setStyleSheet("""
            color: white;
            font-size: 10pt;
            font-family: courier monospace;
        """)
        #Set to same color as parent
        self.title.setStyleSheet(f'QWidget {{background-color: {self.parent.BG_Color};}}')
        self.setLayout(self.Bar_Layout)
        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def Menu_Button_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized() # Not a true "maximized" window, but that is beneficial, because when on MacOS, I don't want to take over the screen, just take up available space.

    def Roll_Up_btn_clicked(self):
        self.parent.showNormal()

    def Restore_btn_clicked(self):
        self.parent.showNormal()


    def change_background(self):
        # Open settings(text) file, read contents, assign values.  Time to implement in CLI file and return.
        self.parent.BG_Color = "\#ffffff"
        self.parent.FG_Color = "\#000000"
        self.parent.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 14pt; color: {self.parent.FG_Color};}}")
        self.title.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Restore_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.btn_max.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #print( self.parent.BG_Color, self.parent.FG_Color, self.parent.pressing)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Note_Window()
    window.show()
    sys.exit(app.exec())
