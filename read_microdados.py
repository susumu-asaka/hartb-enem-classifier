class Graded:
    sg_provas = ["cn", "ch", "lc", "mt"]

    def __init__(self):
        self.nu_comparecimento_cn = 0
        self.nu_aprovacao_cn = 0
        self.nu_comparecimento_ch = 0
        self.nu_aprovacao_ch = 0
        self.nu_comparecimento_lc = 0
        self.nu_aprovacao_lc = 0
        self.nu_comparecimento_mt = 0
        self.nu_aprovacao_mt = 0

    def record_grades(self, grades):
        for p in range(len(grades)):
            if grades[p] != "":
                sg_prova = Graded.sg_provas[p]
                attr = "nu_comparecimento_" + sg_prova
                setattr(self, attr, getattr(self, attr) + 1)
                if float(grades[p]) >= 650:
                    attr = "nu_aprovacao_" + sg_prova
                    setattr(self, attr, getattr(self, attr) + 1)

    @staticmethod
    def write_header(file):
        file.write("NU_COMPARECIMENTO_CN")
        file.write(",PC_APROVACAO_CN")
        file.write(",NU_COMPARECIMENTO_CH")
        file.write(",PC_APROVACAO_CH")
        file.write(",NU_COMPARECIMENTO_LC")
        file.write(",PC_APROVACAO_LC")
        file.write(",NU_COMPARECIMENTO_MT")
        file.write(",PC_APROVACAO_MT")

    def write_grades(self, file):
        for p in range(4):
            sg_prova = Graded.sg_provas[p]
            nu_comparecimento_prova = getattr(
                self, "nu_comparecimento_" + sg_prova
            )
            file.write(f",{nu_comparecimento_prova}")
            pc_aprovacao_prova = (
                (
                    getattr(self, "nu_aprovacao_" + sg_prova)
                    / nu_comparecimento_prova
                )
                if nu_comparecimento_prova != 0
                else 0
            )
            file.write(f",{format(pc_aprovacao_prova, '.3f')}")


class Municipio(Graded):
    def __init__(self, co_municipio, no_municipio, sg_uf):
        super().__init__()
        self.co_municipio = co_municipio
        self.no_municipio = no_municipio
        self.sg_uf = sg_uf


class Escola(Graded):
    def __init__(
        self,
        co_escola,
        co_municipio,
        tp_dependencia_adm,
        tp_localizacao,
        tp_sit_func,
    ):
        super().__init__()
        self.co_escola = co_escola
        self.co_municipio = co_municipio
        self.tp_dependencia_adm = tp_dependencia_adm
        self.tp_localizacao = tp_localizacao
        self.tp_sit_func = tp_sit_func


def str_to_int(string):
    if string != "":
        return int(string)
    else:
        return 0


municipios = {}

escolas = {0: Escola(0, 0, 0, 0, 0)}

with open(
    "/Users/susum/Downloads/Microdados Enem 2017/DADOS/"
    "microdados_enem_2017.csv"
) as f:
    # read header
    f.readline()
    line = f.readline()
    i = 0
    while line:
        i += 1
        if i % 61000 == 0:
            print(i // 61000)
        fields = line.split(";")
        co_municipio_residencia = int(fields[2])
        no_municipio_residencia = fields[3]
        sg_uf_municipio_residencia = fields[5]
        co_esc = str_to_int(fields[20])
        co_municipio_esc = str_to_int(fields[21])
        tp_dependencia_adm_esc = str_to_int(fields[25])
        tp_localizacao_esc = str_to_int(fields[26])
        tp_sit_func_esc = str_to_int(fields[27])
        municipio = municipios.setdefault(
            co_municipio_residencia,
            Municipio(
                co_municipio_residencia,
                no_municipio_residencia,
                sg_uf_municipio_residencia,
            ),
        )
        municipio.record_grades(fields[90:94])
        escola = escolas.setdefault(
            co_esc,
            Escola(
                co_esc,
                co_municipio_esc,
                tp_dependencia_adm_esc,
                tp_localizacao_esc,
                tp_sit_func_esc,
            ),
        )
        escola.record_grades(fields[90:94])
        line = f.readline()

with open("./data/municipios.csv", "w") as f:
    f.write("CO_MUNICIPIO")
    f.write(",NO_MUNICIPIO")
    f.write(",SG_UF,")
    Municipio.write_header(f)
    f.write("\n")
    m: Municipio
    for m in municipios.values():
        f.write(f"{m.co_municipio}")
        f.write(f",{m.no_municipio}")
        f.write(f",{m.sg_uf}")
        m.write_grades(f)
        f.write("\n")

with open("./data/escolas.csv", "w") as f:
    f.write("CO_ESCOLA")
    f.write(",CO_MUNICIPIO")
    f.write(",TP_DEPENDENCIA_ADM")
    f.write(",TP_LOCALIZACAO")
    f.write(",TP_SIT_FUNC,")
    Escola.write_header(f)
    f.write("\n")
    e: Escola
    for e in escolas.values():
        f.write(f"{e.co_escola}")
        f.write(f",{e.co_municipio}")
        f.write(f",{e.tp_dependencia_adm}")
        f.write(f",{e.tp_localizacao}")
        f.write(f",{e.tp_sit_func}")
        e.write_grades(f)
        f.write("\n")
