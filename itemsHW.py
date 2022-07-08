import pandas as pd


list_all_items = []
list_all_quantities = []
list_site_name = []
list_woID = []


def lists_to_dataframe(l1, l2, l3, l4):
    MO_df = pd.DataFrame(columns=['Reason', 'Item Code', 'Quantity', 'WO ID'])
    to_append_df = pd.DataFrame(list(zip(l1, l2, l3, l4)), columns=['Reason', 'Item Code', 'Quantity', 'WO ID'])
    temp_df = pd.concat([MO_df, to_append_df], axis=0)
    temp1_df = temp_df[temp_df.Quantity != 0]
    MO_df = temp1_df
    return MO_df


class SM:
    def __init__(self, site_name, woID, type_SM, qty_SM):
        self.type_SM = type_SM
        self.qty_SM = qty_SM
        self.site_name = site_name
        self.woID = woID

        self.dest_df = pd.DataFrame(columns=['Reason', 'Item Code', 'Quantity', 'WO ID'])
        self.SM_list = [self.get_SM_itemCode()]
        self.SM_quantity_list = [self.get_qty_SM()]
        self.site_name_list = [site_name] * len(self.SM_list)
        self.woID_list = [woID] * len(self.SM_list)
        list_all_items.extend(self.SM_list)
        list_all_quantities.extend(self.SM_quantity_list)
        list_site_name.extend(self.site_name_list)
        list_woID.extend(self.woID_list)

    def get_type_SM(self):
        return self.type_SM

    def get_qty_SM(self):
        return self.qty_SM

    def get_SM_itemCode(self):
        itemCode_SM = ""
        if self.type_SM == "FSMF":
            itemCode_SM = "BSS-HW-NSN-472181A"
        elif self.type_SM == "FBBA":
            itemCode_SM = "BSS-HW-NSN-472182A"
        elif self.type_SM == "FBBC":
            itemCode_SM = "3G-HW-NOKIA-472797A"
        else:
            print("SM not recognized")
        return itemCode_SM


class RF:
    def __init__(self, site_name, woID,  type_RF, qty_RF):
        self.type_RF = type_RF
        self.qty_RF = qty_RF
        print(f"RF module type is {self.get_type_RF()} and item code {self.get_RF_itemCode()} "
              f"with quantity = {self.get_qty_RF()} ")

        self.RF_list = [self.get_RF_itemCode(), self.get_FMCH_itemCode(), self.get_CASSING_itemCode(),
                        self.get_EMHA_itemCode(), self.get_FSES_itemCode()]
        self.RF_quantity_list = [self.get_qty_RF(), self.get_FMCH(), self.get_CASSING(), self.get_EMHA(), self.get_FSES()]
        self.site_name_list = [site_name] * len(self.RF_list)
        self.woID_list = [woID] * len(self.RF_list)
        list_all_items.extend(self.RF_list)
        list_all_quantities.extend(self.RF_quantity_list)
        list_site_name.extend(self.site_name_list)
        list_woID.extend(self.woID_list)

    def get_type_RF(self):
        return self.type_RF

    def get_qty_RF(self):
        return self.qty_RF

    def get_RF_itemCode(self):
        itemCode_RF = ""
        if self.type_RF == "ARGA":
            itemCode_RF = "BSS-HW-NOKIA-474800A"
        elif self.type_RF == "AREA":
            itemCode_RF = "BSS-HW-NOKIA-474198A"
        elif self.type_RF == "ARDA":
            itemCode_RF = "BSS-HW-NOKIA-474840A"
        elif self.type_RF == "FRGT":
            itemCode_RF = "BSS-HW-NSN-472810A"
        elif self.type_RF == "FXED":
            itemCode_RF = "BSS-HW-NSN-472924A"
        elif self.type_RF == "FXDB":
            itemCode_RF = "3G-HW-NOKIA-472573A"
        elif self.type_RF == "FRGU":
            itemCode_RF = "BSS-HW-NSN-472956A"
        else:
            print("RF not recognized")
        return itemCode_RF

    def get_FMCH(self):
        if self.type_RF == "AREA" or self.type_RF == "ARDA" or self.type_RF == "ARGA":
            qty_FMCH = self.qty_RF
        else:
            qty_FMCH = 0
        return qty_FMCH

    @staticmethod
    def get_FMCH_itemCode():
        itemCode_FMCH = "BSS-HW-NOKIA-473186A"
        return itemCode_FMCH

    def get_CASSING(self):
        if self.type_RF == "AREA" or self.type_RF == "ARDA" or self.type_RF == "ARGA":
            qty_CASSING = self.qty_RF
        else:
            qty_CASSING = 0
        return qty_CASSING

    @staticmethod
    def get_CASSING_itemCode():
        itemCode_CASSING = "New-HW-NOKIA-082795A"
        return itemCode_CASSING

    def get_EMHA(self):
        if self.type_RF == "FXDB" or self.type_RF == "FRGT" or self.type_RF == "FXED" or self.type_RF == "FRGU":
            qty_EMHA = self.qty_RF
        else:
            qty_EMHA = 0
        return qty_EMHA

    @staticmethod
    def get_EMHA_itemCode():
        itemCode_EMHA = "3G-HW-NOKIA-470316A"
        return itemCode_EMHA

    def get_FSES(self):
        if self.type_RF == "FXDB" or self.type_RF == "FRGT" or self.type_RF == "FXED" or self.type_RF == "FRGU":
            qty_FSES = self.qty_RF
        else:
            qty_FSES = 0

        return qty_FSES

    @staticmethod
    def get_FSES_itemCode():
        itemCode_FSES = "3G-HW-NOKIA-472285A"
        return itemCode_FSES


