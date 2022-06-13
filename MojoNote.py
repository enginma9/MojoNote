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
        location = os.environ['HOME'] + '/Python/MacTest/.Notes/' #'/.Library/MojoNote/'
        filename = '0.MojoNote'
        filepath = location + filename
        try:
            File_Handle = open( filepath, 'r')
            File_Contents = str( File_Handle.read() )
            tree = ET.fromstring( File_Contents )
            Listing = tree.findall('note')
        except:
            print("Loading note list failed.")
            quit()
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
            checkbox_Item = QListWidgetItem( (box_id + ".  " + box_name ) )
            checkbox_Item.setFlags( checkbox_Item.flags() | Qt.ItemIsUserCheckable )
            checkbox_Item.setCheckState( Qt.Unchecked )
            self.listWidget.addItem( checkbox_Item )
            Sub_Window = Note_Window()
            self.Sub_Windows.append( Sub_Window )
            # May take this and set it to a function of the Note window itself
            note_filepath = location + box_id + ".MojoNote"
            Note_Handle = open( note_filepath, 'r')
            Note_Contents = str( Note_Handle.read() )
            self.Sub_Windows[self.Notes].Note_Area.setPlainText( Note_Contents )
            self.Sub_Windows[self.Notes].resize(width,height)
            self.Sub_Windows[self.Notes].move(Pos_X, Pos_Y)
            self.Notes = self.Notes + 1
            self.show_hide()

    def show_hide(self):
        for number in range(self.Notes):
            if self.listWidget.item(number).checkState() == Qt.Checked:
                self.Sub_Windows[number].show()
            else:
                self.Sub_Windows[number].hide()

    def Open_Preferences_Window(self):
        # get which item is selected, and pass that number to preferences, then make sure the window is shown
        selected = self.listWidget.currentRow()
        self.P_Window.get_info( selected )
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
        self.P_Window.hide()
        self.Preferences_Button.clicked.connect( self.Open_Preferences_Window )
        # May have to go back and use QListView, and manually implement checkbox (space to check will not activate this ˅ and there doesn't seem to be a QT signal to attach the command to the checkbox directly when it is a checkable list item)
        self.listWidget.itemClicked.connect(lambda: self.show_hide())

    def __del__(self):
        print("Goodbye")

class Note_Window(QDialog):

    def __init__(self):
        super(Note_Window, self).__init__()
        self.BG_Color = "330099"
        self.FG_Color = "ffffff"
        self.Title = "Note"
        self.Opacity = 0.95 # May want to allow changing this transparency from 91-100, but you can also just make the color 2 digits longer for transparency.
        self.Main_Layout  = QVBoxLayout()
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.setWindowTitle("MacTest")
        self.setWindowOpacity( self.Opacity )
        self.Title_Bar = MyBar(self)
        self.Main_Layout.addWidget( self.Title_Bar )
        self.Note_Area = QPlainTextEdit()
        self.Main_Layout.addWidget( self.Note_Area )
        self.Note_Area.setStyleSheet('border: none; font: 12px Arial;')
        self.sizegrip = QSizeGrip(self)
        self.sizegrip.setFixedSize(20, 10)
        self.Main_Layout.addWidget(self.sizegrip)
        self.Main_Layout.setAlignment(self.sizegrip, Qt.AlignBottom | Qt.AlignRight)
        self.setLayout(self.Main_Layout)
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.Main_Layout.addStretch(-1)
        self.setMinimumSize(100,30)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f'QWidget {{background-color: \#{self.BG_Color}; font-size: 12pt; color: \#{self.FG_Color};}}')
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(Note_Window, self).resizeEvent(QResizeEvent)
        self.Note_Area.setMinimumSize( self.width(), self.height() - 30 )

    def change_Foreground(self, FG):
        self.FG_Color = FG

    def change_Background(self, BG):
        self.BG_Color = BG

    def update_formatting(self):
        self.setStyleSheet(f"QWidget {{background-color: \#{self.BG_Color}; font-size: 10pt; color: \#{self.FG_Color};}}")
        self.Title_Bar.update_formatting()

class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.Bar_Layout = QHBoxLayout()
        self.Bar_Layout.setContentsMargins(0,0,0,0)
        self.title = QLabel(self.parent.Title)

        btn_size = 10

        self.Menu_Button = QPushButton("Ξ", flat=True)   #("Ξ")
        self.Menu_Button.clicked.connect(self.Menu_Button_clicked)
        self.Menu_Button.setFixedSize(btn_size,btn_size)
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")

        self.Restore_btn = QPushButton("o", flat=True)
        self.Restore_btn.clicked.connect(self.Restore_btn_clicked)
        self.Restore_btn.setFixedSize(btn_size, btn_size)
        self.Restore_btn.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")

        self.Roll_Up_btn = QPushButton("-", flat=True)
        self.Roll_Up_btn.clicked.connect(self.Roll_Up_btn_clicked)
        self.Roll_Up_btn.setFixedSize(btn_size,btn_size)
        self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")

        self.Max_Button = QPushButton("O", flat=True)
        self.Max_Button.clicked.connect(self.Max_Button_clicked)
        self.Max_Button.setFixedSize(btn_size, btn_size)
        self.Max_Button.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")

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
        self.title.setStyleSheet(f'QWidget {{background-color: \#{self.parent.BG_Color};}}')
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
        window.show()

    def Max_Button_clicked(self):
        self.parent.showMaximized()

    def Roll_Up_btn_clicked(self):
        #print(self.parent.width())
        self.parent.resize(self.parent.width(), 30 ) # self.parent.height())

    def Restore_btn_clicked(self):
        self.parent.showNormal()

    def change_background(self):
        self.parent.change_Background("\#ffffff")
        self.parent.change_Foreground("\#000000")
        self.parent.update_formatting()

    def update_formatting(self):
        self.title.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")
        self.Restore_btn.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")
        self.Roll_Up_btn.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")
        self.Max_Button.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")

