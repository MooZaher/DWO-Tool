from PyQt5.QtWidgets import QMessageBox


####################################
#        GUI General Methods       #
####################################

# Call for Success Message to user anywhere in app
def success_message(self, caption,  message):
    QMessageBox.about(self, caption, message)


# Method for showing window on screen
def openWindow(window, ui):
    ui.setupUi(window)
    window.show()


# Method to swap between two windows
def swapWindows(w1, w2):
    w1.close()
    w2.show()


# Navigation Buttons Functions for all Windows in Manager
def navigation_btn_click(self):
    # Welcome Window Buttons actions
    self.welcomeWindow.upgradeWinBtn.clicked.connect(lambda: swapWindows(self.welcomeWindow, self.upgradeWindow))
    self.welcomeWindow.newsiteWinBtn.clicked.connect(lambda: swapWindows(self.welcomeWindow, self.newsiteTechWindow))
    self.welcomeWindow.tddWinBtn.clicked.connect(lambda: swapWindows(self.welcomeWindow, self.tddWindow))

    # Upgrade Window Buttons actions
    self.upgradeWindow.backBtn_upgrade.clicked.connect(
        lambda: [swapWindows(self.upgradeWindow, self.welcomeWindow), reset_upgrade_window(self.upgradeWindow)])


    # Configuration Window Buttons actions
    self.newsiteTechWindow.btn_SRAN.clicked.connect((lambda: swapWindows(self.newsiteTechWindow, self.SRAN_DWO)))
    self.newsiteTechWindow.btn_PICO.clicked.connect((lambda: swapWindows(self.newsiteTechWindow, self.pico)))
    self.newsiteTechWindow.backBTN.clicked.connect(lambda: swapWindows(self.newsiteTechWindow, self.welcomeWindow))

    # SRAN Window Buttons actions
    self.SRAN_DWO.bckBtn_SRAN.clicked.connect(lambda: swapWindows(self.SRAN_DWO, self.newsiteTechWindow))

    # PICO Window Button actions
    self.pico.bckBtn_pico3G.clicked.connect(lambda: swapWindows(self.pico, self.newsiteTechWindow))

    # SRAN Window Buttons actions
    self.tddWindow.backBtn_TDD.clicked.connect(lambda: swapWindows(self.tddWindow, self.welcomeWindow))

###########################################
#        Upgrade Window GUI Methods       #
###########################################
# Method to check whether appending another site to WO is needed or not in upgrade MO
def ask_to_append_upgrade(self):
    res = QMessageBox.question(self, 'Need Anything else?', "Do you want to append another site?",
                               QMessageBox.Yes | QMessageBox.No)
    if res == QMessageBox.Yes:
        reset_upgrade_window(self)
    else:
        self.appendBtn_upgrade.setEnabled(False)
        self.extBtn_upgrade.setEnabled(True)


