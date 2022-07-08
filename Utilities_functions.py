from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
from Utilities_GUI import success_message

upgrade_MO = ""
stock_wb = ""


# Method responsible for generating filtered Stock sheet for claiming POs
def prepare_stock_wb(self):
    global stock_wb
    fileName = QFileDialog.getOpenFileName(filter="Excel (*.xlsx *.xls *.csv)")
    if fileName[1] != "":
        try:
            path = fileName[0]
            df = pd.read_excel(path)
            new_header = df.iloc[4]
            df = df[5:]
            df.columns = new_header
            df1 = df[df.Available > 7]
            stock_wb = df1.sort_values('Locator "PO#"', ascending=True)
            header_list = stock_wb.columns.values
            if len(header_list) == 11:
                stock_wb.drop(stock_wb.columns[[0, 4, 5, 6, 8, 9, 10]], axis=1, inplace=True)
            elif len(header_list) == 8:
                stock_wb.drop(stock_wb.columns[[0, 4, 5, 6]], axis=1, inplace=True)
            cols = list(stock_wb.columns.values)
            cols.pop(cols.index('Item Code'))
            stock_wb = stock_wb[['Item Code'] + cols]
            stock_wb.drop_duplicates(subset="Item Code", keep='first', inplace=True)
            self.label_3.setPixmap(QPixmap(':/images/tick_icon.png'))
            success_message(self, "Done", "Stock Loaded Successfully!")
            self.newsiteWinBtn.setEnabled(True)
            self.upgradeWinBtn.setEnabled(True)
            self.tddWinBtn.setEnabled(True)
            self.upload_stock_btn.setEnabled(False)
            return stock_wb
        except Exception:
            print(Exception)
            self.label_3.setPixmap(QPixmap(':/images/cross_icon.png'))
            success_message(self, "Caution!", "Something went wrong! Please check uploaded file")
    else:
        success_message(self, "Caution!","Balance sheet not uploaded")
        self.label_3.setPixmap(QPixmap(':/images/cross_icon.png'))


