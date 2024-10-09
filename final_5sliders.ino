#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Endereço I2C da PCA9685 (padrão é 0x40)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Definir o intervalo de pulsos para os servos
#define SERVO_MIN  150  // Pulso mínimo (ângulo 0°)
#define SERVO_MAX  600  // Pulso máximo (ângulo 180°)

// Definir os canais da PCA9685 para cada servo
int servo1Channel = 15;  // Canal do servo 1
int servo2Channel = 14;  // Canal do servo 2
int servo3Channel = 13;  // Canal do servo 3
int servo4Channel = 12;  // Canal do servo 4
int servo5Channel = 11;  // Canal do servo 5 (garra)

int servo1Angle = 0;  // Ângulo inicial do servo 1
int servo2Angle = 0;  // Ângulo inicial do servo 2
int servo3Angle = 0;  // Ângulo inicial do servo 3
int servo4Angle = 0;  // Ângulo inicial do servo 4
int servo5Angle = 0;  // Ângulo inicial do servo 5

void setup() {
  Serial.begin(9600);  // Inicializa a comunicação serial
  pwm.begin();
  pwm.setPWMFreq(60);  // Configura a frequência para 60 Hz, ideal para servos
  
  Serial.println("Insira um identificador de servo (1-5) seguido de um valor para mover o servo:");
  Serial.println("Para o servo 5, insira um valor entre 0 e 90.");
  Serial.println("Para os outros servos, insira um valor entre 0 e 180.");
}

// Função para converter o ângulo em valor de pulso
int angleToPulse(int angle, int servoID) {
  // Mapeia o ângulo de acordo com o servoID
  if (servoID == 5) {
    return map(angle, 0, 90, SERVO_MIN, 600);  // 0-90 para o servo 5
  } else if(servoID == 3) {
    return map(angle, 0, 180, SERVO_MAX, SERVO_MIN);  // Mapeamento invertido
  }
  else {
    return map(angle, 0, 180, SERVO_MIN, SERVO_MAX);  // 0-180 para os outros servos
  }
}

void loop() {
  // Verifica se há dados disponíveis na porta serial
  if (Serial.available() > 0) {
    int servoID = Serial.parseInt();  // Primeiro valor: identificador do servo (1-5)
    int inputValue = Serial.parseInt();  // Segundo valor: ângulo do servo
    
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
          if (inputValue >= 0 && inputValue <= 90 && inputValue != servo5Angle) {
            servo5Angle = inputValue;
            pwm.setPWM(servo5Channel, 0, pulse);
            Serial.print("Garra movida para: ");
            Serial.println(servo5Angle);
          } else {
            Serial.println("Para o servo 5, insira um ângulo válido entre 0 e 90.");
          }
          break;
      }
    } else {
      Serial.println("Insira um identificador de servo válido (1-5).");
    }
  }
}
