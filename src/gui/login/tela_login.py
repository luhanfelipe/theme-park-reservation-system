import customtkinter as ctk


class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, servico, on_login_sucesso, on_ir_para_cadastro):
        super().__init__(master)

        self.servico = servico
        self.on_login_sucesso = on_login_sucesso
        self.on_ir_para_cadastro = on_ir_para_cadastro

        # Cores
        COR_BOTAO_ROXO = "#6C63FF"
        COR_HOVER_ROXO = "#5A52D5"

        # Frame central com visual de cartão
        self.frame_login = ctk.CTkFrame(self, corner_radius=15)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_login,
            text="Login do Sistema",
            font=("Arial", 24, "bold")
        )
        self.lbl_titulo.pack(pady=(30, 20), padx=40)

        # Abas Visitante / Admin
        self.tabs = ctk.CTkTabview(self.frame_login, width=320, height=280)
        self.tabs.pack(pady=(0, 20), padx=30)
        self.tabs.add("Visitante")
        self.tabs.add("Admin")

        self._montar_aba_visitante()
        self._montar_aba_admin()

    # ------------------------------------------------------------------
    # ABA VISITANTE
    # ------------------------------------------------------------------
    def _montar_aba_visitante(self):
        COR_BOTAO_ROXO = "#6C63FF"
        COR_HOVER_ROXO = "#5A52D5"

        aba = self.tabs.tab("Visitante")

        self.entry_cpf = ctk.CTkEntry(aba, placeholder_text="CPF (000.000.000-00)", width=260)
        self.entry_cpf.pack(pady=(20, 10))

        self.entry_senha_visitante = ctk.CTkEntry(aba, placeholder_text="Senha", width=260, show="*")
        self.entry_senha_visitante.pack(pady=10)

        self.btn_entrar_visitante = ctk.CTkButton(
            aba,
            text="Entrar",
            width=260,
            fg_color=COR_BOTAO_ROXO,
            hover_color=COR_HOVER_ROXO,
            command=self.fazer_login_visitante
        )
        self.btn_entrar_visitante.pack(pady=(15, 10))

        self.btn_cadastrar = ctk.CTkButton(
            aba,
            text="Não tem conta? Cadastre-se",
            width=260,
            fg_color="transparent",
            hover_color="#2A2D3E",
            text_color="#A0A0A0",
            command=self.on_ir_para_cadastro
        )
        self.btn_cadastrar.pack(pady=(0, 10))

        self.lbl_msg_visitante = ctk.CTkLabel(aba, text="", text_color="red")
        self.lbl_msg_visitante.pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # ABA ADMIN
    # ------------------------------------------------------------------
    def _montar_aba_admin(self):
        COR_BOTAO_ROXO = "#6C63FF"
        COR_HOVER_ROXO = "#5A52D5"

        aba = self.tabs.tab("Admin")

        self.entry_admin_usuario = ctk.CTkEntry(aba, placeholder_text="Usuário", width=260)
        self.entry_admin_usuario.pack(pady=(20, 10))

        self.entry_admin_senha = ctk.CTkEntry(aba, placeholder_text="Senha", width=260, show="*")
        self.entry_admin_senha.pack(pady=10)

        self.btn_entrar_admin = ctk.CTkButton(
            aba,
            text="Entrar como Admin",
            width=260,
            fg_color=COR_BOTAO_ROXO,
            hover_color=COR_HOVER_ROXO,
            command=self.fazer_login_admin
        )
        self.btn_entrar_admin.pack(pady=(15, 10))

        self.lbl_msg_admin = ctk.CTkLabel(aba, text="", text_color="red")
        self.lbl_msg_admin.pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # LOGIN VISITANTE
    # ------------------------------------------------------------------
    def fazer_login_visitante(self):
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha_visitante.get()

        if not cpf or not senha:
            self.lbl_msg_visitante.configure(text="Preencha CPF e senha!", text_color="red")
            return

        visitante = self.servico.autenticar_visitante(cpf, senha)

        if visitante is None:
            self.lbl_msg_visitante.configure(text="CPF ou senha incorretos!", text_color="red")
            return

        self.lbl_msg_visitante.configure(text="Acesso liberado! Entrando...", text_color="green")
        self.after(500, lambda: self.on_login_sucesso(perfil="visitante", cpf=visitante.cpf))

    # ------------------------------------------------------------------
    # LOGIN ADMIN
    # ------------------------------------------------------------------
    def fazer_login_admin(self):
        usuario = self.entry_admin_usuario.get().strip()
        senha = self.entry_admin_senha.get()

        if not usuario or not senha:
            self.lbl_msg_admin.configure(text="Preencha usuário e senha!", text_color="red")
            return

        if not self.servico.autenticar_admin(usuario, senha):
            self.lbl_msg_admin.configure(text="Usuário ou senha incorretos!", text_color="red")
            return

        self.lbl_msg_admin.configure(text="Acesso liberado! Entrando...", text_color="green")
        self.after(500, lambda: self.on_login_sucesso(perfil="admin", cpf=None))