class Pref_Window(QDialog):

    def __init__(self):
        super().__init__()
        self.BG_Color = "110044"
        self.FG_Color = "ffffff"
        self.Title = "Preferences"
        self.selected = 1
        self.Main_Layout  = QVBoxLayout()
        self.Main_Layout.setContentsMargins(0,0,0,0)
        #self.setWindowTitle("MacTest")
        self.setStyleSheet('border-radius: 15px;') #
        self.setWindowOpacity(0.9)
        self.Main_Layout.addWidget( Pref_Bar( self ) )

        self.Title_Label = QLabel("Title:")
        self.Main_Layout.addWidget( self.Title_Label )
        self.Title_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.Title_Edit )
        self.Font_Label = QLabel("Font Size:")
        self.Main_Layout.addWidget( self.Font_Label )
        self.Font_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.Font_Edit )

        self.Position_Label_1 = QLabel("Position X:")
        self.Main_Layout.addWidget( self.Position_Label_1 )
        self.Position_x_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.Position_x_Edit )
        self.Position_Label_2 = QLabel("Position Y:")
        self.Main_Layout.addWidget( self.Position_Label_2 )
        self.Position_y_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.Position_y_Edit )

        self.Size_Label_1 = QLabel("Size X:")
        self.Main_Layout.addWidget( self.Size_Label_1 )
        self.Size_x_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.Size_x_Edit )
        self.Size_Label_2 = QLabel("Size Y:")
        self.Main_Layout.addWidget( self.Size_Label_2 )
        self.Size_y_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.Size_y_Edit )

        self.BG_Color_Label = QLabel("Background Color:")
        self.Main_Layout.addWidget( self.BG_Color_Label )
        self.BG_Color_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.BG_Color_Edit )
        self.FG_Color_Label = QLabel("Font Color: (Omit #, only enter 6 digits)")
        self.Main_Layout.addWidget( self.FG_Color_Label )
        self.FG_Color_Edit = QLineEdit()
        self.Main_Layout.addWidget( self.FG_Color_Edit )

        self.Button_Layout = QHBoxLayout()
        self.Refresh_Button = QPushButton("Refresh")
        self.Button_Layout.addWidget( self.Refresh_Button )
        #self.Refresh_Button.clicked.connect(self.get_info(self.selected))
        self.Set_Button = QPushButton("Set")
        self.Button_Layout.addWidget( self.Set_Button )
        self.Set_Button.clicked.connect(self.Set_Button_clicked)
        self.Main_Layout.addLayout( self.Button_Layout )

        self.setLayout(self.Main_Layout)
        self.Main_Layout.setContentsMargins(0,0,0,0)
        self.Main_Layout.addStretch(-1)
        self.setMinimumSize(200,100)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f'QWidget {{background-color: \#{self.BG_Color}; font-size: 12pt; color: \#{self.FG_Color};}}')
        self.pressing = False

    def get_info( self, selected=1 ):
        self.selected = selected
        x = window.Sub_Windows[selected].Title
        self.Title_Edit.setText(x)
        x = window.Sub_Windows[selected].frameGeometry().x()
        self.Position_x_Edit.setText(str(x))
        x = window.Sub_Windows[selected].frameGeometry().y()
        self.Position_y_Edit.setText(str(x))
        x = window.Sub_Windows[selected].frameGeometry().width()
        self.Size_x_Edit.setText(str(x))
        x = window.Sub_Windows[selected].frameGeometry().height()
        self.Size_y_Edit.setText(str(x))
        x = window.Sub_Windows[selected].BG_Color
        self.BG_Color_Edit.setText(x)
        x = window.Sub_Windows[selected].FG_Color
        self.FG_Color_Edit.setText(x)
        x = window.Sub_Windows[selected].Title

    def Set_Button_clicked(self):
        x = int(self.Size_x_Edit.text())
        y = int(self.Size_y_Edit.text())
        window.Sub_Windows[self.selected].resize( x, y )
        x = int(self.Position_x_Edit.text())
        y = int(self.Position_y_Edit.text())
        window.Sub_Windows[self.selected].move( x, y )
        #if this field has only 6x 0-9/a-f characters, else: turn label red
        window.Sub_Windows[self.selected].change_Background( self.BG_Color_Edit.text() )
        #if this field has only 6x 0-9 characters, else: turn label red
        window.Sub_Windows[self.selected].change_Foreground( self.FG_Color_Edit.text() )
        window.Sub_Windows[self.selected].update_formatting()
        return 0

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
        self.Menu_Button.setStyleSheet(f"QWidget {{background-color: \#{self.parent.BG_Color}; font-size: 10pt; color: \#{self.parent.FG_Color};}}")

        self.title.setFixedHeight(btn_size)
        self.title.setAlignment(Qt.AlignCenter)
        self.Bar_Layout.addWidget(self.Menu_Button)
        self.Bar_Layout.addWidget(self.title)

        self.title.setStyleSheet("""
            color: white;
            font-size: 10pt;
        """)
        #Set to same color as parent
        self.title.setStyleSheet(f'QWidget {{background-color: \#{self.parent.BG_Color};}}')
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

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
