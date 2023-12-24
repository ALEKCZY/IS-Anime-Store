from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont
import mysql.connector
import sys

config = {
    'user': 'db_krinic_o_usr',
    'password': 'DfYaYSueeOQagvr5',
    'host': '5.183.188.132',
    'database': 'db_krinic_ORKqm',
    'port': '3306'
}

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super(AddProductDialog, self).__init__(parent)

        layout = QVBoxLayout()

        self.setWindowTitle("Добавление товара")

        self.name_label = QLabel('Название товара:')
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.category_label = QLabel('ID категории:')
        self.category_input = QLineEdit()
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)

        self.quantity_label = QLabel('Количество:')
        self.quantity_input = QLineEdit()
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        self.price_label = QLabel('Цена:')
        self.price_input = QLineEdit()
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)

        self.add_button = QPushButton('Добавить')
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_product)

        self.setLayout(layout)

    def is_number(self, text):
        return text.isdigit()

    def category_exists(self, category_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            query = "SELECT * FROM category WHERE id_category = %s"
            cursor.execute(query, (category_id,))
            result = cursor.fetchone()
            conn.close()
            return bool(result)
        except Exception as e:
            print(f"Ошибка при проверке существования категории: {e}")
            return False

    def add_product(self):
        name = self.name_input.text()
        category_id = self.category_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()

        if not (name and category_id and quantity and price):
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля')
            return

        if not self.category_exists(category_id):
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Указанной категории не существует')
            return

        if not (self.is_number(quantity) and self.is_number(price)):
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите только цифры в поля количество и цена')
            return

        self.accept()

class ModifyProductDialog(QDialog):
    def __init__(self, conn, cursor, product_data, parent=None):
        super(ModifyProductDialog, self).__init__(parent)
        self.conn = conn
        self.cursor = cursor

        layout = QVBoxLayout()

        self.setWindowTitle("Изменение товара")

        self.name_label = QLabel('Название товара:')
        self.name_input = QLineEdit()
        self.name_input.setText(product_data[1])
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.category_label = QLabel('ID категории:')
        self.category_input = QLineEdit()
        self.category_input.setText(str(product_data[2]))
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)

        self.quantity_label = QLabel('Количество:')
        self.quantity_input = QLineEdit()
        self.quantity_input.setText(str(product_data[3]))
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        self.price_label = QLabel('Цена:')
        self.price_input = QLineEdit()
        self.price_input.setText(str(product_data[4]))
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)

        self.modify_button = QPushButton('Изменить')
        layout.addWidget(self.modify_button)
        self.modify_button.clicked.connect(self.modify_product)

        self.setLayout(layout)
        self.product_id = product_data[0]

    def is_number(self, text):
        return text.isdigit()

    def category_exists(self, category_id):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            query = "SELECT * FROM category WHERE id_category = %s"
            cursor.execute(query, (category_id,))
            result = cursor.fetchone()
            conn.close()
            return bool(result)
        except Exception as e:
            print(f"Ошибка при проверке существования категории: {e}")
            return False

    def modify_product(self):
        name = self.name_input.text()
        category_id = self.category_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()

        if not (name and category_id and quantity and price):
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля')
            return

        if not self.category_exists(category_id):
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Указанной категории не существует')
            return

        if not (self.is_number(quantity) and self.is_number(price)):
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите только цифры в поля количество и цена')
            return

        try:
            query = "UPDATE product SET title = %s, category_id = %s, quantity = %s, price = %s WHERE id_product = %s"
            data = (name, category_id, quantity, price, self.product_id)
            self.cursor.execute(query, data)
            self.conn.commit()
            self.accept()
        except Exception as e:
            print(f"Ошибка при обновлении продукта: {e}")

class AddCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super(AddCategoryDialog, self).__init__(parent)

        layout = QVBoxLayout()

        self.setWindowTitle("Добавление категории")

        self.name_category = QLabel('Название категории:')
        self.category_input = QLineEdit()
        layout.addWidget(self.name_category)
        layout.addWidget(self.category_input)

        self.add_button_cat = QPushButton('Добавить')
        layout.addWidget(self.add_button_cat)
        self.add_button_cat.clicked.connect(self.add_category)

        self.setLayout(layout)

    def add_category(self):
        name = self.category_input.text()

        if not name:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля')
            return

        self.accept()

class ModifyCategoryDialog(QDialog):
    def __init__(self, conn, cursor, category_data, parent=None):
        super(ModifyCategoryDialog, self).__init__(parent)
        self.conn = conn
        self.cursor = cursor

        layout = QVBoxLayout()

        self.setWindowTitle("Изменение категории")

        self.name_category = QLabel('Название категории:')
        self.category_input = QLineEdit()
        self.category_input.setText(category_data[1])
        layout.addWidget(self.name_category)
        layout.addWidget(self.category_input)

        self.modify_button = QPushButton('Изменить')
        layout.addWidget(self.modify_button)
        self.modify_button.clicked.connect(self.modify_category)

        self.setLayout(layout)
        self.category_id = category_data[0]

    def modify_category(self):
        name = self.category_input.text()

        if not name:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля')
            return

        try:
            query = "UPDATE category SET title = %s WHERE id_category = %s"
            data = (name, self.category_id)
            self.cursor.execute(query, data)
            self.conn.commit()
            self.accept()
        except Exception as e:
            print(f"Ошибка при обновлении продукта: {e}")

