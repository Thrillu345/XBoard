# Modern Notice Board Version - X.T.1
'''
    Objective: To design and develop a button-based interactive notice board. And add time.

    Description:
    ~~~~~~~~~~~
    This is a simple notice board with following functionalities:
    " Modern Notice Board X.b.1" have two modes of operation [ Kiosk Mode & Player mode ]

    Kiosk Mode -
        In this mode of operation, a menu of options are given to the user. The menu is as follows:
            01 - Menu
            02 - Map
                2.1 to 2.9 - Map pages 
            03 - Updates
            04 - Events
            05 - Notices
            06 - Placements
            07 - About
                7.1 - About Project
                7.2 - About KITS

    Player Mode -
        In this mode of operation, the information is displayed as a playlist. The basic playlist is as follows:
            00 - Intro
            03 - Updates
            04 - Events
            08 - Placements Till date
            09 - Quote of the day
            10 - Special of the day
            11 - Event Posters *

        ⚠️ The Playlist should not exceed the duration of 60 seconds.
        ➡️ So, basically each page is set to have a default duration of '6' seconds.

    Commonalities -
        Important information should be continuously displayed without keeping others waiting.
        So, few elements are kept common in both kiosk and player modes of operation.
        The common elements are as follows :
             1 - Important Update

    Overall Pages -
        Based on overall mapping, all pages are as follows -
            00 - Intro
            01 - Menu
            02 - Map
            03 - Updates
            04 - Events
            05 - Notices
            06 - Placements
            07 - About
            08 - Placements Till date
            09 - Quote of the day
            10 - Special of the day
            11 - Event Posters
             X - Extra Page

    Workers -
        1. Updater.py
        2. BGM.py
        3. Auto-starter.py
        4. NetworkCheck.py

    @ThrillingStar
'''

# Import necessary modules
import sys, subprocess, vlc, datetime

from PyQt5.QtWidgets    import (QApplication, QWidget, QSizePolicy,
                                QLabel, QPushButton,
                                QVBoxLayout,QHBoxLayout, QGridLayout, QStackedLayout, 
                                QAction)
from PyQt5.QtGui        import QIcon, QPixmap, QPainter
from PyQt5.QtCore       import QTimer, Qt, QSize

stylesheet = """
    QWidget {
        background-color: #ffffff;
        color: white;
        font-family: 'comic sans ms';
    }
             """

class QScrollingLabel(QLabel):

    def __init__(self,text):
        super().__init__()
        self.setText(text)
        #self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignLeft)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(6)
        self.offset = 0

    def scroll_text(self):
        self.offset += 1
        if self.offset >= 3*self.width():
            self.offset = 0
        self.update()

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x = self.width() - self.offset
        painter.drawText(x,2*self.height()//3, self.text())
        

class XBoard(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        print("All Set!")

    def initUI(self):
        ''' Set up the app GUI '''
        self.setWindowTitle("X-Board M")
        self.setWindowIcon(QIcon('Pics/favicon.png'))
        
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setGeometry(rect)
        
        self.font_size = "22"
        
        print("Creating Actions")
        self.createActions()
        
        print("Setting Up Main Window")
        self.setUpMainWindow()
        self.showFullScreen()
        
        self.top_label.setMaximumSize(self.top_label.size())
        

        print("Starting Updator")
        self.updater = subprocess.Popen(["python","Updater.py"])
        print("Starting BGM")
        self.bgm = subprocess.Popen(["python","bgm.py"])
        

    def setUpMainWindow(self):
        ''' Create and arrange main window '''

        # Create the top label
        text = "An important update scrolls here......... A special update which is either very important or recent. Something something something something."
        text = "Hellow..."
        text = text + '\t\t' + text + '\t\t' + text
        
        self.top_label = QScrollingLabel(text)
        self.top_label.setStyleSheet(" font-size: {}pt; background-color: #150000; color: #ff5555; padding: 5px; ".format(self.font_size))
        
        print("Creating Pages...")
        # create main stack pages
        print("Creating Intro Page...")
        self.create_page_00()
        self.setMaximumSize(self.size())
        print("Creating Menu Page...")
        self.create_page_01()
        print("Creating Map Page...")
        self.create_page_02()
        print("Creating Updates Page...")
        self.create_page_03()
        print("Creating Events Page...")
        self.create_page_04()
        print("Creating Notices Page...")
        self.create_page_05()
        print("Creating Placements Page...")
        self.create_page_06()
        print("Creating About Page...")
        self.create_page_07()
        print("Creating Quote Page...")
        self.create_page_08()
        print("Creating Specials Page...")
        self.create_page_09()
        print("Creating Placed Number Page...")
        self.create_page_10()
        #self.create_page_11()
        #self.create_page_x()

        print("Creating Main Stack...")
        # Create the Main Stack and add Pages to the main stack
        self.main_stack = QStackedLayout()
        
        self.main_stack.addWidget(self.page_00)
        self.main_stack.addWidget(self.page_01)
        self.main_stack.addWidget(self.page_02)
        self.main_stack.addWidget(self.page_03)
        self.main_stack.addWidget(self.page_04)
        self.main_stack.addWidget(self.page_05)
        self.main_stack.addWidget(self.page_06)
        self.main_stack.addWidget(self.page_07)
        self.main_stack.addWidget(self.page_08)
        self.main_stack.addWidget(self.page_09)
        self.main_stack.addWidget(self.page_10)
        #self.main_stack.addWidget(self.page_11)
        #self.main_stack.addWidget(self.page_x)

        # Create the main vbox
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0,0,0,0)

        # Add Widgets to the main vbox
        vbox.addWidget(self.top_label)
        vbox.addLayout(self.main_stack)

        # Set the main window layout
        self.setLayout(vbox)

        # Add Actions
        self.addAction(self.exit_act)

        # Time to play
        self.index = 0
        self.ticker = 0
        
        print("Starting Updater Timer...")
        # Set an Updater Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(500)

        print("Starting Playlist Timer...")
        # Set playlist timer
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.play)
        self.timer2.start(6000)


