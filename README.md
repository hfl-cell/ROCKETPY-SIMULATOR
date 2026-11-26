# 🚀 Manual Rápido de Uso — Simulador de Voo (RocketPy)

## Programadores:

* Carlos V.
* Henrique F. L.
* Leonardo M. M.

## 0. Instalação das Bibliotecas

* **Ambiente Python:** O código foi programado em **Python 3**, sendo recomendável utilizar um interpretador que opere nessa versão.
* **Bibliotecas Padrão:** O programa utiliza os módulos nativos `ast`, `contextlib`, `datetime`, `math`, `os`, `pathlib`, `re` e `sys` (não é necessário instalá-los).
* **Dependência Externa:** A única biblioteca que precisa ser instalada manualmente é a `rocketpy`. Execute o seguinte comando no terminal:

```bash
pip install rocketpy==1.13.0
```

---

## 1. Pré-requisitos e Boas Práticas

* **Execução:** Execute o arquivo `main.py` via terminal Python, garantindo que o diretório de execução seja o mesmo onde estão as pastas do projeto.
* **Integridade dos Arquivos:** Não modifique ou apague as pastas `Peças` e `Foguetes`.
* **Backup:** Todos os dados e gráficos são salvos na pasta `RESULTADOS_SIMULACAO` e **são sobrescritos a cada nova execução**. Salve uma cópia antes de rodar novamente.
* **Gráficos:** Sempre feche as janelas de gráficos exibidas na tela para que a execução do código continue.

---

## 2. Passo a Passo da Simulação

Link para o vídeo demonstrativo de uso: 
```base
https://youtu.be/nFE1nzfMWz4
```

### Etapa 1: Ambiente e Lançamento

1. **Condições Atmosféricas:** Escolha entre `1` (Atmosfera padrão ISO) ou `2` (Condições climáticas reais de um local).

```text
---Defina condições atmosféricas---
1 - Atmosfera padrão ISO
2 - Condições reais do local
Selecione uma opção: 2
```

2. **Local e Data (se escolher a opção `2`):** Selecione uma cidade pré-cadastrada (ou insira coordenadas) e informe a data/hora do lançamento em **UTC** (até 7 dias no futuro).

```text
--- Coordenadas do local de lançamento ---
1) Americana
2) Serra_Negra
3) São_Carlos
4) São_Luis_Maranhao
5) Personalizar
Digite o número da opção: 1

--- Data e hora do lançamento (hora em UTC; Brasília = UTC-3), escolha uma data futura em até uma semana ---
Ano: 2026
Mês (1-12): 11
Dia (1-31): 26
Hora UTC (0-23): 12
```

3. **Parâmetros da Base:** Informe a altitude máxima esperada (m), o comprimento da rampa de lançamento (m), o ângulo de inclinação (graus) e o azimute/direção em relação ao Norte (graus).

```text
--- Rampa de decolagem ---
Rampa em metros (Float, ex.: 1.5): 1.5

--- Inclinação de Lançamento ---
Inclinação de lançamento em graus (float, ex.: 89.5): 90

--- Direção de Lançamento ---
Direção de Lançamento em graus (float, ex.: 30.5): 0
```

4. **Validação Climática:** Analise os gráficos climáticos gerados, feche as janelas após conferir e pressione `ENTER` no terminal para avançar.

---

### Etapa 2: Configuração do Foguete

1. **Seleção do Modelo:** Escolha `1` para carregar um foguete pronto do repertório ou `2` para montar um novo.

```text
---Defina foguete usado---
1 - Foguete de Repertório
2 - Montar foguete
Selecione uma opção: 2
```

2. **Montagem (se escolher a opção `2`):** Selecione ou personalize cada componente na ordem solicitada:
   * Motor sólido e sua posição em relação à ponta da ogiva (m);
   * Corpo/fuselagem (`Calisto`);
   * Ogiva (`Nose cone`);
   * Aletas trapezoidais;
   * Paraquedas.

3. **Personalizar (caso escolha personalizar alguma peça):** Serão exibidas, para cada componente, características para preenchimento (valores numéricos ou opções numéricas para textos).

```text
--- Nose (ogiva) ---
1) nose_aleatorio
2) nose_teste
3) Personalizar
Digite o número da opção: 3
length (ex.: 0.558): 0.6
Escolha dentre as opções para 'kind':
1) conical
2) ogive
3) parabolic
4) vonKarman
Selecione o número de uma opção: 3
Definido para 'kind' o parabolic
Nome do novo arquivo (letras, números, _ ou -): teste_apagar
Nose (ogiva): 'teste_apagar' carregado.
```

4. **Salvamento:** Dê um nome ao arquivo (sem espaços ou caracteres especiais) para salvar o foguete montado.

---

### Etapa 3: Análise de Estabilidade e Resultados

1. **Conferência Pré-Voo:** O sistema exibirá os dados de massa, inércia, aerodinâmica e a **Margem Estática Inicial** (em calibres), alertando se o foguete está instável, estável ou superestável. Pressione `ENTER` para simular o voo.

```text
--- DADO FUNDAMENTAL ---
Margem de estabilidade inicial: 6.09 calibres
Foguete SUPERESTÁVEL (margem muito alta). Pode sofrer muito com o vento (weathercocking).
Se quiser continuar aperte ENTER, qualquer outra tecla encerra o programa:
```

2. **Resultados do Voo:** O terminal exibirá o resumo primário (Apogeu, tempo até o apogeu, velocidade máxima e velocidade de saída da rampa).

```text
---Resultados Primarios---
Altitude Máxima (Apogeu): 665.46 metros
Tempo até o Apogeu: 6.19 segundos
Velocidade máxima atingida: 27.29 m/s
Velocidade de saída da rampa: 6.43 m/s
```

3. **Finalização:** Pressione `ENTER` para gerar e salvar os gráficos finais de trajetória na pasta `RESULTADOS_SIMULACAO`.
