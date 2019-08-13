// Código supersônico para simular um controlador no Arduino das Galáxias

String inString = "";    // string to hold input
String inString1 = "";    // string to hold input1

double Er[2] = {0.0, 0.0}; // variável para o dado recebido,
double Ec = 0.0;           // colocamos double mas no Arduino UNO tem a mesma precisão de um float
double gain= 1000;

double Er1[2] = {0.0, 0.0}; // variável para o dado recebido,
double Ec1 = 0.0;           // colocamos double mas no Arduino UNO tem a mesma precisão de um float
double gain1= 2459.85;

int alternate = 0;

void setup() {
  Serial.begin(250000); // abre a porta serial, configura a taxa de transferência para 9600 bps
  Serial.print(Ec,16);//Enviando esforço do controlador para a planta
  Serial.print(' ');
  Serial.println(Ec1,16);
}

void loop() {
  while (Serial.available() == 0) {
    // Enquanto não tiver resposta disponível não faz nada
  }
  // Começa a ler o valor enviado
  int inChar = Serial.read();

  if (inChar != '\n') { // Se não for uma nova linha, então converte o byte para um caracter e adiciona na string
    if (inChar == ' ') {
      alternate = 1;
    }
    else if (alternate == 1) {
      inString1 += (char)inChar;
    } 
    else {
      inString += (char)inChar;
    }
  } 
  else { // se for uma nova linha, então vamos converter para float de fato, e fazer os cálculos
    Er[1] = Er[0];
    Er[0] = (inString.toFloat()); // transforma em float

    Er1[1] = Er1[0];
    Er1[0] = (inString1.toFloat()); // transforma em float
    
    // Calcula o valor controlado, o esforço do controlador
    Ec = gain*(0.7885*Er[0]-0.6974*Er[1])+0.4859*Ec; 
    Ec1 = gain1*(0.7885*Er1[0]-0.6974*Er1[1])+0.4859*Ec1; // Com o segundo ganho
    //Ec = abs(Ec);

    // Retorna o valor para a planta no formato "##.## ##.##/n"
    Serial.print(Ec,16);
    Serial.print(' ');
    Serial.println(Ec1,16);
    inString = ""; // limpa a string de leitura
    inString1 = ""; 

    alternate = 0;
  }
}