###############################################################################################
# Create Pages
###############################################################################################

    def create_page_00(self):
        ''' Create and arrange widgets in INTRO PAGE '''
        # Create INTRO LABEL
        self.intro_label = QLabel(" ECE Dept. presents... \n\n X-BOARD \n\n An AI-Powered Notice Board! ")
        self.intro_label.setStyleSheet(" font-size: {}pt; color: black; background-color: white; border-image: url(Pics/intro.jpg); font-family: 'Quicksand';".format(2*int(self.font_size)));
        self.intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create page widget and set the layout
        self.page_00 = QWidget()
        self.page_00 = self.intro_label

    def create_page_01(self):
        ''' Create and arrange widgets in  MENU PAGE '''
        # Create and add head label
        menu_label = QLabel("Menu")
        menu_label.setStyleSheet(" font-size: {}pt; color: #ff5555; ".format(self.font_size))
        menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        # Set Size Policies for the elements
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # Create grid widgets - map button
        map_button = QPushButton("¹ Map")
        map_button.clicked.connect(self.showMap)
        map_button.setShortcut("1")
        map_button.setSizePolicy(sizePolicy1)

        # Create grid widgets - updates button
        updates_button = QPushButton("Updates ²")
        updates_button.clicked.connect(self.showUpdates)
        updates_button.setShortcut("2")
        updates_button.setSizePolicy(sizePolicy1)

        # Create grid widgets - events button
        events_button = QPushButton(" ³ Events ")
        events_button.clicked.connect(self.showEvents)
        events_button.setShortcut("3")
        events_button.setSizePolicy(sizePolicy1)

        # Create grid widgets - notices button
        notices_button = QPushButton("Notices ⁴")
        notices_button.clicked.connect(self.showNotices)
        notices_button.setShortcut("4")
        notices_button.setSizePolicy(sizePolicy1)

        # Create grid widgets - placements info button
        placements_button = QPushButton("⁵ Placements")
        placements_button.clicked.connect(self.showPlacementsUpdates)
        placements_button.setShortcut("5")
        placements_button.setSizePolicy(sizePolicy1)
        
        # Create grid widgets - about button
        about_button = QPushButton("About ⁶")
        about_button.clicked.connect(self.showAbout)
        about_button.setShortcut("6")
        about_button.setSizePolicy(sizePolicy1)

        # Create grid Widgets - college logo
        logo_label = QLabel()
        #logo_label.setStyleSheet(" border-image: url(Pics/logo_v3.png); ")
        logo_pixmap = QPixmap("Pics/logo_v3.png")
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create grid and add widgets to the grid
        menu_grid = QGridLayout()
        menu_grid.addWidget(map_button,1,3,4,2)
        menu_grid.addWidget(updates_button,1,9,4,2)
        menu_grid.addWidget(events_button,4,1,4,2)
        menu_grid.addWidget(notices_button,4,11,4,2)
        menu_grid.addWidget(placements_button,7,3,4,2)
        menu_grid.addWidget(about_button,7,9,4,2)
        menu_grid.addWidget(logo_label,4,6,4,2)
        
        menu_grid.setContentsMargins(0,0,0,0)

        # Create menu grid container
        menu_grid_c = QWidget()
        menu_grid_c.setLayout(menu_grid)
        menu_grid_c.setStyleSheet('''
                                        QPushButton {
                                            font-size: %spt;
                                            color: 'white';
                                            background-color: #ff5050;
                                            text-align: center;
                                            border: solid;
                                            border-radius: 100px;
                                            /* border-top-left-radius: 70px;
                                            border-bottom-right-radius: 70px;*/
                                            margin: 40px;
                                            padding: 10px;
                                            
                                            /*border-image: url(Pics/bubble.png);*/
                                         }
                                        
                                        QPushButton:pressed {
                                            background-color: #ff4040;
                                         }
                                 '''%(self.font_size))

        # Create MENU PAGE CONTAINER
        self.page_01 = QWidget()
        self.page_01 = menu_grid_c

        # Add actions to the menu page
        self.page_01.addAction(self.intro_act)
        self.page_01.addAction(self.placements_act)
        self.page_01.addAction(self.quote_act)
        self.page_01.addAction(self.specials_act)
        #self.page_01.addAction(self.posters_act)

    def create_page_02(self):
        ''' Create and arrange widgets in the MAP PAGE '''
        # Set Size Policies for the elements
        self.sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # Create elements of map_stack
        main_0 = QLabel()
        main_0.setStyleSheet(" border-image: url('Pics/blueprint.jpg') ; ")

        main_1 = QLabel()
        main_1.setStyleSheet(" border-image: url('Pics/bg1.jpeg') ; ")

        main_2 = QLabel()
        main_2.setStyleSheet(" border-image: url('Pics/blueprint.jpg') ; ")

        main_3 = QLabel()
        main_3.setStyleSheet(" border-image: url('Pics/bg1.jpeg') ; ")

        new_0 = QLabel()
        new_0.setStyleSheet(" border-image: url('Pics/blueprint.jpg') ; ")

        new_1 = QLabel()
        new_1.setStyleSheet(" border-image: url('Pics/bg1.jpeg') ; ")

        new_2 = QLabel()
        new_2.setStyleSheet(" border-image: url('Pics/blueprint.jpg') ; ")

        new_3 = QLabel()
        new_3.setStyleSheet(" border-image: url('Pics/bg1.jpeg') ; ")

        overall = QLabel()
        overall.setStyleSheet(" border-image: url('Pics/blueprint.jpg') ; ")

        # Create map_stack and add elements to the map_stack
        map_stack = QStackedLayout()
        
        map_stack.addWidget(overall)
        map_stack.addWidget(main_0)
        map_stack.addWidget(main_1)
        map_stack.addWidget(main_2)
        map_stack.addWidget(main_3)
        map_stack.addWidget(new_0)
        map_stack.addWidget(new_1)
        map_stack.addWidget(new_2)
        map_stack.addWidget(new_3)


        # Create elements of map_nav
        main_block_label = QLabel("<h1>Main Block</h1>")
        main_block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_block_label.setStyleSheet(" margin-top: 10px; ")
        
        m0_button = QPushButton("1 - Ground floor")
        m0_button.setShortcut("1")
        m0_button.clicked.connect(lambda: map_stack.setCurrentIndex(1))
        
        m1_button = QPushButton("2 - First floor")
        m1_button.setShortcut("2")
        m1_button.clicked.connect(lambda: map_stack.setCurrentIndex(2))
        
        m2_button = QPushButton("3 - Second floor")
        m2_button.setShortcut("3")
        m2_button.clicked.connect(lambda: map_stack.setCurrentIndex(3))

        m3_button = QPushButton("4 - Third floor")
        m3_button.setShortcut("4")
        m3_button.clicked.connect(lambda: map_stack.setCurrentIndex(4))

        new_block_label = QLabel("<h1>New Block</h1>")
        new_block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        new_block_label.setStyleSheet(" margin-top: 0px; ")
        
        n0_button = QPushButton("5 - Ground floor")
        n0_button.setShortcut("5")
        n0_button.clicked.connect(lambda: map_stack.setCurrentIndex(5))

        n1_button = QPushButton("6 - First floor")
        n1_button.setShortcut("6")
        n1_button.clicked.connect(lambda: map_stack.setCurrentIndex(6))

        n2_button = QPushButton("7 - Second floor")
        n2_button.setShortcut("7")
        n2_button.clicked.connect(lambda: map_stack.setCurrentIndex(7))
        
        n3_button = QPushButton("8 - Third floor")
        n3_button.setShortcut("8")
        n3_button.clicked.connect(lambda: map_stack.setCurrentIndex(8))

        overall_label = QLabel("<h1>Site Plan</h1>")
        overall_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overall_label.setStyleSheet(" margin-top: 0px; ")
        
        overall_button = QPushButton("9 - Site Plan")
        overall_button.setShortcut("9")
        overall_button.clicked.connect(lambda: map_stack.setCurrentIndex(0))

        # Create map_nav and add elements to the map_nav layout
        map_nav = QVBoxLayout()

        map_nav.addWidget(main_block_label)
        map_nav.addWidget(m0_button)
        map_nav.addWidget(m1_button)
        map_nav.addWidget(m2_button)
        map_nav.addWidget(m3_button)
        
        map_nav.addWidget(new_block_label)
        map_nav.addWidget(n0_button)
        map_nav.addWidget(n1_button)
        map_nav.addWidget(n2_button)
        map_nav.addWidget(n3_button)

        map_nav.addWidget(overall_label)
        map_nav.addWidget(overall_button)
        
        map_nav.setAlignment(Qt.AlignmentFlag.AlignTop)
        map_nav.setSpacing(0)
        map_nav.setContentsMargins(0,0,0,0)


        # Create elements of map_nav
        main_block_label = QLabel("<h1>Main Block</h1>")
        main_block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_block_label.setStyleSheet(" margin-top: 10px; ")
        
        m0_button = QPushButton("1 - Ground floor")
        m0_button.setShortcut("1")
        m0_button.clicked.connect(lambda: map_stack.setCurrentIndex(1))
        
        m1_button = QPushButton("2 - First floor")
        m1_button.setShortcut("2")
        m1_button.clicked.connect(lambda: map_stack.setCurrentIndex(2))
        
        m2_button = QPushButton("3 - Second floor")
        m2_button.setShortcut("3")
        m2_button.clicked.connect(lambda: map_stack.setCurrentIndex(3))

        m3_button = QPushButton("4 - Third floor")
        m3_button.setShortcut("4")
        m3_button.clicked.connect(lambda: map_stack.setCurrentIndex(4))

        new_block_label = QLabel("<h1>New Block</h1>")
        new_block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        new_block_label.setStyleSheet(" margin-top: 0px; ")
        
        n0_button = QPushButton("5 - Ground floor")
        n0_button.setShortcut("5")
        n0_button.clicked.connect(lambda: map_stack.setCurrentIndex(5))

        n1_button = QPushButton("6 - First floor")
        n1_button.setShortcut("6")
        n1_button.clicked.connect(lambda: map_stack.setCurrentIndex(6))

        n2_button = QPushButton("7 - Second floor")
        n2_button.setShortcut("7")
        n2_button.clicked.connect(lambda: map_stack.setCurrentIndex(7))
        
        n3_button = QPushButton("8 - Third floor")
        n3_button.setShortcut("8")
        n3_button.clicked.connect(lambda: map_stack.setCurrentIndex(8))

        overall_label = QLabel("<h1>Site Plan</h1>")
        overall_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overall_label.setStyleSheet(" margin-top: 0px; ")
        
        overall_button = QPushButton("9 - Site Plan")
        overall_button.setShortcut("9")
        overall_button.clicked.connect(lambda: map_stack.setCurrentIndex(0))

        # Create map_nav and add elements to the map_nav layout
        map_nav = QVBoxLayout()

        map_nav.addWidget(main_block_label)
        map_nav.addWidget(m0_button)
        map_nav.addWidget(m1_button)
        map_nav.addWidget(m2_button)
        map_nav.addWidget(m3_button)
        
        map_nav.addWidget(new_block_label)
        map_nav.addWidget(n0_button)
        map_nav.addWidget(n1_button)
        map_nav.addWidget(n2_button)
        map_nav.addWidget(n3_button)

        map_nav.addWidget(overall_label)
        map_nav.addWidget(overall_button)
        
        map_nav.setAlignment(Qt.AlignmentFlag.AlignTop)
        map_nav.setSpacing(0)
        map_nav.setContentsMargins(0,0,0,0)


        # Create MapNav hbox
        mapNav_hbox = QHBoxLayout()
        mapNav_hbox.addLayout(map_stack)
        mapNav_hbox.addLayout(map_nav)
        mapNav_hbox.setSpacing(0)
        mapNav_hbox.setContentsMargins(0,0,0,0)

        # Back Label
        back_label = QLabel("Press '0' to open Menu")
        back_label.setSizePolicy(self.sizePolicy1)
        back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label.setStyleSheet(f"font-size: {self.font_size}pt; text-align: center; color: #ff5555 ; background-color: #101010 ; padding: 10x; border: None; ")

        # Create Map VBox
        map_vbox = QVBoxLayout()
        map_vbox.addLayout(mapNav_hbox)
        map_vbox.addWidget(back_label)

        map_vbox.setSpacing(0)
        map_vbox.setContentsMargins(0,0,0,0)

        # Create MAP PAGE CONTAINER
        self.page_02 = QWidget()
        self.page_02.setLayout(map_vbox)
        self.page_02.setStyleSheet('''
                                     QPushButton {
                                        color: #000066;
                                        background-color: 'sky blue';
                                        border-radius: 4px;
                                        font-size: 25px;
                                        padding: 10px;
                                        margin: 10px;
                                        border-bottom: 5px solid #4488ff;
                                        text-align: left;
                                        
                                     }
                                     QPushButton:pressed {
                                        border-bottom: NONE;
                                     }
                                     QLabel {
                                        color: #ff5555;
                                        text-align: center;
                                        font-size: 15px;
                                     }
                                 ''')

    def create_page_03(self):
        ''' Create and arrange widgets in the UPDATES PAGE '''
        # Updates Head
        updates_head = QLabel("Updates")
        updates_head.setSizePolicy(self.sizePolicy1)
        updates_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        updates_head.setStyleSheet(f"font-size: {int(self.font_size)+5}pt; color: #eeeeee ; background-color: #333333 ; padding: 2px;")

        # Updates
        self.updates = QLabel("The Updates")
        #self.setUpdates()
        self.updates.setSizePolicy(self.sizePolicy2)
        self.updates.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.updates.setWordWrap(True)
        self.updates.setStyleSheet(f" font-size: {int(self.font_size) - 10}pt; color: #111111; background-color: #eeeeee; border-image: url(Pics/updates.png); padding: 10px;")

        # Back Label
        back_label = QLabel("Press any button to open Menu")
        back_label.setSizePolicy(self.sizePolicy1)
        back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label.setStyleSheet(f"font-size: {self.font_size}pt; color: #ff5050 ; background-color: #101010 ; padding: 2px;")

        # Create Main VBox
        updates_vbox = QVBoxLayout()
        updates_vbox.addWidget(updates_head)
        updates_vbox.addWidget(self.updates)
        updates_vbox.addWidget(back_label)

        updates_vbox.setSpacing(0)
        updates_vbox.setContentsMargins(0,0,0,0)
        
        self.page_03 = QWidget()
        self.page_03.setLayout(updates_vbox)

    def create_page_04(self):
        ''' Create and arrange widgets in the EVENTS PAGE '''
        # Events Head
        events_head = QLabel("Events")
        events_head.setSizePolicy(self.sizePolicy1)
        events_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        events_head.setStyleSheet(f"font-size: {int(self.font_size)+5}pt; color: #ffe6ff ; background-color: purple ; padding: 2px;")

        # Events
        self.events = QLabel("The Events")
        #self.setEvents()
        self.events.setSizePolicy(self.sizePolicy2)
        self.events.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.events.setStyleSheet(f" font-size: {int(self.font_size)-10}pt; border-image: url('Pics/events.png'); color: purple; background-color: #fff7ff; padding: 10px;")
        self.events.setWordWrap(True)

        # Back Label
        back_label = QLabel("Press any button to open Menu")
        back_label.setSizePolicy(self.sizePolicy1)
        back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label.setStyleSheet(f"font-size: {int(self.font_size)}pt; color: #ff5050 ; background-color: #101010 ; padding: 2px;")
        
        # Create Main VBox
        events_vbox = QVBoxLayout()
        events_vbox.addWidget(events_head)
        events_vbox.addWidget(self.events)
        events_vbox.addWidget(back_label)
        
        events_vbox.setSpacing(0)
        events_vbox.setContentsMargins(0,0,0,0)

        # Create Page Container
        self.page_04 = QWidget()
        self.page_04.setLayout(events_vbox)
        

    def create_page_05(self):
        ''' Create and arrange widgets in NOTICES PAGE '''
        # Notices Head
        notices_head = QLabel("Notices")
        notices_head.setSizePolicy(self.sizePolicy1)
        notices_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notices_head.setStyleSheet(f"font-size: {int(self.font_size)+5}pt; color: #e6f9ff ; background-color: #007399 ; padding: 2px;")

        # Notices
        self.notices = QLabel(" The Notices")
        #self.setNotices()
        self.notices.setSizePolicy(self.sizePolicy2)
        self.notices.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.notices.setWordWrap(True)
        self.notices.setStyleSheet(f" font-size: {int(self.font_size)-10}pt; border-image: url(Pics/notices.png); background-color: #e6f9ff; color: #007399; padding: 10px;")

        # Back Label
        back_label = QLabel("Press any button to open Menu")
        back_label.setSizePolicy(self.sizePolicy1)
        back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label.setStyleSheet(f"font-size: {int(self.font_size)}pt; color: #ff5050 ; background-color: #101010 ; padding: 2px;")

        # Create Main VBox
        notices_vbox = QVBoxLayout()
        notices_vbox.addWidget(notices_head)
        notices_vbox.addWidget(self.notices)
        notices_vbox.addWidget(back_label)

        notices_vbox.setSpacing(0)
        notices_vbox.setContentsMargins(0,0,0,0)

        # Create Page Container
        self.page_05 = QWidget()
        self.page_05.setLayout(notices_vbox)

    def create_page_06(self):
        ''' Create and arrange widgets in the PLACEMENTS UPDATES PAGE '''
        # Placements Updates Head
        placements_head = QLabel("Placement Updates")
        placements_head.setSizePolicy(self.sizePolicy1)
        placements_head.setStyleSheet(f" font-size: {int(self.font_size)+5}pt; color: #fffff5; background-color: 'dark green'; padding: 2px;")
        placements_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Placements Updates
        self.placements = QLabel(" Placements Updates ")
        #self.setPlacementsInfo()
        self.placements.setSizePolicy(self.sizePolicy2)
        self.placements.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.placements.setWordWrap(True)
        self.placements.setStyleSheet(f" font-size: {int(self.font_size)-10}pt; border-image: url('Pics/placements.png'); background-color: #fffff5; color: 'dark green'; padding: 10px;")

        # Back Label
        back_label = QLabel("Press any button to open Menu")
        back_label.setSizePolicy(self.sizePolicy1)
        back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label.setStyleSheet(f"font-size: {int(self.font_size)}pt; color: #ff5050 ; background-color: #101010 ; padding: 2px;")

        # Create Main VBox
        placements_vbox = QVBoxLayout()
        placements_vbox.addWidget(placements_head)
        placements_vbox.addWidget(self.placements)
        placements_vbox.addWidget(back_label)

        placements_vbox.setSpacing(0)
        placements_vbox.setContentsMargins(0,0,0,0)

        # Create PLACEMENTS PAGE CONTAINER
        self.page_06 = QWidget()
        self.page_06.setLayout(placements_vbox)

    def create_page_07(self):
        ''' Create and arrange widgets in the ABOUT PAGE '''
        # About KITS
        about_kits_head = QLabel("About KITS")
        about_kits_head.setSizePolicy(self.sizePolicy1)
        about_kits_head.setStyleSheet(f" font-size: {int(self.font_size)+5}pt; color: #ffe6e6 ; background-color: #ff5050 ; padding: 2px;")
        about_kits_head.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Details in About KITS
        about_kits_details = QLabel("""
<h2><b>| KKR & KSR INSTITUTE OF TECHNOLOGY AND SCIENCES</b></h2>
<p><b> KITS was established in the year 2008, by GSR & KKR Educational Society in Vinjanampadu village of Guntur district by Sri.Koye Subba Rao, Chairman.
<br>   • KITS is approved by AICTE and accredited by NBA.
<br>   • KITS is Autonomous and affiliated to JNTU-Kakinada.
</b></p>

<br><b><h2>| VISION</h2></b>
<p><b>  To produce eminent and ethical Engineers and Managers for society by imparting quality professional education with emphasis on human values and holistic excellence. 
</b></p>

<br><b><h2>| MISSION</h2></b>
<p><b> • To incorporate benchmarked teaching and learning pedagogies in curriculum. 
<br>   • To ensure all round development of students through judicious blend of  curricular, co-curricular and extra-curricular activities.
<br>   • To support cross-cultural exchange of knowledge between industry and academy.
<br>   • To provide higher/continued education and research opportunities to the employees of the institution.
</b></p>

""")
        about_kits_details.setSizePolicy(self.sizePolicy2)
        about_kits_details.setAlignment(Qt.AlignmentFlag.AlignTop)
        about_kits_details.setWordWrap(True)
        about_kits_details.setStyleSheet(f""" font-size: {int(self.font_size)-7}pt; background-color: #fffafa ;border-image: url('Pics/clg_aerial.png'); color: #ff3030; padding: 10px; """)

        # Back Label
        back_label = QLabel("Press any button to open Menu")
        back_label.setSizePolicy(self.sizePolicy1)
        back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_label.setStyleSheet(f"font-size: {int(self.font_size)}pt; color: #ff5050 ; background-color: #101010 ; padding: 2px;")

        # Create vbox
        about_vbox = QVBoxLayout()
        about_vbox.addWidget(about_kits_head)
        about_vbox.addWidget(about_kits_details)
        about_vbox.addWidget(back_label)

        about_vbox.setSpacing(0)
        about_vbox.setContentsMargins(0,0,0,0)

        # Create ABOUT PAGE CONTAINER
        self.page_07 = QWidget()
        self.page_07.setLayout(about_vbox)

    def create_page_08(self):
        ''' Create and arrange widgets in PLACED NUMBER PAGE '''
        # Placements till Head
        self.placed_head = QLabel("Students Placed (2019-23 Batch)")
        self.placed_head.setSizePolicy(self.sizePolicy1)
        self.placed_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placed_head.setStyleSheet(f"font-size: {int(self.font_size)+5}pt; color: #e6f9ff ; background-color: #007399 ; padding: 2px;")
        self.placed_head.setWordWrap(True)

        # Number of placements
        self.number = QLabel("374")
        self.setPlacedNumber()
        #pn = self.number.text()
        pn = "374"
        try:
            if int(pn) < 250 :  pn = "250";
            if int(pn) > 500 :  pn = "500";
        except:
            pass
        self.number.setSizePolicy(self.sizePolicy2)
        self.number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number.setStyleSheet(f"""
                                        font-size: {pn}px;
                                        border-image: url('Pics/placements.png');
                                        background-position: center;
                                        background-repeat: no-repeat;
                                        background-color: #fff7ff;
                                        background-color: #e6f9ff;
                                        color: #007399;
                                        padding: 10px;
                                    """)
        
        # Create Main VBox
        placements_till_vbox = QVBoxLayout()
        placements_till_vbox.addWidget(self.placed_head)
        placements_till_vbox.addWidget(self.number)

        placements_till_vbox.setSpacing(0)
        placements_till_vbox.setContentsMargins(0,0,0,0)

        # Create PLACEMENTS TILL PAGE CONTAINER
        self.page_08 = QWidget()
        self.page_08.setLayout(placements_till_vbox)

    def create_page_09(self):
        ''' Create and arrange widgets in QUOTE PAGE '''
        ''' Create and arrange widgets in the QUOTE PAGE '''
        # Quote Head
        quote_head = QLabel(" Quote \n of the day ")
        quote_head.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        quote_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_head.setStyleSheet(f"font-size: 100px; border-image: url(Pics/quote.jpg); color: white ; background-color: purple ; padding: 10px; ")

        # Quote
        self.quote = QLabel(" Jennifer Lopez ")
        #self.setQuote()
        self.quote.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.quote.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.quote.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote.setStyleSheet(f" font-size: 50px; border-image: url(Pics/specials.png); background-color: #fff7ff; color: black; padding: 10px; ")
        self.quote.setWordWrap(True)
        
        # Create Main HBox
        quote_hbox = QHBoxLayout()
        quote_hbox.addWidget(quote_head)
        quote_hbox.addWidget(self.quote)

        quote_hbox.setSpacing(0)
        quote_hbox.setContentsMargins(0,0,0,0)

        # Create QUOTE PAGE CONTAINER
        self.page_09 = QWidget()
        self.page_09.setLayout(quote_hbox)

    def create_page_10(self):
        ''' Create and arrange widgets in SPECIALS PAGE '''
        # Special Head
        special_head = QLabel(" Special \n of the day ")
        special_head.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        special_head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        special_head.setStyleSheet("font-size: 100px; color: #e6ffee ; background-color: #00997a ; border-image: url(Pics/special.jpg); padding: 10px;")

        # Special
        self.special = QLabel("Special comes here")

        #self.setSpecials()
        self.special.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.special.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.special.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.special.setStyleSheet(" font-size: 50px; border-image: url(Pics/specials.png); background-color: #fff7ff; color: #004d3d; padding: 10px;")
        self.special.setWordWrap(True)
        
        # Create Main HBox
        special_hbox = QHBoxLayout()
        special_hbox.addWidget(special_head)
        special_hbox.addWidget(self.special)

        special_hbox.setSpacing(0)
        special_hbox.setContentsMargins(0,0,0,0)

        # Create SPECIALS PAGE CONTAINER
        self.page_10 = QWidget()
        self.page_10.setLayout(special_hbox)

    def create_page_11(self):
        ''' Create and arrange widgets in POSTERS PAGE '''
        # Find all image files in the "posters" folder
        self.image_files = [f for f in os.listdir("Posters") if f.endswith(".jpg") or f.endswith(".png")][:3]

        print(self.image_files)
        self.setPosters()
            
        self.page_11 = QWidget()
        self.page_11.setLayout(self.posters_vbox)

    def create_page_x(self):
        ''' LEFT FOR FUTURE DEVELOPMENT '''
        self.page_x = QWidget()
        pass

