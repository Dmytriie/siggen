"""
Barion

-- GUI Application --

Jul 2015 Xaratustrah
Mar 2016 Xaratustrah


"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QDialog, QTableWidgetItem
from PyQt5.QtGui import QKeyEvent, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QCoreApplication
from mainwindow_ui import Ui_MainWindow
from ui_interface import UI_Interface
from aboutdialog_ui import Ui_AbooutDialog
from particle import Particle
from amedata import AMEData
from ring import Ring
from version import __version__
import os


class mainWindow(QMainWindow, Ui_MainWindow, UI_Interface):
    """
    The main class for the GUI window
    """

    def __init__(self):
        """
        The constructor and initiator.
        :return:
        """
        # initial setup
        super(mainWindow, self).__init__()
        self.setupUi(self)

        # create an instance of the table data and give yourself as UI Interface
        self.ame_data = AMEData(self)

        # take care about ring combo
        self.ring_dict = Ring.get_ring_dict()
        keys = list(self.ring_dict.keys())
        keys.sort()
        self.comboBox_ring.addItems(keys)
        self.current_ring_name = ''

        self.comboBox_ring.setCurrentIndex(4)
        self.on_comboBox_ring_changed(4)

        # fill combo box with names
        self.comboBox_name.addItems(self.ame_data.names_list)

        # UI related stuff
        self.setup_table_view()
        self.connect_signals()

        # A particle to begin with
        self.particle = None
        self.comboBox_name.setCurrentIndex(6)
        self.reinit_particle()

    def setup_table_view(self):
        # setup table view
        self.tableView_model = QStandardItemModel(40, 3)
        self.tableView_model.clear()
        self.tableView_model.setHorizontalHeaderItem(0, QStandardItem('Name'))
        self.tableView_model.setHorizontalHeaderItem(1, QStandardItem('Value'))
        self.tableView_model.setHorizontalHeaderItem(2, QStandardItem('Unit'))
        # self.tableView.verticalHeader().setVisible(False)
        self.tableView.setModel(self.tableView_model)

    def connect_signals(self):
        """
        Connects signals.
        :return:
        """
        self.actionClear_results.triggered.connect(self.on_pushButton_clear)
        self.actionSave_results.triggered.connect(self.save_file_dialog)
        self.actionCalculate.triggered.connect(self.on_pushButton_calculate)
        self.actionShow_table_data.triggered.connect(self.on_pushButton_table_data)
        self.actionIdentify.triggered.connect(self.on_pushButton_identify)
        self.actionIsotopes.triggered.connect(self.show_isotopes)
        self.actionIsobars.triggered.connect(self.show_isobars)
        self.actionIsotones.triggered.connect(self.show_isotones)

        # Action about and Action quit will be shown differently in OSX
        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionQuit.triggered.connect(QCoreApplication.instance().quit)

        self.pushButton_copy_table.clicked.connect(self.on_pushButton_copy_table)
        self.pushButton_clear.clicked.connect(self.on_pushButton_clear)
        self.pushButton_isotopes.clicked.connect(self.show_isotopes)
        self.pushButton_isotones.clicked.connect(self.show_isotones)
        self.pushButton_isobars.clicked.connect(self.show_isobars)
        self.pushButton_save.clicked.connect(self.save_file_dialog)
        self.pushButton_calculate.clicked.connect(self.on_pushButton_calculate)
        self.pushButton_table_data.clicked.connect(self.on_pushButton_table_data)
        self.pushButton_identify.clicked.connect(self.on_pushButton_identify)

        self.pushButton_nav_n.clicked.connect(self.on_nav_n_pressed)
        self.pushButton_nav_ne.clicked.connect(self.on_nav_ne_pressed)
        self.pushButton_nav_e.clicked.connect(self.on_nav_e_pressed)
        self.pushButton_nav_se.clicked.connect(self.on_nav_se_pressed)
        self.pushButton_nav_s.clicked.connect(self.on_nav_s_pressed)
        self.pushButton_nav_sw.clicked.connect(self.on_nav_sw_pressed)
        self.pushButton_nav_w.clicked.connect(self.on_nav_w_pressed)
        self.pushButton_nav_nw.clicked.connect(self.on_nav_nw_pressed)

        self.spinBox_qq.valueChanged.connect(self.on_spinBox_qq_changed)
        self.spinBox_nn.valueChanged.connect(self.on_spinBox_nn_changed)
        self.spinBox_zz.valueChanged.connect(self.on_spinBox_zz_changed)

        self.comboBox_name.currentIndexChanged.connect(self.on_comboBox_name_changed)
        self.comboBox_ring.currentIndexChanged.connect(self.on_comboBox_ring_changed)

    def show_about_dialog(self):
        about_dialog = QDialog()
        about_dialog.ui = Ui_AbooutDialog()
        about_dialog.ui.setupUi(about_dialog)
        about_dialog.ui.label_version.setText('Version: {}'.format(__version__))
        about_dialog.exec_()
        about_dialog.show()

    def show_message(self, message):
        """
        Implementation of an abstract method:
        Show text in status bar
        :param message:
        :return:
        """
        self.statusbar.showMessage(message)

    def show_message_box(self, text):
        """
        Implementation of an abstract method:
        Display a message box.
        :param text:
        :return:
        """
        reply = QMessageBox.question(self, 'Message',
                                     text, QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def show_isotopes(self):
        """
        SLOT
        show isotopes
        :return:
        """
        self.reinit_particle()
        p_array = self.particle.get_isotopes()
        text = 'Isotopes of {} are:\n'.format(self.particle) + '\n'.join(map(str, p_array)) + '\n'
        self.plainTextEdit.appendPlainText(text)

    def show_isotones(self):
        """
        SLOT
        show isotones
        :return:
        """
        self.reinit_particle()
        text = 'Isotones of {} are:\n'.format(self.particle) + '\n'.join(map(str, self.particle.get_isotones())) + '\n'
        self.plainTextEdit.appendPlainText(text)

    def show_isobars(self):
        """
        SLOT
        show isobars
        :return:
        """
        self.reinit_particle()
        text = 'Isobars of {} are:\n'.format(self.particle) + '\n'.join(map(str, self.particle.get_isobars())) + '\n'
        self.plainTextEdit.appendPlainText(text)

    def save_file_dialog(self):
        """
        Show a save file dialog
        :return:
        """
        file_name, _ = QFileDialog.getSaveFileName(self, "Save results", '',
                                                   "Text file (*.txt)")
        if not file_name:
            return
        self.save_results(file_name)

    def save_results(self, file_name):
        """
        Save results to fiven filename.
        :param file_name:
        :return:
        """
        if not self.plainTextEdit.toPlainText():
            self.show_message('No results to save.')
            return

        with open(file_name, 'w') as f:
            f.write(str(self.plainTextEdit.toPlainText()))
            self.show_message('Wrote to file {}.'.format(file_name))

    def check_nuclide_validity(self):
        """
        Check if the given nuclide exists in the table
        :return:
        """
        nuclide_validity = True
        if '{}_{}'.format(self.spinBox_zz.value(), self.spinBox_nn.value()) in self.ame_data.zz_nn_names_dic:
            aa = self.spinBox_zz.value() + self.spinBox_nn.value()
            self.label_name.setText(
                '{} {} {}+'.format(aa, self.ame_data.zz_nn_names_dic[
                    '{}_{}'.format(self.spinBox_zz.value(), self.spinBox_nn.value())], self.spinBox_qq.value()))
            self.show_message('Valid nuclide')
        else:
            self.label_name.setText('------')
            self.show_message('Not a valid nuclide')
            nuclide_validity = False
        return nuclide_validity

    def reinit_particle(self):
        """
        Re initialize the particle with new values
        :return:
        """
        if self.check_nuclide_validity():
            # Here make a particle
            zz = self.spinBox_zz.value()
            nn = self.spinBox_nn.value()
            self.particle = Particle(zz, nn, self.ame_data, self.ring_dict[self.current_ring_name])
            self.particle.qq = self.spinBox_qq.value()
            self.particle.ke_u = self.doubleSpinBox_energy.value()
            self.particle.i_beam_uA = self.doubleSpinBox_beam_current.value()
            self.particle.f_analysis_mhz = self.doubleSpinBox_f_analysis.value()
            if not self.checkBox_circum.isChecked():
                self.particle.path_length_m = self.doubleSpinBox_path_length.value()
            else:
                self.particle.path_length_m = self.ring_dict[self.current_ring_name].circumference

    def keyPressEvent(self, event):
        """
        Keypress event handler
        :return:
        """
        if type(event) == QKeyEvent:
            # here accept the event and do something
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:  # code enter key
                # self.do_calculate()
                self.on_pushButton_calculate()
                event.accept()
            if event.key() == Qt.Key_Space:
                # self.on_pushButton_table_data()
                event.accept()
            if event.key() == Qt.Key_Up:
                print('up')
                event.accept()
        else:
            event.ignore()

    def on_spinBox_zz_changed(self):
        """
        SLOT
        :return:
        """
        self.spinBox_zz.setMinimum(1)
        self.spinBox_zz.setMaximum(self.ame_data.zz_max)
        self.comboBox_name.setCurrentIndex(self.spinBox_zz.value())
        if self.spinBox_qq.value() > self.spinBox_zz.value():
            self.spinBox_qq.setValue(self.spinBox_zz.value())
        self.check_nuclide_validity()

    def on_spinBox_nn_changed(self):
        """
        SLOT
        :return:
        """
        self.spinBox_nn.setMinimum(0)
        self.spinBox_nn.setMaximum(self.ame_data.nn_max)
        self.check_nuclide_validity()

    def on_spinBox_qq_changed(self):
        """
        SLOT
        :return:
        """
        self.spinBox_qq.setMinimum(1)
        self.spinBox_qq.setMaximum(self.ame_data.zz_max)
        if self.spinBox_qq.value() > self.spinBox_zz.value():
            self.spinBox_qq.setValue(self.spinBox_zz.value())
        self.check_nuclide_validity()

    def on_comboBox_name_changed(self, idx):
        """
        SLOT
        :return:
        """
        self.spinBox_zz.setValue(idx)
        self.spinBox_nn.setValue(idx)
        self.spinBox_qq.setValue(idx)

    def on_comboBox_ring_changed(self, idx):
        # ignore index for now
        self.current_ring_name = self.comboBox_ring.itemText(idx)

    def on_pushButton_calculate(self):
        """
        SLOT
        :return:
        """
        self.do_calculate()

    def on_pushButton_clear(self):
        self.plainTextEdit.clear()
        self.setup_table_view()

    def do_calculate(self):
        """
        SLOT
        Do the actual calculation
        :return:
        """
        if self.check_nuclide_validity():
            self.show_message('Valid nuclide.')
            self.reinit_particle()
            self.update_table_view()
        else:
            self.show_message('Not a valid nuclide.')

    def on_pushButton_copy_table(self):
        self.plainTextEdit.appendPlainText(self.particle.calculate_from_energy())

    def on_pushButton_table_data(self):
        """
        SLOT
        :return:
        """
        self.reinit_particle()
        self.plainTextEdit.appendPlainText(self.particle.get_table_data())

    def on_pushButton_identify(self):
        # update rings etc...
        self.reinit_particle()
        try:
            f_actual = float(self.lineEdit_f_actual.text())
            f_unknown = float(self.lineEdit_f_unknown.text())
        except(ValueError):
            self.show_message('Please enter valid frequencies in the text field.')
            return

        range_zz = self.spinBox_range_zz.value()
        range_nn = self.spinBox_range_nn.value()
        max_ee = self.spinBox_max_ee.value()
        accuracy = self.doubleSpinBox_accuracy.value()
        self.plainTextEdit.appendPlainText(
            self.particle.identify(float(f_actual), float(f_unknown), range_zz, range_nn, max_ee, accuracy))

        self.show_message('You may narrow your search either by reducing search area or the sensitivity radius.')

    def on_nav_n_pressed(self):
        """
        SLOT
        :return:
        """
        zz = self.spinBox_zz.value()
        self.spinBox_zz.setValue(zz + 1)

    def on_nav_ne_pressed(self):
        """
        SLOT
        :return:
        """
        zz = self.spinBox_zz.value()
        nn = self.spinBox_nn.value()
        self.spinBox_zz.setValue(zz + 1)
        self.spinBox_nn.setValue(nn + 1)

    def on_nav_e_pressed(self):
        """
        SLOT
        :return:
        """
        nn = self.spinBox_nn.value()
        self.spinBox_nn.setValue(nn + 1)

    def on_nav_se_pressed(self):
        """
        SLOT
        :return:
        """
        zz = self.spinBox_zz.value()
        nn = self.spinBox_nn.value()
        self.spinBox_zz.setValue(zz - 1)
        self.spinBox_nn.setValue(nn + 1)

    def on_nav_s_pressed(self):
        """
        SLOT
        :return:
        """
        zz = self.spinBox_zz.value()
        self.spinBox_zz.setValue(zz - 1)

    def on_nav_sw_pressed(self):
        """
        SLOT
        :return:
        """
        zz = self.spinBox_zz.value()
        nn = self.spinBox_nn.value()
        self.spinBox_zz.setValue(zz - 1)
        self.spinBox_nn.setValue(nn - 1)

    def on_nav_w_pressed(self):
        """
        SLOT
        :return:
        """
        nn = self.spinBox_nn.value()
        self.spinBox_nn.setValue(nn - 1)

    def on_nav_nw_pressed(self):
        """
        SLOT
        :return:
        """
        zz = self.spinBox_zz.value()
        nn = self.spinBox_nn.value()
        self.spinBox_zz.setValue(zz + 1)
        self.spinBox_nn.setValue(nn - 1)

    def update_table_view(self):
        lst = self.particle.calculate_from_energy_list()
        for i in range(len(lst)):
            for j in range(len(lst[0])):
                item = QStandardItem(lst[i][j])
                self.tableView_model.setItem(i, j, item)
        self.tableView.resizeColumnsToContents()
