/*
*/

float Er[2] = {0.0, 0.0}; // variável para o dado recebido
float Ec = 0.0;

void setup() {
  Serial.begin(9600); // abre a porta serial, configura a taxa de transferência para 9600 bps
  Serial.println(valueToSend, 8);
}

void loop() {
  while (Serial.available() == 0) {
    // Enquanto não tiver resposta disponível não faz nada
  }
  Er[1] = Er[0];
  Er[0] = Serial.parseFloat(); // lê do buffer o dado recebido e já transforma em float    
  
  // Calcula o valor controlado, o esforço do controlador
  Ec = Er[0]*58.17-45.57*Er[1]-Ec;  

  // Retorna o valor para a planta
  Serial.println(Ec, 8);
}
