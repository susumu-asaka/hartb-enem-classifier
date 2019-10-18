from typing import Sequence

import pandas as pd
import numpy as np


def str_to_number(strings):
    result = np.zeros((len(strings),))
    for i in range(len(strings)):
        if strings[i] != "":
            if "." in strings[i]:
                result[i] = float(strings[i])
            else:
                result[i] = int(strings[i])
    return result


def group_by_escola(file):
    cols_medias = [
        "Media_CN",
        "Media_CH",
        "Media_LC",
        "Media_MT",
        "Media_Redacao",
    ]
    escolas = pd.DataFrame(columns=["Comparecimento"] + cols_medias)
    escolas.index.name = "Cod_escola"
    with open(file) as f:
        # read header
        f.readline()

        line = f.readline()
        i = 0
        while line:
            i += 1
            if i % 54900 == 0:
                print(i // 54900)
            fields = line.split(";")
            st_conclusao = str_to_number([fields[15]])[0]
            tp_ensino = str_to_number([fields[18]])[0]
            cod_escola = str_to_number([fields[20]])[0]
            if cod_escola != 0 and st_conclusao == 2 and tp_ensino == 1:
                notas = str_to_number(fields[90:94] + fields[109:110])
                if cod_escola in escolas.index:
                    n = escolas.loc[cod_escola, "Comparecimento"]
                    medias = escolas.loc[cod_escola, cols_medias]
                else:
                    n = 0
                    medias = np.array(5 * [0.0])
                escolas.loc[cod_escola, "Comparecimento"] = n + 1
                escolas.loc[cod_escola, cols_medias] = (medias * n + notas) / (
                    n + 1
                )
            line = f.readline()

    escolas.to_csv("./data/escolas.csv")


group_by_escola(
    "/Users/susum/Downloads/microdados_enem2018/DADOS/"
    "MICRODADOS_ENEM_2018.csv"
)
# group_by_escola("./data/sample_enem2018.csv")
