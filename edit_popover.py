from gi.repository import Gtk, Gio, Gdk
from overview_menu import Overview_Menu

class Edit_Popover(Gtk.Window):

    def __init__(self, data):
        # Content Grid
        self.CONTENT_GRID_INDEX = 0          # Array
        self.LAYOUT_GRID_INDEX = 0           # Element
        self.WHITESPACE_LABEL = 1            # Element

        # Layout Widgets
        self.LAYOUT_WIDGET_INDEX = 1         # Array
        self.CATEGORY_LABEL_INDEX = 0        # Element
        self.DATE_LABEL_INDEX = 1            # Element
        self.CURRENCY_LABEL_INDEX = 2        # Element
        self.COST_LABEL_INDEX = 3            # Element
        self.DESCRIPTION_LABEL_INDEX = 4     # Element
        
        # Additional Items
        self.ENTRY_GRID_INDEX = 2            # Element
        self.COST_GRID_INDEX = 3             # Element
        self.UNIQUE_ID_INDEX = 4             # Element
        
        #Initialize Data
        self.unique_id = 0
        self.entryRows = 0
        self.menu = 0
        # Create Widgets
        self.editGrid = Gtk.Grid()
        
        self.editButton = Gtk.Button("Edit")
        self.deleteButton = Gtk.Button("Delete")
        self.selectorBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        # Style Widgets
        self.editButton.set_size_request(100,32)
        self.deleteButton.set_size_request(100,32)
        Gtk.StyleContext.add_class(self.selectorBox.get_style_context(), "linked")
        self.selectorBox.set_margin_start(5)
        self.selectorBox.set_margin_top(5)
        self.selectorBox.set_margin_bottom(5)

        # Connect Widget Handlers
        self.editButton.connect("clicked", self.on_editButton_clicked)

        # Add Widgets to Grid
        self.selectorBox.add(self.editButton)
        self.selectorBox.add(self.deleteButton)
        
        self.editGrid.attach(self.selectorBox,0,0,1,1)

    def margin(self, widget, margin):
        widget.set_margin_start(margin)
        widget.set_margin_top(margin)
        widget.set_margin_bottom(margin)
    
    def on_editDropdown_clicked(self, button, editPopover, unique_id, entryRows, menu):
        if editPopover.get_visible():
            editPopover.hide()
        else:
            editPopover.show_all()
        self.unique_id = unique_id
        self.entryRows = entryRows
        self.menu = menu

    def on_editButton_clicked(self, *args):
        # Create editing widgets
        self.categoryComboBoxText = Gtk.ComboBoxText()
        self.costEntry = Gtk.Entry()
                
        self.calendar = Gtk.Calendar()
        self.calendarButton = Gtk.Button()
        self.calendarPopover = Gtk.Popover.new(self.calendarButton)
        self.calendarPopover.add(self.calendar)
        self.calendarButton.connect("clicked", self.on_calendarDropdown_clicked, self.calendarPopover)

        #Style Editing Widgets
        self.categoryComboBoxText.set_margin_start(5)
        self.categoryComboBoxText.set_margin_top(8)
        self.categoryComboBoxText.set_margin_bottom(8)
        
        self.calendarButton.set_margin_start(5)
        self.calendarButton.set_margin_top(8)
        self.calendarButton.set_margin_bottom(8)
        self.calendarButton.set_margin_end(5)

        self.costEntry.set_width_chars(5)
        self.costEntry.set_alignment(1)
        self.costEntry.set_margin_start(5)
        self.costEntry.set_margin_top(8)
        self.costEntry.set_margin_bottom(8)
        
        # Replace label widgets with editing widgets
        for i in range(0, len(self.entryRows)):
            if self.entryRows[i][self.UNIQUE_ID_INDEX] == self.unique_id:
                for j in range(1,len(self.menu)):
                    self.categoryComboBoxText.append_text(self.menu[j][1])
                    if self.menu[j][1] == self.entryRows[i][self.LAYOUT_WIDGET_INDEX][self.CATEGORY_LABEL_INDEX].get_text():
                        self.categoryComboBoxText.set_active(j-1)
                
                # Category
                self.entryRows[i][self.LAYOUT_WIDGET_INDEX][self.CATEGORY_LABEL_INDEX].hide()
                self.entryRows[i][self.ENTRY_GRID_INDEX].attach(self.categoryComboBoxText,0,1,1,1)
                self.categoryComboBoxText.show()
                
                # Date
                
                self.entryRows[i][self.LAYOUT_WIDGET_INDEX][self.DATE_LABEL_INDEX].hide()
                self.entryRows[i][self.ENTRY_GRID_INDEX].attach(self.calendarButton,1,1,1,1)
                self.calendarButton.set_label(self.entryRows[i][self.LAYOUT_WIDGET_INDEX][self.DATE_LABEL_INDEX].get_text())
                self.calendarButton.show()
                
                # Cost
                self.entryRows[i][self.LAYOUT_WIDGET_INDEX][self.COST_LABEL_INDEX].hide()
                self.entryRows[i][self.COST_GRID_INDEX].attach(self.costEntry,1,0,1,1)
                self.costEntry.set_text(self.entryRows[i][self.LAYOUT_WIDGET_INDEX][self.COST_LABEL_INDEX].get_text())
                self.costEntry.show()
                # Description
    
    def on_calendarDropdown_clicked(self, button, calendarPopover):
        if calendarPopover.get_visible():
            calendarPopover.hide()
        else:
            calendarPopover.show_all()

