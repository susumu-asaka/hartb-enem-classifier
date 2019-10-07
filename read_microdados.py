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
        for p in range(3):
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

    def write(self, file):
        for p in range(3):
            sg_prova = Graded.sg_provas[p]
            nu_comparecimento_prova = getattr(self, "nu_comparecimento_" + sg_prova)
            nu_aprovacao_prova = getattr(self, "nu_comparecimento_" + sg_prova)
            file.write(f",{nu_comparecimento_prova}")
            file.write(f",{100 * nu_aprovacao_prova / nu_comparecimento_prova}")


class Municipio(Graded):
    def __init__(self, co_municipio, no_municipio, sg_uf):
        super().__init__()
        self.co_municipio = co_municipio
        self.no_municipio = no_municipio
        self.sg_uf = sg_uf


class Escola(Graded):
    def __init__(self, co_escola, co_municipio, tp_dependencia_adm,
                 tp_localizacao, tp_sit_func):
        super().__init__()
        self.co_escola = co_escola
        self.co_municipio = co_municipio
        self.tp_dependencia_adm = tp_dependencia_adm
        self.tp_localizacao = tp_localizacao
        self.tp_sit_func = tp_sit_func


municipios = {}

escolas = {0: Escola(0, 0, 0, 0, 0)}


def record_grades(nu_notas):
    municipio = municipios.setdefault(
        co_municipio_residencia,
        Municipio(
            co_municipio_residencia,
            no_municipio_residencia,
            sg_uf_municipio_residencia,
        ),
    )
    escola = escolas.setdefault(
        co_escola,
        Escola(
            co_escola,
            co_municipio_esc,
            tp_dependencia_adm_esc,
            tp_localizacao_esc,
            tp_sit_func_esc,
        ),
    )
    for p in range(3):
        if nu_notas[p] != "":
            municipio[3 + 2 * p] += 1
            escola[5 + 2 * p] += 1
            if float(nu_notas[p]) >= 650:
                municipio[4 + 2 * p] += 1
                escola[6 + 2 * p] += 1


with open(
        "/Users/susum/Downloads/Microdados Enem 2017/DADOS/microdados_enem_2017.csv"
) as file:
    # read header
    file.readline()
    # read 1st record
    line = file.readline()
    for i in range(200):
        fields = line.split(";")
        co_municipio_residencia = int(fields[2])
        no_municipio_residencia = fields[3]
        sg_uf_municipio_residencia = fields[5]
        if fields[20] != "":
            co_escola = int(fields[20])
            co_municipio_esc = int(fields[21])
            tp_dependencia_adm_esc = int(fields[25])
            tp_localizacao_esc = int(fields[26])
            tp_sit_func_esc = int(fields[27])
        else:
            co_escola = 0
            co_municipio_esc = 0
            tp_dependencia_adm_esc = 0
            tp_localizacao_esc = 0
            tp_sit_func_esc = 0
        record_grades(fields[90:94])


def write_header_provas():
    file.write("NU_COMPARECIMENTO_CN")
    file.write(",PC_APROVACAO_CN")
    file.write(",NU_COMPARECIMENTO_CH")
    file.write(",PC_APROVACAO_CH")
    file.write(",NU_COMPARECIMENTO_LC")
    file.write(",PC_APROVACAO_LC")
    file.write(",NU_COMPARECIMENTO_MT")
    file.write(",PC_APROVACAO_MT")


def write_provas(registro, offset):
    for p in range(3):
        nu_comparecimento_prova = registro[offset + 2 * p]
        nu_aprovacao_prova = registro[offset + 1 + 2 * p]
        file.write(f",{nu_comparecimento_prova}")
        file.write(f",{100 * nu_aprovacao_prova / nu_comparecimento_prova}")


with open("./data/municipios.csv", "w") as file:
    file.write("CO_MUNICIPIO")
    file.write(",NO_MUNICIPIO")
    file.write(",SG_UF")
    write_header_provas()
    m: Municipio
    for m in municipios.values():
        file.write(f"{m.co_municipio}")
        file.write(f",{m.no_municipio}")
        file.write(f",{m.sg_uf}")
        write_provas(m, 3)
        file.write("\n")

with open("./data/escolas.csv", "w") as file:
    file.write("CO_ESCOLA")
    file.write(",CO_MUNICIPIO")
    file.write(",TP_DEPENDENCIA_ADM")
    file.write(",TP_LOCALIZACAO")
    file.write(",TP_SIT_FUNC")
    write_header_provas()
    e: Escola
    for e in escolas.values():
        file.write(f",{e.co_escola}")
        file.write(f",{e.co_municipio}")
        file.write(f",{e.tp_dependencia_adm}")
        file.write(f",{e.tp_localizacao}")
        file.write(f",{e.tp_sit_func}")
        write_provas(e, 5)
        file.write("\n")