# Method to hide all items in upgrade window
def upgrade_items_hide(self):
    self.checkBox_SM.setEnabled(True)
    self.checkBox_RF.setEnabled(True)
    self.checkBox_accessories.setEnabled(True)
    self.checkBox_cables.setEnabled(True)
    self.checkBox_jumpers.setEnabled(True)
    self.checkBox_TX.setEnabled(True)
    self.qty_FSMF.hide()
    self.label_FSMF.hide()

    self.qty_ASIA.hide()
    self.label_ASIA.hide()

    self.qty_ABIA.hide()
    self.label_ABIA.hide()

    self.qty_FBBA.hide()
    self.label_FBBA.hide()

    self.qty_FBBC.hide()
    self.label_FBBC.hide()

    self.qty_FXDB.hide()
    self.label_FXDB.hide()

    self.qty_AREA.hide()
    self.label_AREA.hide()

    self.qty_FHDB.hide()
    self.label_FHDB.hide()

    self.qty_RDSA_kit.hide()
    self.label_RDSA_kit.hide()

    self.qty_RDSA_cable.hide()
    self.label_RDSA_cable.hide()

    self.qty_FXEB.hide()
    self.label_FXEB.hide()

    self.qty_FXED.hide()
    self.label_FXED.hide()

    self.qty_FXEF.hide()
    self.label_FXEF.hide()

    self.qty_FHEB.hide()
    self.label_FHEB.hide()

    self.qty_ARDA.hide()
    self.label_ARDA.hide()

    self.qty_FRGU.hide()
    self.label_FRGU.hide()

    self.qty_FRGT.hide()
    self.label_FRGT.hide()

    self.qty_FRGX.hide()
    self.label_FRGX.hide()

    self.qty_ARGA.hide()
    self.label_ARGA.hide()

    self.qty_FTIB.hide()
    self.label_FTIB.hide()

    self.qty_FTIF.hide()
    self.label_FTIF.hide()

    self.qty_FIQB.hide()
    self.label_FIQB.hide()

    self.qty_FSEP.hide()
    self.label_FSEP.hide()

    self.qty_FSEC.hide()
    self.label_FSEC.hide()

    self.qty_FSES.hide()
    self.label_FSES.hide()

    self.qty_FMFA.hide()
    self.label_FMFA.hide()

    self.qty_FMCA.hide()
    self.label_FMCA.hide()

    self.qty_EMHA.hide()
    self.label_EMHA.hide()

    self.qty_EMHH.hide()
    self.label_EMHH.hide()

    self.qty_FPKC.hide()
    self.label_FPKC.hide()

    self.qty_FPFC.hide()
    self.label_FPFC.hide()

    self.qty_FPFH.hide()
    self.label_FPFH.hide()

    self.qty_FPFD.hide()
    self.label_FPFD.hide()

    self.qty_FOSL.hide()
    self.label_FOSL.hide()

    self.qty_FOSN.hide()
    self.label_FOSN.hide()

    self.qty_FOSD.hide()
    self.label_FOSD.hide()

    self.qty_FOSH.hide()
    self.label_FOSH.hide()

    self.qty_7_16_9m.hide()
    self.label_9716.hide()

    self.qty_4to7_9m.hide()
    self.label_947.hide()

    self.qty_7to4_9m.hide()
    self.label_974.hide()

    self.qty_4_3_9m.hide()
    self.label_943.hide()

    self.qty_7_16_5m.hide()
    self.label_5716.hide()

    self.qty_4to7_5m.hide()
    self.label_547.hide()

    self.qty_7to4_5m.hide()
    self.label_574.hide()

    self.qty_4_3_5m.hide()
    self.label_543.hide()

    self.qty_ESFA.hide()
    self.label_ESFA.hide()

    self.qty_ESFB.hide()
    self.label_ESFB.hide()

    self.qty_FTSF.hide()
    self.label_FTSF.hide()

    self.qty_FUFAS.hide()
    self.label_FUFAS.hide()

    self.qty_FUFAY.hide()
    self.label_FUFAY.hide()

    self.qty_FUFBB.hide()
    self.label_FUFBB.hide()

    self.qty_FSEE.hide()
    self.label_FSEE.hide()

    self.qty_FSEB.hide()
    self.label_FSEB.hide()

    self.qty_FSEF.hide()
    self.label_FSEF.hide()

    self.qty_FSAH.hide()
    self.label_FSAH.hide()

    self.qty_FSAP.hide()
    self.label_FSAP.hide()

    self.qty_FPCA.hide()
    self.label_FPCA.hide()

    self.qty_FPCB.hide()
    self.label_FPCB.hide()

    self.qty_FTCR.hide()
    self.label_FTCR.hide()


