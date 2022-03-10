from MyMethod import *
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from BaselineRemoval import BaselineRemoval
from sklearn.ensemble import IsolationForest


class ValidMode():

    def __init__(self, valid_window):
        self.valid_window = valid_window
        self.blank_value = None
        self.header = None
        self.sep = None
        self.shift_idx = None
        self.spectrum_idx = None
        self.peak_location = None
        self.offset_range = None
        self.out_count = None
        self.baseline_remove = False

    def load_blank(self):
        try:
            # 读取参数
            self.peak_location = int(self.valid_window.peak_location.text())
            self.offset_range = int(self.valid_window.offset_range.text())
            self.out_count = int(self.valid_window.out_count_box.text())
        except:
            self.valid_window.reporter_browser.setText('请选择正确参数！')

        try:
            # 读取的文件来源选择
            if self.valid_window.other_select_button.isChecked():
                header = int(self.valid_window.header_line.text())
                sep = str(self.valid_window.sep_line.text())
                shift_idx = int(self.valid_window.shift_line.text())
                spectrum_idx = int(self.valid_window.spectrum_line.text())
            else:
                if self.valid_window.renishaw_select_button.isChecked():
                    header = 0
                    sep = '\t'
                    shift_idx = 0
                    spectrum_idx = 1
                elif self.valid_window.ezraman_select_button.isChecked():
                    header = 2
                    sep = ','
                    shift_idx = 0
                    spectrum_idx = 1
                elif self.valid_window.iramanplus_select_button.isChecked():
                    header = 1
                    sep = ';'
                    shift_idx = 0
                    spectrum_idx = 1
                self.valid_window.header_line.setText(str(header))
                self.valid_window.sep_line.setText(str(sep))
                self.valid_window.shift_line.setText(str(shift_idx))
                self.valid_window.spectrum_line.setText(str(spectrum_idx))
                # 获取读取相关的类属性
                self.header = header
                self.sep = sep
                self.shift_idx = shift_idx
                self.spectrum_idx = spectrum_idx

            files = QFileDialog.getOpenFileNames(self.valid_window, '加载文件', '/', "拉曼光谱 (*.txt)")[0]
            if not files:
                self.valid_window.reporter_browser.setText('请选择文件！')
                return
            first_time = True
            for file in files:
                shift, spectrum = txt_loader(file, header=header, sep=sep, shift_idx=shift_idx, spectrum_idx=spectrum_idx)
                spectrum = np.array(spectrum)

                # 去基线
                if self.valid_window.bs_remove_button.isChecked():
                    self.baseline_remove = True
                    if not np.all(spectrum == 0):
                        spectrum = BaselineRemoval(spectrum).ZhangFit()
                if first_time:
                    blank_spectra = spectrum
                    first_time = False
                else:
                    blank_spectra = np.vstack((blank_spectra, spectrum))

        except:
                self.valid_window.reporter_browser.setText('发生错误，请检查读取参数与文件是否匹配!')
                return
        # 如果只加载一个文件，则还要补上维度
        if blank_spectra.ndim == 1:
            blank_spectra = np.expand_dims(blank_spectra, axis=0)

        # 获取峰位
        peak_location = self.peak_location
        offset_range = self.offset_range
        dist = list(abs(num) for num in list(np.array(shift)-peak_location))
        peak_idx = np.argmin(dist)

        # 考虑峰位飘移的光谱最大值, 重新标定光谱范围
        for i in range(len(blank_spectra)):
            peak_offset = np.argmax(blank_spectra[i, peak_idx-offset_range-1:peak_idx+offset_range])
            real_peak = peak_idx - offset_range + peak_offset
            temp_spectrum = blank_spectra[i, real_peak-2:real_peak+3]
            if i == 0:
                temp_spectra = temp_spectrum
            else:
                temp_spectra = np.vstack((temp_spectra, temp_spectrum))
        blank_spectra = temp_spectra
        # 如果只加载一个文件，则还要补上维度
        if blank_spectra.ndim == 1:
            blank_spectra = np.expand_dims(blank_spectra, axis=0)
        # 进行筛选处理
        out_count = min(self.out_count, len(blank_spectra))

        # 方法一
        if self.valid_window.method1_button.isChecked():
            clf = IsolationForest(random_state=0).fit(blank_spectra)
            label = clf.predict(blank_spectra)
            score = clf.score_samples(blank_spectra)
            output_idxs = np.argsort(-score)[:out_count]
            # print(output_idxs)
            blank_spectra = list(blank_spectra[idx] for idx in output_idxs)
            blank_spectra = np.array(blank_spectra)

        # 方法二
        if self.valid_window.method2_button.isChecked():
            while len(blank_spectra) > out_count:
                dist = []
                spectra_mean = np.mean(blank_spectra, axis=0)
                for spectrum in blank_spectra:
                    dist.append(np.linalg.norm(spectrum - spectra_mean, ord=2, axis=0, keepdims=False))
                max_idx = np.argmax(dist)
                blank_spectra = np.delete(blank_spectra, max_idx, axis=0)

        # 方法三
        if self.valid_window.method3_button.isChecked():
            self.valid_window.reporter_browser.setText('暂不支持方法3!')
            return

        # 不进行筛选
        if self.valid_window.no_classify_button.isChecked():
            pass
        # 获取blank值
        self.blank_value = np.mean(np.amax(blank_spectra, axis=1), axis=0)
        self.valid_window.blank_statu_label.setText('Blank已加载，强度为%d'% self.blank_value)

    def valid(self):
        if not self.blank_value:
            self.valid_window.reporter_browser.setText('请先加载blank!')
            return
        else:
            header = self.header
            sep = self.sep
            shift_idx = self.shift_idx
            spectrum_idx = self.spectrum_idx
            peak_location = self.peak_location
            out_count = self.out_count
            blank_value = self.blank_value
            try:
                files = QFileDialog.getOpenFileNames(self.valid_window, '加载文件', '/', "拉曼光谱 (*.txt)")[0]
                if not files:
                    self.valid_window.reporter_browser.setText('请选择文件！')
                    return
                first_time = True
                for file in files:
                    shift, spectrum = txt_loader(file, header=header, sep=sep, shift_idx=shift_idx,
                                                 spectrum_idx=spectrum_idx)
                    # 去基线
                    if self.baseline_remove:
                        if not np.all(spectrum == 0):
                            spectrum = BaselineRemoval(spectrum).ZhangFit()
                    if first_time:
                        valid_spectra = spectrum
                        first_time = False
                    else:
                        valid_spectra = np.vstack((valid_spectra, spectrum))

            except:
                self.valid_window.reporter_browser.setText('发生错误，请检查读取参数与文件是否匹配!')
                return
            # 如果只加载一个文件，则还要补上维度
            if np.array(valid_spectra).ndim == 1:
                valid_spectra = np.expand_dims(valid_spectra, axis=0)
            # 获取峰位
            peak_location = self.peak_location
            offset_range = self.offset_range
            dist = list(abs(num) for num in list(np.array(shift) - peak_location))
            peak_idx = np.argmin(dist)

            # 考虑峰位飘移的光谱最大值, 重新标定光谱范围
            for i in range(len(valid_spectra)):
                peak_offset = np.argmax(valid_spectra[i, peak_idx - offset_range-1:peak_idx + offset_range])
                real_peak = peak_idx - offset_range + peak_offset
                temp_spectrum = valid_spectra[i, real_peak - 2:real_peak + 3]
                if i == 0:
                    temp_spectra = temp_spectrum
                else:
                    temp_spectra = np.vstack((temp_spectra, temp_spectrum))
            valid_spectra = temp_spectra
            # 如果只加载一个文件，则还要补上维度
            if np.array(valid_spectra).ndim == 1:
                valid_spectra = np.expand_dims(valid_spectra, axis=0)
            # 进行筛选处理
            out_count = min(self.out_count, len(valid_spectra))

            # 方法一
            if self.valid_window.method1_button.isChecked():
                clf = IsolationForest(random_state=0).fit(valid_spectra)
                label = clf.predict(valid_spectra)
                score = clf.score_samples(valid_spectra)
                output_idxs = np.argsort(-score)[:out_count]
                valid_spectra = list(valid_spectra[idx] for idx in output_idxs)

            # 方法二
            if self.valid_window.method2_button.isChecked():
                while len(valid_spectra) > out_count:
                    dist = []
                    spectra_mean = np.mean(valid_spectra, axis=0)
                    for spectrum in valid_spectra:
                        dist.append(np.linalg.norm(spectrum - spectra_mean, ord=2, axis=0, keepdims=False))
                    max_idx = np.argmax(dist)
                    valid_spectra = np.delete(valid_spectra, max_idx, axis=0)

            # 方法三
            if self.valid_window.method3_button.isChecked():
                self.valid_spectra.reporter_browser.setText('暂不支持方法3!')
                return

            # 不进行筛选
            if self.valid_window.no_classify_button.isChecked():
                pass

            # 获取待检测光谱的平均峰值
            valid_value = np.mean(np.amax(valid_spectra, axis=1), axis=0)
            ratio = valid_value / blank_value
            cutoff = float(self.valid_window.cutoff_box.text())
            if ratio >= cutoff:
                result = '阳性'
                color = 'red'
            else:
                result = '阴性'
                color = 'black'
            if self.baseline_remove:
                baseline_mode = '去基线'
            else:
                baseline_mode = '未去基线'
            reporter = """
                <h4>检测报告</h4>
                <p>基线模式：%s</p>
                <p>筛选数目为：%d，筛选峰位为：%d</p>
                <p>Blank强度为：%d，检测强度为：%d</p>
                <p>Cutoff值为：%0.3f，检测强度比值为：%0.3f</p>
                <p>检测结果为：<span style="color: %s">%s</span></p>
            """ % (baseline_mode, out_count, peak_location, blank_value, valid_value, cutoff, ratio, color, result)
            self.valid_window.reporter_browser.setText(reporter)