#######################################################################################
# Creation of Actions
#######################################################################################

    def createActions(self):
        ''' Create actions for the application '''

        # Intro action
        self.intro_act = QAction("&Intro")
        self.intro_act.setShortcut("i")
        self.intro_act.triggered.connect(self.showIntro)

        # Placements Till action
        self.placements_act = QAction("&Placements")
        self.placements_act.setShortcut("p")
        self.placements_act.triggered.connect(self.showPlacementsTill)

        # Quote action
        self.quote_act = QAction("&Quote")
        self.quote_act.setShortcut("q")
        self.quote_act.triggered.connect(self.showQuote)

        # Specials action
        self.specials_act = QAction("&Specials")
        self.specials_act.setShortcut("s")
        self.specials_act.triggered.connect(self.showSpecials)

#         # Posters action
#         self.posters_act = QAction("&Posters")
#         self.posters_act.setShortcut("e")
#         self.posters_act.triggered.connect(self.showPosters)
        
        # Exit action
        self.exit_act = QAction("&Close")
        self.exit_act.setShortcut("-")
        self.exit_act.triggered.connect(self.close)

#########################################################################################
# show() functions
#########################################################################################

    def showIntro(self):
        ''' Open intro '''
        self.main_stack.setCurrentIndex(0)

    def showMenu(self):
        ''' Open Menu '''
        self.main_stack.setCurrentIndex(1)

    def showMap(self):
        ''' Open Map '''
        self.main_stack.setCurrentIndex(2)

    def showUpdates(self):
        ''' Open Updates '''
        self.main_stack.setCurrentIndex(3)

    def showEvents(self):
        ''' Open Events '''
        self.main_stack.setCurrentIndex(4)

    def showNotices(self):
        ''' Open Notices '''
        self.main_stack.setCurrentIndex(5)

    def showPlacementsUpdates(self):
        ''' Open Placements Updates '''
        self.main_stack.setCurrentIndex(6)

    def showAbout(self):
        ''' Open About '''
        self.main_stack.setCurrentIndex(7)

    def showPlacementsTill(self):
        ''' Open Placements Till '''
        self.main_stack.setCurrentIndex(8)

    def showQuote(self):
        ''' Open Quote '''
        self.main_stack.setCurrentIndex(9)

    def showSpecials(self):
        ''' Open Specials '''
        self.main_stack.setCurrentIndex(10)

    def showPosters(self):
        ''' Open Posters '''
        self.main_stack.setCurrentIndex(11)

