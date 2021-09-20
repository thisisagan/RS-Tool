from MyMethod import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import numpy as np


class EasyMode():
    shift: None
    spectra: None

    def __init__(self, easy_window):
        self.easy_window = easy_window

    def read_file(self):
        if self.easy_window.renishaw_button.isChecked():
            header = 0
            sep = '\t'
            shift_idx = 0
            spectrum_idx = 1
        elif self.easy_window.ez_button.isChecked():
            header = 2
            sep = ','
            shift_idx = 0
            spectrum_idx = 1
        elif self.easy_window.iraman_button.isChecked():
            header = 1
            sep = ';'
            shift_idx = 0
            spectrum_idx = 1
        fname = QFileDialog.getOpenFileNames(self.easy_window, '加载文件', '/', "拉曼光谱 (*.txt)")
        shift = None
        spectra = []
        if fname[0]:
            for file in fname[0]:
                    shift, spectrum = txt_loader(file, header=header, sep=sep, shift_idx=shift_idx, spectrum_idx=spectrum_idx)
                    spectra.append(spectrum)
            self.shift = np.array(shift).reshape(1, len(shift))
            self.spectra = np.array(spectra)

    def process(self):
        try:
            self.read_file()
            if self.spectra.shape[0] > 1:
                self.spectra = prefer_spectra(self.spectra)
            content = np.append(self.shift, self.spectra, axis=0)
            avg = np.average(self.spectra, axis=0).reshape(1, -1)
            std = np.std(self.spectra, ddof=1, axis=0).reshape(1, -1)
            content = np.append(content, avg, axis=0)
            content = np.append(content, std, axis=0)
            self.content = content
        except:
            return
        
    def save_file(self):
        try:
            if self.content.any():
                filename = QFileDialog.getSaveFileName(self.easy_window, '文件另存为', '/', "拉曼光谱 (*.txt)")
                header = 'raman shift\t' + 'specturm\t'*(len(self.content)-3) + 'avg\tstd'
                np.savetxt(filename[0], self.content.T, fmt='%.04f', delimiter='\t', header=header)
        except:
            return
