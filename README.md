# Branch and Bound com PuLP

Este projeto implementa um algoritmo de Branch and Bound para problemas de programação inteira binária, utilizando a biblioteca PuLP para resolver as relaxações lineares. O programa lê um arquivo de entrada com a definição do problema, resolve a versão relaxada (com variáveis contínuas entre 0 e 1), identifica se a solução é inteira e, se não for, realiza ramificações sobre a variável mais fracionária até encontrar a melhor solução viável.

O arquivo de entrada deve ter o seguinte formato:

<num_variaveis> 
<num_restricoes>
<c1 c2 c3 ... cn>
<a11 a12 ... a1n> <b1>
<a21 a22 ... a2n> <b2>
...

Exemplo:

## 3 2            # número de variáveis e número de restrições
## 3 2 1          # função objetivo: max 3x0 + 2x1 + 1x2
## 1 2 3 4        # restrição 1: 1x0 + 2x1 + 3x2 <= 4
## 2 2 1 3        # restrição 2: 2x0 + 2x1 + 1x2 <= 3
Neste exemplo, queremos maximizar 3x0 + 2x1 + 1x2, sujeito a duas restrições, com variáveis binárias x0, x1, x2 ∈ {0,1}.

Para executar o projeto, é necessário ter Python instalado. Recomenda-se o uso de ambiente virtual (venv) para isolar as dependências. Para isso, abra o terminal no diretório do projeto e execute o comando:

python -m venv venv

Em seguida, ative o ambiente:

No Windows (CMD): venv\Scripts\activate  
No Windows (PowerShell): .\venv\Scripts\Activate.ps1  
No Linux/macOS: source venv/bin/activate

Com o ambiente ativado, instale a biblioteca necessária:

pip install pulp

Você pode salvar os pacotes utilizados com:

pip freeze > requirements.txt

E restaurar em outro ambiente com:

pip install -r requirements.txt

Para rodar o programa, use o comando:

python main.py caminho/do/arquivo.txt

Exemplo:

python main.py exemplo.txt

Se houver uma solução viável, o programa imprimirá o melhor valor da função objetivo e a solução binária correspondente, como por exemplo:

Melhor valor encontrado: 7.0  
Solução: [1.0, 1.0, 0.0]

Esse valor é a melhor solução inteira encontrada com base na técnica de branch and bound. O algoritmo resolve a relaxação linear do problema, verifica se a solução é inteira e, caso não seja, escolhe a variável mais próxima de 0.5 para ramificar. Ele tenta os dois ramos (forçando a variável a 0 e a 1) e repete o processo recursivamente, guardando a melhor solução inteira encontrada.

Este projeto utiliza Python 3.7+ e a biblioteca PuLP. Para dúvidas, sugestões ou contribuições, abra uma issue ou pull request. O projeto está sob licença MIT.