########################################################################################
# Update Labels
########################################################################################

    def setTop(self):
        ''' Updating Top '''
        with open("rss/top.txt",'r') as f:
            text = f.read()
            text = text + '\t\t' + text
            self.top_label.setText(text)
            
    def setIntro(self):
        ''' Update Time '''
        text = " ECE Dept. presents... \n\n AI-Powered Notice Board! "
        now = datetime.datetime.now()
        ts = now.strftime("%I:%M %p")
        
        self.intro_label.setText(text+'\n\n'+ts)

    def setUpdates(self):
        ''' Updating Updates '''
        with open("rss/updates.txt",'r') as f:
            text = f.read()
            self.updates.setText(text)

    def setEvents(self):
        ''' Updating Events '''
        with open("rss/events.txt",'r') as f:
            text = f.read()
            self.events.setText(text)

    def setNotices(self):
        ''' Updating Notices '''
        with open("rss/notices.txt",'r') as f:
            text = f.read()
            self.notices.setText(text)

    def setPlacementsInfo(self):
        ''' Updating Placements data '''
        with open("rss/placements.txt",'r') as f:
            text = f.read()
            self.placements.setText(text)
            #print(text)

    def setPlacedNumber(self):
        ''' Updating Placements number '''
        with open("rss/placed.txt",'r') as f:
            text = f.read().split('\n')
            print(text)
            batch, num = text[0], text[1]
            self.placed_head.setText("Students Placed ({})".format(batch))
            self.number.setText(num)

    def setQuote(self):
        ''' Updating Quote '''
        with open("rss/quote.txt",'r') as f:
            text = f.read()
            self.quote.setText(text)

    def setSpecials(self):
        ''' Updating Special '''
        with open("rss/special.txt",'r') as f:
            text = f.read()
            self.special.setText(text)

    def setPosters(self):
        ''' Updating Posters '''
        # Create Stacked Layout
        self.poster_stack = QStackedLayout()
        
        # Find all image files in the "posters" folder
        self.image_files = [f for f in os.listdir("Posters") if f.endswith(".jpg") or f.endswith(".png")][:3]

        # Create a page for each image
        for image_file in self.image_files:
            image_path = "Posters/"+image_file
            label = QLabel()
            #pixmap = QPixmap(image_path)
            #label.setPixmap(pixmap)
            #label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            #print(label.width(), label.height())
            label.setStyleSheet(" border-image: url({}); ".format(image_path))
            self.poster_stack.addWidget(label)

        self.toggle_button = QPushButton("Toggler")
        self.toggle_button.setStyleSheet("background-color: black")
        self.toggle_button.clicked.connect(self.toggle)
        self.posters_vbox = QVBoxLayout()
        self.posters_vbox.addLayout(self.poster_stack)
        self.posters_vbox.addWidget(self.toggle_button)

        print(" all set ")

    def toggle(self):
        index = self.poster_stack.currentIndex()
        print(index,len(self.image_files))
        try:
            if index < len(self.image_files)-1:
                index += 1
                self.poster_stack.setCurrentIndex(index)
            else:
                index = 0
                self.poster_stack.setCurrentIndex(index)
        except e:
            print(e)

        print("updated index: ",index)


