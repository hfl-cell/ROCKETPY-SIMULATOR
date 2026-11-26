#Avisos e Orientações

print("---ROCKET.PY SIMULATOR---")
print("\nSimulador da dinâmica do voo de foguetes de espaço-modelismo baseado na biblioteca rocket.py")

print("\n---AVISOS---")
print("\nO simulador é projetado para simular somente foguetes de combustível sólido convencionais")
print("Todos os resultados serão salvos automaticamente na pasta 'RESULTADOS_SIMULACAO', mas" "\n" "CUIDADO: os arquivos serão sobrescritos pela próxima simulação, salve uma cópia antes")
print("NÃO altere os arquivos ou pastas presentes em \"Peças\" ou \"Foguetes\". Resultará em travamentos ou má operação" "\nEnquanto os gráficos estiverem abertos o programa não rodará,  feche-os após consulta")

print("\nPrograma iniciando, aguarde")

#-------------------------------------------------------------------------------------------------------

# Bibliotecas

import banco_dados
import contextlib
import entrada
import datetime
from pathlib import Path
from rocketpy import Environment, SolidMotor, Rocket, Flight
import sys

#========================================================================================
# Entradas do Usuário: condições atmosfericas
#========================================================================================

print("---Defina condições atmosféricas---")
print("   1 - Atmosfera padrão ISO")
print("   2 - Condições reais do local")

while True:
    confirmacao = input("Selecione uma opção:" )
    if confirmacao == "1" or confirmacao == "2":
        break
    else:
        print("Entrada inválida")
print("Opção escolhida:", confirmacao)

entrada.coletar_condicoes_lancamento()

# Copiando os valores preenchidos para o main.py
local = entrada.local
altura_max = entrada.altura_max


print("Aguarde, os gráficos de estabilidade estão sendo gerados, uma janela será aberta com as condições climáticas")


# ------------------------------------------------------------------------------------------------------

# Definir o Ambiente (Localização, data, condição atmosférica, altura máxima de processamento e gravidade) e condições de lançamento

env = Environment(
    latitude= local["latitude"], 
    longitude=local["longitude"], 
    elevation=local["altura"],
    max_expected_height = altura_max,
    gravity = None)

if confirmacao == "2":
    entrada.escolher_data_hora()
    ano_mes_dia_horaUTC = entrada.ano_mes_dia_horaUTC
    env.set_date(ano_mes_dia_horaUTC)
    env.set_atmospheric_model(type='Forecast', file='GFS')
elif confirmacao == "1":
    env.set_atmospheric_model(type="standard_atmosphere")

print("\nCarregando dados, aguarde")

rail_length = entrada.rail_length
inclination = entrada.inclination
heading = entrada.heading

#--------------------------------------------------------------------------------------

# Exibe ao usuário os dados da atmosfera para conferir e salvar

print("Salvando gráficos")
env.plots.atmospheric_model()
env.plots.atmospheric_model(filename="./RESULTADOS_SIMULAÇÃO/modelo_atmosferico_graficos.png")

print("gráficos salvos")

confirmacao = input("Se quiser continuar aperte ENTER, qualquer outra tecla encerra o programa: ")

if confirmacao != "":
    sys.exit("Programa Encerrado.")

print("Programa proceguindo execussão")

#========================================================================================
# Entradas do Usuário: configurações do foguete
#========================================================================================

print("\n---Defina foguete usado---")
print("   1 - Foguete de Repertório")
print("   2 - Montar foguete")

while True:
    confirmacao = input("Selecione uma opção:" )
    if confirmacao == "1" or confirmacao == "2":
        break
    else:
        print("Entrada inválida")
print("Opção escolhida:", confirmacao)

