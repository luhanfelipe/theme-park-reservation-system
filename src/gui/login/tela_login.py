import customtkinter as ctk
from src.utils.formatadores import formatar_cpf
from src.gui.componentes.tema import (
    COR_BOTAO, COR_BOTAO_HOVER, COR_FUNDO_APP,
    COR_ERRO, COR_SUCESSO, carregar_fundo,
)


class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, servico, on_login_sucesso, on_ir_para_cadastro):
        super().__init__(master)

        self.servico = servico
        self.on_login_sucesso = on_login_sucesso
        self.on_ir_para_cadastro = on_ir_para_cadastro

        # --- Imagem de fundo ---
        self._fundo_img = carregar_fundo((1100, 650))
        if self._fundo_img is not None:
            self._label_fundo = ctk.CTkLabel(self, image=self._fundo_img, text="")
            self._label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Frame central com visual de cartão ---
        self.frame_login = ctk.CTkFrame(self, corner_radius=15, fg_color=COR_FUNDO_APP)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_login,
            text="Bem-Vindo(a)",
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
        aba = self.tabs.tab("Visitante")

        self.entry_cpf = ctk.CTkEntry(aba, placeholder_text="CPF (000.000.000-00)", width=260)
        self.entry_cpf.pack(pady=(20, 10))
        self.entry_cpf.bind("<KeyRelease>", self._limitar_cpf_login)
        self.entry_cpf.bind("<FocusOut>", self._formatar_cpf_login)

        self.entry_senha_visitante = ctk.CTkEntry(aba, placeholder_text="Senha", width=260, show="*")
        self.entry_senha_visitante.pack(pady=10)

        self.btn_entrar_visitante = ctk.CTkButton(
            aba,
            text="Entrar",
            width=260,
            fg_color=COR_BOTAO,
            hover_color=COR_BOTAO_HOVER,
            command=self.fazer_login_visitante
        )
        self.btn_entrar_visitante.pack(pady=(15, 10))

        self.btn_cadastrar = ctk.CTkButton(
            aba,
            text="Não tem conta? Cadastre-se",
            width=260,
            fg_color="transparent",
            hover_color="#2A1F18",
            text_color="#C4B5A8",
            command=self.on_ir_para_cadastro
        )
        self.btn_cadastrar.pack(pady=(0, 10))

        self.lbl_msg_visitante = ctk.CTkLabel(
            aba, text="",
            text_color=COR_ERRO,
            fg_color="transparent"
        )
        self.lbl_msg_visitante.pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # ABA ADMIN
    # ------------------------------------------------------------------
    def _montar_aba_admin(self):
        aba = self.tabs.tab("Admin")

        self.entry_admin_usuario = ctk.CTkEntry(aba, placeholder_text="Usuário", width=260)
        self.entry_admin_usuario.pack(pady=(20, 10))

        self.entry_admin_senha = ctk.CTkEntry(aba, placeholder_text="Senha", width=260, show="*")
        self.entry_admin_senha.pack(pady=10)

        self.btn_entrar_admin = ctk.CTkButton(
            aba,
            text="Entrar como Admin",
            width=260,
            fg_color=COR_BOTAO,
            hover_color=COR_BOTAO_HOVER,
            command=self.fazer_login_admin
        )
        self.btn_entrar_admin.pack(pady=(15, 10))

        self.lbl_msg_admin = ctk.CTkLabel(
            aba, text="",
            text_color=COR_ERRO,
            fg_color="transparent"
        )
        self.lbl_msg_admin.pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # FORMATAÇÃO E LIMITAÇÃO DE CPF
    # ------------------------------------------------------------------
    def _limitar_cpf_login(self, event=None):
        """Impede que o campo CPF passe de 11 dígitos enquanto digita."""
        texto = self.entry_cpf.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if len(apenas_numeros) > 11:
            apenas_numeros = apenas_numeros[:11]
        if texto != apenas_numeros:
            self.entry_cpf.delete(0, "end")
            self.entry_cpf.insert(0, apenas_numeros)

    def _formatar_cpf_login(self, event=None):
        """Formata o CPF ao sair do campo (perde foco)."""
        texto_atual = self.entry_cpf.get()
        formatado = formatar_cpf(texto_atual)
        if formatado != texto_atual:
            self.entry_cpf.delete(0, "end")
            self.entry_cpf.insert(0, formatado)

    # ------------------------------------------------------------------
    # LOGIN VISITANTE
    # ------------------------------------------------------------------
    def fazer_login_visitante(self):
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha_visitante.get()

        if not cpf or not senha:
            self.lbl_msg_visitante.configure(text="Preencha CPF e senha!", text_color=COR_ERRO)
            return

        visitante = self.servico.autenticar_visitante(cpf, senha)

        if visitante is None:
            self.lbl_msg_visitante.configure(text="CPF ou senha incorretos!", text_color=COR_ERRO)
            return

        self.lbl_msg_visitante.configure(text="Acesso liberado! Entrando...", text_color=COR_SUCESSO)
        self.after(500, lambda: self.on_login_sucesso(perfil="visitante", cpf=visitante.cpf))

    # ------------------------------------------------------------------
    # LOGIN ADMIN
    # ------------------------------------------------------------------
    def fazer_login_admin(self):
        usuario = self.entry_admin_usuario.get().strip()
        senha = self.entry_admin_senha.get()

        if not usuario or not senha:
            self.lbl_msg_admin.configure(text="Preencha usuário e senha!", text_color=COR_ERRO)
            return

        if not self.servico.autenticar_admin(usuario, senha):
            self.lbl_msg_admin.configure(text="Usuário ou senha incorretos!", text_color=COR_ERRO)
            return

        self.lbl_msg_admin.configure(text="Acesso liberado! Entrando...", text_color=COR_SUCESSO)
        self.after(500, lambda: self.on_login_sucesso(perfil="admin", cpf=None))
