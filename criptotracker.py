import csv
import sys
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QTime
import requests
from threading import Timer
import sqlite3 as sql


class mainWindow(QMainWindow):
    """this class defines the constructor for the mainWindow class."""
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.show()
        self.deleteDatabase()
        self.updatePrice()
        self.dataBaseCreation()
        self.userInputPrice()
        self.pushBotton()
        self.comparePrice()
        
    
        
   
  
    def closeEvent(self, event):
        """This method is called when the window is closed."""
        self.timer.cancel()
        event.accept()
   
    def updatePrice(self):
        """This method is updating every 5 seconds."""
        self.label_price.setText(self.getPrice())
        self.label_updated.setText(self.updatedAt())
        with open('crypto.csv', 'a') as csvfile:
            fieldnames = ['Price', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Price': self.getPrice(), 'Time': self.updatedAt()})
            # writer.writerow({'Price': self.getPrice()})
        self.timer = Timer(5, self.updatePrice)
        self.timer.start()
        
    def getPrice(self):
            """This method is getting the price from the API; and returns the price in €"""
            api = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
            requestResponse = requests.get(api).json()
            price = requestResponse['EUR']
            return f'{price}' 
        
    def updatedAt(self):
        """This method is getting the time from the API; and returns the time in the format HH:MM:SS"""
        time = datetime.now().strftime('%H:%M:%S')
        return "Updated at: " f'{time}' 
    
    # Crea una base de datos sqlite con un valor llamado "desired_price" que es un float
    def dataBaseCreation(self):
        """This function create a database with the name "desired_price"."""
        conn = sql.connect('database.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS desired_price (desired_price FLOAT)")
        conn.commit()
        conn.close()
    
    def userInputPrice(self):
        user_value = self.textInput.toPlainText()
        conn = sql.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM desired_price")
        c.execute("INSERT INTO desired_price VALUES (?)", (user_value,))
        conn.commit()
        conn.close()
        self.textInput.clear()
        return user_value
    
    def pushBotton(self):
        self.pushButton.clicked.connect(self.userInputPrice)
        print(self.userInputPrice())
    
    
    
    def comparePrice(self):
        conn = sql.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM desired_price")
        desired_price = c.fetchone()[0]

        if desired_price >= self.getPrice():
            print("yes", self.getPrice())
        else:
            print("no", self.getPrice())
            
        conn.commit()
        conn.close()
    
    def deleteDatabase(self):
        conn = sql.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM desired_price")
        conn.commit()
        conn.close()
        
    
      
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())