# Method to show all items in upgrade window
def upgrade_items_show(self):
    self.checkBox_SM.setEnabled(False)
    self.checkBox_RF.setEnabled(False)
    self.checkBox_accessories.setEnabled(False)
    self.checkBox_cables.setEnabled(False)
    self.checkBox_jumpers.setEnabled(False)
    self.checkBox_TX.setEnabled(False)

    self.qty_FSMF.show()
    self.label_FSMF.show()

    self.qty_ASIA.show()
    self.label_ASIA.show()

    self.qty_ABIA.show()
    self.label_ABIA.show()

    self.qty_FBBA.show()
    self.label_FBBA.show()

    self.qty_FBBC.show()
    self.label_FBBC.show()

    self.qty_FXDB.show()
    self.label_FXDB.show()

    self.qty_AREA.show()
    self.label_AREA.show()

    self.qty_FHDB.show()
    self.label_FHDB.show()

    self.qty_RDSA_kit.show()
    self.label_RDSA_kit.show()

    self.qty_RDSA_cable.show()
    self.label_RDSA_cable.show()

    self.qty_FXEB.show()
    self.label_FXEB.show()

    self.qty_FXED.show()
    self.label_FXED.show()

    self.qty_FXEF.show()
    self.label_FXEF.show()

    self.qty_FHEB.show()
    self.label_FHEB.show()

    self.qty_ARDA.show()
    self.label_ARDA.show()

    self.qty_FRGU.show()
    self.label_FRGU.show()

    self.qty_FRGT.show()
    self.label_FRGT.show()

    self.qty_FRGX.show()
    self.label_FRGX.show()

    self.qty_ARGA.show()
    self.label_ARGA.show()

    self.qty_FTIB.show()
    self.label_FTIB.show()

    self.qty_FTIF.show()
    self.label_FTIF.show()

    self.qty_FIQB.show()
    self.label_FIQB.show()

    self.qty_FSEP.show()
    self.label_FSEP.show()

    self.qty_FSEC.show()
    self.label_FSEC.show()

    self.qty_FSES.show()
    self.label_FSES.show()

    self.qty_FMFA.show()
    self.label_FMFA.show()

    self.qty_FMCA.show()
    self.label_FMCA.show()

    self.qty_EMHA.show()
    self.label_EMHA.show()

    self.qty_EMHH.show()
    self.label_EMHH.show()

    self.qty_FPKC.show()
    self.label_FPKC.show()

    self.qty_FPFC.show()
    self.label_FPFC.show()

    self.qty_FPFH.show()
    self.label_FPFH.show()

    self.qty_FPFD.show()
    self.label_FPFD.show()

    self.qty_FOSL.show()
    self.label_FOSL.show()

    self.qty_FOSN.show()
    self.label_FOSN.show()

    self.qty_FOSD.show()
    self.label_FOSD.show()

    self.qty_FOSH.show()
    self.label_FOSH.show()

    self.qty_7_16_9m.show()
    self.label_9716.show()

    self.qty_4to7_9m.show()
    self.label_947.show()

    self.qty_7to4_9m.show()
    self.label_974.show()

    self.qty_4_3_9m.show()
    self.label_943.show()

    self.qty_7_16_5m.show()
    self.label_5716.show()

    self.qty_4to7_5m.show()
    self.label_547.show()

    self.qty_7to4_5m.show()
    self.label_574.show()

    self.qty_4_3_5m.show()
    self.label_543.show()

    self.qty_ESFA.show()
    self.label_ESFA.show()

    self.qty_ESFB.show()
    self.label_ESFB.show()

    self.qty_FTSF.show()
    self.label_FTSF.show()

    self.qty_FUFAS.show()
    self.label_FUFAS.show()

    self.qty_FUFAY.show()
    self.label_FUFAY.show()

    self.qty_FUFBB.show()
    self.label_FUFBB.show()

    self.qty_FSEE.show()
    self.label_FSEE.show()

    self.qty_FSEB.show()
    self.label_FSEB.show()

    self.qty_FSEF.show()
    self.label_FSEF.show()

    self.qty_FSAH.show()
    self.label_FSAH.show()

    self.qty_FSAP.show()
    self.label_FSAP.show()

    self.qty_FPCA.show()
    self.label_FPCA.show()

    self.qty_FPCB.show()
    self.label_FPCB.show()

    self.qty_FTCR.show()
    self.label_FTCR.show()


# Method responsible for "All items" checkbox state in upgrade Window
def upgrade_all_checkBox(self):
    if self.checkBox_all.isChecked():
        upgrade_items_show(self)
    else:
        upgrade_items_hide(self)


