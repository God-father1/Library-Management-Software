from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import MySQLdb

ui,_ = loadUiType('library.ui')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Ui_Changes()
        self.Handel_Buttons()
        self.Show_Category()
        self.Show_Author()
        self.Show_Publisher()
        self.Show_Publisher_Combobox()
        self.Show_Category_Combobox()
        self.Show_Author_Combobox()

    def Handel_Ui_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Buttons(self):
        self.pushButton_5.clicked.connect(self.Show_Themes)
        self.pushButton_21.clicked.connect(self.Hiding_Themes)
        self.pushButton.clicked.connect(self.Open_day_to_day)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_27.clicked.connect(self.Open_Client_Tab)
        self.pushButton_3.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Setting_Tab)
        self.pushButton_7.clicked.connect(self.Add_New_Books)
        self.pushButton_9.clicked.connect(self.Delete_Books)
        self.pushButton_10.clicked.connect(self.Search_Books)
        self.pushButton_14.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_16.clicked.connect(self.Add_Publisher)
        self.pushButton_8.clicked.connect(self.Edit_Books)
        self.pushButton_9.clicked.connect(self.Delete_Books)
        self.pushButton_11.clicked.connect(self.Add_New_user)
        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_13.clicked.connect(self.Edit_User)

        self.pushButton_22.clicked.connect(self.Dark_Blue)
        self.pushButton_17.clicked.connect(self.Clasic)
        self.pushButton_18.clicked.connect(self.Orange)
        self.pushButton_19.clicked.connect(self.Dark_Orange)
        self.pushButton_20.clicked.connect(self.Light)

    def Show_Themes(self):
        self.groupBox_3.show()

    def Hiding_Themes(self):
        self.groupBox_3.hide()



