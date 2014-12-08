from gi.repository import Gtk, Gio, Gdk
from sidebar import Sidebar
from calc import Calc

class Income():

    def __init__(self, data):
        # Define Sidebar Menu
        self.data = data 
        self.calc = Calc(self.data)
        self.view = Sidebar(self.data) 

        self.view.generate_sidebars(self.data.incomeMenu)
        self.view.display_content(self.data.income, self.data.incomeMenu)

        # Add Signal Handling
        self.view.menuListBox.connect("row-selected",self.view.menu_clicked, self.data.income, self.data.incomeMenu)
        self.view.subMenuListBox.connect("row-selected",self.view.subMenu_clicked, self.data.income, self.data.incomeMenu)
