#==============================================================================================
# Esse arquivo contém, além das funções usadas para criar/acessar os arquivos durante operação do programa
#Os modelos dos dicionário necessários ao código
#===============================================================================================

# Bibliotecas

import re
import pathlib as pa

#-----------------------------------------------------------------------------------------------

# Confere se as pastas existem e, se não existir, cria:


for pastas in ["./Peças", "./RESULTADOS_SIMULAÇÃO", "./Foguetes_repertorio"]:
    caminho = pa.Path(pastas)
    caminho.mkdir(parents=True, exist_ok=True)
    
for subpasta in ["cordenadas","motores_solidos", "calistos", "noses", "aletas_trapezoidais", "paraquedas"]:
    pasta = pa.Path("./Peças")
    caminho = pasta / subpasta
    caminho.mkdir(parents=True, exist_ok=True)

#-----------------------------------------------------------------------------------------------

# Funções de manipulação de arquivos

def salvar_arq(peça, nome, dicio):
    items = ("cordenadas","motores_solidos", "calistos", "noses", "aletas_trapezoidais", "paraquedas")
    def salvando(peça, nome, **dicio):
        from pathlib import Path

        pasta = items[int(peça)]
        raiz = "./Peças/" + pasta
        caminho = Path(raiz)
        caminho.mkdir(parents=True, exist_ok=True)
        name_file = str(nome) +".txt"
        caminho_completo = caminho /name_file
        conteudo = str(dicio) 
        with open(caminho_completo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        return None
    salvando(peça, nome, **dicio)
    
    return None

def salvar_foguete(**escolha):
    while True:
        nome = input("Nome do novo arquivo (letras, números, _ ou -): ").strip()
        if not re.fullmatch(r"[\w\-]+", nome):
            print("Nome inválido.")
        else:
            break
    raiz = pa.Path("./Foguetes_repertorio")
    name_file = str(nome) +".txt"
    caminho = raiz/name_file
    with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(str(escolha))
    return print(f"Configurações de foguete salvos como: {name_file}")

#------------------------------------------------------------------------------------------

# Modelo do dicionário que salva as peças e informações

escolhas ={
    "local": None,
    "ano_mes_dia_horaUTC": None,
    "altura_max": None,
    "motor_escolhido": None,
    "calisto_escolhido": None,
    "posicao_motor": None,
    "nose_escolhido": None,
    "aleta_escolhida": None,
    "paraquedas_escolhido": None
}

#------------------------------------------------------------------------------------------

# 0 - Locais de Lançamento

cordenadas = {
        "latitude": -21.960641,
        "longitude": -47.482122,
        "altura": 640
    }

#--------------------------------------------------------------------------------------------

# 1 - Opções de Motores Sólidos

motores_solidos = {
    "thrust_source": "caminho_para_curva_de_empuxo.eng", # Curva de empuxo
    "dry_mass": 1.815,                                  # Massa seca do motor (kg)
    "dry_inertia": (0.125, 0.125, 0.002),               # Inércia seca (I11, I22, I33) em kg*m²
    "burn_time": 3.9,                                   # Tempo de queima (s)
    "grain_number": 5,
    "grain_separation": 0.005,                          # Separação entre os grãos (m)
    "grain_density": 1700,
    "grain_outer_radius": 0.033,
    "grain_initial_inner_radius": 0.015,
    "grain_initial_height": 0.12,
    "grains_center_of_mass_position": 0.397,            # Posição do CM dos grãos (m)
    "center_of_dry_mass_position": 0.317,               # Posição do CM seco do motor (m)
    "nozzle_radius": 0.014,
    "throat_radius": 0.0075
}

#--------------------------------------------------------------------------------------------

# 2 - Opções de Calistos

calistos ={
        "radius": 0.0635,          # Raio do corpo do foguete (em metros)
        "mass":14.426,            # Massa sem o motor (em kg)
        "inertia":(0.0561,0.0561,0.0034),       # Momento de inércia (em kg*m²)
        "power_off_drag": 0.4,     # Coeficiente de arrasto (Cd) com motor desligado (pode ser arquivo função)
        "power_on_drag": 0.4,      # Coeficiente de arrasto (Cd) com motor ligado
        "center_of_mass_without_motor": 0, # Posição do CM sem motor (em metros, a partir da ogiva)
        # "coordinate_system_orientation":"nose_to_tail"
}

#--------------------------------------------------------------------------------------------

# 3 - Opções de Noses(Ogivas)

noses = {
        "length": 0.558,          # Comprimento da ogiva (em metros)
        # "position": 0,            # Sempre na posição 0 (ponta do foguete)
        "kind":["conical", "ogive", "parabolic", "vonKarman"]
}

#--------------------------------------------------------------------------------------------

# 4 - Opções de Aletas

aletas_trapezoidais = {
        "n": 4 ,               # Número de aletas (geralmente 3 ou 4)
        "root_chord":0.120,      # Corda da raiz (comprimento da base colada no foguete)
        "tip_chord":0.060,       # Corda da ponta (comprimento do topo da aleta)
        "span": 0.110,            # Envergadura (altura da aleta para fora do tubo)
        "position":1.2,          # Posição da raiz da aleta a partir da ogiva
        "cant_angle":0,          # Ângulo de inclinação (para induzir rotação, se desejar)
}

#--------------------------------------------------------------------------------------------

# 5 - Padrão de de Paraquedas

paraquedas ={
            "name":["drougue","main"],
            "cd_s":10.0,             # Cd (coeficiente de arrasto) multiplicado pela área do paraquedas (m²)
            # "trigger":"apogee",      # Momento da abertura ("apogee" ou uma função personalizada)
            "sampling_rate":100,     # Taxa de amostragem do sensor fictício
            "lag":1.5                # Atraso em segundos entre o comando e a abertura real
    }