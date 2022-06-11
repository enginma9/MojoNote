import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
from os import listdir
import xml.etree.ElementTree as ET

class MainWindow(QMainWindow):
    x = 0

    def Set_Up(self):
        #open the file to pull data from
        location = os.environ['HOME'] + '/Python/MacTest/.Notes/'
        filename = '0.MojoNote'
        filepath = location + filename
        #start paste
        print("File to open: " + filename )
        print("Open: " +  filepath + "\n ")
        try:
            File_Handle = open( filepath, 'r')
            File_Contents = str( File_Handle.read() )
            tree = ET.fromstring( File_Contents )
            Listing = tree.findall('note')
            print('Note count:', len( tree.findall('note') ))
        except:
            print("Loading note list failed.")

        self.Note_List = list()
        self.Notes = 0

        for item in Listing:
            box_id = str( item.find('id').text )
            box_name = str( item.find('name').text )
            width = int( item.find('width').text)
            height = int( item.find('height').text)
            Pos_X = int( item.find('Position_x').text)
            Pos_Y = int( item.find('Position_y').text)
            BG_Color = str(item.find('BG_Color').text)
            FG_Color = str(item.find('FG_Color').text)

            #print(box_name, "Position:(" + str(Pos_X) + "," + str(Pos_Y) + ") Size:(" + str(width) + "," + str(height) + ")", BG_Color,FG_Color)

            checkbox_Item = QListWidgetItem( box_name )
            checkbox_Item.setFlags( checkbox_Item.flags() | Qt.ItemIsUserCheckable )
            checkbox_Item.setCheckState( Qt.Unchecked )
            self.listWidget.addItem( checkbox_Item )
            Sub_Window = Note_Window()
            self.Sub_Windows.append( Sub_Window )
            #self.Sub_Windows[self.Notes].show()
            self.Sub_Windows[self.Notes].resize(width,height)
            self.Sub_Windows[self.Notes].move(Pos_X, Pos_Y)
            #self.Sub_Windows[Notes].setStyleSheet(f'QWidget {{background-color: {BG_Color}; font-size: 14pt; color: {FG_Color};}}') #replace with custom class function
            self.Notes = self.Notes + 1
            self.show_hide()

    def show_hide(self):
        for number in range(self.Notes):
            if self.listWidget.item(number).checkState() == Qt.Checked:
                self.Sub_Windows[number].show()
            else:
                self.Sub_Windows[number].hide()

    def Open_Preferences_Window(self):
        self.P_Window.show()
        return 0

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MojoNote")
        self.my_palette = QPalette()
        self.Main_Layout = QVBoxLayout()
        self.widget = QWidget()
        self.Sub_Windows = []
        #Set theme
        self.my_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.my_palette.setColor(QPalette.WindowText, Qt.white)
        self.my_palette.setColor(QPalette.Base, QColor(53, 53, 53))
        self.my_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.my_palette.setColor(QPalette.ToolTipBase, Qt.white)
        self.my_palette.setColor(QPalette.ToolTipText, Qt.white)
        self.my_palette.setColor(QPalette.Text, Qt.white)
        self.my_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.my_palette.setColor(QPalette.ButtonText, Qt.white)
        self.my_palette.setColor(QPalette.BrightText, Qt.red)
        self.my_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.my_palette.setColor(QPalette.Highlight, QColor(170, 70, 255)) #make purple
        self.my_palette.setColor(QPalette.HighlightedText, Qt.black)
        #Assign colors and style to window
        qApp.setPalette(self.my_palette)
        qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 0px solid white; margin: 0; padding: 0; }")

        self.listWidget = QListWidget()
        self.Preferences_Button = QPushButton("Note Preferences")
        self.Main_Layout.addWidget( self.listWidget )

        self.Main_Layout.addWidget( self.Preferences_Button )
        self.widget.setLayout( self.Main_Layout )
        self.setCentralWidget( self.widget )
        #self.hide()
        self.Set_Up()
        # create Preferences window, and hide it.
        self.P_Window = Pref_Window()
        self.P_Window.show()
        self.Preferences_Button.clicked.connect( self.Open_Preferences_Window )
        # May have to go back and use QListView, and manually implement checkbox (space to check will not activate this ˅ and there doesn't seem to be a QT signal to attach the command to the checkbox directly when it is a checkable list item)
        self.listWidget.itemClicked.connect(lambda: self.show_hide())

    def __del__(self):
        print("Goodbye")

class Note_Window(QDialog):

    def __init__(self):
        super(Note_Window, self).__init__()
        self.BG_Color = "\#000000"
        self.FG_Color = "\#ffffff"
        self.Title = "Note"
        self.Main_Layout  = QVBoxLayout()
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.setWindowTitle("MacTest")
        self.setWindowOpacity(0.9)
        self.Main_Layout.addWidget( MyBar( self ) )
        self.Note_Area = QTextEdit("Enter text here.")
        self.Main_Layout.addWidget( self.Note_Area )
        self.Note_Area.setStyleSheet('border: none; font: 12px Arial;')
        self.setLayout(self.Main_Layout)
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.Main_Layout.addStretch(-1)
        self.setMinimumSize(200,100)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f'QWidget {{background-color: {self.BG_Color}; font-size: 12pt; color: {self.FG_Color};}}')
        self.pressing = False

