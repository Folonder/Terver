import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSpinBox, \
    QPushButton, QLabel, QLineEdit, QGridLayout, QTabWidget, QDoubleSpinBox

from Lab6.ChiTable import ChiTable
from Lab6.statistic import Distribution
from scipy.stats import chi2

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use('Qt5Agg')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle('Проверка гипотезы о нормальном расрпеделении')

        # Create the tab widget
        self.tab_widget = QTabWidget()

        # Create the table widget
        self.table = QTableWidget()

        # Create the spin box for selecting the number of columns
        self.spin_box = QSpinBox()
        self.spin_box.setRange(1, 10)  # Set the range of columns

        # Create the button
        self.button = QPushButton('Посчитать')
        self.button.clicked.connect(self.calculate)

        # Create the labels and line edit fields
        self.labels = []
        self.line_edits = []
        for _ in range(6):
            label = QLabel()
            line_edit = QLineEdit()
            self.labels.append(label)
            self.line_edits.append(line_edit)

        # Set the layout for the main window
        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0, 1, 2)
        layout.addWidget(self.spin_box, 1, 0, 1, 2)

        # Add the labels and line edit fields to the layout
        for row, (label, line_edit) in enumerate(zip(self.labels, self.line_edits), start=2):
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(label, row, 0)
            layout.addWidget(line_edit, row, 1)

        layout.addWidget(self.button, 8, 0, 1, 2)

        # Create a widget for the first tab and set the layout
        first_tab_widget = QWidget()
        first_tab_widget.setLayout(layout)

        # Add the first tab widget to the tab widget
        self.tab_widget.addTab(first_tab_widget, 'Ряд распределения')

        # Create a widget for the second tab
        second_tab_widget = QWidget()

        # Create the label and spin box for the second tab
        significance_label = QLabel('Уровень значимости a:')
        self.alpha_spin_box = QDoubleSpinBox()
        self.alpha_spin_box.setRange(0.0, 10.0)
        self.alpha_spin_box.setSingleStep(0.01)
        self.alpha_spin_box.setDecimals(2)
        self.alpha_spin_box.setValue(0.01)
        self.alpha_spin_box.valueChanged.connect(self.calculate_chi)

        # Set the layout for the second tab
        second_tab_layout = QVBoxLayout()
        second_tab_layout.addWidget(significance_label)
        second_tab_layout.addWidget(self.alpha_spin_box)
        second_tab_widget.setLayout(second_tab_layout)

        self.chi_table = ChiTable()
        self.alpha_table = QPushButton("Посмотреть таблицу")
        self.alpha_table.clicked.connect(self.chi_table.show)
        second_tab_layout.addWidget(self.alpha_table)

        self.labels2 = []
        for _ in range(6):
            self.labels2.append(QLabel())

        for i in self.labels2:
            i.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            second_tab_layout.addWidget(i)

        # Add the second tab widget to the tab widget
        self.tab_widget.addTab(second_tab_widget, 'Критерий согласия Пирсона')

        self.third_tab_widget = QWidget()
        self.probabilities_lables = []
        for _ in range(6):
            self.probabilities_lables.append(QLabel())

        self.tab_widget.addTab(self.third_tab_widget, 'Теоретические вероятности')

        # Set the central widget as the tab widget
        self.setCentralWidget(self.tab_widget)

        # Connect the spin box value changed signal to update the table
        self.spin_box.valueChanged.connect(self.update_table)

        # Set the initial number of columns
        self.update_table()

        self.distribution = Distribution()
        self.fill_lables()

    def fill_lables(self):
        self.labels[0].setText(f'Xв = Σ(i=1, n)((Ni * Xi)/N) = ')
        self.labels[1].setText(f'Dв = Σ(i=1, n)(Ni * ((Xi-Xв) ^ 2))/N) = ')
        self.labels[2].setText(f'σв = sqrt(Dв) = ')
        self.labels[3].setText(f'S = sqrt(n / (n - 1) * Dв) = ')
        self.labels[4].setText('a* = ')
        self.labels[5].setText('σ* = ')

    def update_table(self):
        num_columns = self.spin_box.value()

        # Set the number of columns in the table
        self.table.setColumnCount(num_columns)

        # Set the number of rows in the table
        num_rows = 7
        self.table.setRowCount(num_rows)

        # Set the vertical header labels
        row_labels = ['xi; xi+1', 'ni', 'Wi', 'ci', 'n`i = p_i*n', '(n`i - ni)^2', '(n`i - ni)^2 / n`i']
        for row, label in enumerate(row_labels):
            item = QTableWidgetItem(label)
            self.table.setVerticalHeaderItem(row, item)

    def calculate(self):
        self.distribution.set_interval_row(self.get_interval_row())
        self.fillTable()
        self.fillLineEdits()
        self.calculate_chi()
        self.calculate_probabilities()
        self.plot_normal_density()
        self.plot_histopolygon()
        plt.show()

    def get_interval_row(self):
        values = []
        for row in range(2):
            row_values = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    row_values.append(item.text())
                else:
                    row_values.append('')
            values.append(row_values)
        vars = [tuple(map(float, var.split(';'))) for var in values[0]]
        vals = list(map(float, values[1]))
        interval_row = dict()
        for i in range(len(vals)):
            interval_row[vars[i]] = vals[i]
        # interval_row = {(0, 10): 16, (10, 20): 48, (20, 30): 70, (30, 40): 47, (40, 50): 19 }
        return interval_row

    def fillLineEdits(self):
        self.line_edits[0].setText(f'{self.distribution.Xv}')
        self.line_edits[1].setText(f'{self.distribution.Dv}')
        self.line_edits[2].setText(f'{self.distribution.sigma}')
        self.line_edits[3].setText(f'{self.distribution.S}')
        self.line_edits[4].setText(f'{self.distribution.a}')
        self.line_edits[5].setText(f'{self.distribution.sigma}')

    def fillTable(self):
        for i in range(len(self.distribution.W)):
            self.table.setItem(2, i, QTableWidgetItem(str(round(self.distribution.W[i], 3))))
            self.table.setItem(3, i, QTableWidgetItem(str(round(self.distribution.middles[i], 3))))
            pi = self.distribution.get_normal_theoretical_probability(self.distribution.intervals[i])
            npi = pi * self.distribution.n_sum
            n_square = (npi - self.distribution.N[i]) ** 2
            chi_2 = n_square / npi
            self.table.setItem(4, i, QTableWidgetItem(str(round(npi, 3))))
            self.table.setItem(5, i, QTableWidgetItem(str(round(n_square, 3))))
            self.table.setItem(6, i, QTableWidgetItem(str(round(chi_2, 3))))

    def calculate_chi(self):
        alpha = self.alpha_spin_box.value()
        k = self.spin_box.value() - 3
        if k > 0 and self.distribution.sigma:
            chi2_crit = round(chi2.ppf(1 - alpha, k), 5)
            chi2_exp = round(self.distribution.get_normal_chi2(), 5)
        self.labels2[0].setText(f"Количество степеней свободы k = (m - 3) = {k}")
        self.labels2[1].setText(f"X^2крит = {chi2_crit}")
        self.labels2[2].setText(f"X^2набл = Σ((ni-n`i) ^ 2 / n`i) = {chi2_exp}")
        self.labels2[3].setText(f"Проверка гипотезы:")
        if chi2_exp > chi2_crit:
            self.labels2[4].setText(f"Гипотеза опровергнута")
        else:
            self.labels2[4].setText(f"Гипотеза не опровергнута")

    def calculate_probabilities(self):
        layout = QVBoxLayout()
        for i in self.distribution.intervals:
            label = QLabel()
            label.setText(f"Теоретическая вероятность: {i} = {self.distribution.get_normal_theoretical_probability(i)}")
            layout.addWidget(label)
        self.third_tab_widget.setLayout(layout)

    def plot_normal_density(self):
        plot_data = self.distribution.process_normal_density(self.distribution.a, self.distribution.sigma)
        fig, ax = plt.subplots(1, 1)
        ax.plot(plot_data[0], plot_data[1])
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('f*(x)')
        plt.subplot(1, 1, 1)

    def plot_histopolygon(self):
        plot_data = self.distribution.process_normal_density(self.distribution.a, self.distribution.sigma)
        fig, ax = plt.subplots(1, 1)
        bounds = [i[0] for i in self.distribution.intervals] + [self.distribution.intervals[-1][1]]
        ws = []
        for i, weight in enumerate(self.distribution.W):
            ws.append(weight / self.distribution.h)
        ax.hist(self.distribution.middles, bins=bounds, weights=ws)

        ax.plot(self.distribution.middles, ws)
        ax.scatter(self.distribution.middles, ws)
        ax.plot(plot_data[0], plot_data[1])
        ax.grid(True)
        ax.set_xlabel('xi*')
        ax.set_ylabel('ni/nh')
        plt.subplot(1, 1, 1)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