# Method responsible for RF items in upgrade Window
def upgrade_RF_checkBox(self):
    if self.checkBox_RF.isChecked():
        self.qty_FXDB.show()
        self.label_FXDB.show()

        self.qty_AREA.show()
        self.label_AREA.show()

        self.qty_FHDB.show()
        self.label_FHDB.show()

        self.qty_RDSA_kit.show()
        self.label_RDSA_kit.show()

        self.qty_RDSA_cable.show()
        self.label_RDSA_cable.show()

        self.qty_FXEB.show()
        self.label_FXEB.show()

        self.qty_FXED.show()
        self.label_FXED.show()

        self.qty_FXEF.show()
        self.label_FXEF.show()

        self.qty_FHEB.show()
        self.label_FHEB.show()

        self.qty_ARDA.show()
        self.label_ARDA.show()

        self.qty_FRGU.show()
        self.label_FRGU.show()

        self.qty_FRGT.show()
        self.label_FRGT.show()

        self.qty_FRGX.show()
        self.label_FRGX.show()

        self.qty_ARGA.show()
        self.label_ARGA.show()

        self.qty_FSEP.show()
        self.label_FSEP.show()

        self.qty_FSEC.show()
        self.label_FSEC.show()

        self.qty_FSES.show()
        self.label_FSES.show()

        self.qty_FMFA.show()
        self.label_FMFA.show()

        self.qty_FMCA.show()
        self.label_FMCA.show()

        self.qty_EMHA.show()
        self.label_EMHA.show()

        self.qty_EMHH.show()
        self.label_EMHH.show()

        self.qty_FPKC.show()
        self.label_FPKC.show()

        self.qty_FOSL.show()
        self.label_FOSL.show()

        self.qty_FOSN.show()
        self.label_FOSN.show()

        self.qty_FOSD.show()
        self.label_FOSD.show()

        self.qty_FOSH.show()
        self.label_FOSH.show()

        self.qty_FUFAS.show()
        self.label_FUFAS.show()

        self.qty_FUFAY.show()
        self.label_FUFAY.show()

        self.qty_FUFBB.show()
        self.label_FUFBB.show()

        self.qty_FPCA.show()
        self.label_FPCA.show()

        self.qty_FPCB.show()
        self.label_FPCB.show()

    else:
        self.qty_FXDB.hide()
        self.label_FXDB.hide()

        self.qty_AREA.hide()
        self.label_AREA.hide()

        self.qty_FHDB.hide()
        self.label_FHDB.hide()

        self.qty_RDSA_kit.hide()
        self.label_RDSA_kit.hide()

        self.qty_RDSA_cable.hide()
        self.label_RDSA_cable.hide()

        self.qty_FXEB.hide()
        self.label_FXEB.hide()

        self.qty_FXED.hide()
        self.label_FXED.hide()

        self.qty_FXEF.hide()
        self.label_FXEF.hide()

        self.qty_FHEB.hide()
        self.label_FHEB.hide()

        self.qty_ARDA.hide()
        self.label_ARDA.hide()

        self.qty_FRGU.hide()
        self.label_FRGU.hide()

        self.qty_FRGT.hide()
        self.label_FRGT.hide()

        self.qty_FRGX.hide()
        self.label_FRGX.hide()

        self.qty_ARGA.hide()
        self.label_ARGA.hide()

        self.qty_FSEP.hide()
        self.label_FSEP.hide()

        self.qty_FSEC.hide()
        self.label_FSEC.hide()

        self.qty_FSES.hide()
        self.label_FSES.hide()

        self.qty_FMFA.hide()
        self.label_FMFA.hide()

        self.qty_FMCA.hide()
        self.label_FMCA.hide()

        self.qty_EMHA.hide()
        self.label_EMHA.hide()

        self.qty_EMHH.hide()
        self.label_EMHH.hide()

        self.qty_FPKC.hide()
        self.label_FPKC.hide()

        self.qty_FOSL.hide()
        self.label_FOSL.hide()

        self.qty_FOSN.hide()
        self.label_FOSN.hide()

        self.qty_FOSD.hide()
        self.label_FOSD.hide()

        self.qty_FOSH.hide()
        self.label_FOSH.hide()

        self.qty_FUFAS.hide()
        self.label_FUFAS.hide()

        self.qty_FUFAY.hide()
        self.label_FUFAY.hide()

        self.qty_FUFBB.hide()
        self.label_FUFBB.hide()

        self.qty_FPCA.hide()
        self.label_FPCA.hide()

        self.qty_FPCB.hide()
        self.label_FPCB.hide()


# Method responsible for TX items in upgrade Window
def upgrade_TX_checkBox(self):
    if self.checkBox_TX.isChecked():
        self.qty_FTIB.show()
        self.label_FTIB.show()

        self.qty_FTIF.show()
        self.label_FTIF.show()

        self.qty_FIQB.show()
        self.label_FIQB.show()

    else:
        self.qty_FTIB.hide()
        self.label_FTIB.hide()

        self.qty_FTIF.hide()
        self.label_FTIF.hide()

        self.qty_FIQB.hide()
        self.label_FIQB.hide()


# Method responsible for SM items in upgrade Window
def upgrade_SM_checkBox(self):
    if self.checkBox_SM.isChecked():
        self.qty_FSMF.show()
        self.label_FSMF.show()

        self.qty_ASIA.show()
        self.label_ASIA.show()

        self.qty_ABIA.show()
        self.label_ABIA.show()

        self.qty_FBBA.show()
        self.label_FBBA.show()

        self.qty_FBBC.show()
        self.label_FBBC.show()

        self.qty_FTIF.show()
        self.label_FTIF.show()

        self.qty_FPFD.show()
        self.label_FPFD.show()

        self.qty_FPFC.show()
        self.label_FPFC.show()

        self.qty_FPFH.show()
        self.label_FPFH.show()

        self.qty_FOSH.show()
        self.label_FOSH.show()

        self.qty_FPCA.show()
        self.label_FPCA.show()

        self.qty_FMCA.show()
        self.label_FMCA.show()

        self.qty_FUFAS.show()
        self.label_FUFAS.show()

        self.qty_FPCA.show()
        self.label_FPCA.show()

        self.qty_FPCB.show()
        self.label_FPCB.show()

    else:
        self.qty_FSMF.hide()
        self.label_FSMF.hide()

        self.qty_ASIA.hide()
        self.label_ASIA.hide()

        self.qty_ABIA.hide()
        self.label_ABIA.hide()

        self.qty_FBBA.hide()
        self.label_FBBA.hide()

        self.qty_FBBC.hide()
        self.label_FBBC.hide()

        self.qty_FTIF.hide()
        self.label_FTIF.hide()

        self.qty_FPFD.hide()
        self.label_FPFD.hide()

        self.qty_FPFC.hide()
        self.label_FPFC.hide()

        self.qty_FPFH.hide()
        self.label_FPFH.hide()

        self.qty_FOSH.hide()
        self.label_FOSH.hide()

        self.qty_FPCA.hide()
        self.label_FPCA.hide()

        self.qty_FMCA.hide()
        self.label_FMCA.hide()

        self.qty_FUFAS.hide()
        self.label_FUFAS.hide()

        self.qty_FPCA.hide()
        self.label_FPCA.hide()

        self.qty_FPCB.hide()
        self.label_FPCB.hide()


