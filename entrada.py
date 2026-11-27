import ast
import banco_dados
import datetime
import math
import os
from pathlib import Path
import re
import sys

os.chdir(Path(__file__).resolve().parent)

INTEIROS_POSITIVOS = ("n", "grain_number", "sampling_rate")

RAIZ = Path("./Peças")
PASTAS = ("cordenadas", "motores_solidos", "calistos", "noses", "aletas_trapezoidais", "paraquedas")   # mesma ordem do salvar_arq
MODELOS = (banco_dados.cordenadas, banco_dados.motores_solidos, banco_dados.calistos,
           banco_dados.noses, banco_dados.aletas_trapezoidais, banco_dados.paraquedas)

# Variáveis globais (mesmos nomes usados no main.py)
local = ano_mes_dia_horaUTC = altura_max = posicao_motor = None
motor_escolhido = calisto_escolhido = nose_escolhido = aleta_escolhida = paraquedas_escolhido = None
rail_length = inclination = heading = None

def pedir(msg, tipo, regra, ajuda):
    """Repete a pergunta até o usuário digitar um valor do tipo certo (int/float) que passe na regra."""
    while True:
        try:
            v = tipo(input(msg).strip().replace(",", "."))
            if math.isfinite(v) and regra(v):
                return v
        except ValueError:
            pass
        print(f"Valor inválido: {ajuda}.")


def personalizar(i):
    """Opção 'personalizar': pergunta os valores (usando o modelo do banco_dados) e cria o arquivo com salvar_arq."""
    dicio = {}
    for chave, modelo in MODELOS[i].items():
        while True:
            if isinstance(modelo, list):
                print(f"\nEscolha dentre as opções para '{chave}':")
                for it in range(len(modelo)):
                    print(f" {it+1}) {modelo[it]}")
                x = input(f"Selecione o número de uma opção: ")
                try:
                    dicio[chave] = modelo[int(x)-1]
                    print(f"Definido para '{chave}' o {modelo[int(x)-1]}\n")
                    break
                except:
                    continue
            if isinstance(modelo, str):
                dicio[chave] = escolher_curva_motor()
                break
            texto = input(f"{chave} (ex.: {modelo}): ").strip()
            if isinstance(modelo, tuple):
                try:
                    val = ast.literal_eval(texto)
                    if isinstance(val, tuple) and len(val) == len(modelo) and all(isinstance(x, (int, float)) for x in val):
                        dicio[chave] = val
                        break
                except (ValueError, SyntaxError):
                    pass
            elif not isinstance(modelo, str):
                try:
                    v = float(texto.replace(",", "."))
                    if math.isfinite(v):
                        deve_ser_inteiro = isinstance(modelo, int) or chave in INTEIROS_POSITIVOS  #verifica se o campo exige inteiro
                        if deve_ser_inteiro:
                            if v.is_integer():
                                v_int = int(v)
                                if chave not in INTEIROS_POSITIVOS or v_int > 0:
                                    dicio[chave] = v_int
                                    break
                        else:
                            dicio[chave] = v
                            break
                except ValueError:
                    pass
                print("Valor inválido.")
    while True:
        nome = input("Nome do novo arquivo (letras, números, _ ou -): ").strip()
        if not re.fullmatch(r"[\w\-]+", nome):
            print("Nome inválido.")
        elif (RAIZ / PASTAS[i] / f"{nome}.txt").exists():
            print("Já existe um arquivo com esse nome, escolha outro.")
        else:
            break
    banco_dados.salvar_arq(i, nome, dicio)
    print(f"Arquivo '{nome}.txt' criado.")
    return RAIZ / PASTAS[i] / f"{nome}.txt"

def escolher_foguete():
    """Lista os arquivos da pasta, o usuário escolhe um e devolve o dicionário salvo nele."""
    pasta = Path("./Foguetes_repertorio")
    arquivos = sorted(pasta.glob("*.txt"))
    if not arquivos:
        print('\nNenhum arquivo .txt encontrado na pasta "Foguetes_repertorio"., \n\nO programa iniciará a função personalizar')
        return None
    else:
        print("\n--- Foguetes disponíveis ---")
        for n, arq in enumerate(arquivos, 1):
            print(f" {n}) {arq.stem}")
        n = pedir(
            "Digite o número da opção: ",
            int,
            lambda v: 1 <= v <= len(arquivos),
            f"digite um número inteiro de 1 a {len(arquivos)}",
        )
        arquivo = arquivos[n - 1]
        dados = ast.literal_eval(arquivo.read_text(encoding="utf-8"))
        print(f"\"Foguetes_repertorio\": '{arquivo.stem}' carregado.")
        return dados


def escolher(i, rotulo):
    """Lista os arquivos da pasta, o usuário escolhe um (ou personaliza) e devolve o dicionário salvo nele."""
    arquivos = sorted((RAIZ / PASTAS[i]).glob("*.txt"))
    print(f"\n--- {rotulo} ---")
    if not (RAIZ / PASTAS[i]).is_dir():
        print(f"Pasta '{RAIZ / PASTAS[i]}' não encontrada. Rode o programa de dentro da pasta do projeto.")
    for n, arq in enumerate(arquivos, 1):
        print(f"  {n}) {arq.stem}")
    print(f"  {len(arquivos) + 1}) Personalizar")
    n = pedir("Digite o número da opção: ", int, lambda v: 1 <= v <= len(arquivos) + 1,
              f"digite um número inteiro de 1 a {len(arquivos) + 1}")
    arquivo = personalizar(i) if n == len(arquivos) + 1 else arquivos[n - 1]
    dados = ast.literal_eval(arquivo.read_text(encoding="utf-8"))
    print(f"{rotulo}: '{arquivo.stem}' carregado.")
    return dados