if confirmacao == "1":

    escolhido = entrada.escolher_foguete()

    if isinstance(escolhido, dict):
        # Copiando os valores preenchidos para o main.py
        posicao_motor = escolhido["posicao_motor"]
        motor_escolhido = escolhido["motor_escolhido"]
        calisto_escolhido = escolhido["calisto_escolhido"]
        nose_escolhido = escolhido["nose_escolhido"]
        aleta_escolhida = escolhido["aleta_escolhida"]
        paraquedas_escolhido = escolhido["paraquedas_escolhido"]
    else:
        confirmacao = "2"

if confirmacao == "2":
    entrada.coletar_foguete()

    # Copiando os valores preenchidos para o main.py
    posicao_motor = entrada.posicao_motor
    motor_escolhido = entrada.motor_escolhido
    calisto_escolhido = entrada.calisto_escolhido
    nose_escolhido = entrada.nose_escolhido
    aleta_escolhida = entrada.aleta_escolhida
    paraquedas_escolhido = entrada.paraquedas_escolhido
    

    #Salvando Foguete com esses componentes:

    escolhas = {
        "posicao_motor": posicao_motor,
        "motor_escolhido": motor_escolhido,
        "calisto_escolhido": calisto_escolhido,
        "nose_escolhido": nose_escolhido,
        "aleta_escolhida": aleta_escolhida,
        "paraquedas_escolhido": paraquedas_escolhido}
    
    banco_dados.salvar_foguete(**escolhas)
    

#----------------------------------------------------------------------------------------

# Definir o Tipo de Motor e suas características:

motor = SolidMotor(
    thrust_source=motor_escolhido["thrust_source"],
    dry_mass=motor_escolhido["dry_mass"],
    dry_inertia=motor_escolhido["dry_inertia"],
    burn_time=motor_escolhido["burn_time"],
    grain_number=motor_escolhido["grain_number"],
    grain_separation=motor_escolhido["grain_separation"],
    grain_density=motor_escolhido["grain_density"],
    grain_outer_radius=motor_escolhido["grain_outer_radius"],
    grain_initial_inner_radius=motor_escolhido["grain_initial_inner_radius"],
    grain_initial_height=motor_escolhido["grain_initial_height"],
    grains_center_of_mass_position=motor_escolhido["grains_center_of_mass_position"],
    center_of_dry_mass_position=motor_escolhido["center_of_dry_mass_position"],
    nozzle_radius=motor_escolhido["nozzle_radius"],
    throat_radius=motor_escolhido["throat_radius"]
)

#----------------------------------------------------------------------------------
# Construindo o Foguete
#----------------------------------------------------------------------------------

# Adicionando Calisto
calisto = Rocket(
    radius=calisto_escolhido["radius"],
    mass=calisto_escolhido["mass"],
    inertia=calisto_escolhido["inertia"],
    power_off_drag=calisto_escolhido["power_off_drag"],
    power_on_drag=calisto_escolhido["power_on_drag"],
    center_of_mass_without_motor=calisto_escolhido["center_of_mass_without_motor"],
    coordinate_system_orientation="nose_to_tail",
)

# Adicionar o motor ao foguete
calisto.add_motor(motor, position=posicao_motor)

# Adicionar nose (ogiva)
nose_cone = calisto.add_nose(
    length=nose_escolhido["length"],
    kind=nose_escolhido["kind"],
    position= 0
)

# Adicionar aletas
fins = calisto.add_trapezoidal_fins(
    n= aleta_escolhida["n"],                 
    root_chord=aleta_escolhida["root_chord"],
    tip_chord=aleta_escolhida["tip_chord"],      
    span=aleta_escolhida["span"],            
    position=aleta_escolhida["position"],       
    cant_angle=aleta_escolhida["cant_angle"],
)


# Adicionar paraquedas
main_parachute = calisto.add_parachute(
    name=paraquedas_escolhido["name"],
    cd_s=paraquedas_escolhido["cd_s"],
    trigger="apogee",
    sampling_rate=paraquedas_escolhido["sampling_rate"],
    lag=paraquedas_escolhido["lag"]                
)

#---------------------------------------------------------------------------------------------------

# Exibe ao usuário os dados da montagem para conferir e salvar