# Method responsible for cables items in upgrade Window
def upgrade_cables_checkBox(self):
    if self.checkBox_cables.isChecked():
        self.qty_RDSA_cable.show()
        self.label_RDSA_cable.show()

        self.qty_ESFA.show()
        self.label_ESFA.show()

        self.qty_ESFB.show()
        self.label_ESFB.show()

        self.qty_FTSF.show()
        self.label_FTSF.show()

        self.qty_FUFAS.show()
        self.label_FUFAS.show()

        self.qty_FUFAY.show()
        self.label_FUFAY.show()

        self.qty_FUFBB.show()
        self.label_FUFBB.show()

        self.qty_FSEE.show()
        self.label_FSEE.show()

        self.qty_FSEB.show()
        self.label_FSEB.show()

        self.qty_FSEF.show()
        self.label_FSEF.show()

        self.qty_FSAH.show()
        self.label_FSAH.show()

        self.qty_FSAP.show()
        self.label_FSAP.show()

        self.qty_FPCA.show()
        self.label_FPCA.show()

        self.qty_FPCB.show()
        self.label_FPCB.show()

        self.qty_FTCR.show()
        self.label_FTCR.show()

    else:
        self.qty_RDSA_cable.hide()
        self.label_RDSA_cable.hide()

        self.qty_ESFA.hide()
        self.label_ESFA.hide()

        self.qty_ESFB.hide()
        self.label_ESFB.hide()

        self.qty_FTSF.hide()
        self.label_FTSF.hide()

        self.qty_FUFAS.hide()
        self.label_FUFAS.hide()

        self.qty_FUFAY.hide()
        self.label_FUFAY.hide()

        self.qty_FUFBB.hide()
        self.label_FUFBB.hide()

        self.qty_FSEE.hide()
        self.label_FSEE.hide()

        self.qty_FSEB.hide()
        self.label_FSEB.hide()

        self.qty_FSEF.hide()
        self.label_FSEF.hide()

        self.qty_FSAH.hide()
        self.label_FSAH.hide()

        self.qty_FSAP.hide()
        self.label_FSAP.hide()

        self.qty_FPCA.hide()
        self.label_FPCA.hide()

        self.qty_FPCB.hide()
        self.label_FPCB.hide()

        self.qty_FTCR.hide()
        self.label_FTCR.hide()


# Method responsible for jumpers items in upgrade Window
def upgrade_jumpers_checkBox(self):
    if self.checkBox_jumpers.isChecked():
        self.qty_7_16_9m.show()
        self.label_9716.show()

        self.qty_4to7_9m.show()
        self.label_947.show()

        self.qty_7to4_9m.show()
        self.label_974.show()

        self.qty_4_3_9m.show()
        self.label_943.show()

        self.qty_7_16_5m.show()
        self.label_5716.show()

        self.qty_4to7_5m.show()
        self.label_547.show()

        self.qty_7to4_5m.show()
        self.label_574.show()

        self.qty_4_3_5m.show()
        self.label_543.show()

    else:
        self.qty_7_16_9m.hide()
        self.label_9716.hide()

        self.qty_4to7_9m.hide()
        self.label_947.hide()

        self.qty_7to4_9m.hide()
        self.label_974.hide()

        self.qty_4_3_9m.hide()
        self.label_943.hide()

        self.qty_7_16_5m.hide()
        self.label_5716.hide()

        self.qty_4to7_5m.hide()
        self.label_547.hide()

        self.qty_7to4_5m.hide()
        self.label_574.hide()

        self.qty_4_3_5m.hide()
        self.label_543.hide()