############### Opening tabs #########################
    def Open_day_to_day(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Client_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Setting_Tab(self):
        self.tabWidget.setCurrentIndex(4)



####################### Books ###########################

    def Add_New_Books(self):

        ####    connecting to database #####
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        ####### Geting Values############

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_5.currentIndex()
        book_author = self.comboBox_4.currentIndex()
        book_publisher = self.comboBox_3.currentIndex()
        book_price = self.lineEdit_5.text()

        self.cur.execute('''INSERT INTO book (book_name, book_description, book_code, book_category, book_author, book_publisher, book_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)''',(book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))

        self.db.commit()

        self.lineEdit_2.setText('')
        self.textEdit_2.setPlainText('')
        self.lineEdit_3.setText('')
        self.lineEdit_5.setText('')
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)

        self.statusBar().showMessage('New Book Added !')




    def Search_Books(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        book_title =self.lineEdit_8.text()
        sql = ''' SELECT * FROM book WHERE book_name = %s'''
        self.cur.execute(sql, [(book_title)])

        data = self.cur.fetchone()
        print(data)
        self.lineEdit_7.setText(data[0])
        self.lineEdit_4.setText(str(data[2]))
        self.textEdit.setPlainText(data[1])
        self.comboBox_7.setCurrentIndex(data[3])
        self.comboBox_8.setCurrentIndex(data[4])
        self.comboBox_6.setCurrentIndex(data[5])
        self.lineEdit_6.setText(str(data[6]))



    def Delete_Books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_7.text()

        warning = QMessageBox.warning(self , "Delete Book" , "Are you sure you want to DELETE this book?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql= ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql,[(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted Successfully !')
            

    def Edit_Books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_7.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_4.text()
        book_category = self.comboBox_7.currentIndex()
        book_author = self.comboBox_8.currentIndex()
        book_publisher = self.comboBox_6.currentIndex()
        book_price = self.lineEdit_6.text()
        search_book_title= self.lineEdit_8.text()

        self.cur.execute('''
        UPDATE book SET book_name = %s ,book_description=%s, book_code=%s, book_category=%s, book_author=%s, book_publisher=%s, book_price=%s WHERE book_name=%s
        ''',(book_title, book_description, book_code, book_category, book_author, book_publisher, book_price, search_book_title))

        self.db.commit()
        self.lineEdit_8.setText('')
        self.statusBar().showMessage('Details Edited Sucessfully !')


##################  users   ######################


    def Add_New_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        username =self.lineEdit_9.text()
        email = self.lineEdit_13.text()
        password = self.lineEdit_11.text()
        password2 =  self.lineEdit_12.text()

        if password2 == password:
            self.cur.execute('''
            INSERT INTO users(user_name, user_email,user_password) VALUES (%s, %s, %s)''', (username, email, password ))

            self.db.commit()

            self.statusBar().showMessage('User Added Sucessfully !')
        else:
            self.label_31.setText('Password mismatch ! Please retype password.')




    def Edit_User(self):


        username = self.lineEdit_17.text()
        email = self.lineEdit_15.text()
        password = self.lineEdit_18.text()
        password2 = self.lineEdit_16.text()
        originalname = self.lineEdit_10.text()

        if password2 == password:
            self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
            self.cur = self.db.cursor()
            self.cur.execute('''
            UPDATE users SET user_name = %s, user_email = %s, user_password = %s WHERE user_name=%s''',(username,email,password,originalname))
            self.db.commit()
            self.statusBar().showMessage('User Details Edited Sucessfully !')
        else:
            self.label_32.setText('Make sure you have entered correct password again !')

    def Login(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        username= self.lineEdit_10.text()
        password=self.lineEdit_14.text()
        sql= '''SELECT * FROM users'''
        self.cur.execute(sql)
        data=self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                self.statusBar().showMessage('User Identification Successfull !')
                self.groupBox_4.setEnabled(True)
                self.lineEdit_17.setText(row[1])
                self.lineEdit_15.setText(row[2])


#################setting #######################

    def Add_Category(self):


        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_19.text()

        self.cur.execute(''' INSERT INTO category (category_name) VALUES (%s) ''', (category_name,))

        self.db.commit()
        self.lineEdit_19.setText('')
        self.Show_Category()
        self.Show_Category_Combobox()
        self.statusBar().showMessage('New Category Added ! ')


    def Show_Category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT category_name FROM category ''')
        data = self.cur.fetchall()
        
        #print(data)

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_2.setItem(row , column, QTableWidgetItem(str(item)))
                    column+=1

                row_position = self.tableWidget_2.rowCount() 
                self.tableWidget_2.insertRow(row_position)           


    def Add_Author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_20.text()

        self.cur.execute(''' INSERT INTO authors (author_name) VALUES (%s) ''', (author_name,))

        self.db.commit()
        self.lineEdit_20.setText('')
        self.Show_Author()
        self.Show_Author_Combobox()
        self.statusBar().showMessage('New Author Added ! ')



    def Show_Author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT author_name FROM authors ''')
        data = self.cur.fetchall()
        
        #print(data)

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_3.setItem(row , column, QTableWidgetItem(str(item)))
                    column+=1

                row_position = self.tableWidget_3.rowCount() 
                self.tableWidget_3.insertRow(row_position)  

        

    def Add_Publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_21.text()

        self.cur.execute(''' INSERT INTO publisher (publisher_name) VALUES (%s) ''', (publisher_name,))

        self.db.commit()
        self.lineEdit_21.setText('')
        self.Show_Publisher()
        self.Show_Publisher_Combobox()
        self.statusBar().showMessage('New Publisher Added ! ')



    def Show_Publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()
        
        #print(data)

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_4.setItem(row , column, QTableWidgetItem(str(item)))
                    column+=1

                row_position = self.tableWidget_4.rowCount() 
                self.tableWidget_4.insertRow(row_position)  



############### FEtching Data from DB  to Combo box ################################


    def Show_Category_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT category_name FROM category ''')
        data = self.cur.fetchall()
        self.comboBox_5.clear()
        self.comboBox_7.clear()
        for category in data:
            
            self.comboBox_5.addItem(category[0])
            self.comboBox_7.addItem(category[0])




    def Show_Author_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT author_name FROM authors ''')
        data = self.cur.fetchall()
        self.comboBox_4.clear()
        self.comboBox_8.clear()
        for author in data:
            
            self.comboBox_4.addItem(author[0])
            self.comboBox_8.addItem(author[0])





    def Show_Publisher_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='8584', db='library')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()
        self.comboBox_3.clear()
        self.comboBox_6.clear()

        for publisher in data:
            
            self.comboBox_3.addItem(publisher[0])
            self.comboBox_6.addItem(publisher[0])



#################   Themes $####################

    def Dark_Blue(self):
        style = open('themes/darkblue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
    

    def Clasic(self):
        style = open('themes/clasic.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


    def Light(self):
        style = open('themes/light.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


    def Orange(self):
        style = open('themes/orange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)







def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()