########################################################################################
# Update Labels
########################################################################################

    def update_labels(self):
        ''' Update the data '''
        try:
            self.setIntro()
            self.setUpdates()
            self.setEvents()
            self.setNotices()
            self.setPlacementsInfo()
            self.setPlacedNumber()
            self.setQuote()
            self.setSpecials()
            
        except Exception as e:
            print(f'Error in update_labels: {e}')



########################################################################################
# Play Contents
########################################################################################

    def play(self):
        ''' Play Playlist '''
        self.setTop()
        
        self.playlist = [0,3,4,8,9,10,0]
        self.main_stack.setCurrentIndex(self.playlist[self.index])
        print('Index set to',self.main_stack.currentIndex())

        self.index+=1
        if self.index == 7:
            self.index = 0
            self.showIntro()
            

########################################################################################
# Key Press Event
########################################################################################

    def keyPressEvent(self,event):
        ''' Open Menu Page if any key press is detected '''
        key = event.key()
        print(key,'key pressed')
        self.main_stack.setCurrentIndex(1)
        self.timer2.stop()
        QTimer.singleShot(30000, self.timer2.start)  # 30 seconds
        super().keyPressEvent(event)
        

########################################################################################
# Close Event
########################################################################################

    def closeEvent(self,event):
        ''' Close Event '''
        self.top_label.timer.stop()
        self.timer.stop()
        self.timer2.stop()

        self.updater.terminate()
        self.updater.communicate()

        self.bgm.terminate()
        self.bgm.communicate()

        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = XBoard()
    sys.exit(app.exec())
