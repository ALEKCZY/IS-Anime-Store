from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import mysql.connector
import sys

config = {
  'user': 'db_krinic_o_usr',
  'password': 'DfYaYSueeOQagvr5',
  'host': '5.183.188.132',
  'database': 'db_krinic_ORKqm',
  'port': '3306'
}

class Ui_AnimeStore(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        background = QPixmap("D:/python/anime_phone.jpg")
        background = background.scaled(MainWindow.size(), QtCore.Qt.IgnoreAspectRatio)
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

        self.mainMenuButton = QtWidgets.QPushButton(self.centralwidget)
        self.mainMenuButton.setGeometry(QtCore.QRect(400, 250, 75, 23))
        self.mainMenuButton.setObjectName("mainMenuButton")

        self.categoriesButton = QtWidgets.QPushButton(self.centralwidget)
        self.categoriesButton.setGeometry(QtCore.QRect(503, 250, 75, 23))
        self.categoriesButton.setObjectName("categoriesButton")

        self.ordersButton = QtWidgets.QPushButton(self.centralwidget)
        self.ordersButton.setGeometry(QtCore.QRect(606, 250, 75, 23))
        self.ordersButton.setObjectName("ordersButton")

        self.productsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.productsTable.setGeometry(QtCore.QRect(400, 300, 552, 559))
        self.productsTable.setObjectName("productsTable")
        self.productsTable.setColumnCount(3)
        self.productsTable.setHorizontalHeaderLabels(["Товар", "Категория", "Количество"])
        self.productsTable.setColumnWidth(0, 250)
        self.productsTable.setColumnWidth(1, 150)
        self.productsTable.setColumnWidth(2, 120)

        self.fillProductsTable()

        self.categoryTable = QtWidgets.QTableWidget(self.centralwidget)
        self.categoryTable.setGeometry(QtCore.QRect(400, 300, 422, 400))
        self.categoryTable.setObjectName("categoryTable")
        self.categoryTable.setColumnCount(2)
        self.categoryTable.setHorizontalHeaderLabels(["ID", "Категория"])
        self.categoryTable.setColumnWidth(0, 150)
        self.categoryTable.setColumnWidth(1, 250)
        self.categoryTable.setVisible(False)

        self.productsCategory = QtWidgets.QTableWidget(self.centralwidget)
        self.productsCategory.setGeometry(QtCore.QRect(1000, 300, 680, 400))
        self.productsCategory.setObjectName("productsCategory")
        self.productsCategory.setColumnCount(3)
        self.productsCategory.setHorizontalHeaderLabels(["Товар", "Категория", "Количество"])
        self.productsCategory.setColumnWidth(0, 150)
        self.productsCategory.setColumnWidth(1, 250)
        self.productsCategory.setColumnWidth(2, 250)
        self.productsCategory.setVisible(False)

        self.ordersTable = QtWidgets.QTableWidget(self.centralwidget)
        self.ordersTable.setGeometry(QtCore.QRect(400, 300, 830, 650))
        self.ordersTable.setObjectName("ordersTable")
        self.ordersTable.setColumnCount(6)
        self.ordersTable.setHorizontalHeaderLabels(["ID", "Товар", "Количество", "Дата", "Статус", "Сумма"])
        self.ordersTable.setColumnWidth(3, 150)
        self.ordersTable.setVisible(False)

        self.ordersLabel = QtWidgets.QLabel(self.centralwidget)
        self.ordersLabel.setGeometry(QtCore.QRect(1000, 260, 510, 50))
        self.ordersLabel.setObjectName("ordersLabel")
        self.ordersLabel.setText("Окно оформления заказов")
        self.ordersLabel.setStyleSheet("background-color: rgba(169, 169, 169, 200); border-radius: 10px; font-size: 18px; font-family: Arial;")
        self.ordersLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.OperLabel = QtWidgets.QLabel(self.centralwidget)
        self.OperLabel.setGeometry(QtCore.QRect(1530, 256, 200, 300))
        self.OperLabel.setObjectName("OperLabel")
        self.OperLabel.setText("Увеличить/Уменьшить\nкол-во товаров")
        self.OperLabel.setStyleSheet("background-color: rgba(169, 169, 169, 200); border-radius: 10px; font-size: 16px; font-family: Arial;")
        self.OperLabel.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        self.orderSearchLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.orderSearchLineEdit.setGeometry(QtCore.QRect(1210, 26, 250, 40))
        self.orderSearchLineEdit.setObjectName("orderSearchLineEdit")

        self.orderSearchButton = QtWidgets.QPushButton(self.centralwidget)
        self.orderSearchButton.setGeometry(QtCore.QRect(1100, 20, 75, 23))
        self.orderSearchButton.setObjectName("orderSearchButton")

        self.orderList = QtWidgets.QTableWidget(self.centralwidget)
        self.orderList.setGeometry(QtCore.QRect(1000, 300, 510, 500))
        self.orderList.setObjectName("orderList")
        self.orderList.setColumnCount(4)
        self.orderList.setHorizontalHeaderLabels(["Товар", "Цена", "Количество", "Сумма"])

        self.addToOrderButton = QtWidgets.QPushButton(self.centralwidget)
        self.addToOrderButton.setGeometry(QtCore.QRect(1577, 325, 30, 30))
        self.addToOrderButton.setObjectName("addToOrderButton")

        self.removeFromOrderButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeFromOrderButton.setGeometry(QtCore.QRect(1577, 385, 30, 30))
        self.removeFromOrderButton.setObjectName("removeFromOrderButton")

        self.checkoutButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkoutButton.setGeometry(QtCore.QRect(1200, 850, 100, 30))
        self.checkoutButton.setObjectName("checkoutButton")

        exit_icon = QtGui.QIcon("D:/python/pngwing.com.png")

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(1850, 10, 50, 50))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setIcon(exit_icon)
        self.exitButton.setIconSize(QtCore.QSize(50, 50))

        self.mainMenuButton.setStyleSheet(button_style)
        self.categoriesButton.setStyleSheet(button_style)
        self.ordersButton.setStyleSheet(button_style)
        self.checkoutButton.setStyleSheet(button_style)
        self.addToOrderButton.setStyleSheet(button_style)
        self.removeFromOrderButton.setStyleSheet(button_style)
        self.orderSearchButton.setStyleSheet(button_style)

        self.productsTable.setStyleSheet(table_style)
        self.categoryTable.setStyleSheet(table_style)
        self.productsCategory.setStyleSheet(table_style)
        self.ordersTable.setStyleSheet(table_style)
        self.orderList.setStyleSheet(table_style)

        self.ordersButton.clicked.connect(self.clearOrders)
        self.mainMenuButton.clicked.connect(self.showMainMenu)
        self.productsTable.cellClicked.connect(self.addSelectedProductToOrder)
        self.addToOrderButton.clicked.connect(self.increaseQuantity)
        self.removeFromOrderButton.clicked.connect(self.decreaseQuantity)
        self.checkoutButton.clicked.connect(self.createOrder)
        self.orderSearchButton.clicked.connect(self.searchProduct)
        self.exitButton.clicked.connect(self.exitApplication)
        self.categoriesButton.clicked.connect(self.clearUI)
        MainWindow.setCentralWidget(self.centralwidget)

        self.productsTable.itemDoubleClicked.connect(self.prevent_edit)
        self.categoryTable.itemDoubleClicked.connect(self.prevent_edit)
        self.productsCategory.itemDoubleClicked.connect(self.prevent_edit)
        self.ordersTable.itemDoubleClicked.connect(self.prevent_edit)
        self.orderList.itemDoubleClicked.connect(self.prevent_edit)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setWindowTitle("ИС для магазина аниме атрибутики")
        self.mainMenuButton.setText("Главная")
        self.categoriesButton.setText("Категории")
        self.ordersButton.setText("Заказы")
        self.orderSearchButton.setText("Поиск")
        self.addToOrderButton.setText("+")
        self.removeFromOrderButton.setText("-")
        self.checkoutButton.setText("Оформить")

    def fillProductsTable(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT p.title, c.title AS category, p.quantity 
                FROM product p
                INNER JOIN category c ON p.category_id = c.id_category
            """)

            rows = cursor.fetchall()

            self.productsTable.setRowCount(0)

            self.productsTable.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(val))
                    self.productsTable.setItem(i, j, item)

            conn.close()
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")

    def addSelectedProductToOrder(self, row, column):
        selected_product = {}
        for i in range(self.productsTable.columnCount()):
            header = self.productsTable.horizontalHeaderItem(i).text()
            item = self.productsTable.item(row, i)
            if item is not None:
                selected_product[header] = item.text()

        title = selected_product.get('Товар', '')
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("SELECT price, quantity FROM product WHERE title = %s", (title,))
            result = cursor.fetchone()

            if result:
                price = float(result[0])
                available_quantity = int(result[1])

                if available_quantity > 0:
                    quantity = 1
                    total_price = price * quantity

                    row_position = self.orderList.rowCount()
                    self.orderList.insertRow(row_position)

                    for j, header in enumerate(self.orderList.horizontalHeaderItem(i).text() for i in range(self.orderList.columnCount())):
                        if header == 'Количество':
                            item = QtWidgets.QTableWidgetItem(str(quantity))
                        elif header == 'Сумма':
                            item = QtWidgets.QTableWidgetItem(str(total_price))
                        elif header == 'Цена':
                            item = QtWidgets.QTableWidgetItem(str(price))
                        else:
                            item = QtWidgets.QTableWidgetItem(selected_product.get(header, ''))
                        self.orderList.setItem(row_position, j, item)
                else:
                    print("Товар недоступен для заказа, количество равно 0")

            conn.close()
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")

    def increaseQuantity(self):
        selected_row = self.orderList.currentRow()
        if selected_row >= 0:
            quantity_item = self.orderList.item(selected_row, 2)
            price_item = self.orderList.item(selected_row, 1)
            current_quantity = int(quantity_item.text())
            current_quantity += 1
            product_name = self.orderList.item(selected_row, 0).text()
            available_quantity = self.getAvailableQuantityFromDB(product_name)

            if current_quantity <= available_quantity:
                quantity_item.setText(str(current_quantity))

                total_price = float(price_item.text()) * current_quantity
                total_price_item = QtWidgets.QTableWidgetItem(str(total_price))
                self.orderList.setItem(selected_row, 3, total_price_item)
            else:
                print("Доступное количество товара недостаточно")

    def getAvailableQuantityFromDB(self, product_name):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("SELECT quantity FROM product WHERE title = %s", (product_name,))
            result = cursor.fetchone()

            if result:
                available_quantity = int(result[0])
                conn.close()
                return available_quantity
            else:
                conn.close()
                return 0
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")
            return 0


    def decreaseQuantity(self):
        selected_row = self.orderList.currentRow()
        if selected_row >= 0:
            quantity_item = self.orderList.item(selected_row, 2)
            price_item = self.orderList.item(selected_row, 1)
            current_quantity = int(quantity_item.text())
            current_quantity -= 1

            if current_quantity > 0:
                quantity_item.setText(str(current_quantity))

                total_price = float(price_item.text()) * current_quantity
                total_price_item = QtWidgets.QTableWidgetItem(str(total_price))
                self.orderList.setItem(selected_row, 3, total_price_item)
            else:
                self.orderList.removeRow(selected_row)


    def createOrder(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            for row in range(self.orderList.rowCount()):
                product_name = self.orderList.item(row, 0).text()
                quantity = int(self.orderList.item(row, 2).text())
                sum = float(self.orderList.item(row, 3).text())

                cursor.execute("SELECT id_product FROM product WHERE title = %s", (product_name,))
                result = cursor.fetchone()

                if result:
                    product_id = result[0]

                    cursor.execute(
                        "UPDATE product SET quantity = quantity - %s WHERE id_product = %s",
                        (quantity, product_id)
                    )

                    cursor.execute(
                        "INSERT INTO orders (product_id, quantity, sum) VALUES (%s, %s, %s)",
                        (product_id, quantity, sum)
                    )
            print("Заказ оформлен")

            self.orderList.clearContents()
            self.orderList.setRowCount(0)


            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")


    def searchProduct(self):
        search_text = self.orderSearchLineEdit.text()
        if search_text:
            rows = self.productsTable.rowCount()
            for row in range(rows):
                item = self.productsTable.item(row, 0)
                if item and search_text.lower() in item.text().lower():
                    self.productsTable.selectRow(row)
                    break

    def exitApplication(self):
        QtWidgets.QApplication.quit()
        print("Соединение разорвано")

    def MainProd(self):
        self.productsTable.setVisible(True)
        self.orderList.setVisible(True)
        self.addToOrderButton.setVisible(True)
        self.removeFromOrderButton.setVisible(True)
        self.checkoutButton.setVisible(True)
        self.ordersLabel.setVisible(True)
        self.OperLabel.setVisible(True)
        self.categoryTable.setVisible(False)
        self.productsCategory.setVisible(False)
        self.ordersTable.setVisible(False)

    def showMainMenu(self):
        self.MainProd()

    def clearUI(self):
        self.productsTable.setVisible(False)
        self.orderList.setVisible(False)
        self.addToOrderButton.setVisible(False)
        self.removeFromOrderButton.setVisible(False)
        self.checkoutButton.setVisible(False)
        self.ordersTable.setVisible(False)
        self.ordersLabel.setVisible(False)
        self.OperLabel.setVisible(False)
        self.categoryTable.setVisible(True)
        self.productsCategory.setVisible(True)
        self.loadCategories()


    def clearOrders(self):
        self.productsTable.setVisible(False)
        self.orderList.setVisible(False)
        self.addToOrderButton.setVisible(False)
        self.removeFromOrderButton.setVisible(False)
        self.checkoutButton.setVisible(False)
        self.categoryTable.setVisible(False)
        self.productsCategory.setVisible(False)
        self.ordersLabel.setVisible(False)
        self.OperLabel.setVisible(False)
        self.ordersTable.setVisible(True)
        self.loadOrders()

    def showProductsForCategory(self, row, column):
        categoryId = int(self.categoryTable.item(row, 0).text())

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT p.title, c.title AS category, p.quantity 
                FROM product p
                INNER JOIN category c ON p.category_id = c.id_category
                WHERE p.category_id = %s
            """, (categoryId,))

            rows = cursor.fetchall()

            self.productsCategory.setRowCount(0)

            self.productsCategory.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(val))
                    self.productsCategory.setItem(i, j, item)

            conn.close()
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")

    def loadCategories(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("SELECT id_category, title FROM category")
            rows = cursor.fetchall()

            self.categoryTable.cellClicked.connect(self.showProductsForCategory)

            self.categoryTable.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(val))
                    self.categoryTable.setItem(i, j, item)

            conn.close()
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")

    def loadOrders(self):
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            cursor.execute("SELECT id_orders, product_id, quantity, date, status, sum FROM orders")
            rows = cursor.fetchall()

            self.ordersTable.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(val))
                    self.ordersTable.setItem(i, j, item)

            conn.close()
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")

    def prevent_edit(self, item):
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    main = Ui_AnimeStore()
    main.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())