class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.Bar_Layout = QHBoxLayout()
        self.Bar_Layout.setContentsMargins(0,0,0,0)
        self.title = QLabel(self.parent.Title)

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

        self.Max_Button = QPushButton("O", flat=True)
        self.Max_Button.clicked.connect(self.Max_Button_clicked)
        self.Max_Button.setFixedSize(btn_size, btn_size)
        self.Max_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

        self.title.setFixedHeight(btn_size)
        self.title.setAlignment(Qt.AlignCenter)
        self.Bar_Layout.addWidget(self.Menu_Button)
        self.Bar_Layout.addWidget(self.title)
        self.Bar_Layout.addWidget(self.Roll_Up_btn)
        self.Bar_Layout.addWidget(self.Restore_btn)
        self.Bar_Layout.addWidget(self.Max_Button)

        self.title.setStyleSheet("""
            color: white;
            font-size: 10pt;
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
        self.parent.hide()

    def Max_Button_clicked(self):
        self.parent.showMaximized()
        # Not a true "maximized" window, but that is beneficial,
        #  because when on MacOS, I don't want to take over the screen,
        #  just take up available space.

    def Roll_Up_btn_clicked(self):
        self.parent.showNormal()

    def Restore_btn_clicked(self):
        self.parent.showNormal()

    def change_background(self):
        self.change_Background("\#ffffff")
        self.change_Foreground("\#000000")

    def change_Foreground(self, FG):
        self.parent.FG_Color = FG
        self.parent.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 14pt; color: {self.parent.FG_Color};}}")
        self.title.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Restore_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Max_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

    def change_Background(self, BG):
        self.parent.BG_Color = BG
        self.parent.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.title.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Restore_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Max_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        print( self.parent.BG_Color, self.parent.FG_Color, self.parent.pressing)

class Pref_Window(QDialog):

    BG_Color = "\#000000"
    FG_Color = "\#ffffff"
    Title = "Preferences"


    def __init__(self):
        super().__init__()
        self.Main_Layout  = QVBoxLayout()
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.setWindowTitle("MacTest")
        self.setWindowOpacity(0.9)
        self.Main_Layout.addWidget( Pref_Bar( self ) )
        #self.Note_Area = QTextEdit("Enter text here.")
        #self.Main_Layout.addWidget( self.Note_Area )
        #self.Note_Area.setStyleSheet('border: none; font: 12px Arial;')
        self.setLayout(self.Main_Layout)
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.Main_Layout.addStretch(-1)
        self.setMinimumSize(200,100)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f'QWidget {{background-color: {self.BG_Color}; font-size: 12pt; color: {self.FG_Color};}}')
        self.pressing = False

class Pref_Bar(QWidget):

    def __init__(self, parent):
        super(Pref_Bar, self).__init__()
        self.parent = parent
        self.Bar_Layout = QHBoxLayout()
        self.Bar_Layout.setContentsMargins(0,0,0,0)
        self.title = QLabel(self.parent.Title)

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

        self.Max_Button = QPushButton("O", flat=True)
        self.Max_Button.clicked.connect(self.Max_Button_clicked)
        self.Max_Button.setFixedSize(btn_size, btn_size)
        self.Max_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

        self.title.setFixedHeight(btn_size)
        self.title.setAlignment(Qt.AlignCenter)
        self.Bar_Layout.addWidget(self.Menu_Button)
        self.Bar_Layout.addWidget(self.title)
        #self.Bar_Layout.addWidget(self.Roll_Up_btn)
        #self.Bar_Layout.addWidget(self.Restore_btn)
        #self.Bar_Layout.addWidget(self.Max_Button)

        self.title.setStyleSheet("""
            color: white;
            font-size: 10pt;
        """)
        #Set to same color as parent
        self.title.setStyleSheet(f'QWidget {{background-color: {self.parent.BG_Color};}}')
        self.setLayout(self.Bar_Layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(Pref_Bar, self).resizeEvent(QResizeEvent)
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
        self.parent.hide()

    def Max_Button_clicked(self):
        self.parent.showMaximized()
        # Not a true "maximized" window, but that is beneficial,
        #  because when on MacOS, I don't want to take over the screen,
        #  just take up available space.

    def Roll_Up_btn_clicked(self):
        self.parent.showNormal()

    def Restore_btn_clicked(self):
        self.parent.showNormal()

    def change_background(self):
        self.change_Background("\#ffffff")
        self.change_Foreground("\#000000")

    def change_Foreground(self, FG):
        self.parent.FG_Color = FG
        self.parent.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 14pt; color: {self.parent.FG_Color};}}")
        self.title.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #self.Restore_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #self.Max_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")

    def change_Background(self, BG):
        self.parent.BG_Color = BG
        self.parent.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.title.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #self.Restore_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #self.Max_Button.setStyleSheet(f"QWidget {{background-color: {self.parent.BG_Color}; font-size: 10pt; color: {self.parent.FG_Color};}}")
        #print( self.parent.BG_Color, self.parent.FG_Color, self.parent.pressing)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
