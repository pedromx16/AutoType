# AutoType

**AutoType** é um aplicativo de automação de digitação desenvolvido em Python, com interface gráfica moderna e controles personalizáveis.

## Funcionalidades

- Digitação automática de textos.
- Controle de velocidade.
- Temporizador para início da digitação.
- Interrupção utilizando a tecla ESC.
- Interface gráfica com CustomTkinter.

## Tecnologias utilizadas

- Python
- CustomTkinter
- Keyboard
- PyInstaller

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/AutoType.git
cd AutoType
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python main.py
```

## Compilação

Para gerar o executável:

```bash
pyinstaller --noconfirm --clean --onefile --windowed --collect-all customtkinter --name AutoType main.py
```

## Licença

Projeto desenvolvido para fins educacionais e de portfólio.