import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class TXTLoader():
    def __init__(self, header=None, sep=None, shift_idx=None, spectrum_idx=None, scale=0.2):
        self.header = header
        self.sep = sep
        self.shift_idx = shift_idx
        self.raman_dix = shift_idx
        self.scale = scale
    def txt_loader(self, fname):
        if not self.header or not self.sep:
            header = 0
            for row in open(fname):
                if not row[0].isdigit():
                    header += 1
                else:
                    if ';' in row:
                        sep = ';'
                    else:
                        sep = '/t'
                    break
            if header > 5:
                self.shift_idx = 0
                self.spectrum_idx = 4
            else:
                self.shift_idx = 0
                self.spectrum_idx = 1
            data = pd.read_csv(fname, header=header, sep=sep)
        else:
            data = pd.read_csv(fname, header=self.header, sep=self.sep)
        shift = list(data.iloc[:, self.shift_idx])
        spectrum = list(data.iloc[:, self.spectrum_idx])
        return shift, spectrum

    def prefer_spectra(self, spectra):
        clf = IsolationForest(random_state=0, contamination=self.scale).fit(spectrum)
        label = clf.predict(spectra)
        prefer_spectra = []
        # 输出前scale比例的光谱
        for i in range(len(label)):
            if label[i] == 1:
                prefer_spectra.append(spectra[i])
        return np.asarray(prefer_spectra)