class PU_Window(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        background = QPixmap("D:/python/sakura.jpg")
        background = background.scaled(MainWindow.size(), QtCore.Qt.IgnoreAspectRatio)
        background = background.scaled(1950, 600)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(background))
        MainWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        button_style = (
            "QPushButton {"
            "background-color: #FF6347;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: #F0F8FF;"
            "font-size: 18px;"
            "font-style: italic;"
            "min-width: 100px;"
            "min-height: 50px;"
            "}"
            "QPushButton:pressed {"
            "background-color: #45a049;"
            "border-style: inset;"
            "}"
        )

        table_style = """
            QTableWidget {background-color: #f7f7f7; border: 1px solid #ccc;}
            QTableWidget::item {padding: 10px;}
            QTableWidget::item:selected {background-color: #a6e3e9;}
            QHeaderView::section {background-color: #d9d9d9; border: 1px solid #ccc; font-weight: bold;}
        """

        self.panel_label = QtWidgets.QLabel(self.centralwidget)
        self.panel_label.setGeometry(QtCore.QRect(0, 0, 1950, 200))
        self.panel_label.setStyleSheet("background-color: rgba(169, 169, 169, 200); border-radius: 10px; font-size: 22px; font-weight: bold;")
        self.panel_label.setText("Панель управления")
        self.panel_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QFont("Fantasy")
        self.panel_label.setFont(font)

        self.buttons_label = QtWidgets.QLabel(self.centralwidget)
        self.buttons_label.setGeometry(QtCore.QRect(0, 200, 1950, 150))
        self.buttons_label.setStyleSheet("background-color: rgba(120, 169, 169, 200); border-radius: 10px; font-size: 18px;")
        self.buttons_label.setAlignment(QtCore.Qt.AlignCenter)

        self.products_button = QtWidgets.QPushButton(self.centralwidget)
        self.products_button.setGeometry(QtCore.QRect(25, 250, 75, 23))
        self.products_button.setText("Товары")
        self.products_button.clicked.connect(self.product_button_clicked)

        self.categories_button = QtWidgets.QPushButton(self.centralwidget)
        self.categories_button.setGeometry(QtCore.QRect(150, 250, 75, 23))
        self.categories_button.setText("Категории")
        self.categories_button.clicked.connect(self.categories_button_clicked)

        self.add_product_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_product_button.setGeometry(QtCore.QRect(1500, 250, 75, 30))
        self.add_product_button.setText("Добавить")
        self.add_product_button.clicked.connect(self.add_product)

        self.modify_product_button = QtWidgets.QPushButton(self.centralwidget)
        self.modify_product_button.setGeometry(QtCore.QRect(1625, 250, 75, 30))
        self.modify_product_button.setText("Изменить")
        self.modify_product_button.clicked.connect(self.modify_product)

        self.delete_product_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_product_button.setGeometry(QtCore.QRect(1750, 250, 75, 30))
        self.delete_product_button.setText("Удалить")
        self.delete_product_button.clicked.connect(self.delete_product)

        exit_icon = QtGui.QIcon("D:/python/pngwing.com.png")

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(1850, 20, 50, 50))
        self.exit_button.setIcon(exit_icon)
        self.exit_button.setIconSize(QtCore.QSize(50, 50))
        self.exit_button.clicked.connect(self.exit)

        self.products_button.setStyleSheet(button_style)
        self.categories_button.setStyleSheet(button_style)
        self.add_product_button.setStyleSheet(button_style)
        self.modify_product_button.setStyleSheet(button_style)
        self.delete_product_button.setStyleSheet(button_style)

        self.table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.table_widget.setGeometry(QtCore.QRect(0, 350, 1918, 720))

        self.table_widget.setStyleSheet(table_style)

        self.table_widget.itemDoubleClicked.connect(self.prevent_edit)

        self.is_showing_products = True
        self.is_showing_categories = False

        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

        self.show_products()

    def show_products(self):
        self.clear_table()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Название", "ID Категории", "Количество", "Цена"])
        self.table_widget.setColumnWidth(0, 270)
        self.table_widget.setColumnWidth(1, 420)
        self.table_widget.setColumnWidth(2, 370)
        self.table_widget.setColumnWidth(3, 420)
        self.table_widget.setColumnWidth(4, 420)


        query = "SELECT * FROM product"
        self.cursor.execute(query)
        products = self.cursor.fetchall()

        self.table_widget.setRowCount(len(products))
        for row, product in enumerate(products):
            for col, data in enumerate(product):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_widget.setItem(row, col, item)

    def show_categories(self):
        self.clear_table()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Название"])
        self.table_widget.setColumnWidth(0, 1000)
        self.table_widget.setColumnWidth(1, 1000)

        query = "SELECT * FROM category"
        self.cursor.execute(query)
        categories = self.cursor.fetchall()

        self.table_widget.setRowCount(len(categories))
        for row, category in enumerate(categories):
            for col, data in enumerate(category):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_widget.setItem(row, col, item)

    def add_product(self):
        try:
            add_dialog = AddProductDialog()
            if add_dialog.exec_() == QDialog.Accepted:
                name = add_dialog.name_input.text()
                category_id = add_dialog.category_input.text()
                quantity = add_dialog.quantity_input.text()
                price = add_dialog.price_input.text()
                query = "INSERT INTO product (title, category_id, quantity, price) VALUES (%s, %s, %s, %s)"
                data = (name, category_id, quantity, price)
                self.cursor.execute(query, data)
                self.conn.commit()
                self.show_products()
        except Exception as e:
            print(f"Ошибка при добавлении продукта: {e}")


    def modify_product(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            product_data = [self.table_widget.item(current_row, i).text() for i in range(5)]
            modify_dialog = ModifyProductDialog(self.conn, self.cursor, product_data)
            if modify_dialog.exec_() == QDialog.Accepted:
                self.show_products()
        else:
            QtWidgets.QMessageBox.warning(MainWindow, 'Ошибка', 'Выберите товар для изменения')

    def delete_product(self):
        try:
            current_row = self.table_widget.currentRow()
            if current_row >= 0:
                confirmation = QtWidgets.QMessageBox.question(MainWindow, 'Удалить товар', 'Вы уверены, что хотите удалить этот товар?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

                if confirmation == QtWidgets.QMessageBox.Yes:
                    product_id = self.table_widget.item(current_row, 0).text()
                    query = "DELETE FROM product WHERE id_product = %s"
                    data = (product_id,)
                    self.cursor.execute(query, data)
                    self.conn.commit()
                    self.show_products()
            else:
                QtWidgets.QMessageBox.warning(MainWindow, 'Ошибка', 'Выберите товар для удаления')
        except Exception as e:
            QtWidgets.QMessageBox.critical(MainWindow, 'Ошибка', f'Произошла ошибка при удалении товара: {str(e)}')


    def add_category(self):
        try:
            add_dialog2 = AddCategoryDialog()
            if add_dialog2.exec_() == QDialog.Accepted:
                name = add_dialog2.category_input.text()
                query = "INSERT INTO category (title) VALUES (%s)"
                data = (name,)
                self.cursor.execute(query, data)
                self.conn.commit()
                self.show_categories()
        except Exception as e:
            print(f"Ошибка при добавлении продукта: {e}")

    def modify_category(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            category_data = [self.table_widget.item(current_row, i).text() for i in range(2)]
            modify_dialog = ModifyCategoryDialog(self.conn, self.cursor, category_data)
            if modify_dialog.exec_() == QDialog.Accepted:
                self.show_categories()
        else:
            QtWidgets.QMessageBox.warning(MainWindow, 'Ошибка', 'Выберите категорию для изменения')


    def delete_category(self):
        try:
            current_row = self.table_widget.currentRow()
            if current_row >= 0:
                confirmation = QtWidgets.QMessageBox.question(MainWindow, 'Удалить категорию', 'Вы уверены, что хотите удалить эту категорию?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

                if confirmation == QtWidgets.QMessageBox.Yes:
                    category_id = self.table_widget.item(current_row, 0).text()
                    query = "DELETE FROM category WHERE id_category = %s"
                    data = (category_id,)
                    self.cursor.execute(query, data)
                    self.conn.commit()
                    self.show_categories()
            else:
                QtWidgets.QMessageBox.warning(MainWindow, 'Ошибка', 'Выберите категорию для удаления')
        except Exception as e:
            QtWidgets.QMessageBox.critical(MainWindow, 'Ошибка', f'Произошла ошибка при удалении категории: {str(e)}')

    def product_button_clicked(self):
        try:
            if not self.is_showing_products:
                self.is_showing_products = True
                self.is_showing_categories = False
                self.clear_table()
                self.table_widget.setColumnCount(5)
                self.table_widget.setHorizontalHeaderLabels(["ID", "Название", "ID Категории", "Количество", "Цена"])
                self.add_product_button.clicked.disconnect(self.add_category)
                self.modify_product_button.clicked.disconnect(self.modify_category)
                self.delete_product_button.clicked.disconnect(self.delete_category)

                self.add_product_button.clicked.connect(self.add_product)
                self.modify_product_button.clicked.connect(self.modify_product)
                self.delete_product_button.clicked.connect(self.delete_product)
                self.show_products()
        except Exception as e:
            QtWidgets.QMessageBox.critical(MainWindow, 'Ошибка', f'Произошла ошибка при отображении товаров: {str(e)}')

    def categories_button_clicked(self):
        if not self.is_showing_categories:
            self.is_showing_products = False
            self.is_showing_categories = True
            self.clear_table()
            self.table_widget.setColumnCount(2)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Название"])

            self.add_product_button.clicked.disconnect(self.add_product)
            self.modify_product_button.clicked.disconnect(self.modify_product)
            self.delete_product_button.clicked.disconnect(self.delete_product)

            self.add_product_button.clicked.connect(self.add_category)
            self.modify_product_button.clicked.connect(self.modify_category)
            self.delete_product_button.clicked.connect(self.delete_category)
            self.show_categories()

    def prevent_edit(self, item):
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def clear_table(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

    def exit(self):
        QtWidgets.QApplication.quit()
        print("Соединение разорвано")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    main = PU_Window()
    main.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