class Jumpers:
    def __init__(self, siteName, woID, num_sectors, jumper_type, is_GSM, is_DCS, is_UMTS, is_LTE):
        self.siteName = siteName
        self.woID = woID
        self.num_sectors = num_sectors
        self.jumper_type = jumper_type
        self.is_GSM = is_GSM
        self.is_UMTS = is_UMTS
        self.is_LTE = is_LTE
        self.is_DCS = is_DCS

        self.jumper_list = [self.get_jumper_itemCode()]
        self.quantity_list = [self.get_jumper_qty()]
        self.site_name_list = [siteName] * len(self.jumper_list)
        self.woID_list = [woID] * len(self.jumper_list)
        self.dest_df = pd.DataFrame(columns=['Reason', 'Item Code', 'Quantity', 'WO ID'])

        list_all_items.extend(self.jumper_list)
        list_all_quantities.extend(self.quantity_list)
        list_site_name.extend(self.site_name_list)
        list_woID.extend(self.woID_list)

    def get_num_of_sectors(self):
        return self.num_sectors

    def set_num_of_sectors(self, num_of_sectors):
        self.num_sectors = num_of_sectors
        return self.num_sectors

    def get_jumper_type(self):
        return self.jumper_type

    def set_jumper_type(self, type_jumper):
        self.jumper_type = type_jumper
        return self.jumper_type

    def get_jumper_qty(self):
        qty_jumper = 0
        if self.is_GSM:
            gsm_jumper = self.num_sectors * 2
            qty_jumper = qty_jumper + gsm_jumper

        if self.is_DCS:
            gsm_jumper = self.num_sectors * 2
            qty_jumper = qty_jumper + gsm_jumper

        if self.is_UMTS:
            umts_jumper = self.num_sectors * 2
            qty_jumper = qty_jumper + umts_jumper

        if self.is_LTE:
            lte_jumper = self.num_sectors * 2
            qty_jumper = qty_jumper + lte_jumper

        return qty_jumper

    def get_jumper_itemCode(self):
        itemCode_jumper = ""
        if self.jumper_type == "Jumpers_4.3-10 To 4.3-10_5M":
            itemCode_jumper = "BSS-HW-NOKIA-CS75217.05"
        elif self.jumper_type == "Jumpers_4.3-10 To 4.3-10_9M":
            itemCode_jumper = "BSS-HW-NOKIA-CS75108.09"
        elif self.jumper_type == "Jumpers_4.3-10 To 7/16_5M":
            itemCode_jumper = "HW-3G-NOKIA-CS75209.05"
        elif self.jumper_type == "Jumpers_4.3-10 To 7/16_9M":
            itemCode_jumper = "BSS-HW-NOKIA-CS75209.09"
        else:
            print("Jumper type not recognized")

        return itemCode_jumper


