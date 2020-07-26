import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMessageBox,QLabel
import gui_sql
import pyodbc

boxobox = []
var = []
class sql_test (QtWidgets.QMainWindow, gui_sql.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_str)
        self.pushButton1.clicked.connect(self.delete)

    def add_str(self):
        global boxobox, texted
        boxobox = []
        text = self.textEdit.toPlainText()
        count = text.count("\n")

        for i in range(count+1):
            c = QtWidgets.QComboBox(self.widget)
            c.setGeometry(QtCore.QRect(0, (0+i*26), 190, 22))
            #self.scrollArea.setGeometry(QtCore.QRect(230, 10, 211, 40+i*26))
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 192, 40+i*26))
            self.widget.setGeometry(QtCore.QRect(0, 0, 191, (26+i*26)))
            c.setObjectName("comboBox_"+str(i))
            boxobox.append(c)
            #print (c.objectName())
            p=0
            if text.find('\n') > 0:
                p = text.find('\n')
                string = text[:p]
            else:
                string = text
            #string = string.strip()
            string = string.strip()
            text = text[p + 1:]
            lname = string.split(' ')
            #print(lname)
            self.searh(lname[0])
            c.addItems(var)
            c.addItem('--Не найдено--')
            self.title.setText('Всего записей: ' + str(i+1))
            self.title.show()
            self.scrollArea.show()
            c.show()
            self.show()





    def searh(self, lname):

        global var

        cnxn = pyodbc.connect("DRIVER={SQL Server};"
                              "SERVER=10.76.1.35\SQLSERVER2012;"
                              "DATABASE=Orion;"
                              "UID=;"
                              "PWD=")
        cursor = cnxn.cursor()
        cursor2 = cnxn.cursor()
        vir = "SELECT ID,NAME,FirstName,MidName FROM [dbo].[pList] WHERE NAME='"+ lname +"'"
        vir2 = "SELECT Id,OWNERNAME, fingertemplate FROM [dbo].[pMark] where OWNERNAME LIKE '" + lname + "%'"
        cursor.execute(vir)

        var = []
        while 1:
            row = cursor.fetchone()
            if not row:
                break
            name = row[1] + ' ' + row[2] + ' ' + row[3]
            if row[1] == lname:
                var.append(str(row[0])+ ':' + name)

        for count in range(len(var)):
            #print (count)
            cursor2.execute(vir2)

            key = ''
            while 1:
                row2 = cursor2.fetchone()

                if not row2:
                    break
                temp = str(row2[1])
                z = var[count].find(':')
                temp1 = var[count][z+1:]
                if temp1.find(temp)>-1:
                    key = key + ' ' +str(row2[0])

            var[count] = var[count]+ ':' +key

    def delete(self):
        global boxobox
        check = 0
        cnxn = pyodbc.connect("DRIVER={SQL Server};"
                              "SERVER=10.76.1.35\SQLSERVER2012;"
                              "DATABASE=Orion;"
                              "UID=;"
                              "PWD=")
        cursor = cnxn.cursor()
        for i in range(len(boxobox)):
             index = boxobox[i].currentText()
             if index == '--Не найдено--':
                 continue
             delmas = index.split(':')
             delmas[2] = delmas[2].strip()
             delkey = delmas[2].split(' ')
             #print (delmas)
             #print(delmas[0])
             for r in range(len(delkey)):
                 #print (delkey[r])
                 cursor.execute("delete from [dbo].[pMark] where id ='%s'" % delkey[r])
                 cnxn.commit()

             #print(delmas[0])
             cursor.execute("delete from [dbo].[pList] where id ='%s'" % delmas[0])
             cnxn.commit()
             check = 1
        if check == 1:
            QMessageBox.about(self, "Удалено", "Записи успешно удалены.")









def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = sql_test()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

