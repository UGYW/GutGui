import numpy as np
from AnalysisModules.analysis_constant import *
from AnalysisModules.Indices import Index
import logging

class Analysis:
    def __init__(self, data_cube, normal, absorbance, wavelength, index_number, mask=None):
        self.data_cube = data_cube
        self.mask = mask
        self.wavelength = int(wavelength)
        self.normal = bool(normal)
        self.absorbance = bool(absorbance)

        self.index_number = index_number
        self.index = None
        self.index_masked = None

        self.x1 = None
        self.x2 = None
        self.x_absorbance = None
        self.x_reflectance = None
        self.x_absorbance_w = None
        self.x_reflectance_w = None
        self.x_absorbance_masked = None
        self.x_absorbance_masked_w = None
        self.x_reflectance_masked = None
        self.x_reflectance_masked_w = None

        self.sto2 = None
        self.sto2_masked = None
        self.nir = None
        self.nir_masked = None
        self.thi = None
        self.thi_masked = None
        self.twi = None
        self.twi_masked = None

        self._x_absorbance_gradient = None
        self._x_absorbance_gradient_min_1 = None
        self._x_absorbance_gradient_min_2 = None
        self._x_absorbance_min_570_590 = None
        self._x_absorbance_min_740_780 = None
        self._x_absorbance_mean_825_925 = None
        self._x_absorbance_mean_655_735 = None
        self._x_absorbance_mean_530_590 = None
        self._x_absorbance_mean_785_825 = None
        self._x_absorbance_mean_880_900 = None
        self._x_absorbance_mean_955_980 = None

        self._x_reflectance_gradient = None
        self._x_reflectance_gradient_min_1 = None
        self._x_reflectance_gradient_min_2 = None
        self._x_reflectance_min_570_590 = None
        self._x_reflectance_min_740_780 = None
        self._x_reflectance_mean_825_925 = None
        self._x_reflectance_mean_655_735 = None
        self._x_reflectance_mean_530_590 = None
        self._x_reflectance_mean_785_825 = None
        self._x_reflectance_mean_880_900 = None
        self._x_reflectance_mean_955_980 = None

        self.absorption_roi = None
        self.absorption_roi_masked = None

        self.analysis()

    def analysis(self):
        self._calc_general()
        self._calc_sto2()
        self._calc_nir()
        self._calc_thi()
        self._calc_twi()
        self._calc_index(self.index_number)
        self._calc_absorption_spec()

    def update_mask(self, new_mask):
        self.mask = new_mask
        self.analysis()

    def update_wavelength(self, new_wavelength):
        self.wavelength = new_wavelength
        self.analysis()

    def update_normal(self, new_normal):
        self.normal = new_normal
        self.analysis()

    def update_absorbance(self, new_absorbance):
        self.absorbance = new_absorbance
        self.analysis()

    def update_index(self, new_index_number):
        self.index_number = new_index_number
        self.analysis()

    def get_data_cube(self):
        return self.data_cube

    def get_x_absorbance(self):
        return self.x_absorbance

    def get_x_reflectance(self):
        return self.x_reflectance

    def get_x_absorbance_w(self):
        return self.x_absorbance_w

    def get_x_reflectance_w(self):
        return self.x_reflectance_w

    def get_x_absorbance_masked(self):
        return self.x_absorbance_masked

    def get_x_reflectance_masked(self):
        return self.x_reflectance_masked

    def get_x_absorbance_masked_w(self):
        return self.x_absorbance_masked_w

    def get_x_reflectance_masked_w(self):
        return self.x_reflectance_masked_w

    def get_sto2(self):
        return self.sto2

    def get_sto2_masked(self):
        return self.sto2_masked

    def get_nir(self):
        return self.nir

    def get_nir_masked(self):
        return self.nir_masked

    def get_thi(self):
        return self.thi

    def get_thi_masked(self):
        return self.thi_masked

    def get_twi(self):
        return self.twi

    def get_twi_masked(self):
        return self.twi_masked

    def get_index(self):
        return self.index

    def get_index_masked(self):
        return self.index_masked

    def get_absorption_spec(self):
        return self.absorption_roi

    def get_absorption_spec_masked(self):
        return self.absorption_roi_masked

    def get_whole_image_data(self):
        if self.absorbance:
            data = self.get_x_absorbance()
        else:
            data = self.get_x_reflectance()
        return data

    def get_masked_image_data(self):
        if self.absorbance:
            data = self.get_x_absorbance_masked()
        else:
            data = self.get_x_reflectance_masked()
        return data

    def get_wl_data(self):
        if self.absorbance:
            new_data = self.get_x_absorbance_w()
        else:
            new_data = self.get_x_reflectance_w()
        return new_data

    def get_wl_data_masked(self):
        if self.absorbance:
            new_data = self.get_x_absorbance_masked_w()
        else:
            new_data = self.get_x_reflectance_masked_w()
        return new_data

    def get_histogram_data(self, is_masked):
        if is_masked:
            data = self.get_masked_image_data()
        else:
            data = self.get_whole_image_data()
        return data

    def _calc_general(self):
        logging.debug("CALCULATING: ABSORBANCE AND REFLECTANCE...")
        self.__calc_x1()
        self.__calc_x_reflectance()
        self.__calc_x2()
        self.__calc_x_absorbance()

    def _calc_sto2(self):
        logging.debug("CALCULATING: STO2...")
        if self.absorbance:
            self._x_absorbance_gradient = np.gradient(self.x_absorbance, axis=2)
            self._x_absorbance_gradient_min_1 = self._x_absorbance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
            self._x_absorbance_gradient_min_2 = self._x_absorbance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
            self._x_absorbance_min_570_590 = self._x_absorbance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
            self._x_absorbance_min_740_780 = self._x_absorbance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
            temp1 = self._x_absorbance_min_570_590 / R1
            temp2 = self._x_absorbance_min_740_780 / R2
        else:
            self._x_reflectance_gradient = np.gradient(self.x_reflectance, axis=2)
            self._x_reflectance_gradient_min_1 = self._x_reflectance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
            self._x_reflectance_gradient_min_2 = self._x_reflectance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
            self._x_reflectance_min_570_590 = self._x_reflectance_gradient[:, :, 14:18].min(axis=2)  # between 570nm and 590nm
            self._x_reflectance_min_740_780 = self._x_reflectance_gradient[:, :, 48:56].min(axis=2)  # between 740nm and 780nm
            temp1 = self._x_reflectance_min_570_590 / R1
            temp2 = self._x_reflectance_min_740_780 / R2
        self.sto2 = temp1 / (temp1 + temp2)
        logging.debug("Complete Sto2 Mean: " + str(self.sto2[:, :].mean()))
        if self.mask:
            self.sto2_masked = np.ma.array(self.sto2[:, :], mask=[self.mask])
            logging.debug("Masked Sto2 Mean: " + str(self.sto2_masked.mean()))

    def _calc_nir(self):
        logging.debug("CALCULATING: NIR...")
        if self.absorbance:
            self._x_absorbance_mean_825_925 = self.x_absorbance[:, :, 65:85].mean(axis=2)  # between (825nm : 925nm)
            self._x_absorbance_mean_655_735 = self.x_absorbance[:, :, 31:47].mean(axis=2)  # between (655nm : 735nm)
            temp1 = self._x_absorbance_mean_825_925 / self._x_absorbance_mean_655_735
        else:
            self._x_reflectance_mean_825_925 = self.x_reflectance[:, :, 65:85].mean(axis=2)  # between (825nm : 925nm)
            self._x_reflectance_mean_655_735 = self.x_reflectance[:, :, 31:47].mean(axis=2)  # between (655nm : 735nm)
            temp1 = self._x_reflectance_mean_825_925 / self._x_reflectance_mean_655_735
        self.nir = (temp1 - S1) / (S2 - S1)
        logging.debug("Complete NIR Mean: " + str(self.nir[:, :].mean()))
        if self.mask:
            self.nir_masked = np.ma.array(self.nir[:, :], mask=[self.mask])
            logging.debug("Masked NIR Mean: " + str(self.nir_masked.mean()))

    def _calc_thi(self):
        logging.debug("CALCULATING: THI...")
        if self.absorbance:
            self._x_absorbance_mean_530_590 = self.x_absorbance[:, :, 6:18].mean(axis=2)  # between (530nm : 590nm)
            self._x_absorbance_mean_785_825 = self.x_absorbance[:, :, 57:65].mean(axis=2)  # between (785nm : 825nm)
            temp1 = self._x_absorbance_mean_530_590 / self._x_absorbance_mean_785_825
        else:
            self._x_reflectance_mean_530_590 = self.x_reflectance[:, :, 6:18].mean(axis=2)  # between (530nm : 590nm)
            self._x_reflectance_mean_785_825 = self.x_reflectance[:, :, 57:65].mean(axis=2)  # between (785nm : 825nm)
            temp1 = self._x_reflectance_mean_530_590 / self._x_reflectance_mean_785_825
        self.thi = (temp1 - T1) / (T2 - T1)
        logging.debug("Complete THI Mean: " + str(self.thi[:, :].mean()))
        if self.mask:
            self.thi_masked = np.ma.array(self.thi[:, :], mask=[self.mask])
            logging.debug("Masked THI Mean: " + str(self.thi_masked.mean()))

    def _calc_twi(self):
        logging.debug("CALCULATING: TWI...")
        if self.absorbance:
            self._x_absorbance_mean_880_900 = self.x_absorbance[:, :, 76:80].mean(axis=2)  # between (880nm : 900nm)
            self._x_absorbance_mean_955_980 = self.x_absorbance[:, :, 91:96].mean(axis=2)  # between (955nm : 980nm)
            temp1 = self._x_absorbance_mean_880_900 / self._x_absorbance_mean_955_980
        else:
            self._x_reflectance_mean_880_900 = self.x_reflectance[:, :, 76:80].mean(axis=2)  # between (880nm : 900nm)
            self._x_reflectance_mean_955_980 = self.x_reflectance[:, :, 91:96].mean(axis=2)  # between (955nm : 980nm)
            temp1 = self._x_reflectance_mean_880_900 / self._x_reflectance_mean_955_980
        self.twi = (temp1 - U1) / (U2 - U1)
        logging.debug("Complete TWI Mean: " + str(self.twi[:, :].mean()))
        if self.mask:
            self.twi_masked = np.ma.array(self.twi[:, :], mask=[self.mask])
            logging.debug("Masked TWI Mean: " + str(self.twi_masked.mean()))

    def _calc_index(self, index_number):
        logging.debug("CALCULATING: INDEX...")
        if self.absorbance:
            index_module = Index(index_number, self.x_absorbance)
            self.index = index_module.get_index()
            if self.mask:
                masked_index_module = Index(index_number, self.x_absorbance_masked_w)
                self.index_masked = masked_index_module.get_index()
        else:
            index_module = Index(index_number, self.x_reflectance)
            self.index = index_module.get_index()
            if self.mask:
                masked_index_module = Index(index_number, self.x_reflectance_masked)
                self.index_masked = masked_index_module.get_index()

    def _calc_absorption_spec(self):
        logging.debug("CALCULATING: ABSORPTION SPEC...")
        if self.absorbance:
            self.absorption_roi = self._calc_absorption_spec_roi(self.x_absorbance)
            if self.mask:
                self.absorption_roi_masked = self._calc_absorption_spec_roi(self.x_absorbance_masked)
        else:
            self.absorption_roi = self._calc_absorption_spec_roi(self.x_reflectance)
            if self.mask:
                self.absorption_roi_masked = self._calc_absorption_spec_roi(self.x_reflectance_masked)

    def _calc_absorption_spec_roi(self, data):
        absorption_roi = []
        wavelengths = np.arange(500, 1000, 5)

        for i in range(data.shape[2]):
            tmp = np.ma.median(data[:, :, i])
            absorption_roi.append((int(wavelengths[i]), tmp))

        return np.array(absorption_roi)

    def __calc_x1(self):
        if self.normal:
            self.x1 = self.data_cube/self.data_cube.max()
        else:
            self.x1 = self.data_cube

    def __calc_x_reflectance(self):
        self.x_reflectance = self.x1
        self.x_reflectance = np.ma.array(self.x_reflectance, mask=self.data_cube < 0)
        self.x_reflectance_w = self.x_reflectance[:, :, self.wavelength]

        if self.mask:
            self.x_reflectance_masked = np.ma.array(self.x_reflectance[:, :, :], mask=[self.mask] * 100)
            self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength], mask=self.mask)

    def __calc_x2(self):
        self.x1 = self.x1.clip(min=0)
        self.x2 = -np.log(self.x1)

    def __calc_x_absorbance(self):
        self.x_absorbance = np.ma.array(self.x2, mask=~np.isfinite(self.x2))

        if self.normal:
            self.x_absorbance = self.x_absorbance / self.x_absorbance.max()
        self.x_absorbance_w = self.x_absorbance[:, :, self.wavelength]

        if self.mask:
            self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=[self.mask] * 100)
            self.x_absorbance_masked_w = np.ma.array(self.x_absorbance[:, :, self.wavelength], mask=self.mask)