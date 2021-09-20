from MyMethod import *
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from BaselineRemoval import BaselineRemoval
from sklearn.ensemble import IsolationForest

class ProMode():

    def __init__(self, pro_window):
        self.pro_window = pro_window
        self.raw_spectra_dic = None
        self.shift = None
        self.output_idxs = []

    def load_file(self):
        try:
            # 读取的文件来源选择
            if self.pro_window.other_select_button.isChecked():
                header = int(self.pro_window.header_line.text())
                sep = str(self.pro_window.sep_line.text())
                shift_idx = int(self.pro_window.shift_line.text())
                spectrum_idx = int(self.pro_window.spectrum_line.text())
            else:
                if self.pro_window.renishaw_select_button.isChecked():
                    header = 0
                    sep = '\t'
                    shift_idx = 0
                    spectrum_idx = 1
                elif self.pro_window.ezraman_select_button.isChecked():
                    header = 2
                    sep = ','
                    shift_idx = 0
                    spectrum_idx = 1
                elif self.pro_window.iramanplus_select_button.isChecked():
                    header = 1
                    sep = ';'
                    shift_idx = 0
                    spectrum_idx = 1
                self.pro_window.header_line.setText(str(header))
                self.pro_window.sep_line.setText(str(sep))
                self.pro_window.shift_line.setText(str(shift_idx))
                self.pro_window.spectrum_line.setText(str(spectrum_idx))

            files = QFileDialog.getOpenFileNames(self.pro_window, '加载文件', '/', "拉曼光谱 (*.txt)")
            shift = None
            spectra = {}
            if files[0]:
                for file in files[0]:
                    shift, spectrum = txt_loader(file, header=header, sep=sep, shift_idx=shift_idx, spectrum_idx=spectrum_idx)
                    spectra[file.split('/')[-1]] = spectrum
                self.shift = np.array(shift, dtype=int)
                self.raw_spectra_dic = spectra
                self.pro_window.load_label.setText("已加载" + str(len(spectra.keys())) + "个光谱")
                self.pro_window.process_label.setText('等待处理')
                self.output_idxs = range(len(spectra))
        except:
            self.pro_window.load_label.setText('发生错误，请检查读取参数与文件是否匹配')

    def load_dir(self):
        try:
            # 读取的文件来源选择
            if self.pro_window.other_select_button.isChecked():
                header = int(self.pro_window.header_line.text())
                sep = str(self.pro_window.sep_line.text())
                shift_idx = int(self.pro_window.shift_line.text())
                spectrum_idx = int(self.pro_window.spectrum_line.text())
            else:
                if self.pro_window.renishaw_select_button.isChecked():
                    header = 0
                    sep = '\t'
                    shift_idx = 0
                    spectrum_idx = 1
                elif self.pro_window.ezraman_select_button.isChecked():
                    header = 2
                    sep = ','
                    shift_idx = 0
                    spectrum_idx = 1
                elif self.pro_window.iramanplus_select_button.isChecked():
                    header = 1
                    sep = ';'
                    shift_idx = 0
                    spectrum_idx = 1
                self.pro_window.header_line.setText(str(header))
                self.pro_window.sep_line.setText(str(sep))
                self.pro_window.shift_line.setText(str(shift_idx))
                self.pro_window.spectrum_line.setText(str(spectrum_idx))

            dir = QFileDialog.getExistingDirectory(self.pro_window)
            shift = None
            spectra = {}
            if dir:
                for file in os.listdir(dir):
                    if os.path.splitext(file)[-1] == '.txt':
                        file_path = dir + '/' + file
                        shift, spectrum = txt_loader(file_path, header=header, sep=sep, shift_idx=shift_idx, spectrum_idx=spectrum_idx)
                        spectra[file] = spectrum
                self.shift = np.array(shift)
                self.raw_spectra_dic = spectra
                self.output_idxs = range(len(spectra))
                label = "已加载目录" + str(dir)
                self.pro_window.load_label.setText(label[-25:] + '\t'+ str(len(spectra.keys())) + "个光谱")
                self.pro_window.process_label.setText('等待处理')
                self.pro_window.save_label.setText('等待保存')
        except:
            self.pro_window.load_label.setText('发生错误，请检查读取参数与文件是否匹配')


    def process(self):
        try:
            if not self.raw_spectra_dic:
                self.pro_window.process_label.setText('请先加载文件或文件夹')
            else:

                spectra = np.array(list(self.raw_spectra_dic.values()))
                keys = list(self.raw_spectra_dic.keys())
                # 基线处理
                if self.pro_window.bs_remove_button.isChecked():
                    for i in range(len(spectra)):
                        if not np.all(spectra[i] == 0):
                            self.raw_spectra_dic[keys[i]] = spectra[i] = BaselineRemoval(spectra[i]).ZhangFit()

                # 进行筛选处理
                if self.pro_window.no_classify_button.isChecked():
                    self.output_idxs = range(len(spectra))
                    return
                elif len(spectra) < 3:
                    return
                else:
                    # 确定峰位
                    try:
                        peak_location = int(self.pro_window.peak_location.text())
                    except:
                        peak_location = 0

                    if self.shift[0] <= peak_location <= self.shift[-1]:
                        l_border = max(self.shift[0], peak_location - 1)
                        l_index = list(self.shift).index(l_border)
                        r_border = min(self.shift[-1], peak_location + 1)
                        r_index = list(self.shift).index(r_border)
                        judge_spectra = spectra[:, l_index:r_index]

                    else:
                        judge_spectra = spectra

                    # 方法一 分离树
                    if self.pro_window.method1_button.isChecked():
                        clf = IsolationForest(random_state=0).fit(judge_spectra)
                        label = clf.predict(judge_spectra)
                        score = clf.score_samples(judge_spectra)
                        output_idxs = np.argsort(-score)

                    # 方法二 均值迭代
                    if self.pro_window.method2_button.isChecked():
                        judge_dic = {}
                        for i in range(len(judge_spectra)):
                            judge_dic[tuple(judge_spectra[i])] = i
                        output_idxs = []
                        count = len(judge_spectra)
                        while len(judge_dic) > 0:
                            dist = []
                            judge_spectra = list(judge_dic.keys())
                            judge_mean = np.mean(judge_spectra, axis=0)
                            for judge_spectrum in judge_spectra:
                                dist.append(np.linalg.norm(judge_spectrum - judge_mean, ord=2, axis=0, keepdims=False))
                            max_key = judge_spectra[np.argsort(dist)[-1]]
                            output_idxs.append(judge_dic[max_key])
                            del judge_dic[max_key]
                        output_idxs.reverse()
                self.output_idxs = output_idxs
                self.pro_window.process_label.setText('处理完毕！')
                self.pro_window.save_label.setText('等待保存')
        except:
            self.pro_window.process_label.setText('发生错误，请检查处理参数是否正确')

    def save_file(self):
        try:
            # 保存光谱文件
            spectra_data = []
            out_amout = int(self.pro_window.out_amount.text())
            keys = list(self.raw_spectra_dic.keys())
            values = list(self.raw_spectra_dic.values())

            # 数据分析
            spectra_data = (list(values[i] for i in self.output_idxs[:out_amout]))
            spectra_shift = np.array(self.shift)
            spectra_max = np.max(spectra_data, axis=0)
            spectra_min = np.min(spectra_data, axis=0)
            spectra_avg = np.average(spectra_data, axis=0)
            spectra_std = np.std(spectra_data, ddof=1, axis=0)
            analysis_data = np.array([spectra_shift, spectra_max, spectra_min, spectra_avg, spectra_std], dtype=float)
            analysis_header = 'Raman shift\tmax\tmin\tavg\tstd'

            # 合并成一个文件保存
            if self.pro_window.single_sv_button.isChecked():
                spectra_data = np.append(spectra_data, analysis_data[1:, :], axis=0)
                spectra_data = np.insert(spectra_data, 0, spectra_shift, axis=0)
                header = 'raman shift\t' + 'spectrum\t'*out_amout + 'max\tmin\tavg\tstd'
                dst = QFileDialog.getSaveFileName(self.pro_window, '加载文件', '/', "拉曼光谱 (*.txt)")[0]
                if not dst:
                    return
                np.savetxt(dst, spectra_data.T, header=header, fmt='%.04f', delimiter='\t')
            # 多个文件分开保存
            if self.pro_window.multiple_sv_button.isChecked():
                save_dir_path = QFileDialog.getExistingDirectory()
                if not save_dir_path:
                    return
                header = 'raman shift\tspectrum'
                for i in range(out_amout):
                    idx = self.output_idxs[i]
                    dst = os.path.join(save_dir_path, keys[idx])
                    spectrum_data = np.array([spectra_shift, values[idx]], dtype=float)
                    np.savetxt(dst, spectrum_data.T, header=header, fmt='%.04f', delimiter='\t')
                # 保存分析信息
                dst = os.path.join(save_dir_path, 'analysis.txt')
                np.savetxt(dst, analysis_data.T, header=analysis_header, fmt='%.04f', delimiter='\t')
            self.pro_window.save_label.setText('保存成功')
            self.pro_window.process_label.setText('等待处理')
        except:
            self.pro_window.save_label.setText('保存出错')
