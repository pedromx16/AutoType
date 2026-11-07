import customtkinter as ctk
import keyboard
import threading
import time


class AutoType:

    def __init__(self, janela):
        self.janela = janela

        self.janela.title("AutoType")
        self.janela.geometry("600x500")
        self.janela.resizable(False, False)

        self.parar = threading.Event()
        self.executando = False

        # Título
        self.titulo = ctk.CTkLabel(
            janela,
            text="AutoType",
            font=("Arial", 30, "bold")
        )
        self.titulo.pack(pady=(20, 5))

        self.subtitulo = ctk.CTkLabel(
            janela,
            text="Automatização inteligente de digitação",
            text_color="gray"
        )
        self.subtitulo.pack(pady=5)

        # Campo de texto
        self.texto = ctk.CTkTextbox(
            janela,
            width=520,
            height=190,
            font=("Arial", 15)
        )
        self.texto.pack(pady=20)

        self.texto.insert(
            "1.0",
            "Olá! Este texto está sendo digitado automaticamente."
        )

        # Velocidade
        self.velocidade_label = ctk.CTkLabel(
            janela,
            text="Intervalo: 50 ms por caractere"
        )
        self.velocidade_label.pack()

        self.velocidade = ctk.CTkSlider(
            janela,
            from_=0.01,
            to=0.20,
            number_of_steps=19,
            command=self.atualizar_velocidade
        )
        self.velocidade.set(0.05)
        self.velocidade.pack(pady=10)

        # Status
        self.status = ctk.CTkLabel(
            janela,
            text="Aguardando comando...",
            text_color="gray"
        )
        self.status.pack(pady=10)

        # Botões
        self.botao_iniciar = ctk.CTkButton(
            janela,
            text="INICIAR DIGITAÇÃO",
            command=self.iniciar,
            height=40,
            fg_color="#16834B",
            hover_color="#106638"
        )
        self.botao_iniciar.pack(pady=8)

        self.botao_parar = ctk.CTkButton(
            janela,
            text="PARAR",
            command=self.parar_digitacao,
            height=35,
            fg_color="#B83232",
            hover_color="#872323"
        )
        self.botao_parar.pack(pady=5)

        self.hotkey = keyboard.add_hotkey(
            "esc",
            lambda: self.janela.after(0, self.parar_digitacao)
        )

        self.janela.protocol("WM_DELETE_WINDOW", self.fechar)

    def atualizar_velocidade(self, valor):
        ms = int(valor * 1000)
        self.velocidade_label.configure(
            text=f"Intervalo: {ms} ms por caractere"
        )

    def iniciar(self):

        if self.executando:
            return

        texto = self.texto.get("1.0", "end-1c")

        if not texto.strip():
            self.status.configure(
                text="Digite algum texto primeiro!",
                text_color="orange"
            )
            return

        intervalo = self.velocidade.get()

        self.parar.clear()
        self.executando = True
        self.botao_iniciar.configure(state="disabled")

        threading.Thread(
            target=self.digitar,
            args=(texto, intervalo),
            daemon=True
        ).start()

    def digitar(self, texto, intervalo):

        for segundos in range(5, 0, -1):

            if self.parar.is_set():
                break

            self.janela.after(
                0,
                lambda s=segundos: self.status.configure(
                    text=f"Começando em {s} segundos..."
                )
            )

            if self.parar.wait(1):
                break

        if not self.parar.is_set():

            self.janela.after(
                0,
                lambda: self.status.configure(
                    text="Digitando...",
                    text_color="#16834B"
                )
            )

            for caractere in texto:

                if self.parar.is_set():
                    break

                keyboard.write(caractere)

                if self.parar.wait(intervalo):
                    break

        self.janela.after(0, self.finalizar)

    def parar_digitacao(self):
        self.parar.set()
        self.status.configure(
            text="Parando digitação...",
            text_color="orange"
        )

    def finalizar(self):
        self.executando = False
        self.botao_iniciar.configure(state="normal")

        if self.parar.is_set():
            mensagem = "Digitação interrompida."
        else:
            mensagem = "Digitação concluída!"

        self.status.configure(text=mensagem)

    def fechar(self):
        self.parar.set()

        try:
            keyboard.remove_hotkey(self.hotkey)
        except Exception:
            pass

        self.janela.destroy()


# Inicialização do aplicativo

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
app = AutoType(janela)

janela.mainloop()