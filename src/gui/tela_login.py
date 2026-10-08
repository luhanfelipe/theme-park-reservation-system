import customtkinter as ctk

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, on_login_sucesso):
        super().__init__(master)
        
        # Guardamos a função que vai liberar o sistema
        self.on_login_sucesso = on_login_sucesso 

        # Cria um frame menor no centro da tela para ficar com visual de "cartão" de login
        self.frame_login = ctk.CTkFrame(self, corner_radius=15)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_titulo = ctk.CTkLabel(self.frame_login, text="Login do Sistema", font=("Arial", 24, "bold"))
        self.lbl_titulo.pack(pady=(30, 20), padx=40)

        # Campos de texto
        self.entry_usuario = ctk.CTkEntry(self.frame_login, placeholder_text="Usuário", width=250)
        self.entry_usuario.pack(pady=10, padx=40)

        # O parâmetro show="*" transforma o texto em bolinhas de senha!
        self.entry_senha = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", width=250, show="*")
        self.entry_senha.pack(pady=10, padx=40)

        self.btn_entrar = ctk.CTkButton(self.frame_login, text="Entrar", command=self.fazer_login, width=250)
        self.btn_entrar.pack(pady=(20, 10), padx=40)

        self.lbl_mensagem = ctk.CTkLabel(self.frame_login, text="", text_color="red")
        self.lbl_mensagem.pack(pady=(0, 20))

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # Validando com um usuário fixo de testes
        if usuario == "admin" and senha == "1234":
            self.lbl_mensagem.configure(text="Acesso liberado! Entrando...", text_color="green")
            # Usa o método after para esperar meio segundo (500ms) antes de mudar de tela
            self.after(500, self.on_login_sucesso)
        else:
            self.lbl_mensagem.configure(text="Usuário ou senha incorretos!", text_color="red")