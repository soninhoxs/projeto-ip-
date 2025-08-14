# Projeto IP - equipe 1
# Introduçao

- Este é um mini-jogo de plataforma desenvolvido em Pygame, inspirado na clássica animação "Tá Chovendo Hambúrguer". Nele, você pode escolher entre o inventor Flint Lockwood 👨‍🔬 e seu fiel companheiro, o Macaco Steve 🐒, para enfrentar uma chuva de comidas e perigos.
O jogo é dividido em duas fases distintas, cada uma com seus próprios desafios e objetivos.

## **As Fases do Jogo**
- **Fase 1: A Chuva de Hambúrgueres**

Na primeira fase, seu objetivo é sobreviver à chuva de alimentos enquanto coleta 15 hambúrgueres 🍔 para avançar. No entanto, o céu não está apenas para delícias
Bombas 💣 Evite-as a todo custo ou você perderá uma vida.
Cachorros-Quentes Mofados 🌭 Tocar neles não tira vida, mas deixa seu personagem mais lento por alguns segundos, tornando mais difícil desviar dos perigos.

- **Fase 2: Invasão dos Donuts**

Após provar seu valor, você avança para a Fase 2, onde o desafio aumenta drasticamente. A frequência de bombas é muito maior e o objetivo agora é coletar 10 donuts 🍩 para zerar o jogo. Seus reflexos serão testados ao máximo para desviar dos explosivos e pegar os doces.

# Tecnologia utilizadas:
- Python 3.13.3

# Funcionalidades desenvolvidas
- 🎯 Menu inicial com opções de jogar e instruções.
- 📜 Tela de instruções explicando regras e controles.
- 🧍 Seleção de personagem antes de iniciar a partida.
- 🕹 Duas fases jogáveis com objetivos e desafios diferentes.
- 🍔 Coleta de itens bons para ganhar pontos.
- 💣 Desvio de itens ruins para não perder vidas ou pontos.
- 🏆 Sistema de pontuação em tempo real.
- ❤️ Contagem de vidas do jogador.
- 🌀 Efeitos especiais como pulo e lentidão temporária.
- 🔚 Condições de vitória e derrota com tela de game over.

# Bibliotecas utilizadas:

- pygame: Para criação da interface gráfica, controle de eventos e manipulação de imagens/sons.

- random: Para geração de valores aleatórios usados no comportamento do jogo, como a posição e a velocidade dos itens que caem.

- os: Para manipulação de caminhos de arquivos do sistema operacional, garantindo que o jogo encontre as imagens e fontes independentemente de onde for executado (os.path.join).


# Instalação

Siga os passos abaixo para rodar o projeto localmente.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/soninhoxs/projeto-ip-.git](https://github.com/soninhoxs/projeto-ip-.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd projeto-ip-
    ```

3.  **Crie e ative o Ambiente Virtual (Recomendado):**
    Isso cria um ambiente isolado para as dependências do projeto, evitando conflitos.

   - **No Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

   - **No Mac/Linux:**
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```
4.  **Instale as dependências:**
    Com o ambiente virtual ativado, instale o Pygame:
    ```bash
    pip install pygame
    ```

5.  **Execute o jogo:**
    O script principal está dentro da pasta `codigo_jogo`.
    ```bash
    cd codigo_jogo
    python main.py
    ```

### Desativando o Ambiente Virtual

Quando terminar de jogar, você pode desativar o ambiente virtual com o simples comando:
```bash
deactivate
```

# 🎬 Tela Inicial 
![TELA INICIAL](/sprt/tela_inicial.png)

# 🌧️🍔 Instruçao 
![TELA INICIAL](/sprt/instrucoes.png)

# 🤖💥 Cenarios
![TELA INICIAL](sprt/tela_fase1.jpg)
![TELA INICIAL](sprt/tela_fase2.jpg)
![TELA INICIAL](sprt/escolhapersonagens.png)

# 🍕🎉 Vitoria
![TELA INICIAL](/sprt/fim_jogo.png)

# 😞🍔 Derrota
![TELA INICIAL](sprt/tela_perdeu.png)

# Membros da equipe:
- Carlos Vinicius Felix da Silva ***cvfs***
- Efraim Santana Bispo da Silva ***esbs***
- Joyce Gabriele da Silva Pereira ***jgsp3***
- João Gustavo Guimaraes Pires ***jggp***
- João Henrique dos Santos Silva ***jhss2***
- Lucas David Lima Ferreira ***ldlf***

# Divisao de tarefas do grupo
- visual: Carlos | Joyce
- código: Efraim | Joao Gustavo | Joao Henrique
- organização geral: Joao Henrique | Lucas David
- slides e relatório: Joao Henrique | Lucas David