# Method responsible for creating MO template
def df_to_MO_template(dataFrame):
    global upgrade_MO
    if dataFrame is None:
        return None
    else:
        upgrade_MO = dataFrame
        upgrade_MO.insert(1, "Location", "NokiaSiemens", True)
        upgrade_MO.insert(2, "Transaction Type", "Move Order Issue", True)
        upgrade_MO.insert(4, 'From Sub-Inventory', upgrade_MO['Item Code'].map(stock_wb.set_index('Item Code')
                                                                               ['Subinventory']))
        upgrade_MO.insert(5, "From Locator", upgrade_MO['Item Code'].map(stock_wb.set_index('Item Code')
                                                                         ['Locator "PO#"']))
        upgrade_MO.insert(6, "To Sub-Inventory", "", True)
        upgrade_MO.insert(7, "To Locator", "", True)
        upgrade_MO.insert(8, "Serial", "", True)
        upgrade_MO.insert(9, "Reference", "", True)
        upgrade_MO.insert(11, "UOM", "EAC", True)
        upgrade_MO.insert(12, "Account", "1.000.999999.000.000", True)
        upgrade_MO.insert(14, "Backup (Qty)", "", True)

        for cell, row in upgrade_MO.iterrows():
            if row['From Sub-Inventory'] == "nokia-used":
                if row['Item Code'] == "BSS-HW-NSN-472182A":  # FBBA
                    df_FBBA = pd.DataFrame({'Reason': [row['Reason'], row['Reason']],
                                            'Location': ["NokiaSiemens", "NokiaSiemens"],
                                            "Transaction Type": ["Move Order Issue", "Move Order Issue"],
                                            'Item Code': ["BSS-HW-ACCNSN-995297", "BSS-HW-ACCNSN-995298"],
                                            'From Sub-Inventory': ["nokia-used", "nokia-used"],
                                            "From Locator": ["", ""],
                                            "To Sub-Inventory": ["", ""], "To Locator": ["", ""], "Serial": ["", ""],
                                            "Reference": ["", ""], 'Quantity': [row['Quantity'], row['Quantity']],
                                            "UOM": ["EAC", "EAC"],
                                            "Account": ["1.000.999999.000.000", "1.000.999999.000.000"],
                                            'WO ID': [row['WO ID'], row['WO ID']], "Backup (Qty)": ["", ""]})
                    # upgrade_MO = upgrade_MO.append(df_FBBA, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FBBA])

                elif row['Item Code'] == "3G-HW-NOKIA-472797A":  # FBBC
                    df_FBBC = pd.DataFrame(
                        {'Reason': [row['Reason'], row['Reason']], 'Location': ["NokiaSiemens", "NokiaSiemens"],
                         "Transaction Type": ["Move Order Issue", "Move Order Issue"],
                         'Item Code': ["3G-HW-ACCNOK-995297", "3G-HW-ACCNOK-995298"],
                         'From Sub-Inventory': ["nokia-used", "nokia-used"], "From Locator": ["", ""],
                         "To Sub-Inventory": ["", ""], "To Locator": ["", ""], "Serial": ["", ""],
                         "Reference": ["", ""], 'Quantity': [row['Quantity'], row['Quantity']], "UOM": ["EAC", "EAC"],
                         "Account": ["1.000.999999.000.000", "1.000.999999.000.000"],
                         'WO ID': [row['WO ID'], row['WO ID']], "Backup (Qty)": ["", ""]})
                    # upgrade_MO = upgrade_MO.append(df_FBBC, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FBBC])

                elif row['Item Code'] == "BSS-HW-NSN-472311A":  # FTIF
                    df_FTIF = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': ["BSS-HW-ACCNSN-985220"], 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FTIF, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FTIF])

                elif row['Item Code'] == "BSS-HW-NSN-472301A":  # FPFD
                    df_FPFD = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "BSS-HW-ACCNSN-108467", 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FPFD, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FPFD])

                elif row['Item Code'] == "3G-HW-NOKIA-472573A":  # FXDB
                    df_FXDB = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "3G-HW-ACCNOK-086147", 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FXDB, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FXDB])

                elif row['Item Code'] == "BSS-HW-NOKIA-473440A":  # FRGX
                    df_FRGX = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "BSS-HW-ACCNOK-086029", 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FRGX, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FRGX])

                elif row['Item Code'] == "BSS-HW-NSN-472924A":  # FXED
                    df_FXED = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "BSS-HW-ACCNSN-086029", 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FXED, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FXED])

                elif row['Item Code'] == "BSS-HW-NSN-472810A":  # FRGT
                    df_FRGT = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "BSS-HW-ACCNSN-086147", 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FRGT, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FRGT])

                elif row['Item Code'] == "BSS-HW-NSN-472501A":  # FXEB
                    df_FXEB = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "BSS-HW-ACCNOK-086147A", 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FXEB, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FXEB])

                elif row['Item Code'] == "BSS-HW-NSN-472956A":  # FRGU
                    df_FRGU = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "BSS-HW-ACCNOK-086029.FRGU", 'From Sub-Inventory': "nokia-used",
                         "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FRGU, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FRGU])

                elif row['Item Code'] == "BSS-HW-NOKIA-473439A":  # FXEF
                    df_FXEF = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "BSS-HW-ACCNOK-086147.FXEF", 'From Sub-Inventory': "nokia-used",
                         "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FXEF, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FXEF])

                elif row['Item Code'] == "3G-HW-NOKIA-471720A":  # FTIB
                    df_FTIB = pd.DataFrame(
                        {'Reason': row['Reason'], 'Location': "NokiaSiemens", "Transaction Type": "Move Order Issue",
                         'Item Code': "3G-HW-ACCNOK-984677", 'From Sub-Inventory': "nokia-used", "From Locator": "",
                         "To Sub-Inventory": "", "To Locator": "", "Serial": "", "Reference": "",
                         'Quantity': [row['Quantity']], "UOM": "EAC", "Account": "1.000.999999.000.000",
                         'WO ID': row['WO ID'], "Backup (Qty)": ""})
                    # upgrade_MO = upgrade_MO.append(df_FTIB, ignore_index=True)
                    upgrade_MO = pd.concat([upgrade_MO, df_FTIB])

                else:
                    pass

            elif row['From Sub-Inventory'] == "":
                row[cell, 'From Sub-Inventory'] = "nokia-used"
            else:
                pass

        # for cell, row in upgrade_MO.iterrows():
        #     if row['Item Code'] == 'BSS-HW-NOKIA-473187A':
        #         if row['From Sub-Inventory'].cell == '':
        #             df_FMCH = pd.DataFrame({'Reason': [row['Reason'], row['Reason']],
        #                                     'Location': ["NokiaSiemens", "NokiaSiemens"],
        #                                     "Transaction Type": ["Move Order Issue", "Move Order Issue"],
        #                                     'Item Code': ["New-HW-NOKIA-082795A", "BSS-HW-NOKIA-473186A"],
        #                                     'From Sub-Inventory': ["nokia-used", "nokia-used"],
        #                                     "From Locator": ["", ""],
        #                                     "To Sub-Inventory": ["", ""], "To Locator": ["", ""], "Serial": ["", ""],
        #                                     "Reference": ["", ""], 'Quantity': [row['Quantity'], row['Quantity']],
        #                                     "UOM": ["EAC", "EAC"],
        #                                     "Account": ["1.000.999999.000.000", "1.000.999999.000.000"],
        #                                     'WO ID': [row['WO ID'], row['WO ID']], "Backup (Qty)": ["", ""]})
        #             upgrade_MO = upgrade_MO.append(df_FMCH, ignore_index=True)

        return upgrade_MO


# Method responsible for saving output to excel workbook
def save_excel_file(self, dataFrame, site_name):
    if dataFrame is None:
        return None
    else:
        response = QFileDialog.getSaveFileName(caption='Save your MO', directory=f'{site_name} MO',
                                               filter="Excel (*.xlsx *.xls *.csv)")
        if response[0] != "":
            dataFrame.to_excel(response[0], index=False)
            success_message(self, "Done", f"{site_name} MO saved Successfully")
        else:
            success_message(self, "Caution!", "File Not Saved!")


# Methods for sites configuration
def pwr_sector(x, y):
    sector_pwr = x * y
    return sector_pwr


def get_power(x):
    trx_pwr = 0
    if x == "5W":
        trx_pwr = 5
    elif x == "10W":
        trx_pwr = 10
    elif x == "12W":
        trx_pwr = 12
    elif x == "15W":
        trx_pwr = 15
    elif x == "20W":
        trx_pwr = 20
    elif x == "30W":
        trx_pwr = 30
    elif x == "40W":
        trx_pwr = 40
    elif x == "53W":
        trx_pwr = 53
    elif x == "60W":
        trx_pwr = 60
    elif x == "80W":
        trx_pwr = 80
    return trx_pwr
