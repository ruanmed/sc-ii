float Er[2] = {0.0, 0.0}; // variável para o dado recebido
float Ec = 0.0;
void setup() {
  Serial.begin(9600); // abre a porta serial, configura a taxa de transferência para 9600 bps
  Serial.println(Ec);//Enviando esforço do controlador para a planta
}

void loop() {
  while (Serial.available() == 0) {
    // Enquanto não tiver resposta disponível não faz nada
  }
  Er[1] = Er[0];
  Er[0] = (1 -Serial.parseFloat()); // lê do buffer o dado recebido e já transforma em float    
  
  // Calcula o valor controlado, o esforço do controlador
  Ec = 867.3*Er[0]-767.1*Er[1]+0.4859*Ec; 
  //Ec = abs(Ec);

  // Retorna o valor para a planta
  Serial.println(Ec);
}
