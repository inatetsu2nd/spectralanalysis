import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cross_decomposition import PLSRegression

class SpectralDataProcessor:
    def __init__(self, datapath="./dataChapter5/"): # ①
        self.datapath = datapath # ②

    def read_NIR(self):
        allfiles = glob.glob('{}*.csv'.format(self.datapath))
        df_spectra = pd.DataFrame()
        for file in allfiles:
            df = pd.read_csv(file, header=None)
            df_spectra = pd.concat([df_spectra, df.iloc[:, 1]], axis=1)
        df_spectra.columns = range(1, len(allfiles) + 1)
        df_spectra.index = df.iloc[:, 0]
        plt.plot(df_spectra)
        df_spectra = df_spectra.T
        self.spectra = df_spectra # ③
        return df_spectra

    def savigolay_deri(self, window, polynom, order):
        derispec = self.spectra.copy() # ④
        for i in range(len(derispec)):
            derispec.iloc[i] = signal.savgol_filter(derispec.iloc[i], window, polynom, order)
        fig, axes = plt.subplots(2, 1, figsize=(6, 6))
        axes[0].plot(self.spectra.T, 'k')
        axes[1].plot(derispec.T, 'k')
        return derispec

    def SNV(self):
        snvspec = self.spectra.copy() # ⑤
        for i in range(len(snvspec)):
            snvspec.iloc[i] = (snvspec.iloc[i] - snvspec.T.mean().iloc[i]) / snvspec.T.std().iloc[i]
        fig, axes = plt.subplots(2, 1, figsize=(6, 6))
        axes[0].plot(self.spectra.T, 'k')
        axes[1].plot(snvspec.T, 'k')
        return snvspec