// Código supersônico para simular um controlador no Arduino das Galáxias

String inString = "";    // string to hold input

double Er[2] = {0.0, 0.0}; // variável para o dado recebido,
double Ec = 0.0;           // colocamos double mas no Arduino UNO tem a mesma precisão de um float

void setup() {
  Serial.begin(9600); // abre a porta serial, configura a taxa de transferência para 9600 bps
  Serial.println(Ec,16);//Enviando esforço do controlador para a planta
}

void loop() {
  while (Serial.available() == 0) {
    // Enquanto não tiver resposta disponível não faz nada
  }
  // Começa a ler o valor enviado
  int inChar = Serial.read();

  if (inChar != '\n') {
    // Se não for uma nova linha, então converte o byte para um caracter e adiciona na string
    inString += (char)inChar;
  }     
  else { // se for uma nova linha, então vamos converter para float de fato, e fazer os cálculos
    Er[1] = Er[0];
    Er[0] = (1 -inString.toFloat()); // transforma em float    
    
    // Calcula o valor controlado, o esforço do controlador
    Ec = 867.3*Er[0]-767.1*Er[1]+0.4859*Ec; 
    //Ec = abs(Ec);

    // Retorna o valor para a planta
    Serial.println(Ec,16);
    inString = ""; // limpa a string de leitura
  }
}
