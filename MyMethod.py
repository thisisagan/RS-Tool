import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


def txt_loader(fname, header=None, sep=None, shift_idx=None, spectrum_idx=None):
    data = pd.read_csv(fname, header=header, sep=sep)
    shift = list(data.iloc[:, shift_idx])
    spectrum = list(data.iloc[:, spectrum_idx])
    return shift, spectrum


def prefer_spectra(spectra, bad_scale=0.5):
    clf = IsolationForest(random_state=0, contamination=bad_scale).fit(spectra)
    label = clf.predict(spectra)
    prefer_spectra = []
    # 输出比例光谱
    for i in range(len(label)):
        if label[i] == 1:
            prefer_spectra.append(spectra[i])
    return np.asarray(prefer_spectra)
