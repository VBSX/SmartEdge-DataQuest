import serial

# Configurar a porta COM3
porta = serial.Serial('COM3', baudrate=9600, timeout=1)

while True:
    dados = porta.readline().decode('utf-8').strip()  # Lê uma linha de dados
    if dados:
        print(f"Peso recebido: {dados}")  # Exibe o peso recebido