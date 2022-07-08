from time import sleep

import pandas as pd
from PyQt5 import QtWidgets
import sys
import resources_rc
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import Utilities_GUI
import Utilities_functions
import itemsHW
from ui_Pico import Ui_pico_window
from ui_SRAN import Ui_SRANSiteDWO
from ui_TDD import Ui_tddWindow
from ui_WelcomeWindow import Ui_welcomeWindow
from ui_UpgradeWindow import Ui_upgradeWindow
from ui_NewsiteTechWindow import Ui_NewsiteWindow


class WelcomeWindow(QtWidgets.QMainWindow, Ui_welcomeWindow):
    def __init__(self, parent=None):
        super(WelcomeWindow, self).__init__(parent)
        self.setupUi(self)
        self.newsiteWinBtn.setEnabled(False)
        self.upgradeWinBtn.setEnabled(False)
        self.tddWinBtn.setEnabled(False)
        self.upload_stock_btn.clicked.connect(lambda: Utilities_functions.prepare_stock_wb(self))


class SRAN_DWO(QtWidgets.QMainWindow, Ui_SRANSiteDWO):
    def __init__(self, parent=None):
        super(SRAN_DWO, self).__init__(parent)
        self.setupUi(self)
        Utilities_GUI.initial_SRAN_GUI(self)
        self.exitBtn_SRAN.clicked.connect(self.close)
        self.checkBox_GSM.stateChanged.connect(lambda: Utilities_GUI.checkBox_GSM_clicked(self))
        self.checkBox_DCS.stateChanged.connect(lambda: Utilities_GUI.checkBox_DCS_clicked(self))
        self.checkBox_U900.stateChanged.connect(lambda: Utilities_GUI.checkBox_U900_clicked(self))
        self.checkBox_U2100.stateChanged.connect(lambda: [Utilities_GUI.checkBox_U2100_clicked(self),
                                                          self.calculate_UMTS_SUs()])
        self.checkBox_L900.stateChanged.connect(lambda: Utilities_GUI.checkBox_L900_clicked(self))
        self.checkBox_L1800.stateChanged.connect(lambda: Utilities_GUI.checkBox_L1800_clicked(self))
        self.checkBox_L2100.stateChanged.connect(lambda: Utilities_GUI.checkBox_L2100_clicked(self))
        self.executeBtn_SRAN.clicked.connect(self.executeBtn_click)
        self.extract_consolidated_SRAN.clicked.connect(self.extract_consolidated_click)
        self.saveBtn_SRAN.clicked.connect(self.saveBtn_click)

    # Get configuration data from user
    def get_siteName(self):
        return self.siteName_SRAN.text()

    def get_woID(self):
        return self.woID_SRAN.text()

    def get_type_RRH(self):
        return self.RRHtype_SRAN.currentText()

    def get_type_jumper(self):
        return self.jumperType_SRAN.currentText()

    def get_num_of_sectors(self):
        return self.sectors_SRAN.value()

    def get_MIMO_solution(self):
        return self.L1800_MIMO.currentText()

    def get_type_RF900(self):
        return self.B900_RFtype.currentText()

    def get_type_RF1800(self):
        return self.B1800_RFtype.currentText()

    def get_type_RF2100(self):
        return self.B2100_RFtype.currentText()

    def get_L1800_BW(self):
        if self.checkBox_L1800.isChecked():
            L1800_BW = self.L1800_BW.currentText()
        else:
            L1800_BW = 0
        return L1800_BW

    def get_L2100_BW(self):
        if self.checkBox_L2100.isChecked():
            L2100_BW = self.L2100_BW.currentText()
        else:
            L2100_BW = 0
        return L2100_BW

    def get_L900_BW(self):
        if self.checkBox_L900.isChecked():
            L900_BW = self.L900_BW.currentText()
        else:
            L900_BW = 0
        return L900_BW

    def get_L900_pwr(self):
        if self.checkBox_L900.isChecked():
            pwr_l900 = int(self.L900_pwr.currentText())
        else:
            pwr_l900 = 0
        return pwr_l900

    def get_U900_pwr(self):
        if self.checkBox_U900.isChecked():
            pwr_u900 = self.pwr_U900.currentText()
            pwr_u900 = Utilities_functions.get_power(pwr_u900)
        else:
            pwr_u900 = 0
        return pwr_u900

    def get_L2100_pwr(self):
        if self.checkBox_L2100.isChecked():
            pwr_L2100 = self.L2100_pwr.currentText()
        else:
            pwr_L2100 = 0
        return pwr_L2100

    def get_u2100_pwr(self):
        if self.checkBox_U2100.isChecked():
            pwr_u2100 = self.pwr_U2100.currentText()
            pwr_u2100 = Utilities_functions.get_power(pwr_u2100)
        else:
            pwr_u2100 = 0
        return pwr_u2100

    def get_U2100_carriers(self):
        return self.u2100_carriers.value()

    # Calculate System module quantities for SRAN site

    def calculate_GSM_SUs(self):
        gsm_SU = 0
        if self.checkBox_GSM.isChecked():
            tot_trx = self.trx_S1.value() + self.trx_S2.value() + self.trx_S3.value() + self.trx_S4.value()
            if tot_trx <= 24:
                gsm_SU = 2
            elif 25 <= tot_trx <= 36:
                gsm_SU = 3
        else:
            gsm_SU = 0
        return gsm_SU

    def calculate_UMTS_SUs(self):
        U900_SUs = 0
        U2100_SUs = 0

        if self.checkBox_U900.isChecked() and not self.checkBox_U2100.isChecked():
            U900_SUs = 9.5
            U2100_SUs = 0

        elif not self.checkBox_U900.isChecked() and not self.checkBox_U2100.isChecked():
            U900_SUs = 0
            U2100_SUs = 0

        elif self.checkBox_U2100.isChecked() and self.checkBox_U900.isChecked():
            if self.get_num_of_sectors() <= 3:
                self.CE_2100.setText("330")
                self.HSDPA_2100.setText("2")
                self.HSUPA_2100.setText("4")
                U2100_SUs = 11.5
                U900_SUs = 0
            elif self.get_num_of_sectors() >= 4:
                self.CE_2100.setText("450")
                self.HSDPA_2100.setText("3")
                self.HSUPA_2100.setText("6")
                U2100_SUs = 15.5
                U900_SUs = 0
        elif self.checkBox_U2100.isChecked() and not self.checkBox_U900.isChecked():
            if self.get_num_of_sectors() <= 3:
                self.CE_2100.setText("330")
                self.HSDPA_2100.setText("2")
                self.HSUPA_2100.setText("4")
                U2100_SUs = 9.5
                U900_SUs = 0
            elif self.get_num_of_sectors() >= 4:
                self.CE_2100.setText("450")
                self.HSDPA_2100.setText("3")
                self.HSUPA_2100.setText("6")
                U2100_SUs = 11.5
                U900_SUs = 0
        UMTS_SUs = U2100_SUs + U900_SUs
        return UMTS_SUs

    def GU_SBTS_SUs(self):
        qty_FSMF_GU = 0
        qty_FBBC_GU = 0
        SUs_G_U = self.calculate_GSM_SUs() + self.calculate_UMTS_SUs()
        if SUs_G_U == 0:
            pass
        elif 0 < SUs_G_U <= 5.5:
            qty_FSMF_GU = 1
            qty_FBBC_GU = 0
        elif 5.5 < SUs_G_U <= 11.5:
            qty_FSMF_GU = 1
            qty_FBBC_GU = 1
        elif 11.5 < SUs_G_U <= 17.5:
            qty_FSMF_GU = 1
            qty_FBBC_GU = 2
        else:
            pass
        return qty_FSMF_GU, qty_FBBC_GU

    def calculate_LTE_SUs(self):
        L1800_SUs = 0
        L2100_SUs = 0
        L900_SUs = 0
        if self.checkBox_L1800.isChecked():
            if int(self.get_L1800_BW()) >= 15 and self.get_num_of_sectors() <= 3:
                L1800_SUs = 5.5
            elif int(self.get_L1800_BW()) >= 15 and self.get_num_of_sectors() >= 4:
                L1800_SUs = 6.5
            elif int(self.get_L1800_BW()) <= 10 and self.get_num_of_sectors() <= 3:
                L1800_SUs = 5.5
            elif int(self.get_L1800_BW()) <= 10 and self.get_num_of_sectors() >= 4:
                L1800_SUs = 6.5

        if self.checkBox_L900.isChecked():
            if int(self.get_L900_BW()) >= 15 and self.get_num_of_sectors() <= 3:
                L900_SUs = 5.5
            elif int(self.get_L900_BW()) >= 15 and self.get_num_of_sectors() >= 4:
                L900_SUs = 6.5
            elif int(self.get_L900_BW()) <= 10 and self.get_num_of_sectors() <= 3:
                L900_SUs = 3
            elif int(self.get_L900_BW()) <= 10 and self.get_num_of_sectors() >= 4:
                L900_SUs = 4

        if self.checkBox_L2100.isChecked():
            if int(self.get_L2100_BW()) >= 15 and self.get_num_of_sectors() <= 3:
                L2100_SUs = 5.5
            elif int(self.get_L2100_BW()) >= 15 and self.get_num_of_sectors() >= 4:
                L2100_SUs = 6.5
            elif int(self.get_L2100_BW()) <= 10 and self.get_num_of_sectors() <= 3:
                L2100_SUs = 3
            elif int(self.get_L2100_BW()) <= 10 and self.get_num_of_sectors() >= 4:
                L2100_SUs = 4

        LTE_SUs = L900_SUs + L1800_SUs + L2100_SUs
        return LTE_SUs

    def LTE_SBTS_SUs(self):
        qty_FSMF_L = 0
        qty_FBBC_L = 0
        LTE_SUs = self.calculate_LTE_SUs()
        if LTE_SUs == 0:
            pass
        elif 0 < LTE_SUs <= 5.5:
            qty_FSMF_L = 1
            qty_FBBC_L = 0
        elif 5.5 < LTE_SUs <= 11.5:
            qty_FSMF_L = 1
            qty_FBBC_L = 1
        elif 11.5 < LTE_SUs <= 17.5:
            qty_FSMF_L = 1
            qty_FBBC_L = 2
        else:
            pass
        return qty_FSMF_L, qty_FBBC_L

    # RF Quantity for Band 900 Calculations
    def get_trx_cnt_s1(self):
        return self.trx_S1.value()

    def get_trx_cnt_s2(self):
        return self.trx_S2.value()

    def get_trx_cnt_s3(self):
        return self.trx_S3.value()

    def get_trx_cnt_s4(self):
        return self.trx_S4.value()

    def get_trx_pwr_s1(self):
        trxS1_Pwr = Utilities_functions.get_power(self.trxS1_Pwr.currentText())
        return trxS1_Pwr

    def get_trx_pwr_s2(self):
        trxS2_Pwr = Utilities_functions.get_power(self.trxS2_Pwr.currentText())
        return trxS2_Pwr

    def get_trx_pwr_s3(self):
        trxS3_Pwr = Utilities_functions.get_power(self.trxS3_Pwr.currentText())
        return trxS3_Pwr

    def get_trx_pwr_s4(self):
        trxS4_Pwr = Utilities_functions.get_power(self.trxS4_Pwr.currentText())
        return trxS4_Pwr

    def get_pipe_cnt_gsm_s1(self):
        pipe_cnt_s1 = 0
        pipe1_capacity = []
        pipe2_capacity = []
        pipe3_capacity = []

        if self.checkBox_L900.isChecked():
            pipe1_capacity.append(self.get_L900_pwr())
            pipe2_capacity.append(self.get_L900_pwr())
        else:
            pass

        if self.checkBox_U900.isChecked():
            if sum(pipe1_capacity) <= (73 - self.get_U900_pwr()):
                pipe1_capacity.append(self.get_U900_pwr())
            elif sum(pipe2_capacity) <= (73 - self.get_U900_pwr()):
                pipe2_capacity.append(self.get_U900_pwr())
            else:
                pipe3_capacity.append(self.get_U900_pwr())

        if self.get_trx_cnt_s1() == 0:
            pipe_cnt_s1 = 0
        elif 1 <= self.get_trx_cnt_s1() <= 4:
            gsm_pwr = self.get_trx_pwr_s1() * self.get_trx_cnt_s1()
            if sum(pipe1_capacity) <= (73 - gsm_pwr):
                pipe1_capacity.append(gsm_pwr)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr):
                pipe2_capacity.append(gsm_pwr)
            else:
                pipe3_capacity.append(gsm_pwr)
        elif 4 < self.get_trx_cnt_s1() <= 8:
            gsm_pwr_1 = self.get_trx_pwr_s1() * 4
            gsm_pwr_remaining = self.get_trx_pwr_s1() * (self.get_trx_cnt_s1() - 4)
            if sum(pipe1_capacity) <= (73 - gsm_pwr_1):
                pipe1_capacity.append(gsm_pwr_1)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_1):
                pipe2_capacity.append(gsm_pwr_1)
            else:
                pipe3_capacity.append(gsm_pwr_1)

            if sum(pipe1_capacity) <= (73 - gsm_pwr_remaining):
                pipe1_capacity.append(gsm_pwr_remaining)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_remaining):
                pipe2_capacity.append(gsm_pwr_remaining)
            else:
                pipe3_capacity.append(gsm_pwr_remaining)

        if sum(pipe1_capacity) > 0:
            pipe_cnt_s1 = pipe_cnt_s1 + 1
        else:
            pipe_cnt_s1 = 0

        if sum(pipe2_capacity) > 0:
            pipe_cnt_s1 = pipe_cnt_s1 + 1
        else:
            pipe_cnt_s1 = pipe_cnt_s1

        if sum(pipe3_capacity) > 0:
            pipe_cnt_s1 = pipe_cnt_s1 + 1

        return pipe_cnt_s1

    def get_pipe_cnt_gsm_s2(self):
        pipe_cnt_s2 = 0
        pipe1_capacity = []
        pipe2_capacity = []
        pipe3_capacity = []

        if self.checkBox_L900.isChecked():
            pipe1_capacity.append(self.get_L900_pwr())
            pipe2_capacity.append(self.get_L900_pwr())
        else:
            pass

        if self.checkBox_U900.isChecked():
            if sum(pipe1_capacity) <= (73 - self.get_U900_pwr()):
                pipe1_capacity.append(self.get_U900_pwr())
            elif sum(pipe2_capacity) <= (73 - self.get_U900_pwr()):
                pipe2_capacity.append(self.get_U900_pwr())
            else:
                pipe3_capacity.append(self.get_U900_pwr())

        if self.get_trx_cnt_s2() == 0:
            pipe_cnt_s2 = 0
        elif 1 <= self.get_trx_cnt_s2() <= 4:
            gsm_pwr = self.get_trx_pwr_s2() * self.get_trx_cnt_s2()
            if sum(pipe1_capacity) <= (73 - gsm_pwr):
                pipe1_capacity.append(gsm_pwr)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr):
                pipe2_capacity.append(gsm_pwr)
            else:
                pipe3_capacity.append(gsm_pwr)
        elif 4 < self.get_trx_cnt_s2() <= 6:
            gsm_pwr_1 = self.get_trx_pwr_s2() * 4
            gsm_pwr_remaining = self.get_trx_pwr_s2() * (self.get_trx_cnt_s2() - 4)
            if sum(pipe1_capacity) <= (73 - gsm_pwr_1):
                pipe1_capacity.append(gsm_pwr_1)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_1):
                pipe2_capacity.append(gsm_pwr_1)
            else:
                pipe3_capacity.append(gsm_pwr_1)

            if sum(pipe1_capacity) <= (73 - gsm_pwr_remaining):
                pipe1_capacity.append(gsm_pwr_remaining)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_remaining):
                pipe2_capacity.append(gsm_pwr_remaining)
            else:
                pipe3_capacity.append(gsm_pwr_remaining)

        if sum(pipe1_capacity) > 0:
            pipe_cnt_s2 = pipe_cnt_s2 + 1
        else:
            pipe_cnt_s2 = 0

        if sum(pipe2_capacity) > 0:
            pipe_cnt_s2 = pipe_cnt_s2 + 1
        else:
            pipe_cnt_s2 = pipe_cnt_s2

        if sum(pipe3_capacity) > 0:
            pipe_cnt_s2 = pipe_cnt_s2 + 1

        return pipe_cnt_s2

    def get_pipe_cnt_gsm_s3(self):
        pipe_cnt_s3 = 0
        pipe1_capacity = []
        pipe2_capacity = []
        pipe3_capacity = []

        if self.checkBox_L900.isChecked():
            pipe1_capacity.append(self.get_L900_pwr())
            pipe2_capacity.append(self.get_L900_pwr())
        else:
            pass

        if self.checkBox_U900.isChecked():
            if sum(pipe1_capacity) <= (73 - self.get_U900_pwr()):
                pipe1_capacity.append(self.get_U900_pwr())
            elif sum(pipe2_capacity) <= (73 - self.get_U900_pwr()):
                pipe2_capacity.append(self.get_U900_pwr())
            else:
                pipe3_capacity.append(self.get_U900_pwr())

        if self.get_trx_cnt_s3() == 0:
            pipe_cnt_s3 = 0
        elif 1 <= self.get_trx_cnt_s3() <= 4:
            gsm_pwr = self.get_trx_pwr_s3() * self.get_trx_cnt_s3()
            if sum(pipe1_capacity) <= (73 - gsm_pwr):
                pipe1_capacity.append(gsm_pwr)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr):
                pipe2_capacity.append(gsm_pwr)
            else:
                pipe3_capacity.append(gsm_pwr)
        elif 4 < self.get_trx_cnt_s3() <= 6:
            gsm_pwr_1 = self.get_trx_pwr_s3() * 4
            gsm_pwr_remaining = self.get_trx_pwr_s3() * (self.get_trx_cnt_s3() - 4)
            if sum(pipe1_capacity) <= (73 - gsm_pwr_1):
                pipe1_capacity.append(gsm_pwr_1)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_1):
                pipe2_capacity.append(gsm_pwr_1)
            else:
                pipe3_capacity.append(gsm_pwr_1)

            if sum(pipe1_capacity) <= (73 - gsm_pwr_remaining):
                pipe1_capacity.append(gsm_pwr_remaining)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_remaining):
                pipe2_capacity.append(gsm_pwr_remaining)
            else:
                pipe3_capacity.append(gsm_pwr_remaining)

        if sum(pipe1_capacity) > 0:
            pipe_cnt_s3 = pipe_cnt_s3 + 1
        else:
            pipe_cnt_s3 = 0

        if sum(pipe2_capacity) > 0:
            pipe_cnt_s3 = pipe_cnt_s3 + 1
        else:
            pipe_cnt_s3 = pipe_cnt_s3

        if sum(pipe3_capacity) > 0:
            pipe_cnt_s3 = pipe_cnt_s3 + 1

        return pipe_cnt_s3

    def get_pipe_cnt_gsm_s4(self):
        pipe_cnt_s4 = 0
        pipe1_capacity = []
        pipe2_capacity = []
        pipe3_capacity = []

        if self.checkBox_L900.isChecked():
            pipe1_capacity.append(self.get_L900_pwr())
            pipe2_capacity.append(self.get_L900_pwr())
        else:
            pass

        if self.checkBox_U900.isChecked():
            if sum(pipe1_capacity) <= (73 - self.get_U900_pwr()):
                pipe1_capacity.append(self.get_U900_pwr())
            elif sum(pipe2_capacity) <= (73 - self.get_U900_pwr()):
                pipe2_capacity.append(self.get_U900_pwr())
            else:
                pipe3_capacity.append(self.get_U900_pwr())

        if self.get_trx_cnt_s4() == 0:
            pipe_cnt_s4 = 0
        elif 1 <= self.get_trx_cnt_s4() <= 4:
            gsm_pwr = self.get_trx_pwr_s4() * self.get_trx_cnt_s4()
            if sum(pipe1_capacity) <= (73 - gsm_pwr):
                pipe1_capacity.append(gsm_pwr)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr):
                pipe2_capacity.append(gsm_pwr)
            else:
                pipe3_capacity.append(gsm_pwr)
        elif 4 < self.get_trx_cnt_s4() <= 6:
            gsm_pwr_1 = self.get_trx_pwr_s4() * 4
            gsm_pwr_remaining = self.get_trx_pwr_s4() * (self.get_trx_cnt_s4() - 4)
            if sum(pipe1_capacity) <= (73 - gsm_pwr_1):
                pipe1_capacity.append(gsm_pwr_1)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_1):
                pipe2_capacity.append(gsm_pwr_1)
            else:
                pipe3_capacity.append(gsm_pwr_1)

            if sum(pipe1_capacity) <= (73 - gsm_pwr_remaining):
                pipe1_capacity.append(gsm_pwr_remaining)
            elif sum(pipe2_capacity) <= (73 - gsm_pwr_remaining):
                pipe2_capacity.append(gsm_pwr_remaining)
            else:
                pipe3_capacity.append(gsm_pwr_remaining)

        if sum(pipe1_capacity) > 0:
            pipe_cnt_s4 = pipe_cnt_s4 + 1
        else:
            pipe_cnt_s4 = 0

        if sum(pipe2_capacity) > 0:
            pipe_cnt_s4 = pipe_cnt_s4 + 1
        else:
            pipe_cnt_s4 = pipe_cnt_s4

        if sum(pipe3_capacity) > 0:
            pipe_cnt_s4 = pipe_cnt_s4 + 1

        return pipe_cnt_s4

    def get_qty_rf_b900(self):
        qty_rf_b900 = 0
        pipe_list_b900 = []
        if self.get_num_of_sectors() == 0:
            pipe_list_b900 = [0, 0, 0, 0]
        elif self.get_num_of_sectors() == 1:
            pipe_list_b900 = [self.get_pipe_cnt_gsm_s1(), 0, 0, 0]
        elif self.get_num_of_sectors() == 2:
            pipe_list_b900 = [self.get_pipe_cnt_gsm_s1(), self.get_pipe_cnt_gsm_s2(), 0, 0]
        elif self.get_num_of_sectors() == 3:
            pipe_list_b900 = [self.get_pipe_cnt_gsm_s1(), self.get_pipe_cnt_gsm_s2(), self.get_pipe_cnt_gsm_s3(), 0]
        elif self.get_num_of_sectors() == 4:
            pipe_list_b900 = [self.get_pipe_cnt_gsm_s1(), self.get_pipe_cnt_gsm_s2(),
                              self.get_pipe_cnt_gsm_s3(), self.get_pipe_cnt_gsm_s4()]

        if sum(pipe_list_b900) == 0:
            qty_rf_b900 = 0
        elif 0 < sum(pipe_list_b900) <= 3:
            qty_rf_b900 = 1
        elif 3 < sum(pipe_list_b900) <= 6:
            if self.get_type_RF900() == "FXDB":
                qty_rf_b900 = 2
            elif self.get_type_RF900() == "ARDA":
                qty_rf_b900 = 1
        elif 6 < sum(pipe_list_b900) <= 9:
            if self.get_type_RF900() == "FXDB":
                qty_rf_b900 = 3
            elif self.get_type_RF900() == "ARDA":
                qty_rf_b900 = 2
        elif 9 < sum(pipe_list_b900) <= 12:
            if self.get_type_RF900() == "FXDB":
                qty_rf_b900 = 4
            elif self.get_type_RF900() == "ARDA":
                if self.get_num_of_sectors() == 3:
                    qty_rf_b900 = 2
                elif self.get_num_of_sectors() == 4:
                    qty_rf_b900 = 3

        return qty_rf_b900

    # Calculate RF quantity for B1800
    def get_qty_rf_b1800(self):
        qty_rf_b1800 = 0
        if self.checkBox_L1800.isChecked():
            if self.get_num_of_sectors() == 1:
                if self.get_type_RF1800() == "FXED" or self.get_type_RF1800() == "FXEB":
                    qty_rf_b1800 = 1
                elif self.get_type_RF1800() == "AREA":
                    qty_rf_b1800 = 1
            elif self.get_num_of_sectors() == 2:
                if self.get_type_RF1800() == "FXED" or self.get_type_RF1800() == "FXEB":
                    qty_rf_b1800 = 2
                elif self.get_type_RF1800() == "AREA":
                    qty_rf_b1800 = 1
            elif self.get_num_of_sectors() == 3:
                if self.get_type_RF1800() == "FXED" or self.get_type_RF1800() == "FXEB":
                    qty_rf_b1800 = 2
                elif self.get_type_RF1800() == "AREA":
                    qty_rf_b1800 = 1
            elif self.get_num_of_sectors() == 4:
                if self.get_type_RF1800() == "FXED" or self.get_type_RF1800() == "FXEB":
                    qty_rf_b1800 = 3
                elif self.get_type_RF1800() == "AREA":
                    qty_rf_b1800 = 2
        return qty_rf_b1800

    # Calculate RF quantity for B2100
    def get_qty_rf_b2100(self):
        pipe_count = 0
        num_of_sectors = 1
        qty_rf_b2100 = 0

        pipe1_capacity = []
        pipe2_capacity = []
        pipe3_capacity = []
        pipe_count_list = []
        while num_of_sectors != (self.get_num_of_sectors() + 1):
            if self.checkBox_L2100.isChecked():
                pipe1_capacity.append(int(self.get_L2100_pwr()))
                pipe2_capacity.append(int(self.get_L2100_pwr()))
            else:
                pass

            for i in range(int(self.get_U2100_carriers())):
                if self.get_type_RF2100() == "FRGT" or self.get_type_RF2100() == "FRGX" \
                        or self.get_type_RF2100() == "ARGA":
                    if i <= 1:
                        if sum(pipe1_capacity) <= (80 - self.get_u2100_pwr()):
                            pipe1_capacity.append(self.get_u2100_pwr())
                        elif sum(pipe2_capacity) <= (80 - self.get_u2100_pwr()):
                            pipe2_capacity.append(self.get_u2100_pwr())
                        else:
                            pipe3_capacity.append(self.get_u2100_pwr())
                    elif i == 2:
                        if sum(pipe1_capacity) <= (80 - (self.get_u2100_pwr() / 2)):
                            pipe1_capacity.append(self.get_u2100_pwr())
                        elif sum(pipe2_capacity) <= (80 - (self.get_u2100_pwr() / 2)):
                            pipe2_capacity.append(self.get_u2100_pwr())
                        else:
                            pipe3_capacity.append(self.get_u2100_pwr())
                elif self.get_type_RF2100() == "FRGU":
                    if i <= 1:
                        if sum(pipe1_capacity) <= (60 - self.get_u2100_pwr()):
                            pipe1_capacity.append(self.get_u2100_pwr())
                        elif sum(pipe2_capacity) <= (60 - self.get_u2100_pwr()):
                            pipe2_capacity.append(self.get_u2100_pwr())
                        else:
                            pipe3_capacity.append(self.get_u2100_pwr())
                    elif i == 2:
                        if sum(pipe1_capacity) <= (60 - (self.get_u2100_pwr() / 2)):
                            pipe1_capacity.append(self.get_u2100_pwr())
                        elif sum(pipe2_capacity) <= (60 - (self.get_u2100_pwr() / 2)):
                            pipe2_capacity.append(self.get_u2100_pwr())
                        else:
                            pipe3_capacity.append(self.get_u2100_pwr())

            if sum(pipe1_capacity) > 0:
                pipe_count = pipe_count + 1
            else:
                pipe_count = 0

            if sum(pipe2_capacity) > 0:
                pipe_count = pipe_count + 1
            else:
                pipe_count = pipe_count

            if sum(pipe3_capacity) > 0:
                pipe_count = pipe_count + 1

            pipe_count_list.append(pipe_count)

            pipe_count = 0
            pipe1_capacity = []
            pipe2_capacity = []
            pipe3_capacity = []
            num_of_sectors = num_of_sectors + 1

        if sum(pipe_count_list) == 0:
            qty_rf_b2100 = 0
        elif 0 < sum(pipe_count_list) <= 3:
            qty_rf_b2100 = 1
        elif 3 < sum(pipe_count_list) <= 6:
            if self.get_type_RF2100() == "FRGT" or self.get_type_RF2100() == "FRGX":
                qty_rf_b2100 = 2
            elif self.get_type_RF2100() == "ARGA" or self.get_type_RF2100() == "FRGU":
                qty_rf_b2100 = 1
        elif 6 < sum(pipe_count_list) <= 9:
            if self.get_type_RF2100() == "FRGT" or self.get_type_RF2100() == "FRGX":
                qty_rf_b2100 = 3
            elif self.get_type_RF2100() == "ARGA" or self.get_type_RF2100() == "FRGU":
                qty_rf_b2100 = 2
        elif 9 < sum(pipe_count_list) <= 12:
            if self.get_type_RF2100() == "FRGT" or self.get_type_RF2100() == "FRGX":
                qty_rf_b2100 = 4
            elif self.get_type_RF2100() == "ARGA" or self.get_type_RF2100() == "FRGU":
                if self.get_num_of_sectors() == 3:
                    qty_rf_b2100 = 2
                elif self.get_num_of_sectors() == 4:
                    qty_rf_b2100 = 3

        return qty_rf_b2100

    def get_qty_rf_DCS(self):
        global trx_DCS_list
        qty_RF_DCS = 0
        if self.dcs_RFtype.currentText() == "AREA Sharing":
            qty_RF_DCS = 0
        elif self.dcs_RFtype.currentText() == "FXEB" or self.dcs_RFtype.currentText() == "FXEF":
            if self.get_num_of_sectors() == 0:
                trx_DCS_list = [0, 0, 0, 0]
            elif self.get_num_of_sectors() == 1:
                trx_DCS_list = [self.trx_S1_dcs.value(), 0, 0, 0]
            elif self.get_num_of_sectors() == 2:
                trx_DCS_list = [self.trx_S1_dcs.value(), self.trx_S2_dcs.value(), 0, 0]
            elif self.get_num_of_sectors() == 3:
                trx_DCS_list = [self.trx_S1_dcs.value(), self.trx_S2_dcs.value(), self.trx_S3_dcs.value(), 0]
            elif self.get_num_of_sectors() == 4:
                trx_DCS_list = [self.trx_S1_dcs.value(), self.trx_S2_dcs.value(), self.trx_S3_dcs.value(),
                                self.trx_S4_dcs.value()]

            pipe_DCS = []
            for i in trx_DCS_list:
                if i == 0:
                    pipe_DCS.append(0)
                else:
                    pipe_DCS.append(1)
            if sum(pipe_DCS) == 0:
                qty_RF_DCS = 0
            elif sum(pipe_DCS) <= 3:
                qty_RF_DCS = 1
            else:
                qty_RF_DCS = 2
        return qty_RF_DCS

    def get_type_RF_DCS(self):
        if self.dcs_RFtype.currentText() == "AREA Sharing":
            type_RF_DCS = self.dcs_RFtype.setCurrentText("")
        else:
            type_RF_DCS = self.dcs_RFtype.currentText()

        return type_RF_DCS

    # Execute Button function
    def executeBtn_click(self):
        qty_FSMF_SRAN = self.GU_SBTS_SUs()[0] + self.LTE_SBTS_SUs()[0]
        qty_FBBC_SRAN = self.GU_SBTS_SUs()[1] + self.LTE_SBTS_SUs()[1]

        self.trgt_FSMF_text.setText("FSMF")
        self.trgt_FBBC_text.setText("FBBC")
        self.trgt_900_text.setText(self.get_type_RF900())
        self.trgt_900RF_qty.setText(str(self.get_qty_rf_b900()))
        self.trgt_1800RF_qty.setText(str(self.get_qty_rf_b1800()))
        self.trgt_2100RF_qty.setText(str(self.get_qty_rf_b2100()))
        self.trgt_2100_text.setText(self.get_type_RF2100())
        self.trgt_1800_text.setText(self.get_type_RF1800())
        self.trgt_FSMF_qty.setText(str(qty_FSMF_SRAN))
        self.trgt_FBBC_qty.setText(str(qty_FBBC_SRAN))
        self.trgt_RF_qty_DCS.setText(str(self.get_qty_rf_DCS()))
        self.trgt_DCS_text.setText(str(self.get_type_RF_DCS()))

    # Get final output of configuration
    def get_MO_qty_FSMF(self):
        return int(self.trgt_FSMF_qty.text())

    def get_MO_qty_FBBC(self):
        return int(self.trgt_FBBC_qty.text())

    def get_MO_qty_RF(self):
        total_needed_RFs = int(self.trgt_900RF_qty.text()) + int(self.trgt_2100RF_qty.text()) + int(
            self.trgt_1800RF_qty.text()) + int(self.trgt_RF_qty_DCS.text())
        return total_needed_RFs

    # Save all items into a MO template for oracle
    def saveBtn_click(self):
        fsmf_MO = itemsHW.SM(self.get_siteName(), self.get_woID(), "FSMF", self.get_MO_qty_FSMF())
        fbbc_MO = itemsHW.SM(self.get_siteName(), self.get_woID(), "FBBC", self.get_MO_qty_FBBC())
        rf900_MO = itemsHW.RF(self.get_siteName(), self.get_woID(), self.get_type_RF900(), self.get_qty_rf_b900())
        rf1800_MO = itemsHW.RF(self.get_siteName(), self.get_woID(), self.get_type_RF1800(), self.get_qty_rf_b1800())
        rf2100_MO = itemsHW.RF(self.get_siteName(), self.get_woID(), self.get_type_RF2100(), self.get_qty_rf_b2100())
        rf_DCS_MO = itemsHW.RF(self.get_siteName(), self.get_woID(), self.get_type_RF_DCS(), self.get_qty_rf_DCS())

        jumper_MO = itemsHW.Jumpers(self.get_siteName(), self.get_woID(), self.get_num_of_sectors(),
                                    self.get_type_jumper(), self.checkBox_GSM.isChecked(),
                                    self.checkBox_DCS.isChecked(),
                                    self.checkBox_U2100.isChecked(), self.checkBox_L1800.isChecked())
        items_MO = itemsHW.HW_items(self.get_siteName(), self.get_woID(), self.get_MO_qty_FSMF(), self.get_MO_qty_RF(),
                                    self.get_type_RRH())

        itemsHW.lists_to_dataframe(itemsHW.list_site_name, itemsHW.list_all_items, itemsHW.list_all_quantities,
                                   itemsHW.list_woID)
        sran_MO = Utilities_functions.df_to_MO_template(
            itemsHW.lists_to_dataframe(itemsHW.list_site_name, itemsHW.list_all_items, itemsHW.list_all_quantities,
                                       itemsHW.list_woID))
        Utilities_functions.save_excel_file(self, sran_MO, self.get_siteName())

    # Extract consolidated sheet for SRAN sites
    def extract_consolidated_click(self):
        empty_df = pd.DataFrame()
        # Consolidate Sheet -- HW Tab
        sheet_HW_headings = ['Site name', 'Code', 'Solution', 'SM', '900 RFs', '1800 RFs', '2100 RFs']
        target_SM = self.trgt_FSMF_qty.text() + self.trgt_FSMF_text.text() + '+' + \
                    self.trgt_FBBC_qty.text() + self.trgt_FBBC_text.text()
        target_900RF = self.trgt_900RF_qty.text() + self.trgt_900_text.text()
        if self.trgt_RF_qty_DCS.text() == 0 or self.trgt_DCS_text.text() == 'None':
            target_1800RF = self.trgt_1800RF_qty.text() + self.trgt_1800_text.text()
        else:
            target_1800RF = self.trgt_1800RF_qty.text() + self.trgt_1800_text.text() + '+' + \
                            self.trgt_RF_qty_DCS.text() + self.trgt_DCS_text.text()
        target_2100RF = self.trgt_2100RF_qty.text() + self.trgt_2100_text.text()
        sheet_HW = pd.DataFrame(columns=sheet_HW_headings)

        content_HW = pd.DataFrame([{'Site name': self.get_siteName(), 'Code': self.get_siteName(), 'Solution': 'SRAN',
                                    'SM': target_SM, '900 RFs': target_900RF, '1800 RFs': target_1800RF,
                                    '2100 RFs': target_2100RF}])
        sheet_HW = sheet_HW.append(content_HW, ignore_index=False)

        # Consolidated Sheet -- Power mapping Tab
        sheet_pwrMAP_headings = ['Site name', 'Code', 'Target GSM Config', 'TRX S1', 'TRX S2', 'TRX S3', 'TRX S4',
                                 'Total GSM TRX', 'Target TRX pwr', 'TRX Pwr S1', 'TRX Pwr S2', 'TRX Pwr S3',
                                 'TRX Pwr S4', 'S1 GSM Total power', 'S2 GSM Total power', 'S3 GSM Total power',
                                 'S4 GSM Total power', 'U900 power S1', 'U900 power S2', 'U900 power S3',
                                 'U900 power S4', '2nd U900 power S1', '2nd U900 power S2', '2nd U900 power S3',
                                 '2nd U900 power S4', 'U2100 F1', 'U2100 F2', 'U2100 F3', 'S1 DCS TRX', 'S2 DCS TRX',
                                 'S3 DCS TRX', 'S4 DCS TRX']
        sheet_pwrMAP = pd.DataFrame(columns=sheet_pwrMAP_headings)
        target_gsm_config = str(self.get_trx_cnt_s1()) + " " + str(self.get_trx_cnt_s2()) + " " + str(
            self.get_trx_cnt_s3()) + " " \
                            + str(self.get_trx_cnt_s4())
        target_gsm_pwr = str(self.get_trx_pwr_s1()) + " " + str(self.get_trx_pwr_s2()) + " " + str(
            self.get_trx_pwr_s3()) \
                         + " " + str(self.get_trx_pwr_s4())

        total_gsm_trx = self.get_trx_cnt_s1() + self.get_trx_cnt_s2() + self.get_trx_cnt_s3() + self.get_trx_cnt_s4()
        content_pwrMAP = [
            {'Site name': self.get_siteName(), 'Code': self.get_siteName(), 'Target GSM Config': target_gsm_config,
             'TRX S1': self.get_trx_cnt_s1(), 'TRX S2': self.get_trx_cnt_s2(), 'TRX S3': self.get_trx_cnt_s3(),
             'TRX S4': self.get_trx_cnt_s4(), 'Total GSM TRX': total_gsm_trx, 'Target TRX pwr': target_gsm_pwr,
             'TRX Pwr S1': self.get_trx_pwr_s1(), 'TRX Pwr S2': self.get_trx_pwr_s2(),
             'TRX Pwr S3': self.get_trx_pwr_s3(), 'TRX Pwr S4': self.get_trx_pwr_s4(),
             'S1 GSM Total power': self.get_trx_pwr_s1() * self.get_trx_cnt_s1(),
             'S2 GSM Total power': self.get_trx_pwr_s2() * self.get_trx_cnt_s2(),
             'S3 GSM Total power': self.get_trx_pwr_s3() * self.get_trx_cnt_s3(),
             'S4 GSM Total power': self.get_trx_pwr_s4() * self.get_trx_cnt_s4(),
             'U900 power S1': self.get_U900_pwr(), 'U900 power S2': self.get_U900_pwr(),
             'U900 power S3': self.get_U900_pwr(), 'U900 power S4': self.get_U900_pwr(),
             '2nd U900 power S1': self.get_U900_pwr(), '2nd U900 power S2': self.get_U900_pwr(),
             '2nd U900 power S3': self.get_U900_pwr(), '2nd U900 power S4': self.get_U900_pwr(),
             'U2100 F1': self.get_u2100_pwr(), 'U2100 F2': self.get_u2100_pwr(), 'U2100 F3': self.get_u2100_pwr(),
             'S1 DCS TRX': self.trx_S1_dcs.value(), 'S2 DCS TRX': self.trx_S2_dcs.value(),
             'S3 DCS TRX': self.trx_S3_dcs.value(), 'S4 DCS TRX': self.trx_S4_dcs.value()}]
        sheet_pwrMAP = sheet_pwrMAP.append(content_pwrMAP, ignore_index=False)

        sheet_cellSet_headings = ['Site name', 'Code', 'SRAN BB cell set', '900 RF cell Set 1', '900 RF cell Set 2',
                                  '900 RF cell Set 3', '2100 RF cell Set 1', '2100 RF cell Set 2', '1800 RF cell Set 1',
                                  '1800 RF cell Set 2']
        sheet_cellSet = pd.DataFrame(columns=sheet_cellSet_headings)
        content_cellSet = [
            {'Site name': self.get_siteName(), 'Code': self.get_siteName(), 'SRAN BB cell set': 'target_gsm_config',
             '900 RF cell Set 1': '', '900 RF cell Set 2': '', '900 RF cell Set 3': '', '2100 RF cell Set 1': '',
             '2100 RF cell Set 2': '', '1800 RF cell Set 1': '', '1800 RF cell Set 2': ''}]

        sheet_cellSet = sheet_cellSet.append(content_cellSet, ignore_index=False)

        response = QFileDialog.getSaveFileName(caption='Save your Consolidated sheet',
                                               directory=f'{self.siteName_SRAN.text()} Consolidated Sheet',
                                               filter="Excel (*.xlsx *.xls *.csv)")
        if response[0] == "":
            Utilities_GUI.success_message(self, "Caution!", "Please specify save location!")
        else:
            writer = pd.ExcelWriter(response[0], engine='openpyxl')
            sheet_HW.to_excel(writer, sheet_name='HW', index=False)
            empty_df.to_excel(writer, sheet_name='IP Design', index=False)
            empty_df.to_excel(writer, sheet_name='Configuration', index=False)
            sheet_cellSet.to_excel(writer, sheet_name='Cell Sets', index=False)
            sheet_pwrMAP.to_excel(writer, sheet_name='Power Mapping', index=False)
            writer.save()
            Utilities_GUI.success_message(self, "Done", "Consolidated sheet extracted!")