class HW_items:
    # RRH Type = Feederless, Feeder, Roof Top
    def __init__(self, siteName, woID, qty_SM, qty_RF, type_RRH):
        self.qty_SM = qty_SM
        self.qty_RF = qty_RF
        self.type_RRH = type_RRH

        self.items_list = \
            [self.get_FMFA_itemCode(), self.get_FMCA_itemCode(), self.get_FTIF_itemCode(), self.get_FPFD_itemCode(),
             self.get_FSAP_itemCode(), self.get_FSEE_itemCode(), self.get_FTCR_itemCode(), self.get_FPCA_itemCode(),
             self.get_FOSH_itemCode(), self.get_FUFAY_itemCode(), self.get_FUFAS_itemCode(), self.get_FUFBB_itemCode(),
             self.get_FPKC_itemCode()]
        self.quantity_list = [self.get_FMFA(), self.get_FMCA(), self.get_FTIF(), self.get_FPFD(), self.get_FSAP(),
                              self.get_FSEE(), self.get_FTCR(), self.get_FPCA(), self.get_FOSH(), self.get_FUFAY(),
                              self.get_FUFAS(), self.get_FUFBB(), self.get_FPKC()]
        self.site_name_list = [siteName] * len(self.items_list)
        self.woID_list = [woID] * len(self.items_list)
        self.dest_df = pd.DataFrame(columns=['Reason', 'Item Code', 'Quantity', 'WO ID'])

        list_all_items.extend(self.items_list)
        list_all_quantities.extend(self.quantity_list)
        list_site_name.extend(self.site_name_list)
        list_woID.extend(self.woID_list)

    def get_RRH_type(self):
        return self.type_RRH

    def set_RRH_type(self, type_RRH):
        self.type_RRH = type_RRH
        return self.type_RRH

    def get_FMFA(self):
        if self.qty_RF > 7:
            qty_FMFA = 2
        else:
            qty_FMFA = 1

        return qty_FMFA

    @staticmethod
    def get_FMFA_itemCode():
        itemCode_FMFA = "BSS-HW-NSN-470149A"
        return itemCode_FMFA

    def get_FMCA(self):
        qty_FMCA = self.qty_SM
        return qty_FMCA

    @staticmethod
    def get_FMCA_itemCode():
        itemCode_FMCA = "HW-3G-NOKIA-470239A"
        return itemCode_FMCA

    def get_FTIF(self):
        qty_FTIF = 0
        if self.qty_SM == 0:
            qty_FTIF = 0
        elif self.qty_SM == 1 or self.qty_SM == 2:
            qty_FTIF = 1
        elif self.qty_SM > 2:
            qty_FTIF = 2

        return qty_FTIF

    @staticmethod
    def get_FTIF_itemCode():
        itemCode_FTIF = "BSS-HW-NSN-472311A"
        return itemCode_FTIF

    def get_FPFD(self):
        qty_FPFD = self.qty_SM
        return qty_FPFD

    @staticmethod
    def get_FPFD_itemCode():
        itemCode_FPFD = "BSS-HW-NSN-472301A"
        return itemCode_FPFD

    @staticmethod
    def get_FSAP():
        qty_FSAP = 1
        return qty_FSAP

    @staticmethod
    def get_FSAP_itemCode():
        itemCode_FSAP = "BSS-HW-NOKIA-474118A"
        return itemCode_FSAP

    @staticmethod
    def get_FSEE():
        qty_FSEE = 1
        return qty_FSEE

    @staticmethod
    def get_FSEE_itemCode():
        itemCode_FSEE = "BSS-HW-NOKIA-473751A"
        return itemCode_FSEE

    @staticmethod
    def get_FTCR():
        qty_FTCR = 1
        return qty_FTCR

    @staticmethod
    def get_FTCR_itemCode():
        itemCode_FTCR = "HW-3G-NOKIA-471408A"
        return itemCode_FTCR

    def get_FPCA(self):
        if self.get_RRH_type() == "Feeder":
            qty_FPCA = int(self.qty_SM) + int(self.qty_RF)
        elif self.get_RRH_type() == "Feederless":
            qty_FPCA = 0
        return qty_FPCA

    @staticmethod
    def get_FPCA_itemCode():
        itemCode_FPCA = "BSS-HW-NOKIA-472806A"
        return itemCode_FPCA

    def get_FOSH(self):
        qty_FOSH = (self.get_FUFAY() + self.get_FUFAS() + self.get_FUFBB()) * 2
        return qty_FOSH

    @staticmethod
    def get_FOSH_itemCode():
        itemCode_FOSH = "BSS-HW-NSN-472579A"
        return itemCode_FOSH

    def get_FUFAY(self):
        if self.type_RRH == "Feederless":
            qty_FUFAY = self.qty_RF
        else:
            qty_FUFAY = 0
        return qty_FUFAY

    @staticmethod
    def get_FUFAY_itemCode():
        itemCode_FUFAY = "BSS-HW-NOKIA-473302A"
        return itemCode_FUFAY

    def get_FUFAS(self):
        qty_FUFAS = 0
        if self.qty_SM == 1:
            if self.type_RRH == "Feeder":
                qty_FUFAS = self.qty_RF
            else:
                qty_FUFAS = 0

        elif self.qty_SM == 2:
            if self.type_RRH == "Feeder":
                qty_FUFAS = self.qty_RF + 2
            else:
                qty_FUFAS = 2

        return qty_FUFAS

    @staticmethod
    def get_FUFAS_itemCode():
        itemCode_FUFAS = "BSS-HW-NOKIA-473288A"
        return itemCode_FUFAS

    def get_FUFBB(self):
        if self.type_RRH == "Roof Top":
            qty_FUFBB = self.qty_RF
        else:
            qty_FUFBB = 0
        return qty_FUFBB

    @staticmethod
    def get_FUFBB_itemCode():
        itemCode_FUFBB = "BSS-HW-NOKIA-473304ABSS"
        return itemCode_FUFBB

    def get_FPKC(self):
        qty_FPKC = 0
        if self.type_RRH == "Feederless":
            if self.qty_RF % 2 == 0:
                qty_FPKC = self.qty_RF

            elif self.qty_RF % 2 != 0:
                qty_FPKC = self.qty_RF + 1
        else:
            qty_FPKC = 0

        return qty_FPKC

    @staticmethod
    def get_FPKC_itemCode():
        itemCode_FPKC = "BSS-HW-NSN-472821A"
        return itemCode_FPKC