# Method responsible for accessories items in upgrade Window
def upgrade_accessories_checkBox(self):
    if self.checkBox_accessories.isChecked():

        self.qty_FSEP.show()
        self.label_FSEP.show()

        self.qty_FSEC.show()
        self.label_FSEC.show()

        self.qty_FSES.show()
        self.label_FSES.show()

        self.qty_FMFA.show()
        self.label_FMFA.show()

        self.qty_FMCA.show()
        self.label_FMCA.show()

        self.qty_EMHA.show()
        self.label_EMHA.show()

        self.qty_EMHH.show()
        self.label_EMHH.show()

        self.qty_FPKC.show()
        self.label_FPKC.show()

        self.qty_FPFC.show()
        self.label_FPFC.show()

        self.qty_FPFH.show()
        self.label_FPFH.show()

        self.qty_FPFD.show()
        self.label_FPFD.show()

        self.qty_FOSL.show()
        self.label_FOSL.show()

        self.qty_FOSN.show()
        self.label_FOSN.show()

        self.qty_FOSD.show()
        self.label_FOSD.show()

        self.qty_FOSH.show()
        self.label_FOSH.show()

        self.qty_ESFA.show()
        self.label_ESFA.show()

        self.qty_ESFB.show()
        self.label_ESFB.show()

        self.qty_FTSF.show()
        self.label_FTSF.show()

    else:

        self.qty_FSEP.hide()
        self.label_FSEP.hide()

        self.qty_FSEC.hide()
        self.label_FSEC.hide()

        self.qty_FSES.hide()
        self.label_FSES.hide()

        self.qty_FMFA.hide()
        self.label_FMFA.hide()

        self.qty_FMCA.hide()
        self.label_FMCA.hide()

        self.qty_EMHA.hide()
        self.label_EMHA.hide()

        self.qty_EMHH.hide()
        self.label_EMHH.hide()

        self.qty_FPKC.hide()
        self.label_FPKC.hide()

        self.qty_FPFC.hide()
        self.label_FPFC.hide()

        self.qty_FPFH.hide()
        self.label_FPFH.hide()

        self.qty_FPFD.hide()
        self.label_FPFD.hide()

        self.qty_FOSL.hide()
        self.label_FOSL.hide()

        self.qty_FOSN.hide()
        self.label_FOSN.hide()

        self.qty_FOSD.hide()
        self.label_FOSD.hide()

        self.qty_FOSH.hide()
        self.label_FOSH.hide()

        self.qty_ESFA.hide()
        self.label_ESFA.hide()

        self.qty_ESFB.hide()
        self.label_ESFB.hide()

        self.qty_FTSF.hide()
        self.label_FTSF.hide()


# Method to initialize all Values in Upgrade Window
def reset_upgrade_window(self):
    upgrade_items_hide(self)
    self.appendBtn_upgrade.setEnabled(True)
    self.saveBtn_upgrade.setEnabled(False)
    self.checkBox_all.setChecked(False)
    self.checkBox_SM.setChecked(False)
    self.checkBox_RF.setChecked(False)
    self.checkBox_TX.setChecked(False)
    self.checkBox_accessories.setChecked(False)
    self.checkBox_cables.setChecked(False)
    self.checkBox_jumpers.setChecked(False)
    self.sitename_upgrade.setText("")
    self.woID_upgrade.setText("")
    self.qty_FSMF.setValue(0)
    self.qty_ASIA.setValue(0)
    self.qty_ABIA.setValue(0)
    self.qty_FBBA.setValue(0)
    self.qty_FBBC.setValue(0)
    self.qty_FXDB.setValue(0)
    self.qty_AREA.setValue(0)
    self.qty_FHDB.setValue(0)
    self.qty_RDSA_kit.setValue(0)
    self.qty_RDSA_cable.setValue(0)
    self.qty_FXEB.setValue(0)
    self.qty_FXED.setValue(0)
    self.qty_FXEF.setValue(0)
    self.qty_FHEB.setValue(0)
    self.qty_ARDA.setValue(0)
    self.qty_FRGU.setValue(0)
    self.qty_FRGT.setValue(0)
    self.qty_FRGX.setValue(0)
    self.qty_ARGA.setValue(0)
    self.qty_FTIB.setValue(0)
    self.qty_FTIF.setValue(0)
    self.qty_FIQB.setValue(0)
    self.qty_FSEP.setValue(0)
    self.qty_FSEC.setValue(0)
    self.qty_FSES.setValue(0)
    self.qty_FMFA.setValue(0)
    self.qty_FMCA.setValue(0)
    self.qty_EMHA.setValue(0)
    self.qty_EMHH.setValue(0)
    self.qty_FPKC.setValue(0)
    self.qty_FPFC.setValue(0)
    self.qty_FPFH.setValue(0)
    self.qty_FPFD.setValue(0)
    self.qty_FOSL.setValue(0)
    self.qty_FOSN.setValue(0)
    self.qty_FOSD.setValue(0)
    self.qty_FOSH.setValue(0)
    self.qty_7_16_9m.setValue(0)
    self.qty_4to7_9m.setValue(0)
    self.qty_7to4_9m.setValue(0)
    self.qty_4_3_9m.setValue(0)
    self.qty_7_16_5m.setValue(0)
    self.qty_4to7_5m.setValue(0)
    self.qty_7to4_5m.setValue(0)
    self.qty_4_3_5m.setValue(0)
    self.qty_ESFA.setValue(0)
    self.qty_ESFB.setValue(0)
    self.qty_FTSF.setValue(0)
    self.qty_FUFAS.setValue(0)
    self.qty_FUFAY.setValue(0)
    self.qty_FUFBB.setValue(0)
    self.qty_FSEE.setValue(0)
    self.qty_FSEB.setValue(0)
    self.qty_FSEF.setValue(0)
    self.qty_FSAH.setValue(0)
    self.qty_FSAP.setValue(0)
    self.qty_FPCA.setValue(0)
    self.qty_FPCB.setValue(0)
    self.qty_FTCR.setValue(0)


