with open(
    "/Users/susum/Downloads/microdados_enem2018/DADOS/"
    "MICRODADOS_ENEM_2018.csv"
) as file_in, open("./data/sample_enem2018.csv", "w") as file_out:
    for i in range(200):
        line = file_in.readline()
        file_out.write(line)
