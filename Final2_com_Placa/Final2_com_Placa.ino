#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Endereço I2C da PCA9685 (padrão é 0x40)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Definir o intervalo de pulsos para o servo (ajustar conforme o seu servo)
#define SERVO_MIN  150 // Pulso mínimo (ângulo 0°)
#define SERVO_MAX  600 // Pulso máximo (ângulo 180°)

// Definir os canais da PCA9685 para cada servo
int servo1Channel = 15;  // Canal do servo 1
int servo2Channel = 14;  // Canal do servo 2
int servo3Channel = 13;  // Canal do servo 3
int servo4Channel = 12;  // Canal do servo 4
int servo5Channel = 11;  // Canal do servo 5 (novo servo)

int servo1Angle = 0;  // Ângulo inicial do servo 1
int servo2Angle = 0;  // Ângulo inicial do servo 2
int servo3Angle = 0;  // Ângulo inicial do servo 3
int servo4Angle = 0;  // Ângulo inicial do servo 4
int servo5Angle = 0;  // Ângulo inicial do servo 5

void setup() {
  Serial.begin(9600);  // Inicializa a comunicação serial
  pwm.begin();
  pwm.setPWMFreq(60);  // Configura a frequência para 60 Hz, ideal para servos
  
  Serial.println("Insira um identificador de servo (1-5) seguido de um valor entre 0 e 180 para mover o servo:");
  Serial.println("Para o servo 5, insira 90 para fechado e 180 para aberto.");
}

// Função para converter o ângulo em valor de pulso
int angleToPulse(int angle, int servoID) {
  // Inverter o mapeamento de pulsos para o Servo 3
  if (servoID == 3) {
    return map(angle, 0, 180, SERVO_MAX, SERVO_MIN);  // Mapeamento invertido
  } else {
    return map(angle, 0, 180, SERVO_MIN, SERVO_MAX);  // Mapeamento normal
  }
}

void loop() {
  // Verifica se há dados disponíveis na porta serial
  if (Serial.available() > 0) {
    int servoID = Serial.parseInt();  // Primeiro valor: identificador do servo (1-5)
    int inputValue = Serial.parseInt();  // Segundo valor: ângulo do servo (0-180)
    
    // Verifica se o identificador do servo está entre 1 e 5
    if ((servoID >= 1 && servoID <= 5)) {
      int pulse = angleToPulse(inputValue, servoID);  // Converte o ângulo em pulso
      
      switch (servoID) {
        case 1:
          if (inputValue >= 0 && inputValue <= 180 && inputValue != servo1Angle) {
            servo1Angle = inputValue;
            pwm.setPWM(servo1Channel, 0, pulse);
            Serial.print("Servo 1 movido para: ");
            Serial.println(servo1Angle);
          } else {
            Serial.println("Insira um ângulo válido entre 0 e 180.");
          }
          break;

        case 2:
          if (inputValue >= 0 && inputValue <= 180 && inputValue != servo2Angle) {
            servo2Angle = inputValue;
            pwm.setPWM(servo2Channel, 0, pulse);
            Serial.print("Servo 2 movido para: ");
            Serial.println(servo2Angle);
          } else {
            Serial.println("Insira um ângulo válido entre 0 e 180.");
          }
          break;

        case 3:
          if (inputValue >= 0 && inputValue <= 180 && inputValue != servo3Angle) {
            servo3Angle = inputValue;
            pwm.setPWM(servo3Channel, 0, pulse);
            Serial.print("Servo 3 movido para: ");
            Serial.println(servo3Angle);
          } else {
            Serial.println("Insira um ângulo válido entre 0 e 180.");
          }
          break;

        case 4:
          if (inputValue >= 0 && inputValue <= 180 && inputValue != servo4Angle) {
            servo4Angle = inputValue;
            pwm.setPWM(servo4Channel, 0, pulse);
            Serial.print("Servo 4 movido para: ");
            Serial.println(servo4Angle);
          } else {
            Serial.println("Insira um ângulo válido entre 0 e 180.");
          }
          break;

        case 5:
          // Condições especiais para o servo 5: apenas 90 (fechado) e 180 (aberto)
          if ((inputValue == 90 || inputValue == 180) && inputValue != servo5Angle) {
            servo5Angle = inputValue;
            pwm.setPWM(servo5Channel, 0, pulse);
            Serial.print("Servo 5 movido para: ");
            Serial.println(servo5Angle == 90 ? "Fechado (90)" : "Aberto (180)");
          } else {
            Serial.println("Para o servo 5, insira 90 para fechado ou 180 para aberto.");
          }
          break;
      }
    } else {
      Serial.println("Insira um identificador de servo válido (1-5).");
    }
  }
}
