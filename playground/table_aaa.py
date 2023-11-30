from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

table = QTableWidget(3, 4)

# Set data in the table
for i in range(3):
    for j in range(4):
        item = QTableWidgetItem(f'Item {i+1}-{j+1}')
        table.setItem(i, j, item)

# Set header labels
table.setHorizontalHeaderLabels(['General Header', '', '', ''])

# Set general cell in the upper row
table.setItem(0, 0, QTableWidgetItem('General Cell'))

# Merge header cells for subheaders
table.setSpan(1, 1, 1, 1)
table.setSpan(1, 2, 1, 1)
table.setSpan(1, 3, 1, 1)

# Set subheader labels
table.setHorizontalHeaderItem(1, QTableWidgetItem('Subheader 1'))
table.setHorizontalHeaderItem(2, QTableWidgetItem('Subheader 2'))
table.setHorizontalHeaderItem(3, QTableWidgetItem('Subheader 3'))

layout.addWidget(table)
window.setLayout(layout)

window.show()
app.exec()
