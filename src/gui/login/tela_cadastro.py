import customtkinter as ctk
from src.utils.formatadores import formatar_cpf
from src.gui.componentes.tema import (
    COR_FUNDO_APP, COR_CARD, COR_INPUT, COR_TEXTO, COR_TEXTO_SEC,
    COR_BOTAO, COR_BOTAO_HOVER, COR_BORDA_NEON,
    COR_SUCESSO, COR_ERRO,
)


class TelaCadastro(ctk.CTkScrollableFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master, fg_color=COR_FUNDO_APP)

        self._scrollbar.grid_forget()
        self.servico = servico

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self,
            text="⬅ Voltar ao Login",
            width=120,
            height=32,
            fg_color="transparent",
            border_width=1,
            border_color=COR_BORDA_NEON,
            hover_color=COR_CARD,
            text_color=COR_TEXTO,
            command=comando_voltar
        )
        self.btn_voltar.pack(anchor="nw", padx=20, pady=(20, 0))

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="👤 Criar Nova Conta",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COR_TEXTO
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # --- FORMULÁRIO ---
        self.frame_form = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color=COR_CARD,
            border_width=1,
            border_color=COR_BORDA_NEON
        )
        self.frame_form.pack(pady=10, padx=20, anchor="center")

        # --- LINHA 0: Nome e Idade ---
        self.lbl_nome = ctk.CTkLabel(self.frame_form, text="Nome do Visitante:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_nome.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 2))
        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: Maria Silva", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_nome.grid(row=1, column=0, padx=15, pady=(0, 10))

        self.lbl_idade = ctk.CTkLabel(self.frame_form, text="Idade:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_idade.grid(row=0, column=1, sticky="w", padx=15, pady=(12, 2))
        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 25", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_idade.grid(row=1, column=1, padx=15, pady=(0, 10))

        # --- LINHA 1: CPF e Data de Nascimento ---
        self.lbl_cpf = ctk.CTkLabel(self.frame_form, text="CPF (só números):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_cpf.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_cpf = ctk.CTkEntry(self.frame_form, placeholder_text="00000000000", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_cpf.grid(row=3, column=0, padx=15, pady=(0, 10))
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)
        self.entry_cpf.bind("<FocusOut>", self._formatar_cpf_cadastro)

        self.lbl_data = ctk.CTkLabel(self.frame_form, text="Data de Nasc. (DDMMAAAA):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_data.grid(row=2, column=1, sticky="w", padx=15, pady=(5, 2))
        self.entry_data = ctk.CTkEntry(self.frame_form, placeholder_text="01012000", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_data.grid(row=3, column=1, padx=15, pady=(0, 10))
        self.entry_data.bind("<KeyRelease>", self.limitar_data)

        # --- LINHA 2: E-mail e Passe ---
        self.lbl_email = ctk.CTkLabel(self.frame_form, text="E-mail:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_email.grid(row=4, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_email = ctk.CTkEntry(self.frame_form, placeholder_text="exemplo@email.com", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_email.grid(row=5, column=0, padx=15, pady=(0, 10))

        self.lbl_passe = ctk.CTkLabel(self.frame_form, text="Tipo de Passe:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_passe.grid(row=4, column=1, sticky="w", padx=15, pady=(5, 2))
        self.combo_passe = ctk.CTkComboBox(
            self.frame_form,
            values=["Normal", "Passe Anual", "VIP"],
            width=220,
            fg_color=COR_INPUT,
            border_color="#374151",
            button_color=COR_BOTAO,
            button_hover_color=COR_BOTAO_HOVER
        )
        self.combo_passe.grid(row=5, column=1, padx=15, pady=(0, 10))
        self.combo_passe.set("Normal")

        # --- Campo Senha ---
        self.lbl_senha = ctk.CTkLabel(self.frame_form, text="Senha de Acesso:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_senha.grid(row=8, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_senha = ctk.CTkEntry(self.frame_form, placeholder_text="•••••", width=220, fg_color=COR_INPUT, border_color="#374151", show="*")
        self.entry_senha.grid(row=9, column=0, padx=15, pady=(0, 10))

        # --- DADOS BANCÁRIOS ---
        self.lbl_num_cartao = ctk.CTkLabel(self.frame_form, text="Número do Cartão (Opcional):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_num_cartao.grid(row=6, column=0, sticky="w", padx=15, pady=(5, 2))

        self.entry_num_cartao = ctk.CTkEntry(self.frame_form, placeholder_text="0000 0000 0000 0000", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_num_cartao.grid(row=7, column=0, padx=15, pady=(0, 10))
        self.entry_num_cartao.bind("<KeyRelease>", self.limitar_num_cartao)

        self.lbl_val_cvc = ctk.CTkLabel(self.frame_form, text="Validade (MM/AA)  e  CVC:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_val_cvc.grid(row=6, column=1, sticky="w", padx=15, pady=(5, 2))

        self.frame_val_cvc = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        self.frame_val_cvc.grid(row=7, column=1, sticky="w", padx=15, pady=(0, 10))

        self.entry_val_cartao = ctk.CTkEntry(self.frame_val_cvc, placeholder_text="MM/AA", width=100, fg_color=COR_INPUT, border_color="#374151")
        self.entry_val_cartao.pack(side="left", padx=(0, 10))
        self.entry_val_cartao.bind("<KeyRelease>", self.limitar_val_cartao)

        self.entry_cvc_cartao = ctk.CTkEntry(self.frame_val_cvc, placeholder_text="CVC", width=110, fg_color=COR_INPUT, border_color="#374151")
        self.entry_cvc_cartao.pack(side="left")
        self.entry_cvc_cartao.bind("<KeyRelease>", self.limitar_cvc_cartao)

        # --- BOTÃO DE AÇÃO ---
        self.btn_salvar = ctk.CTkButton(
            self.frame_form, text=" ✓ Cadastrar Visitante",
            fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"), height=38, width=200,
            command=self.salvar_visitante
        )
        self.btn_salvar.grid(row=10, column=0, columnspan=2, pady=(15, 15))

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_mensagem.grid(row=11, column=0, columnspan=2, pady=(0, 10))

    def limitar_cpf(self, event):
        texto = self.entry_cpf.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if texto != apenas_numeros or len(apenas_numeros) > 11:
            self.entry_cpf.delete(0, "end")
            self.entry_cpf.insert(0, apenas_numeros[:11])

    def _formatar_cpf_cadastro(self, event=None):
        """Formata o CPF ao sair do campo (perde foco)."""
        texto_atual = self.entry_cpf.get()
        formatado = formatar_cpf(texto_atual)
        if formatado != texto_atual:
            self.entry_cpf.delete(0, "end")
            self.entry_cpf.insert(0, formatado)

    def limitar_data(self, event):
        texto = self.entry_data.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if texto != apenas_numeros or len(apenas_numeros) > 8:
            self.entry_data.delete(0, "end")
            self.entry_data.insert(0, apenas_numeros[:8])

    def limitar_num_cartao(self, event):
        texto = self.entry_num_cartao.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if texto != apenas_numeros or len(apenas_numeros) > 16:
            self.entry_num_cartao.delete(0, "end")
            self.entry_num_cartao.insert(0, apenas_numeros[:16])

    def limitar_val_cartao(self, event):
        texto = self.entry_val_cartao.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if texto != apenas_numeros or len(apenas_numeros) > 4:
            self.entry_val_cartao.delete(0, "end")
            self.entry_val_cartao.insert(0, apenas_numeros[:4])

    def limitar_cvc_cartao(self, event):
        texto = self.entry_cvc_cartao.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if texto != apenas_numeros or len(apenas_numeros) > 4:
            self.entry_cvc_cartao.delete(0, "end")
            self.entry_cvc_cartao.insert(0, apenas_numeros[:4])

    def salvar_visitante(self):
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        cpf = self.entry_cpf.get()
        data = self.entry_data.get()
        email = self.entry_email.get()
        passe = self.combo_passe.get()
        num_cartao = self.entry_num_cartao.get()
        val_cartao = self.entry_val_cartao.get()
        cvc_cartao = self.entry_cvc_cartao.get()
        senha = self.entry_senha.get()

        if not nome or not idade or not cpf:
            self.lbl_mensagem.configure(text="⚠ Preencha pelo menos Nome, Idade e CPF!", text_color=COR_ERRO)
            return

        cpf_limpo = "".join(filter(str.isdigit, cpf))
        data_limpa = "".join(filter(str.isdigit, data))

        if len(cpf_limpo) == 11:
            cpf = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

        if len(data_limpa) == 8:
            data = f"{data_limpa[:2]}/{data_limpa[2:4]}/{data_limpa[4:]}"

        cartao_formatado = ""
        if num_cartao or val_cartao or cvc_cartao:
            cartao_formatado = f"Num: {num_cartao} | Val: {val_cartao} | CVC: {cvc_cartao}"

        msg = self.servico.cadastrar_visitante(nome, idade, cpf, data, email, passe, cartao_formatado, senha)

        if "Erro" in msg:
            self.lbl_mensagem.configure(text=f"⚠ {msg}", text_color=COR_ERRO)
        else:
            self.lbl_mensagem.configure(text="✓ Conta criada com sucesso! Volte para fazer login.", text_color=COR_SUCESSO)

        # Limpar os campos
        self.entry_nome.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_cpf.delete(0, 'end')
        self.entry_data.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_num_cartao.delete(0, 'end')
        self.entry_val_cartao.delete(0, 'end')
        self.entry_cvc_cartao.delete(0, 'end')
        self.entry_senha.delete(0, 'end')
        self.combo_passe.set("Normal")
        