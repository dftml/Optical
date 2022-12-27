import pandas as pd
import numpy as np

try:
    df_load_real = pd.read_csv("epsilon_real.out", sep="\t", header=None)
    
    if df_load_real[0].dtypes == "O":
        df_series_real = df_load_real[0].apply(lambda x: x.split())
        df_real = pd.DataFrame(df_series_real.apply(lambda x: round(float(x[0]), 2)))
        df_real[1] = df_series_real.apply(lambda x: float(x[1]))

    else:
        df_real = df_load_real

except Exception as e:
    print(f"{e} rename the file to epsilon_real.out")


else:
    try:
        df_load_img = pd.read_csv("epsilon_img.out", sep="\t", header=None)

        if df_load_img[0].dtypes == "O":
            df_series_img = df_load_img[0].apply(lambda x: x.split())
            df_img = pd.DataFrame(df_series_img.apply(lambda x: round(float(x[0]), 2)))
            df_img[1] = df_series_img.apply(lambda x: float(x[1]))

        else:
            df_img = df_load_img

        # Absorption Coefficient α(ω):
        absorbtion = df_img[0] * (
            np.sqrt(2 * (np.sqrt(np.power(df_real[1], 2) + np.power(df_img[1], 2)) - df_real[1])))

        # convert the photon energy into wavelength (cm-1)
        absorbtion = absorbtion * 50689.053

        with open("absorption.data", "w") as f1:
            for i in range(len(absorbtion)):
                f1.write(f"{df_real[0][i]} \t {absorbtion[i]} \n")

        # Refractive index n(ω):
        refractive = np.sqrt((np.sqrt(np.power(df_real[1], 2) + np.power(df_img[1], 2)) + df_real[1]) / 2)

        with open("refractive.data", "w") as f1:
            for i in range(len(refractive)):
                f1.write(f"{df_real[0][i]} \t {refractive[i]} \n")

        # Extinction coefficient k(ω):
        extinction = np.sqrt((np.sqrt(np.power(df_real[1], 2) + np.power(df_img[1], 2)) - df_real[1]) / 2)

        with open("extinction.data", "w") as f1:
            for i in range(len(extinction)):
                f1.write(f"{df_real[0][i]} \t {extinction[i]} \n")

        # Reﬂectivity R(ω) or ReflectanceR(ω):
        reflectance = (np.power(refractive - 1, 2) + np.power(extinction, 2)) / (
                np.power(refractive + 1, 2) + np.power(extinction, 2))

        with open("reflectance.data", "w") as f1:
            for i in range(len(reflectance)):
                f1.write(f"{df_real[0][i]} \t {reflectance[i]} \n")

        # Conductivity σ(ω):
        conductivity = (df_img[0] * df_img[1]) / (4 * np.pi)

        # convert the photon energy into frequency (siemens per metre(Sm-1))
        conductivity = conductivity * 168959.704

        with open("conductivity.data", "w") as f1:
            for i in range(len(conductivity)):
                f1.write(f"{df_real[0][i]} \t {conductivity[i]} \n")

        # Energy loss function L(ω):
        loss = df_img[1] / (df_real[1] + df_img[1])

        with open("Energyloss.data", "w") as f1:
            for i in range(len(loss)):
                f1.write(f"{df_real[0][i]} \t {loss[i]} \n")


    except Exception as e:
        print(f"{e} rename the file to epsilon_img.out")