print("--- Confira as configurações do foguete estão sendo gerados---")

calisto.draw()
calisto.draw(filename="./RESULTADOS_SIMULAÇÃO/desenho_foguete.png")

calisto.info()                  # Imprime um resumo completo com a posição do CM, CP e peso total

margem = margem = float(calisto.static_margin(0))

print("\n--- DADO FUNDAMENTAL ---")

print(f"\nMargem de estabilidade inicial: {margem:.2f} calibres")

if margem < 1.0:
    print("Foguete INSTÁVEL (margem muito baixa). Adicione peso no nariz ou aumente as aletas.")
elif margem > 3.0:
    print("Foguete SUPERESTÁVEL (margem muito alta). Pode sofrer muito com o vento (weathercocking).")
else:
    print("Foguete ESTÁVEL (dentro da faixa recomendada).")

confirmacao = input("\nSe quiser continuar aperte ENTER, qualquer outra tecla encerra o programa: ")

if confirmacao != "":
    sys.exit("\nPrograma Encerrado.")

with open("./RESULTADOS_SIMULAÇÃO/Dados_foguete_simulado.txt", "a", encoding="utf-8") as fog:
    with contextlib.redirect_stdout(fog):
        calisto.info()
print("\nDados salvos")


#---------------------------------------------------------------------------------------------------

# Executar a Simulação de Voo

print("\nAguarde, os resultados estão sendo gerados")

voo = Flight(rocket=calisto, environment=env, rail_length=rail_length, inclination=inclination, heading=heading)

print("\n---Resultados Primarios---")
# Fornece informações essenciais
print(f"Altitude Máxima (Apogeu): {voo.apogee:.2f} metros")
print(f"Tempo até o Apogeu: {voo.apogee_time:.2f} segundos")
print(f"Velocidade máxima atingida: {voo.max_speed:.2f} m/s")
print(f"Velocidade de saída da rampa: {voo.out_of_rail_velocity:.2f} m/s")

with open("./RESULTADOS_SIMULAÇÃO/Resultados_foguete_simulado", "w", encoding="utf-8") as fog:
    fog.write(f"Altitude Máxima (Apogeu): {voo.apogee:.2f} metros\n")
    fog.write(f"Tempo até o Apogeu: {voo.apogee_time:.2f} segundos\n")
    fog.write(f"Velocidade máxima atingida: {voo.max_speed:.2f} m/s\n")
    fog.write(f"Velocidade de saída da rampa: {voo.out_of_rail_velocity:.2f} m/s\n")
print("\nDados salvos")

confirmacao = input("\nSe quiser continuar aperte ENTER, qualquer outra tecla encerra o programa: ")

if confirmacao != "":
    sys.exit("\nPrograma Encerrado.")

print("\nOs gráficos estão sendo gerados, aguarde")

try:
    calisto.plots.static_margin()
    calisto.plots.static_margin(filename="./RESULTADOS_SIMULAÇÃO/grafico_margem_estabilidade.png")
    voo.plots.trajectory_3d() 
    voo.plots.linear_kinematics_data()
    voo.plots.trajectory_3d(filename="./RESULTADOS_SIMULAÇÃO/grafico_trajetoria_3d.png") 
    voo.plots.linear_kinematics_data(filename="./RESULTADOS_SIMULAÇÃO/graficos_cinematicos.png")
    calisto.plots.drag_curves()
    calisto.plots.drag_curves(filename="./RESULTADOS_SIMULAÇÃO/curvas_arrasto.png")
    calisto.plots.thrust_to_weight()
    calisto.plots.thrust_to_weight(filename="./RESULTADOS_SIMULAÇÃO/empuxo_peso.png")
except:
    print("\n---Foguete divergiu, foguete teve falha no voo---")
    sys,exit("\nFechando programa" \
    "\n..." \
    "\n...")

print("simulação concluída")
print("CUIDADO: os arquivos serão sobrescritos após a simulação ser rodada novamente, copi-os em outra pasta")