def escolher_curva_motor():
    """Lista os arquivos da pasta, o usuário escolhe um arquivo salvo nele."""
    pasta = Path("./Peças/curvas_propulsao_motores")
    arquivos = sorted(pasta.glob("*.eng"))
    if not arquivos:
        print('\nNenhum arquivo .eng encontrado na pasta "curvas_propulsao_motores", \n\n Insira na pasta sua curva de propulsão .eng (um arquivo csv com extensão .eng)')
        sys.exit("Programa Encerrado")
        return None
    else:
        print("\n--- Curvas de propulsao disponíveis ---")
        for n, arq in enumerate(arquivos, 1):
            print(f" {n}) {arq.stem}")
        n = pedir(
            "Digite o número da opção: ",
            int,
            lambda v: 1 <= v <= len(arquivos),
            f"digite um número inteiro de 1 a {len(arquivos)}",)
        arquivo = arquivos[n - 1]
        curva = arquivo
        print(f"\"curvas_propulsao_motores\": '{arquivo.stem}' carregado.")
        return str(curva)

def escolher_coordenadas():
    global local
    local = escolher(0, "Coordenadas do local de lançamento")

def escolher_motor():
    global motor_escolhido
    motor_escolhido = escolher(1, "Motor sólido")

def escolher_calisto():
    global calisto_escolhido
    calisto_escolhido = escolher(2, "Calisto")

def escolher_nose():
    global nose_escolhido
    nose_escolhido = escolher(3, "Nose (ogiva)")

def escolher_aleta():
    global aleta_escolhida
    aleta_escolhida = escolher(4, "Aletas trapezoidais")

def escolher_paraquedas():
    global paraquedas_escolhido
    paraquedas_escolhido = escolher(5, "Paraquedas")


def escolher_posicao_motor():
    global posicao_motor
    print("\n--- Posição do motor ---")
    posicao_motor = pedir("Distância da ponta da ogiva até o motor, em metros (ex: 1.5): ", float,
                          lambda v: v > 0, "digite um número decimal maior que 0")
    print(f"Posição do motor: {posicao_motor} m")


def escolher_data_hora():
    global ano_mes_dia_horaUTC
    print("\n--- Data e hora do lançamento (hora em UTC; Brasília = UTC-3), escolha uma data futura em até uma semana ---")
    while True:
        data_lançamento = (pedir("Ano: ", int, lambda v: 2000 <= v <= 2100, "inteiro entre 2000 e 2100"),
             pedir("Mês (1-12): ", int, lambda v: 1 <= v <= 12, "inteiro de 1 a 12"),
             pedir("Dia (1-31): ", int, lambda v: 1 <= v <= 31, "inteiro de 1 a 31"),
             pedir("Hora UTC (0-23): ", int, lambda v: 0 <= v <= 23, "inteiro de 0 a 23"))
        try:
            data = datetime.datetime(*data_lançamento, tzinfo=datetime.timezone.utc)
        except ValueError:
            print("Essa data não existe, digite de novo.")
            continue
        hoje = datetime.datetime.now(datetime.timezone.utc)
        if hoje <= data <= hoje + datetime.timedelta(days=7):
            break
        else:
            print("\nData em intevalo não aceito, digite novamente\n")
    ano_mes_dia_horaUTC = data_lançamento
    print(f"Lançamento: {data_lançamento}")


def escolher_altura_max():
    global altura_max
    print("\n--- Altura máxima de voo ---")
    altura_max = pedir("Altura máxima em metros (inteiro, ex.: 5000): ", int, lambda v: v > 0,
                       "digite um número inteiro maior que 0")
    print(f"Altura máxima: {altura_max} m")

def escolher_rampa():
    global rail_length, inclination, heading
    print("\n--- Rampa de decolagem ---")
    rail_length = pedir("Rampa em metros (Float, ex.: 1.5): ", float, lambda v: v > 0, "digite um número inteiro maior que 0")
    print(f"Rampa: {rail_length} m")

def escolher_direcao():
    global inclination, heading
    print("\n--- Inclinação de Lançamento ---")
    inclination = pedir("Inclinação de lançamento em graus (float, ex.: 89.5): ", float, lambda v: v > 0 and v <= 90, "digite um ângulo de 90(vertical) a 0 graus")
    print(f"Inclinação: {inclination} graus")

    print("\n--- Direção de Lançamento ---")
    heading = pedir("Direção de Lançamento em graus (float, ex.: 30.5): ", float, lambda v: v >= 0 and v <= 360, "digite um angulo horário entre 0(Norte) e 360 graus")
    print(f"Inclinação: {heading} graus em relação ao norte")

def coletar_condicoes_lancamento():
    escolher_coordenadas()
    escolher_altura_max()
    escolher_rampa()
    escolher_direcao()

def coletar_foguete():
    escolher_motor()
    escolher_posicao_motor()
    escolher_calisto()
    escolher_nose()
    escolher_aleta()
    escolher_paraquedas()