# Methods GUI SRAN DWO
def initial_SRAN_GUI(self):
    # 2G Configuration
    self.label_3.hide()
    self.label_5.hide()
    self.label_14.hide()
    self.label_15.hide()
    self.label_45.hide()
    self.trx_S1.hide()
    self.trx_S2.hide()
    self.trx_S3.hide()
    self.trx_S4.hide()
    self.trxS1_Pwr.hide()
    self.trxS2_Pwr.hide()
    self.trxS3_Pwr.hide()
    self.trxS4_Pwr.hide()
    self.B900_RFtype.hide()
    self.label_49.hide()
    self.dcs_RFtype.hide()
    self.label_16.hide()
    self.label_12.hide()
    self.label_19.hide()
    self.label_20.hide()
    self.trx_S1_dcs.hide()
    self.trx_S2_dcs.hide()
    self.trx_S3_dcs.hide()
    self.trx_S4_dcs.hide()
    # 3G Configuration
    self.label_25.hide()
    self.label_26.hide()
    self.label_27.hide()
    self.label_28.hide()
    self.label_46.hide()
    self.label_48.hide()
    self.u2100_carriers.hide()
    self.CE_2100.hide()
    self.HSUPA_2100.hide()
    self.HSDPA_2100.hide()
    self.CE_900.hide()
    self.HSUPA_900.hide()
    self.HSDPA_900.hide()
    self.pwr_U2100.hide()
    self.pwr_U900.hide()
    self.B2100_RFtype.hide()
    # LTE Configuration
    self.checkBox_L900.setEnabled(False)
    self.checkBox_L2100.setEnabled(False)
    self.label_39.hide()
    self.label_34.hide()
    self.label_42.hide()
    self.label_35.hide()
    self.label_36.hide()
    self.label_37.hide()
    self.label_38.hide()
    self.label_40.hide()
    self.label_41.hide()
    self.label_47.hide()
    self.L900_BW.hide()
    self.L900_pwr.hide()
    self.L1800_BW.hide()
    self.L1800_pwr.hide()
    self.L2100_BW.hide()
    self.L2100_pwr.hide()
    self.B1800_RFtype.hide()


def checkBox_DCS_clicked(self):
    if self.checkBox_DCS.isChecked():
        self.label_49.show()
        self.dcs_RFtype.show()
        self.label_16.show()
        self.label_12.show()
        self.label_19.show()
        self.label_20.show()
        self.trx_S1_dcs.show()
        self.trx_S2_dcs.show()
        self.trx_S3_dcs.show()
        self.trx_S4_dcs.show()

    else:
        self.label_49.hide()
        self.dcs_RFtype.hide()
        self.label_16.hide()
        self.label_12.hide()
        self.label_19.hide()
        self.label_20.hide()
        self.trx_S1_dcs.hide()
        self.trx_S2_dcs.hide()
        self.trx_S3_dcs.hide()
        self.trx_S4_dcs.hide()


