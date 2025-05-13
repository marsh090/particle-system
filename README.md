# Particle Simulation

**Versão:** 0.1.0

Um simulador de partículas feito em Python, utilizando pygame, numpy, pillow e pydantic.

## Como rodar o simulador

### Pré-requisitos

- Python 3.11.x
- [Poetry](https://python-poetry.org/)

### Instalação das dependências

```bash
cd app
poetry install
```

---

## Como gerar o executável

### Para Linux

1. Gere o executável:
    ```bash
    poetry run python build.py
    ```
2. O executável estará em `app/dist/particle_simulation`.
3. Torne-o executável (se necessário):
    ```bash
    chmod +x dist/particle_simulation
    ```
4. (Opcional) Crie um atalho no menu do sistema:
    - Use o arquivo `app/particle_simulation.desktop` já pronto.
    - Para adicionar ao menu:
      ```bash
      cp app/particle_simulation.desktop ~/.local/share/applications/
      ```

### Para Windows

1. Clone o projeto em um computador com Windows.
2. Instale Python 3.11.x e Poetry.
3. No terminal:
    ```bash
    cd app
    poetry install
    poetry run python build.py
    ```
4. O executável estará em `app/dist/particle_simulation.exe`.

---

## Observações

- O executável é standalone, não precisa de Python instalado na máquina de destino.
- O ícone do app aparece automaticamente no Windows. No Linux, use o arquivo `.desktop` para o atalho com ícone.
- Para personalizar o ícone, basta trocar o arquivo `app/assets/icon.png` (Linux) ou adicionar `icon.ico` (Windows).

---

## Sobre

Projeto criado por **Lucas Zanon**.

Sinta-se à vontade para fazer fork do projeto e sugerir suas próprias modificações! 