class PicoWindow(QtWidgets.QMainWindow, Ui_pico_window):
    def __init__(self, parent=None):
        super(PicoWindow, self).__init__(parent)
        self.setupUi(self)
        self.exitBtn.clicked.connect(lambda: self.close())
        self.saveBtn_pico3G.clicked.connect(lambda: Utilities_functions.save_excel_file(self, self.create_pico_MO(),
                                                                                        self.sitename_Pico.text()))

    def create_pico_MO(self):
        row1 = ""
        row2 = ""
        row3 = ""

        if self.sitename_Pico.text() == "":
            Utilities_GUI.success_message(self, "Caution!", "Please Enter Site name")
            return None
        else:
            if self.woID_Pico.text() == "":
                Utilities_GUI.success_message(self, "Caution!","Please Enter WO ID")
                return None
            else:
                if self.qty_pico.value() <= 0:
                    Utilities_GUI.success_message(self, "Caution!","Quantity of units not valid!")
                    return None
                else:
                    pico_headings = ["Reason", "Item Code", "Quantity", "WO ID"]

                    if self.tech_pico_unit.currentText() == "3G Unit":
                        row1 = [self.sitename_Pico.text(), "BSS-HW-NOKIA-473234A", self.qty_pico.value(),
                                self.woID_Pico.text()]
                        row2 = [self.sitename_Pico.text(), "BSS-HW-NOKIA-473215A", self.qty_pico.value(),
                                self.woID_Pico.text()]

                    elif self.tech_pico_unit.currentText() == "4G Unit":
                        row1 = [self.sitename_Pico.text(), "RAN-HW-NOKIA-473136A", self.qty_pico.value(),
                                self.woID_Pico.text()]
                        row2 = [self.sitename_Pico.text(), "BSS-HW-NOKIA-473215A", self.qty_pico.value(),
                                self.woID_Pico.text()]

                    elif self.tech_pico_unit.currentText() == "3G+4G Unit":
                        row1 = [self.sitename_Pico.text(), "RAN-HW-NOKIA-473136A", self.qty_pico.value(),
                                self.woID_Pico.text()]
                        row2 = [self.sitename_Pico.text(), "BSS-HW-NOKIA-473234A", self.qty_pico.value(),
                                self.woID_Pico.text()]
                        row3 = [self.sitename_Pico.text(), "BSS-HW-NOKIA-473215A", self.qty_pico.value() * 2,
                                self.woID_Pico.text()]

                    pico_output = pd.DataFrame(columns=pico_headings)
                    rows = [row1, row2, row3]
                    for r in range(len(rows)):
                        df_length = len(pico_output)
                        pico_output.loc[df_length] = rows[r]
                    pico_output = pico_output[pico_output.Quantity != ""]

            Utilities_functions.df_to_MO_template(pico_output)
            return pico_output


