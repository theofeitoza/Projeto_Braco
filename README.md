<div id="top"></div>

<div align="center">

🦾 Controlador de Braço Robótico
Interface Gráfica para Controle, Gravação e Reprodução de Movimentos de um Braço Robótico de 5 Eixos.

<img alt="last-commit" src="https://img.shields.io/github/last-commit/theofeitoza/projeto_braco?style=flat&logo=git&logoColor=white&color=0080ff"> <img alt="repo-top-language" src="https://img.shields.io/github/languages/top/theofeitoza/Projeto_Braco?style=flat&color=0080ff">

<p><em>Tecnologias Utilizadas:</em></p> <img alt="Python" src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white"> <img alt="Flet" src="https://img.shields.io/badge/Flet-00D46A.svg?style=flat&logo=python&logoColor=white"> <img alt="Arduino" src="https://img.shields.io/badge/Arduino-00979D.svg?style=flat&logo=Arduino&logoColor=white">

</div>

📜 Índice
Visão Geral

✨ Funcionalidades

🔧 Arquitetura do Sistema

🏁 Como Começar

Pré-requisitos de Hardware

Pré-requisitos de Software

Configuração e Instalação

Execução

<hr>

🚀 Visão Geral
Este projeto consiste em um sistema completo para o controle de um braço robótico de 5 graus de liberdade (DOF). O sistema é composto por duas partes principais:

Firmware para Arduino: Um código (.ino) que é carregado em um microcontrolador Arduino para gerenciar o controle de baixo nível dos servo motores através de um driver PCA9685.

Interface Gráfica (GUI): Uma aplicação desktop desenvolvida em Python com o framework Flet. A interface permite o controle manual em tempo real de cada junta do braço, além de oferecer funcionalidades para gravar, salvar, importar e reproduzir sequências de movimentos.

A comunicação entre a interface gráfica e o Arduino é realizada via porta serial (USB).

<hr>

✨ Funcionalidades
🕹️ Controle em Tempo Real: Mova cada uma das 5 juntas do braço (Base, Ombro, Cotovelo, Mão e Garra) usando sliders intuitivos.

💾 Gravação de Posições: Salve a pose atual do braço robótico em um dos três slots de memória.

📂 Exportar e Importar Movimentos: Exporte sequências de posições salvas para um arquivo de texto (posicoes.txt) e importe-as posteriormente.

▶️ Reprodução Automatizada: Execute sequências de movimentos salvas no arquivo posicoes.txt com um clique, permitindo a automação de tarefas.

🔄 Reset de Posição: Retorne o braço para uma posição inicial pré-definida de forma rápida.

💻 Interface Gráfica Amigável: Interface limpa e funcional, construída com Flet, para facilitar a interação com o hardware.

<hr>

🔧 Arquitetura do Sistema
O fluxo de controle do sistema funciona da seguinte maneira:

Interface Gráfica (Python/Flet) ↔️ Comunicação Serial (USB) ↔️ Arduino + Driver PCA9685 ↔️ Servo Motores do Braço

<hr>

🏁 Como Começar
Siga os passos abaixo para configurar e executar o projeto.

Pré-requisitos de Hardware
Um microcontrolador compatível com Arduino (ex: Arduino Uno, Nano).

Driver de Servo Motor PCA9685 I2C.

5 Servo Motores (compatíveis com o braço).

Estrutura de um braço robótico.

Fonte de alimentação externa para os servos.

Fios e protoboard para as conexões.

Pré-requisitos de Software
Python 3.8+

Arduino IDE

Bibliotecas Python: flet e pyserial.

Configuração e Instalação
Hardware:

Conecte os 5 servo motores aos canais 11, 12, 13, 14 e 15 do driver PCA9685.

Conecte o driver PCA9685 ao Arduino (pinos SDA e SCL).

Alimente o driver PCA9685 e o Arduino com as fontes de energia apropriadas.

Firmware (Arduino):

Abra o arquivo final_5sliders/final_5sliders.ino na Arduino IDE.

Instale a biblioteca Adafruit PWM Servo Driver através do Gerenciador de Bibliotecas (Sketch > Include Library > Manage Libraries...).

Selecione a placa e a porta COM correta no menu Tools.

Clique em "Upload" para gravar o código no Arduino.

Software (Python GUI):

Clone o repositório:

Bash

❯ git clone https://github.com/theofeitoza/Projeto_Braco.git
Navegue até o diretório do projeto:

Bash

❯ cd Projeto_Braco
Instale as dependências Python:

Bash

❯ pip install flet pyserial
Execução
Com o hardware montado e o firmware carregado, conecte o Arduino ao computador via USB.

Verifique a Porta COM: Identifique em qual porta COM o Arduino está conectado (você pode ver isso na Arduino IDE ou no Gerenciador de Dispositivos do seu sistema operacional).

Atualize o Script Python: Abra o arquivo principal Python e, se necessário, altere a linha abaixo para corresponder à sua porta COM:

Python

# Altere 'COM5' para a porta correta
ser = serial.Serial('COM5', 9600, timeout=1) 
Execute a aplicação:

Bash

# Certifique-se de que você está no diretório correto
❯ python seu_script_principal.py 
Substitua seu_script_principal.py pelo nome do seu arquivo Python.

A interface gráfica será iniciada, e você poderá começar a controlar o braço robótico.

<hr>

<div align="left"> <a href="#top">⬆ Voltar ao topo</a> </div>
