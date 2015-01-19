from gi.repository import Gtk, Gio
from decimal import *
import os.path, sys 
import sqlite3 as lite

class Data():
    # Create Database if none exists
    if(os.path.isfile('budget.db') == False):
        try:
            con = lite.connect('budget.db')

            cur = con.cursor()
            cur.execute('create table menu(type VARCHAR(30), name VARCHAR(50), menuOrder INT, menuID INT PRIMARY KEY);')
            cur.execute('create table transactions(menuID INT, year INT, month INT, day INT, value REAL, description VARCHAR(100), transactionsID INT PRIMARY KEY);')
                           
            data = cur.fetchone()

        except (lite.Error, e): 
            print("Error %s:" % e.args[0])
            sys.exit(1)

        finally:
            if con:
               con.close()

    # Menu Indexes
    MENU_TYPE_INDEX = 0
    MENU_NAME_INDEX = 1
    MENU_ORDER_INDEX = 2
    MENU_ID_INDEX = 3

    # Transactions Indexes
    TRANSACTION_MENU_INDEX = 0
    TRANSACTION_MENU_ID_INDEX = 0
    TRANSACTION_MENU_NAME_INDEX = 1

    TRANSACTION_DATE_INDEX = 1
    TRANSACTION_DATE_YEAR_INDEX = 0
    TRANSACTION_DATE_MONTH_INDEX = 1
    TRANSACTION_DATE_DAY_INDEX = 2

    TRANSACTION_VALUE_INDEX = 2
    TRANSACTION_DESCRIPTION_INDEX = 3
    TRANSACTION_ID_INDEX = 4

    LATEST_MENU_ID = 0
    LATEST_ID = 0

    def __init__(self):
        #Indexes for data arrays

        self.transactionsMenu = []
        self.transactions = []
        self.yearMenu = []

        self.transaction_view = 0
        self.overview = 0
        
        self.allMonthMenu = [[0, "All"],
                            [1, "January"],
                            [2, "February"],
                            [3, "March"],
                            [4, "April"],
                            [5, "May"],
                            [6, "June"],
                            [7, "July"],
                            [8, "August"],
                            [9, "September"],
                            [10, "October"],
                            [11, "November"],
                            [12, "December"],
                            ]

    def add_category(self, menuType, category):
        self.LATEST_MENU_ID += 1
        if(os.path.isfile('budget.db')):
            con = lite.connect('budget.db')
            row = [(str(menuType),str(category),"10",str(self.LATEST_MENU_ID))]
        
            cur = con.cursor()
            cur.execute('INSERT INTO menu VALUES(?,?,?,?)', row[0])
            con.commit()

            self.transactionsMenu = []
            self.transactions = []
            
            # Refresh data and views
            self.import_data()
            self.transaction_view.generate_sidebars()
            self.transaction_view.display_content()
            self.overview.redisplay_info()
    
    def add_data(self, category, year, month, day, value, description, transactionID):
        for i in range(0,len(self.transactionsMenu)):
            if category == self.transactionsMenu[i][self.MENU_NAME_INDEX]:
                category = self.transactionsMenu[i][self.MENU_ID_INDEX]

        if(os.path.isfile('budget.db')):
            con = lite.connect('budget.db')
            row = [(str(category),str(year),str(month),str(day),str(value),str(description),str(transactionID))]
        
            cur = con.cursor()
            cur.execute('INSERT INTO transactions VALUES(?,?,?,?,?,?,?)', row[0])
            con.commit()

            self.transactionsMenu = []
            self.transactions = []
            
            # Refresh data and views
            self.import_data()
            self.transaction_view.generate_sidebars()
            self.transaction_view.display_content()
            self.overview.redisplay_info()

    def connect_data_views(self, transaction_view, overview):
        self.transaction_view = transaction_view
        self.overview = overview

    def delete_category(self, uniqueID):
        if(os.path.isfile('budget.db')):
            con = lite.connect('budget.db')
        
            cur = con.cursor()
            cur.execute('SELECT type FROM menu WHERE menuID = '+ str(uniqueID))
            row = cur.fetchone()
            if row[0] == "income":
                cur.execute('UPDATE transactions SET menuID = -1 WHERE menuID = ' + str(uniqueID))
            elif row[0] == "expense":
                cur.execute('UPDATE transactions SET menuID = -2 WHERE menuID = ' + str(uniqueID))
            cur.execute('delete from menu where menuID = ' + str(uniqueID))
            con.commit()
                
            self.transactionsMenu = []
            self.transactions = []
            
            # Refresh data and views
            self.import_data()
            self.transaction_view.generate_sidebars()
            self.transaction_view.display_content()
            self.overview.redisplay_info()
    
    def delete_data(self, uniqueID):
        if(os.path.isfile('budget.db')):
            con = lite.connect('budget.db')
            cur = con.cursor()
            cur.execute('DELETE FROM transactions WHERE transactionsID = ' + str(uniqueID))
            con.commit()

            self.transactionsMenu = []
            self.transactions = []
            
            # Refresh data and views
            self.import_data()
            self.transaction_view.generate_sidebars()
            self.transaction_view.display_content()
            self.overview.redisplay_info()
    
    def edit_category(self, uniqueID, newLabel):
        if(os.path.isfile('budget.db')):
            con = lite.connect('budget.db')
            row = [(str(newLabel),str(uniqueID))]
        
            cur = con.cursor()
            cur.execute('UPDATE menu SET name = ? WHERE menuID = ?', row[0])
            con.commit()

            self.transactionsMenu = []
            self.transactions = []
            
            # Refresh data and views
            self.import_data()
            self.transaction_view.generate_sidebars()
            self.transaction_view.display_content()
            self.overview.redisplay_info()

    def import_data(self):
        
        if(os.path.isfile('budget.db')):
            con = lite.connect('budget.db')

            cur = con.cursor()
            cur.execute('SELECT * FROM menu;')
            rows = cur.fetchall()
            for row in rows:
                self.arr = []
                self.arr.append(row[0].strip())             # Type
                self.arr.append(row[1].strip())             # Name
                self.arr.append(row[2])                     # Order
                self.arr.append(row[3])                     # menuID
                if self.LATEST_MENU_ID < row[3]:
                    self.LATEST_MENU_ID = row[3]
                self.transactionsMenu.append(self.arr)
            
            cur.execute('SELECT * FROM transactions;')    
            rows = cur.fetchall()
            for row in rows:
                self.arr = []
                self.catArr = []
                self.dateArr = []
                self.catArr.append(row[0])                  # menuID
                for i in range(0, len(self.transactionsMenu)):
                    if row[0] == self.transactionsMenu[i][3]:
                        self.catArr.append(self.transactionsMenu[i][1])     # Name
                self.dateArr.append(row[1])                 # year
                self.dateArr.append(row[2])                 # month
                self.dateArr.append(row[3])                 # day
                self.arr.append(self.catArr)
                self.arr.append(self.dateArr)
                self.arr.append(row[4])                     # Value
                self.arr.append(row[5].strip())             # Description
                self.arr.append(row[6])                     # transactionID
                if self.LATEST_ID < row[6]:
                    self.LATEST_ID = row[6]
                self.sort_data(self.transactions, self.arr)
            
            cur = con.cursor()
            cur.execute('SELECT DISTINCT year FROM transactions ORDER BY year DESC;') 
            rows = cur.fetchall()
            
            self.yearMenu.append("All")
            for row in rows:
                self.yearMenu.append(str(row[0]))

    def sort_data(self, data, arr):
        if len(data) == 0:
            data.append(arr)
        else:
            flag = False
            for i in range(len(data)):
                # If entry's year is equal to array's year
                if data[i][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_YEAR_INDEX] == int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_YEAR_INDEX]):
                    # If entry's month is equal to array's month
                    if data[i][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX]):
                        # If entry's day is equal to array's day
                        if data[i][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX]):
                            data.insert(i, arr)
                            flag = True
                            break
                        # If entry's day is less than array's day
                        elif data[i][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] > int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX]):
                            for j in range(i, len(data)):
                                if data[j][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX]):
                                    if data[j][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] <= int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX]):
                                        data.insert(j, arr)
                                        flag = True
                                        break
                                else:
                                    data.insert(j , arr)
                                    flag = True
                                    break
                            break
                        # If entry's day is greater than array's day
                        elif data[i][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] < int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX]):
                            data.insert(i , arr)
                            flag = True
                            break
                    # If entry's month is less than array's month
                    elif data[i][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] < int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX]):
                        data.insert(i , arr)
                        flag = True
                        break
                # If entry's year is less than income array's year
                elif data[i][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_YEAR_INDEX] < int(arr[self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_YEAR_INDEX]):
                    data.insert(i , arr)
                    flag = True
                    break

            if flag == False:
                data.append(arr)
           
    def translate_date(self,data,index):
        dateString = ""
        
        if index == "edit":
            if data[1] == 0:
                dateString += ("January")
            elif data[1] == 1:
                dateString += ("February")
            elif data[1] == 2:
                dateString += ("March")
            elif data[1] == 3:
                dateString += ("April")
            elif data[1] == 4:
                dateString += ("May")
            elif data[1] == 5:
                dateString += ("June")
            elif data[1] == 6:
                dateString += ("July")
            elif data[1] == 7:
                dateString += ("August")
            elif data[1] == 8:
                dateString += ("September")
            elif data[1] == 9:
                dateString += ("October")
            elif data[1] == 10:
                dateString += ("November")
            elif data[1] == 11:
                dateString += ("December")
            else:
                dateString += ("Month Fail")
            
            dateString += (" " + str(data[2]))

            if data[2] == 1:
                dateString += ("st")
            elif data[2] == 21:
                dateString += ("st")
            elif data[2] == 31:
                dateString += ("st")
            elif data[2] == 2:
                dateString += ("nd")
            elif data[2] == 22:
                dateString += ("nd")
            elif data[2] == 3:
                dateString += ("rd")
            elif data[2] == 23:
                dateString += ("rd")
            else:
                dateString += ("th")
            
            dateString += ", "
            dateString += str(data[0])
        
        elif index == "month":
            if data == "January":
                dateString = 1
            elif data == "February":
                dateString = 2
            elif data == "March":
                dateString = 3
            elif data == "April":
                dateString = 4
            elif data == "May":
                dateString = 5
            elif data == "June":
                dateString = 6
            elif data == "July":
                dateString = 7
            elif data == "August":
                dateString = 8
            elif data == "September":
                dateString = 9
            elif data == "October":
                dateString = 10
            elif data == "November":
                dateString = 11
            elif data == "December":
                dateString  = 12
            else:
                dateString = ("Month Fail")
            
        else:
            if data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 1:
                dateString += ("January")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 2:
                dateString += ("February")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 3:
                dateString += ("March")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 4:
                dateString += ("April")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 5:
                dateString += ("May")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 6:
                dateString += ("June")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 7:
                dateString += ("July")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 8:
                dateString += ("August")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 9:
                dateString += ("September")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 10:
                dateString += ("October")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 11:
                dateString += ("November")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_MONTH_INDEX] == 12:
                dateString += ("December")
            else:
                dateString += ("Month Fail")

            dateString += (" " + str(data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX]))

            if data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == 1:
                dateString += ("st")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == 21:
                dateString += ("st")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == 31:
                dateString += ("st")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == 2:
                dateString += ("nd")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == 22:
                dateString += ("nd")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == 3:
                dateString += ("rd")
            elif data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_DAY_INDEX] == 23:
                dateString += ("rd")
            else:
                dateString += ("th")

            dateString += ", "
            dateString += str(data[index][self.TRANSACTION_DATE_INDEX][self.TRANSACTION_DATE_YEAR_INDEX])
                
        return dateString
    
    def update_data(self, category, year, month, day, value, description, transactionID):
        for i in range(0,len(self.transactionsMenu)):
            if category == self.transactionsMenu[i][self.MENU_NAME_INDEX]:
                category = self.transactionsMenu[i][self.MENU_ID_INDEX]

        if(os.path.isfile('budget.db')):
            con = lite.connect('budget.db')
            row = [(str(category),str(year),str(month),str(day),str(value),str(description),str(transactionID))]
        
            cur = con.cursor()
            cur.execute('update transactions set menuID = ?, year = ?, month = ?, day = ?, value = ?, description = ? where transactionsID = ?', row[0])
            con.commit()

            self.transactionsMenu = []
            self.transactions = []
            
            # Refresh data and views
            self.import_data()
            self.transaction_view.generate_sidebars()
            self.transaction_view.display_content()
            self.overview.redisplay_info()
    