class UpgradeWindow(QtWidgets.QMainWindow, Ui_upgradeWindow):
    def __init__(self, parent=None):
        super(UpgradeWindow, self).__init__(parent)
        self.setupUi(self)
        Utilities_GUI.upgrade_items_hide(self)
        self.extBtn_upgrade.setEnabled(False)
        self.saveBtn_upgrade.setEnabled(False)
        self.checkBox_all.stateChanged.connect(lambda: Utilities_GUI.upgrade_all_checkBox(self))
        self.checkBox_SM.stateChanged.connect(lambda: Utilities_GUI.upgrade_SM_checkBox(self))
        self.checkBox_RF.stateChanged.connect(lambda: Utilities_GUI.upgrade_RF_checkBox(self))
        self.checkBox_accessories.stateChanged.connect(lambda: Utilities_GUI.upgrade_accessories_checkBox(self))
        self.checkBox_cables.stateChanged.connect(lambda: Utilities_GUI.upgrade_cables_checkBox(self))
        self.checkBox_jumpers.stateChanged.connect(lambda: Utilities_GUI.upgrade_jumpers_checkBox(self))
        self.checkBox_TX.stateChanged.connect(lambda: Utilities_GUI.upgrade_TX_checkBox(self))
        self.exitBtn.clicked.connect(lambda: self.close())
        self.appendBtn_upgrade.clicked.connect(lambda: self.append_upgrade_clicked())
        self.extBtn_upgrade.clicked.connect(lambda: [Utilities_functions.df_to_MO_template(self.dest_df),
                                                     Utilities_GUI.success_message(self, "Done",
                                                                                   "Your file is ready to be saved"),
                                                     self.saveBtn_upgrade.setEnabled(True),
                                                     self.extBtn_upgrade.setEnabled(False)])
        self.saveBtn_upgrade.clicked.connect(lambda: Utilities_functions.save_excel_file(self,
                                                                                         Utilities_functions.upgrade_MO,
                                                                                         "Upgrade"))
        self.uploadBtn_upgrade.clicked.connect(
            lambda: Utilities_functions.save_excel_file(self, Utilities_functions.df_to_MO_template(
                self.upgrade_file_upload()), "Upgrade"))
        self.dest_df = pd.DataFrame(columns=['Reason', 'Item Code', 'Quantity', 'WO ID'])

    def get_upgrade_siteName(self):
        return self.sitename_upgrade.text()

    def get_upgrade_woID(self):
        return self.woID_upgrade.text()

    # noinspection PyAttributeOutsideInit
    def append_upgrade_clicked(self):
        global result_woID_missing
        if self.get_upgrade_siteName() == "":
            Utilities_GUI.success_message(self, "Caution!", "You have to add a valid site name to proceed")

        else:
            if self.woID_upgrade.text() == "":
                result_woID_missing = QMessageBox.question(self, 'Caution!',
                                                           "No WO ID added. Output File will have empty WO ID. Are you "
                                                           "sure you want to continue?",
                                                           QMessageBox.Yes | QMessageBox.No)
                if result_woID_missing == QMessageBox.No:
                    Utilities_GUI.success_message(self,"Caution!", "Please add Wo ID to proceed")
                    return None
                else:
                    pass

            self.site_name_list = [self.sitename_upgrade.text()] * 59
            self.woID_list = [self.woID_upgrade.text()] * 59
            self.item_Code_list = ["BSS-HW-NSN-472181A", "BSS-HW-NOKIA-473095A", "BSS-HW-NOKIA-473096A",
                                   "BSS-HW-NSN-472182A",
                                   "3G-HW-NOKIA-472797A", "3G-HW-NOKIA-472573A", "BSS-HW-NOKIA-474198A",
                                   "BSS-HW-NSN-472649A",
                                   "3G-HW-NOKIA-472454A", "3G-HW-NOKIA-995386A", "BSS-HW-NSN-472501A",
                                   "BSS-HW-NSN-472924A",
                                   "BSS-HW-NOKIA-473439A", "BSS-HW-NSN-472650A", "BSS-HW-NOKIA-474840A",
                                   "BSS-HW-NSN-472956A",
                                   "BSS-HW-NSN-472810A", "BSS-HW-NOKIA-473440A", "BSS-HW-NOKIA-474800A",
                                   "3G-HW-NOKIA-471720A",
                                   "BSS-HW-NSN-472311A", "3G-HW-NOKIA-472234A", "BSS-HW-NOKIA-473246A",
                                   "3G-HW-NOKIA-471397A",
                                   "3G-HW-NOKIA-472285A", "BSS-HW-NSN-470149A", "HW-3G-NOKIA-470239A",
                                   "3G-HW-NOKIA-470316A",
                                   "BSS-HW-NOKIA-473187A", "BSS-HW-NSN-472821A", "BSS-HW-NOKIA-472508A",
                                   "BSS-HW-NOKIA-CS7136001",
                                   "BSS-HW-NSN-472301A", "BSS-HW-NOKIA-472807A", "BSS-HW-NOKIA-472811A",
                                   "BSS-HW-NSN-471881A",
                                   "BSS-HW-NSN-472579A", "BSS-HW-NOKIA-CS72700.39", "BSS-HW-NOKIA-CS75209.09",
                                   "BSS-HW-NOKIA-CS75208.09",
                                   "BSS-HW-NOKIA-CS75108.09", "BSS-HW-NOKIA-CS72700.35", "HW-3G-NOKIA-CS75209.05",
                                   "BSS-HW-NOKIA-CS75208.05",
                                   "BSS-HW-NOKIA-CS75217.05", "3G-HW-NOKIA-471371A", "BSS-HW-NSN-472685A",
                                   "BSS-HW-NSN-472509A",
                                   "BSS-HW-NOKIA-473288A", "BSS-HW-NOKIA-473302A", "BSS-HW-NOKIA-473304ABSS",
                                   "BSS-HW-NOKIA-473751A",
                                   "3G-HW-NOKIA-471424A", "RAN-HW-NOKIA-474880A", "BSS-HW-NSN-472839A",
                                   "BSS-HW-NOKIA-474118A",
                                   "BSS-HW-NOKIA-472806A", "BSS-HW-NSN-472817A", "BSS-HW-NOKIA-471408A"]
            self.qty_list = [self.qty_FSMF.value(), self.qty_ASIA.value(), self.qty_ABIA.value(), self.qty_FBBA.value(),
                             self.qty_FBBC.value(), self.qty_FXDB.value(), self.qty_AREA.value(), self.qty_FHDB.value(),
                             self.qty_RDSA_kit.value(), self.qty_RDSA_cable.value(), self.qty_FXEB.value(),
                             self.qty_FXED.value(), self.qty_FXEF.value(), self.qty_FHEB.value(), self.qty_ARDA.value(),
                             self.qty_FRGU.value(), self.qty_FRGT.value(), self.qty_FRGX.value(), self.qty_ARGA.value(),
                             self.qty_FTIB.value(), self.qty_FTIF.value(), self.qty_FIQB.value(), self.qty_FSEP.value(),
                             self.qty_FSEC.value(), self.qty_FSES.value(), self.qty_FMFA.value(), self.qty_FMCA.value(),
                             self.qty_EMHA.value(), self.qty_EMHH.value(), self.qty_FPKC.value(), self.qty_FPFC.value(),
                             self.qty_FPFH.value(), self.qty_FPFD.value(), self.qty_FOSL.value(), self.qty_FOSN.value(),
                             self.qty_FOSD.value(), self.qty_FOSH.value(), self.qty_7_16_9m.value(),
                             self.qty_4to7_9m.value(), self.qty_7to4_9m.value(), self.qty_4_3_9m.value(),
                             self.qty_7_16_5m.value(), self.qty_4to7_5m.value(), self.qty_7to4_5m.value(),
                             self.qty_4_3_5m.value(), self.qty_ESFA.value(), self.qty_ESFB.value(),
                             self.qty_FTSF.value(),
                             self.qty_FUFAS.value(), self.qty_FUFAY.value(), self.qty_FUFBB.value(),
                             self.qty_FSEE.value(),
                             self.qty_FSEB.value(), self.qty_FSEF.value(), self.qty_FSAH.value(), self.qty_FSAP.value(),
                             self.qty_FPCA.value(), self.qty_FPCB.value(), self.qty_FTCR.value()]

            self.append_to_MO(self.site_name_list, self.item_Code_list, self.qty_list, self.woID_list)
            Utilities_GUI.ask_to_append_upgrade(self)

    def append_to_MO(self, site_name_list, item_code_list, qty_list, woID_list):
        append = True
        while append:
            to_append_df = pd.DataFrame(list(zip(site_name_list, item_code_list, qty_list, woID_list)),
                                        columns=['Reason', 'Item Code', 'Quantity', 'WO ID'])
            temp_df = pd.concat([self.dest_df, to_append_df], axis=0)
            temp1_df = temp_df[temp_df.Quantity != 0]
            self.dest_df = temp1_df
            append = False
        return self.dest_df

    def upgrade_file_upload(self):
        fileName = QFileDialog.getOpenFileName(filter="Excel (*.xlsx *.xls *.csv)")
        if fileName[1] == "":
            Utilities_GUI.success_message(self, "Caution!","No file uploaded")
            self.label_2.setPixmap(QPixmap(':/images/cross_icon.png'))
        else:
            path = fileName[0]
            upgrade_file_df = pd.read_excel(path)
            header_list = list(upgrade_file_df.columns.values)

            if header_list[0] != 'Reason' or header_list[1] != 'WO ID' or header_list[2] != 'HW needed':
                self.label_2.setPixmap(QPixmap(':/images/cross_icon.png'))
                Utilities_GUI.success_message(self, "Caution!", "File not recognized. Please upload Upgrade Template file")
                return None
            else:
                self.label_2.setPixmap(QPixmap(':/images/tick_icon.png'))
                for cell, row in upgrade_file_df.iterrows():
                    if pd.isna(row['Reason']):
                        Utilities_GUI.success_message(self,"Caution!", f"Not Validated, Missing Site name in row {cell + 2}")
                        print(f"Not Validated, Missing Site name in row {cell + 2}")
                        return None
                    elif pd.isna(row['WO ID']):
                        Utilities_GUI.success_message(self, "Caution!",f"Not Validated, Missing WO ID for site {row['Reason']}")
                        print(f"Not Validated, Missing WO ID for site {row['Reason']}")
                        return None

                    elif pd.isna(row['HW needed']):
                        Utilities_GUI.success_message(self, "Caution!",f"Not Validated, No HW requested for site {row['Reason']}")
                        print(f"Not Validated, No HW requested for site {row['Reason']}")
                        return None

                    else:
                        print(f"You requested {row['HW needed']} for site {row['Reason']} with WO ID {row['WO ID']} ")

                Utilities_GUI.success_message(self, "Done", "Validated")

                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.replace('/', ' ', regex = True)
                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.replace('_', ' ', regex = True)
                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.replace('-', ' ', regex = True)
                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.replace('+', ' ', regex = True)
                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.replace('&', ' ', regex = True)
                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.replace(';', ' ', regex = True)
                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.replace(',', ' ', regex = True)

                upgrade_file_df.loc[:, "HW needed"] = upgrade_file_df.loc[:, "HW needed"].str.split(' ')
                upgrade_file_df = upgrade_file_df.explode('HW needed').reset_index(drop=True)
                upgrade_file_df['Item Code'] = upgrade_file_df.loc[:, "HW needed"]
                upgrade_file_df.rename(columns={'HW needed': 'Quantity'}, inplace=True)

                upgrade_file_df['Quantity'] = upgrade_file_df['Quantity'].str.replace('[A-Z]', '', regex=True)
                upgrade_file_df['Quantity'] = upgrade_file_df['Quantity'].str.replace('[a-z]', '', regex=True)

                upgrade_file_df['Item Code'] = upgrade_file_df['Item Code'].str.replace('[0-9]', '', regex=True)
                upgrade_file_df['Item Code'] = upgrade_file_df['Item Code'].str.upper()
                upgrade_file_df = upgrade_file_df[['Reason', 'Item Code', 'Quantity', 'WO ID']]

                for cell, row in upgrade_file_df.iterrows():
                    if row['Item Code'] == "FSMF":
                        row['Item Code'] = "BSS-HW-NSN-472181A"
                    elif row['Item Code'] == "FBBA":
                        row['Item Code'] = "BSS-HW-NSN-472182A"
                    elif row['Item Code'] == "FBBC":
                        row['Item Code'] = "3G-HW-NOKIA-472797A"
                    elif row['Item Code'] == "ARGA":
                        row['Item Code'] = "BSS-HW-NOKIA-474800A"
                    elif row['Item Code'] == "AREA":
                        row['Item Code'] = "BSS-HW-NOKIA-474198A"
                    elif row['Item Code'] == "ARDA":
                        row['Item Code'] = "BSS-HW-NOKIA-474840A"
                    elif row['Item Code'] == "FRGT":
                        row['Item Code'] = "BSS-HW-NSN-472810A"
                    elif row['Item Code'] == "FXED":
                        row['Item Code'] = "BSS-HW-NSN-472924A"
                    elif row['Item Code'] == "FXDB":
                        row['Item Code'] = "3G-HW-NOKIA-472573A"
                    elif row['Item Code'] == "FRGU":
                        row['Item Code'] = "BSS-HW-NSN-472956A"
                    elif row['Item Code'] == "EMHH":
                        row['Item Code'] = "BSS-HW-NOKIA-473187A"
                    elif row['Item Code'] == "EMHA":
                        row['Item Code'] = "3G-HW-NOKIA-470316A"
                    elif row['Item Code'] == "FSES":
                        row['Item Code'] = "3G-HW-NOKIA-472285A"
                    elif row['Item Code'] == "FMFA":
                        row['Item Code'] = "BSS-HW-NSN-470149A"
                    elif row['Item Code'] == "FMCA":
                        row['Item Code'] = "HW-3G-NOKIA-470239A"
                    elif row['Item Code'] == "FTIF":
                        row['Item Code'] = "BSS-HW-NSN-472311A"
                    elif row['Item Code'] == "FPFD":
                        row['Item Code'] = "BSS-HW-NSN-472301A"
                    elif row['Item Code'] == "FSAP":
                        row['Item Code'] = "BSS-HW-NOKIA-474118A"
                    elif row['Item Code'] == "FSEE":
                        row['Item Code'] = "BSS-HW-NOKIA-473751A"
                    elif row['Item Code'] == "FTCR":
                        row['Item Code'] = "HW-3G-NOKIA-471408A"
                    elif row['Item Code'] == "FPCA":
                        row['Item Code'] = "BSS-HW-NOKIA-472806A"
                    elif row['Item Code'] == "FOSH":
                        row['Item Code'] = "BSS-HW-NSN-472579A"
                    elif row['Item Code'] == "FUFAY":
                        row['Item Code'] = "BSS-HW-NOKIA-473302A"
                    elif row['Item Code'] == "FUFAS":
                        row['Item Code'] = "BSS-HW-NOKIA-473288A"
                    elif row['Item Code'] == "FUFBB":
                        row['Item Code'] = "BSS-HW-NOKIA-473304ABSS"
                    elif row['Item Code'] == "FPKC":
                        row['Item Code'] = "BSS-HW-NSN-472821A"
                    elif row['Item Code'] == "ASIA":
                        row['Item Code'] = "BSS-HW-NOKIA-473095A"
                    elif row['Item Code'] == "ABIA":
                        row['Item Code'] = "BSS-HW-NOKIA-473096A"
                    elif row['Item Code'] == "FIQB":
                        row['Item Code'] = "3G-HW-NOKIA-472234A"
                    elif row['Item Code'] == "ESFA":
                        row['Item Code'] = "3G-HW-NOKIA-471371A"
                    elif row['Item Code'] == "ESFB":
                        row['Item Code'] = "BSS-HW-NSN-472685A"
                    elif row['Item Code'] == "FTSF":
                        row['Item Code'] = "BSS-HW-NSN-472509A"
                    elif row['Item Code'] == "FPCB":
                        row['Item Code'] = "BSS-HW-NSN-472817A"
                    elif row['Item Code'] == "FSAH":
                        row['Item Code'] = "BSS-HW-NOKIA-472839A"
                    elif row['Item Code'] == "FHDB":
                        row['Item Code'] = "BSS-HW-NSN-472649A"
                    elif row['Item Code'] == "FHEB":
                        row['Item Code'] = "BSS-HW-NSN-472650A"
                    elif row['Item Code'] == "FPFC":
                        row['Item Code'] = "BSS-HW-NOKIA-472508A"
                    elif row['Item Code'] == "FPFH":
                        row['Item Code'] = "BSS-HW-NOKIA-CS7136001"
                    elif row['Item Code'] == "FOSL":
                        row['Item Code'] = "BSS-HW-NOKIA-472807A"
                    elif row['Item Code'] == "FOSD":
                        row['Item Code'] = "BSS-HW-NSN-471881A"
                    elif row['Item Code'] == "FOSN":
                        row['Item Code'] = "BSS-HW-NOKIA-472811A"
                    elif row['Item Code'] == "FRGX":
                        row['Item Code'] = "BSS-HW-NOKIA-473440A"
                    elif row['Item Code'] == "FSEP":
                        row['Item Code'] = "BSS-HW-NOKIA-473246A"
                    elif row['Item Code'] == "FSEC":
                        row['Item Code'] = "3G-HW-NOKIA-471397A"
                    elif row['Item Code'] == "FXEF":
                        row['Item Code'] = "BSS-HW-NOKIA-473439A"
                    elif row['Item Code'] == "FXEB":
                        row['Item Code'] = "BSS-HW-NSN-472501A"
                    elif row['Item Code'] == "FSEB":
                        row['Item Code'] = "3G-HW-NOKIA-471424A"
                    elif row['Item Code'] == "FTIB":
                        row['Item Code'] = "3G-HW-NOKIA-471720A"
                    elif row['Item Code'] == "FMCH":
                        row['Item Code'] = "BSS-HW-NOKIA-473186A"
                    elif row['Item Code'] == "CASSING":
                        row['Item Code'] = "New-HW-NOKIA-082795A"
                upgrade_file_df['Quantity'] = upgrade_file_df['Quantity'].astype(int)

                Utilities_GUI.success_message(self, "Done", "MO upload is ready to be saved!")
            return upgrade_file_df


