def load_stylesheet():

    return """
/* ==========================================================
   GLOBAL
========================================================== */

QWidget{
    color: white;
    font-family: "Segoe UI";
    font-size: 12px;
}

QMainWindow{
    background: #1E1E1E;
}

QStatusBar{
    background: #252526;
    color: white;
}


/* ==========================================================
   PAGE
========================================================== */

QWidget#DashboardPage,
QWidget#CameraPage,
QWidget#SensorPage,
QWidget#ControlPage,
QWidget#SettingsPage{
    background: #1E1E1E;
}


/* ==========================================================
   CARD
========================================================== */

QFrame#Card{
    background: #2D2D30;
    border: 1px solid #3E3E42;
    border-radius: 12px;
}


/* ==========================================================
   LABEL
========================================================== */

QLabel#TitleLabel{
    font-size: 18px;
    font-weight: bold;
}

QLabel#Logo{
    font-size: 24px;
    font-weight: bold;
    color: white;
}

QLabel#Subtitle{
    color: #B0B0B0;
    font-size: 11px;
}


/* ==========================================================
   BUTTON
========================================================== */

QPushButton#PrimaryButton{
    background: #0A84FF;
    border: none;
    border-radius: 8px;
    color: white;
    padding: 8px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#PrimaryButton:hover{
    background: #2894FF;
}

QPushButton#PrimaryButton:pressed{
    background: #0064D2;
}


/* ==========================================================
   STATUS BADGE
========================================================== */

QLabel#StatusOnline{
    background: #1B5E20;
    color: white;
    border-radius: 10px;
    padding: 5px 10px;
}

QLabel#StatusOffline{
    background: #8B0000;
    color: white;
    border-radius: 10px;
    padding: 5px 10px;
}


/* ==========================================================
   SIDEBAR
========================================================== */

QWidget#Sidebar{
    background: #252932;
    border-right: 1px solid #3B4252;
}

QPushButton#SidebarButton{

    background:transparent;

    border:none;

    border-radius:12px;

    color:white;

    text-align:left;

    padding:14px 16px;

    font-size:13px;

    font-weight:600;

}

QPushButton#SidebarButton:hover{

    background:#313844;

}

QPushButton#SidebarButton:checked{

    background:#0A84FF;

}

QPushButton#SidebarButton::icon{

    padding-left:10px;

}


/* ==========================================================
   CONNECTION PANEL
========================================================== */

QWidget#ConnectionPanel{
    background: #2F3542;
    border: 1px solid #404654;
    border-radius: 12px;
}

QLabel#ConnectionTitle{
    font-size: 15px;
    font-weight: bold;
}

QLabel#ConnectionStatus{
    color: #E74C3C;
    font-weight: bold;
}


/* ==========================================================
   INPUT
========================================================== */

QComboBox{
    background: #252932;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 6px;
    color: white;
}

QComboBox::drop-down{
    border: none;
}

QComboBox QAbstractItemView{
    background: #252932;
    color: white;
    selection-background-color: #0A84FF;
}


/* ==========================================================
   SCROLLBAR
========================================================== */

QScrollBar:vertical{
    background: #252932;
    width: 10px;
    border: none;
}

QScrollBar::handle:vertical{
    background: #4A4F5A;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover{
    background: #5E6573;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical{
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical{
    background: transparent;
}

QLabel#CardTitle{

    font-size:15px;

    font-weight:bold;

    color:white;

    padding-bottom:8px;

}

/* ==========================================================
   TOOLBAR BUTTON
========================================================== */

QPushButton#ToolbarButton{
    background:#2F3542;
    border:1px solid #404654;
    border-radius:8px;
    color:white;
    padding:8px;
    font-size:13px;
    font-weight:bold;
}

QPushButton#ToolbarButton:hover{
    background:#3A4252;
}

QPushButton#ToolbarButton:pressed{
    background:#20242C;
}
"""