def checkBox_GSM_clicked(self):
    if self.checkBox_GSM.isChecked():
        self.trxS1_Pwr.setCurrentText('10W')
        self.trxS2_Pwr.setCurrentText('10W')
        self.trxS3_Pwr.setCurrentText('10W')
        self.trxS4_Pwr.setCurrentText('10W')
        self.label_3.show()
        self.label_5.show()
        self.label_14.show()
        self.label_15.show()
        self.label_45.show()
        self.trx_S1.show()
        self.trx_S2.show()
        self.trx_S3.show()
        self.trx_S4.show()
        self.trxS1_Pwr.show()
        self.trxS2_Pwr.show()
        self.trxS3_Pwr.show()
        self.trxS4_Pwr.show()
        self.B900_RFtype.show()
    else:
        self.label_3.hide()
        self.label_5.hide()
        self.label_14.hide()
        self.label_15.hide()
        self.label_45.hide()
        self.trx_S1.hide()
        self.trx_S2.hide()
        self.trx_S3.hide()
        self.trx_S4.hide()
        self.trxS1_Pwr.hide()
        self.trxS2_Pwr.hide()
        self.trxS3_Pwr.hide()
        self.trxS4_Pwr.hide()
        self.B900_RFtype.hide()


def checkBox_U900_clicked(self):
    if self.checkBox_U900.isChecked():
        self.label_25.show()
        self.label_26.show()
        self.label_27.show()
        self.label_28.show()
        self.label_46.show()
        self.CE_900.show()
        self.HSUPA_900.show()
        self.HSDPA_900.show()
        self.pwr_U900.show()
        self.B2100_RFtype.show()
        self.CE_900.setText("275")
        self.HSUPA_900.setText("2")
        self.HSDPA_900.setText("1")
    else:
        self.label_25.hide()
        self.label_26.hide()
        self.label_27.hide()
        self.label_28.hide()
        self.label_46.hide()
        self.CE_900.hide()
        self.HSUPA_900.hide()
        self.HSDPA_900.hide()
        self.pwr_U900.hide()
        self.B2100_RFtype.hide()


def checkBox_U2100_clicked(self):
    if self.checkBox_U2100.isChecked():
        self.label_25.show()
        self.label_26.show()
        self.label_27.show()
        self.label_28.show()
        self.label_46.show()
        self.label_48.show()
        self.u2100_carriers.show()
        self.CE_2100.show()
        self.HSUPA_2100.show()
        self.HSDPA_2100.show()
        self.pwr_U2100.show()
        self.B2100_RFtype.show()
    else:
        self.label_25.hide()
        self.label_26.hide()
        self.label_27.hide()
        self.label_28.hide()
        self.label_46.hide()
        self.label_48.hide()
        self.u2100_carriers.hide()
        self.CE_2100.hide()
        self.HSUPA_2100.hide()
        self.HSDPA_2100.hide()
        self.pwr_U2100.hide()
        self.B2100_RFtype.hide()


def checkBox_L900_clicked(self):
    if self.checkBox_L900.isChecked():
        self.label_39.show()
        self.label_35.show()
        self.label_36.show()
        self.L900_BW.show()
        self.L900_pwr.show()

    else:
        self.label_39.hide()
        self.label_35.hide()
        self.label_36.hide()
        self.L900_BW.hide()
        self.L900_pwr.hide()


def checkBox_L2100_clicked(self):
    if self.checkBox_L2100.isChecked():
        self.label_34.show()
        self.label_40.show()
        self.label_41.show()
        self.L2100_BW.show()
        self.L2100_pwr.show()

    else:
        self.label_34.hide()
        self.label_40.hide()
        self.label_41.hide()
        self.L2100_BW.hide()
        self.L2100_pwr.hide()


def checkBox_L1800_clicked(self):
    if self.checkBox_L1800.isChecked():
        self.checkBox_L900.setEnabled(True)
        self.checkBox_L2100.setEnabled(True)
        self.L900_BW.setCurrentText('5')
        self.L1800_BW.setCurrentText('15')
        self.L2100_BW.setCurrentText('5')
        self.L1800_pwr.setCurrentText('60')
        self.label_42.show()
        self.label_37.show()
        self.label_38.show()
        self.label_47.show()
        self.L1800_BW.show()
        self.L1800_pwr.show()
        self.B1800_RFtype.show()

    else:
        self.checkBox_L900.setEnabled(False)
        self.checkBox_L2100.setEnabled(False)
        self.checkBox_L900.setChecked(False)
        self.checkBox_L2100.setChecked(False)
        self.label_42.hide()
        self.label_37.hide()
        self.label_38.hide()
        self.label_47.hide()
        self.L1800_BW.hide()
        self.L1800_pwr.hide()
        self.B1800_RFtype.hide()