class NewsiteTechWindow(QtWidgets.QMainWindow, Ui_NewsiteWindow):
    def __init__(self, parent=None):
        super(NewsiteTechWindow, self).__init__(parent)
        self.setupUi(self)
        self.exitBTN.clicked.connect(self.close)


class TDDWindow(QtWidgets.QMainWindow, Ui_tddWindow):
    def __init__(self, parent=None):
        super(TDDWindow, self).__init__(parent)
        self.setupUi(self)
        self.exitBtn_TDD.clicked.connect(self.close)
        self.uploadTDDBtn.clicked.connect(
            lambda: [Utilities_functions.save_excel_file(self, Utilities_functions.df_to_MO_template(
                self.tdd_file_upload()), "TDD")])
        self.executeBtn_TDD.clicked.connect(lambda: Utilities_functions.save_excel_file(
            self, Utilities_functions.df_to_MO_template(self.tdd_MO()), "TDD"))

    def tdd_MO(self):
        common_TDD_df = pd.DataFrame({'Reason': [self.get_siteName_TDD(), self.get_siteName_TDD(), self.get_siteName_TDD(),
                                                 self.get_siteName_TDD(), self.get_siteName_TDD(), self.get_siteName_TDD(),
                                                 self.get_siteName_TDD(), self.get_siteName_TDD(), self.get_siteName_TDD(),
                                                 self.get_siteName_TDD(), self.get_siteName_TDD(),
                                                 self.get_siteName_TDD(), self.get_siteName_TDD(),
                                                 self.get_siteName_TDD(), self.get_siteName_TDD(),
                                                 self.get_siteName_TDD(), self.get_siteName_TDD(),
                                                 self.get_siteName_TDD(), self.get_siteName_TDD()], 'Item Code': ["BSS-HW-NOKIA-473098A", "BSS-HW-NOKIA-473764A",
                                                    "BSS-HW-NOKIA-475266A",
                                                    "BSS-HW-NOKIA-473096A", "BSS-HW-NOKIA-475893A",
                                                    "BSS-HW-NOKIA-475972A",
                                                    "RAN-HW-NOKIA-474074A", "BSS-HW-NOKIA-471605A",
                                                    "BSS-HW-NOKIA-472577A",
                                                    "RAN-HW-NOKIA-471812A", "BSS-HW-NSN-472509A",
                                                    "BSS-HW-NOKIA-473288A",
                                                    "BSS-HW-NSN-472579A", "BSS-HW-NOKIA-CS7136001",
                                                    "BSS-HW-NOKIA-470316A", "BSS-HW-NSN-472821A",
                                                    "BSS-HW-NOKIA-CS7136015", "BSS-HW-NOKIA-471880A",
                                                    "BSS-HW-NOKIA-473278A"], 'Quantity': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 4, 1, 2,
                                                   1], 'WO ID': [self.get_woID_TDD(), self.get_woID_TDD(), self.get_woID_TDD(),
                                                self.get_woID_TDD(),
                                                self.get_woID_TDD(), self.get_woID_TDD(), self.get_woID_TDD(),
                                                self.get_woID_TDD(),
                                                self.get_woID_TDD(), self.get_woID_TDD(), self.get_woID_TDD(),
                                                self.get_woID_TDD(),
                                                self.get_woID_TDD(), self.get_woID_TDD(), self.get_woID_TDD(),
                                                self.get_woID_TDD(),
                                                self.get_woID_TDD(), self.get_woID_TDD(),
                                                self.get_woID_TDD()]})

        dep_TDD_df = pd.DataFrame({'Reason': [self.get_siteName_TDD(), self.get_siteName_TDD(), self.get_siteName_TDD(), self.get_siteName_TDD(),
                                              self.get_siteName_TDD(), self.get_siteName_TDD(), self.get_siteName_TDD(), self.get_siteName_TDD()], 'Item Code': ["BSS-HW-NOKIA-473941A", "BSS-HW-NOKIA-475690A",
                                                 "BSS-HW-NOKIA-475336A", "BSS-HW-NOKIA-474283A",
                                                 "BSS-HW-NOKIA-474271A", "BSS-HW-NOKIA-474483A",
                                                 "BSS-HW-NOKIA-474289A", "BSS-HW-NOKIA-CS75217.05"],
                                   'Quantity': [self.get_num_of_sectors_TDD(), self.get_num_of_sectors_TDD(),
                                                self.get_num_of_sectors_TDD() * 2, self.get_num_of_sectors_TDD(),
                                                self.get_num_of_sectors_TDD(), self.get_num_of_sectors_TDD(),
                                                self.get_num_of_sectors_TDD(), self.get_num_of_sectors_TDD() * 4],
                                   'WO ID': [self.get_woID_TDD(), self.get_woID_TDD(),self.get_woID_TDD(), self.get_woID_TDD(),
                                             self.get_woID_TDD(), self.get_woID_TDD(), self.get_woID_TDD(), self.get_woID_TDD()]})

        tdd_MO_df = pd.concat([dep_TDD_df, common_TDD_df])
        return tdd_MO_df

    def get_siteName_TDD(self):
        return self.siteName_TDD.text()

    def get_woID_TDD(self):
        return self.woID_TDD.text()

    def get_num_of_sectors_TDD(self):
        return self.sectors_TDD.value()



    def tdd_file_upload(self):
        fileName = QFileDialog.getOpenFileName(filter="Excel (*.xlsx *.xls *.csv)")
        if fileName[1] == "":
            Utilities_GUI.success_message(self, "Caution!", "No file uploaded")
            self.label_2.setPixmap(QPixmap(':/images/cross_icon.png'))
        else:
            path = fileName[0]
            tdd_file_df = pd.read_excel(path)
            header_list = list(tdd_file_df.columns.values)

            if header_list[0] != 'Reason' or header_list[1] != 'WO ID' or header_list[2] != 'HW needed':
                self.label_2.setPixmap(QPixmap(':/images/cross_icon.png'))
                Utilities_GUI.success_message(self,"Caution!", "File not recognized. Please upload Upgrade Template file")
                return None
            else:
                self.label_2.setPixmap(QPixmap(':/images/tick_icon.png'))
                for cell, row in tdd_file_df.iterrows():
                    if pd.isna(row['Reason']):
                        Utilities_GUI.success_message(self,"Caution!", f"Not Validated, Missing Site name in row {cell + 2}")
                        print(f"Not Validated, Missing Site name in row {cell + 2}")
                        return None
                    elif pd.isna(row['WO ID']):
                        Utilities_GUI.success_message(self,"Caution!", f"Not Validated, Missing WO ID for site {row['Reason']}")
                        print(f"Not Validated, Missing WO ID for site {row['Reason']}")
                        return None

                    elif pd.isna(row['HW needed']):
                        Utilities_GUI.success_message(self,"Caution!",f"Not Validated, No HW requested for site {row['Reason']}")
                        print(f"Not Validated, No HW requested for site {row['Reason']}")
                        return None

                    else:
                        print(f"You requested {row['HW needed']} for site {row['Reason']} with WO ID {row['WO ID']} ")

                Utilities_GUI.success_message(self, "Done", "Validated")

                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.replace('/', ' ', regex = True)
                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.replace('_', ' ', regex = True)
                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.replace('-', ' ', regex = True)
                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.replace('+', ' ', regex = True)
                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.replace('&', ' ', regex = True)
                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.replace(';', ' ', regex = True)
                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.replace(',', ' ', regex = True)
                tdd_file_df.loc[:, "HW needed"] = tdd_file_df.loc[:, "HW needed"].str.split(' ')
                tdd_file_df = tdd_file_df.explode('HW needed').reset_index(drop=True)
                tdd_file_df['Item Code'] = tdd_file_df.loc[:, "HW needed"]
                tdd_file_df.rename(columns={'HW needed': 'Quantity'}, inplace=True)

                tdd_file_df['Quantity'] = tdd_file_df['Quantity'].str.replace('[A-Z]', '', regex=True)
                tdd_file_df['Quantity'] = tdd_file_df['Quantity'].str.replace('[a-z]', '', regex=True)

                tdd_file_df['Item Code'] = tdd_file_df['Item Code'].str.replace('[0-9]', '', regex=True)
                tdd_file_df['Item Code'] = tdd_file_df['Item Code'].str.upper()
                tdd_file_df = tdd_file_df[['Reason', 'Item Code', 'Quantity', 'WO ID']]

                for cell, row in tdd_file_df.iterrows():
                    if row['Item Code'] == "FSMF":
                        row['Item Code'] = "BSS-HW-NSN-472181A"
                    elif row['Item Code'] == "FBBA":
                        row['Item Code'] = "BSS-HW-NSN-472182A"
                    elif row['Item Code'] == "FBBC":
                        row['Item Code'] = "3G-HW-NOKIA-472797A"
                    elif row['Item Code'] == "ARGA":
                        row['Item Code'] = "BSS-HW-NOKIA-474800A"
                    elif row['Item Code'] == "AREA":
                        row['Item Code'] = "BSS-HW-NOKIA-474198A"
                    elif row['Item Code'] == "ARDA":
                        row['Item Code'] = "BSS-HW-NOKIA-474840A"
                    elif row['Item Code'] == "FRGT":
                        row['Item Code'] = "BSS-HW-NSN-472810A"
                    elif row['Item Code'] == "FXED":
                        row['Item Code'] = "BSS-HW-NSN-472924A"
                    elif row['Item Code'] == "FXDB":
                        row['Item Code'] = "3G-HW-NOKIA-472573A"
                    elif row['Item Code'] == "FRGU":
                        row['Item Code'] = "BSS-HW-NSN-472956A"
                    elif row['Item Code'] == "EMHH":
                        row['Item Code'] = "BSS-HW-NOKIA-473187A"
                    elif row['Item Code'] == "EMHA":
                        row['Item Code'] = "3G-HW-NOKIA-470316A"
                    elif row['Item Code'] == "FSES":
                        row['Item Code'] = "3G-HW-NOKIA-472285A"
                    elif row['Item Code'] == "FMFA":
                        row['Item Code'] = "BSS-HW-NSN-470149A"
                    elif row['Item Code'] == "FMCA":
                        row['Item Code'] = "HW-3G-NOKIA-470239A"
                    elif row['Item Code'] == "FTIF":
                        row['Item Code'] = "BSS-HW-NSN-472311A"
                    elif row['Item Code'] == "FPFD":
                        row['Item Code'] = "BSS-HW-NSN-472301A"
                    elif row['Item Code'] == "FSAP":
                        row['Item Code'] = "BSS-HW-NOKIA-474118A"
                    elif row['Item Code'] == "FSEE":
                        row['Item Code'] = "BSS-HW-NOKIA-473751A"
                    elif row['Item Code'] == "FTCR":
                        row['Item Code'] = "HW-3G-NOKIA-471408A"
                    elif row['Item Code'] == "FPCA":
                        row['Item Code'] = "BSS-HW-NOKIA-472806A"
                    elif row['Item Code'] == "FOSH":
                        row['Item Code'] = "BSS-HW-NSN-472579A"
                    elif row['Item Code'] == "FUFAY":
                        row['Item Code'] = "BSS-HW-NOKIA-473302A"
                    elif row['Item Code'] == "FUFAS":
                        row['Item Code'] = "BSS-HW-NOKIA-473288A"
                    elif row['Item Code'] == "FUFBB":
                        row['Item Code'] = "BSS-HW-NOKIA-473304ABSS"
                    elif row['Item Code'] == "FPKC":
                        row['Item Code'] = "BSS-HW-NSN-472821A"
                    elif row['Item Code'] == "ASIA":
                        row['Item Code'] = "BSS-HW-NOKIA-473095A"
                    elif row['Item Code'] == "ABIA":
                        row['Item Code'] = "BSS-HW-NOKIA-473096A"
                    elif row['Item Code'] == "FIQB":
                        row['Item Code'] = "3G-HW-NOKIA-472234A"
                    elif row['Item Code'] == "ESFA":
                        row['Item Code'] = "3G-HW-NOKIA-471371A"
                    elif row['Item Code'] == "ESFB":
                        row['Item Code'] = "BSS-HW-NSN-472685A"
                    elif row['Item Code'] == "FTSF":
                        row['Item Code'] = "BSS-HW-NSN-472509A"
                    elif row['Item Code'] == "FPCB":
                        row['Item Code'] = "BSS-HW-NSN-472817A"
                    elif row['Item Code'] == "FSAH":
                        row['Item Code'] = "BSS-HW-NOKIA-472839A"
                    elif row['Item Code'] == "FHDB":
                        row['Item Code'] = "BSS-HW-NSN-472649A"
                    elif row['Item Code'] == "FHEB":
                        row['Item Code'] = "BSS-HW-NSN-472650A"
                    elif row['Item Code'] == "FPFC":
                        row['Item Code'] = "BSS-HW-NOKIA-472508A"
                    elif row['Item Code'] == "FPFH":
                        row['Item Code'] = "BSS-HW-NOKIA-CS7136001"
                    elif row['Item Code'] == "FOSL":
                        row['Item Code'] = "BSS-HW-NOKIA-472807A"
                    elif row['Item Code'] == "FOSD":
                        row['Item Code'] = "BSS-HW-NSN-471881A"
                    elif row['Item Code'] == "FOSN":
                        row['Item Code'] = "BSS-HW-NOKIA-472811A"
                    elif row['Item Code'] == "FRGX":
                        row['Item Code'] = "BSS-HW-NOKIA-473440A"
                    elif row['Item Code'] == "FSEP":
                        row['Item Code'] = "BSS-HW-NOKIA-473246A"
                    elif row['Item Code'] == "FSEC":
                        row['Item Code'] = "3G-HW-NOKIA-471397A"
                    elif row['Item Code'] == "FXEF":
                        row['Item Code'] = "BSS-HW-NOKIA-473439A"
                    elif row['Item Code'] == "FXEB":
                        row['Item Code'] = "BSS-HW-NSN-472501A"
                    elif row['Item Code'] == "FSEB":
                        row['Item Code'] = "3G-HW-NOKIA-471424A"
                    elif row['Item Code'] == "FTIB":
                        row['Item Code'] = "3G-HW-NOKIA-471720A"
                    elif row['Item Code'] == "FMCH":
                        row['Item Code'] = "BSS-HW-NOKIA-473186A"
                    elif row['Item Code'] == "CASSING":
                        row['Item Code'] = "New-HW-NOKIA-082795A"

                for cell, row in tdd_file_df.iterrows():
                    if row['Item Code'] == "TDD":
                        common_TDD_df = pd.DataFrame({'Reason': [row['Reason'], row['Reason'], row['Reason'],
                                                                 row['Reason'], row['Reason'], row['Reason'],
                                                                 row['Reason'], row['Reason'], row['Reason'],
                                                                 row['Reason'], row['Reason'], row['Reason'],
                                                                 row['Reason'], row['Reason'], row['Reason'],
                                                                 row['Reason'], row['Reason'], row['Reason'],row['Reason']],
                                                      'Item Code': ["BSS-HW-NOKIA-473098A", "BSS-HW-NOKIA-473764A",
                                                                    "BSS-HW-NOKIA-475266A",
                                                                    "BSS-HW-NOKIA-473096A", "BSS-HW-NOKIA-475893A",
                                                                    "BSS-HW-NOKIA-475972A",
                                                                    "RAN-HW-NOKIA-474074A", "BSS-HW-NOKIA-471605A",
                                                                    "BSS-HW-NOKIA-472577A",
                                                                    "RAN-HW-NOKIA-471812A", "BSS-HW-NSN-472509A",
                                                                    "BSS-HW-NOKIA-473288A",
                                                                    "BSS-HW-NSN-472579A", "BSS-HW-NOKIA-CS7136001",
                                                                    "BSS-HW-NOKIA-470316A", "BSS-HW-NSN-472821A",
                                                                    "BSS-HW-NOKIA-CS7136015", "BSS-HW-NOKIA-471880A",
                                                                    "BSS-HW-NOKIA-473278A"],
                                                      'Quantity': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 4, 1, 2,
                                                                   1],
                                                      'WO ID': [row['WO ID'], row['WO ID'], row['WO ID'], row['WO ID'],
                                                                row['WO ID'], row['WO ID'], row['WO ID'], row['WO ID'],
                                                                row['WO ID'], row['WO ID'], row['WO ID'], row['WO ID'],
                                                                row['WO ID'], row['WO ID'], row['WO ID'], row['WO ID'],
                                                                row['WO ID'], row['WO ID'], row['WO ID']]})

                        dep_TDD_df = pd.DataFrame({'Reason': [row['Reason'], row['Reason'], row['Reason'], row['Reason'],
                                                              row['Reason'], row['Reason'], row['Reason'], row['Reason']],
                                                   'Item Code': ["BSS-HW-NOKIA-473941A", "BSS-HW-NOKIA-475690A",
                                                                 "BSS-HW-NOKIA-475336A", "BSS-HW-NOKIA-474283A",
                                                                 "BSS-HW-NOKIA-474271A", "BSS-HW-NOKIA-474483A",
                                                                 "BSS-HW-NOKIA-474289A", "BSS-HW-NOKIA-CS75217.05"],
                                                   'Quantity': [row['Quantity'], row['Quantity'], int(row['Quantity'])*2,
                                                                row['Quantity'], row['Quantity'], row['Quantity'],
                                                                row['Quantity'], int(row['Quantity'])*4],
                                                   'WO ID': [row['WO ID'], row['WO ID'], row['WO ID'], row['WO ID'],
                                                             row['WO ID'], row['WO ID'], row['WO ID'], row['WO ID']]})

                        tdd_file_df = pd.concat([tdd_file_df, common_TDD_df])
                        tdd_file_df = pd.concat([tdd_file_df, dep_TDD_df])

                tdd_file_df['Quantity'] = tdd_file_df['Quantity'].astype(int)
                tdd_file_df = tdd_file_df[tdd_file_df['Item Code'] != "TDD"]

                Utilities_GUI.success_message(self, "Done" , "MO upload is ready to be saved!")

            return tdd_file_df


class Manager:
    def __init__(self):
        # Creating All App Windows
        self.welcomeWindow = WelcomeWindow()
        self.upgradeWindow = UpgradeWindow()
        self.newsiteTechWindow = NewsiteTechWindow()
        self.SRAN_DWO = SRAN_DWO()
        self.pico = PicoWindow()
        self.tddWindow = TDDWindow()

        # Navigation Buttons between windows
        Utilities_GUI.navigation_btn_click(self)

        # Start the program
        self.welcomeWindow.show()


#####################
#        MAIN       #
#####################
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    manager = Manager()
    sys.exit(app.exec_())
