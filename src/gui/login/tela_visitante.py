import customtkinter as ctk

class TelaVisitante(ctk.CTkScrollableFrame):
    def __init__(self, master, servico, comando_voltar):
        # O "master" é o frame_principal lá do main.py. Fundo transparente para herdar a cor do main.
        super().__init__(master, fg_color="transparent")

        self._scrollbar.grid_forget()
        
        self.servico = servico 

        # Cores da Paleta Magia Premium
        COR_FUNDO_VIDRO = "#2A2D3E"
        COR_BORDA_NEON = "#5A52D5"
        COR_BOTAO_ROXO = "#6C63FF"
        COR_HOVER_ROXO = "#5A52D5"
        COR_TEXTO = "#FFFFFF"
        COR_TEXTO_SEC = "#A0A0A0"
        COR_INPUT_BG = "#1F1D2B" # Fundo mais escuro para os campos de texto

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self, 
            text="⬅ Voltar", 
            width=80, 
            height=32,
            fg_color="transparent", 
            border_width=1, 
            border_color=COR_BORDA_NEON,
            hover_color=COR_FUNDO_VIDRO,
            text_color=COR_TEXTO,
            command=comando_voltar
        )
        self.btn_voltar.pack(anchor="nw", padx=20, pady=(20, 0))

        # --- TÍTULO DA TELA ---
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="👤 Cadastro de Visitantes", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COR_TEXTO
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # --- FORMULÁRIO DE CADASTRO ---
        self.frame_form = ctk.CTkFrame(
            self, 
            corner_radius=15, 
            fg_color=COR_FUNDO_VIDRO, 
            border_width=1, 
            border_color=COR_BORDA_NEON
        )
        self.frame_form.pack(pady=10, padx=20, anchor="center")

        # --- LINHA 0: Nome e Idade ---
        # Campo Nome
        self.lbl_nome = ctk.CTkLabel(self.frame_form, text="Nome do Visitante:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_nome.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 2))
        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: Maria Silva", width=220, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_nome.grid(row=1, column=0, padx=15, pady=(0, 10))

        # Campo Idade
        self.lbl_idade = ctk.CTkLabel(self.frame_form, text="Idade:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_idade.grid(row=0, column=1, sticky="w", padx=15, pady=(12, 2))
        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 25", width=220, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_idade.grid(row=1, column=1, padx=15, pady=(0, 10))

        # --- LINHA 1: CPF e Data de Nascimento ---
        # Campo CPF
        self.lbl_cpf = ctk.CTkLabel(self.frame_form, text="CPF (só números):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_cpf.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_cpf = ctk.CTkEntry(self.frame_form, placeholder_text="00000000000", width=220, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_cpf.grid(row=3, column=0, padx=15, pady=(0, 10))
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)

        # Campo Data de Nascimento
        self.lbl_data = ctk.CTkLabel(self.frame_form, text="Data de Nasc. (DDMMAAAA):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_data.grid(row=2, column=1, sticky="w", padx=15, pady=(5, 2))
        self.entry_data = ctk.CTkEntry(self.frame_form, placeholder_text="01012000", width=220, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_data.grid(row=3, column=1, padx=15, pady=(0, 10))
        self.entry_data.bind("<KeyRelease>", self.limitar_data)

        # --- LINHA 2: E-mail e Passe ---
        # Campo E-mail
        self.lbl_email = ctk.CTkLabel(self.frame_form, text="E-mail:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_email.grid(row=4, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_email = ctk.CTkEntry(self.frame_form, placeholder_text="exemplo@email.com", width=220, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_email.grid(row=5, column=0, padx=15, pady=(0, 10))

        # Campo Tipo de Passe
        self.lbl_passe = ctk.CTkLabel(self.frame_form, text="Tipo de Passe:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_passe.grid(row=4, column=1, sticky="w", padx=15, pady=(5, 2))
        self.combo_passe = ctk.CTkComboBox(
            self.frame_form, 
            values=["Normal", "Passe Anual", "VIP"], 
            width=220,
            fg_color=COR_INPUT_BG, 
            border_color="#374151", 
            button_color=COR_BOTAO_ROXO, 
            button_hover_color=COR_HOVER_ROXO
        )
        self.combo_passe.grid(row=5, column=1, padx=15, pady=(0, 10))
        self.combo_passe.set("Normal")

        # --- DADOS BANCÁRIOS---

        self.lbl_num_cartao = ctk.CTkLabel(self.frame_form, text="Número do Cartão (Opcional):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_num_cartao.grid(row=6, column=0, sticky="w", padx=15, pady=(5, 2))

        self.entry_num_cartao = ctk.CTkEntry(self.frame_form, placeholder_text="0000 0000 0000 0000", width=220, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_num_cartao.grid(row=7, column=0, padx=15, pady=(0, 10))
        self.entry_num_cartao.bind("<KeyRelease>", self.limitar_num_cartao)

        self.lbl_val_cvc = ctk.CTkLabel(self.frame_form, text="Validade (MM/AA)  e  CVC:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_val_cvc.grid(row=6, column=1, sticky="w", padx=15, pady=(5, 2))

        self.frame_val_cvc = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        self.frame_val_cvc.grid(row=7, column=1, sticky="w", padx=15, pady=(0, 10))

        self.entry_val_cartao = ctk.CTkEntry(self.frame_val_cvc, placeholder_text="MM/AA", width=100, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_val_cartao.pack(side="left", padx=(0, 10)) # Margem à direita para separar do CVC
        self.entry_val_cartao.bind("<KeyRelease>", self.limitar_val_cartao)

        self.entry_cvc_cartao = ctk.CTkEntry(self.frame_val_cvc, placeholder_text="CVC", width=110, fg_color=COR_INPUT_BG, border_color="#374151")
        self.entry_cvc_cartao.pack(side="left")
        self.entry_cvc_cartao.bind("<KeyRelease>", self.limitar_cvc_cartao)

        # --- BOTÃO DE AÇÃO (Roxo Premium) ---
        self.btn_salvar = ctk.CTkButton(
            self.frame_form, text=" ✓ Cadastrar Visitante", 
            fg_color=COR_BOTAO_ROXO, hover_color=COR_HOVER_ROXO,
            font=ctk.CTkFont(size=14, weight="bold"), height=38, width=200,
            command=self.salvar_visitante
        )

        self.btn_salvar.grid(row=8, column=0, columnspan=2, pady=(15, 15))

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_mensagem.grid(row=9, column=0, columnspan=2, pady=(0, 10))

        # --- LISTAGEM DE VISITANTES ---
        self.lbl_lista = ctk.CTkLabel(self, text=" 👤 Visitantes Cadastrados", font=ctk.CTkFont(size=16, weight="bold"), text_color=COR_TEXTO)
        self.lbl_lista.pack(pady=(15, 5))

        self.frame_lista = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_lista.pack(pady=5, padx=20, fill="both", expand=True)

        # Carrega a lista inicial de visitantes
        self.atualizar_lista()

    def limitar_cpf(self, event):
        texto = self.entry_cpf.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if texto != apenas_numeros or len(apenas_numeros) > 11:
            self.entry_cpf.delete(0, "end")
            self.entry_cpf.insert(0, apenas_numeros[:11])

    def limitar_data(self, event):
        texto = self.entry_data.get()
        apenas_numeros = "".join(filter(str.isdigit, texto))
        if texto != apenas_numeros or len(apenas_numeros) > 8:
            self.entry_data.delete(0, "end")
            self.entry_data.insert(0, apenas_numeros[:8])

    def limitar_num_cartao(self, event):
        texto = self.entry_num_cartao.get()
        # Filtra para deixar apenas números (impede letras e espaços) e corta no 16
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

        if not nome or not idade or not cpf:
            self.lbl_mensagem.configure(text="⚠ Preencha pelo menos Nome, Idade e CPF!", text_color="#f87171")
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

        msg = self.servico.cadastrar_visitante(nome, idade, cpf, data, email, passe, cartao_formatado)
        self.lbl_mensagem.configure(text=f"✓ {msg}", text_color="#34d399")

        # Limpar os campos
        self.entry_nome.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_cpf.delete(0, 'end')
        self.entry_data.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_num_cartao.delete(0, 'end')
        self.entry_val_cartao.delete(0, 'end')
        self.entry_cvc_cartao.delete(0, 'end')
        self.combo_passe.set("Normal")

        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        visitantes = self.servico.listar_visitantes()

        if not visitantes:
            lbl_vazio = ctk.CTkLabel(
                self.frame_lista, 
                text="Nenhum visitante cadastrado ainda.", 
                font=ctk.CTkFont(size=14, slant="italic"), 
                text_color="#A0A0A0" # Cor mais discreta
            )
            lbl_vazio.pack(pady=30)
            return

        for v in visitantes:
            # Card combinando com o tema escuro/roxo
            card = ctk.CTkFrame(self.frame_lista, corner_radius=10, fg_color="#252836", border_width=1, border_color="#374151")
            card.pack(pady=4, padx=5, fill="x")

            # Topo do Card
            frame_topo = ctk.CTkFrame(card, fg_color="transparent")
            frame_topo.pack(fill="x", padx=15, pady=(8, 2))

            lbl_nome = ctk.CTkLabel(frame_topo, text=v.nome, font=ctk.CTkFont(size=15, weight="bold"), text_color="#FFFFFF")
            lbl_nome.pack(side="left")

            # Formatando as badges de prioridade com fundo
            tipo_passe = str(v.tipo_passe).upper()
            if "VIP" in tipo_passe:
                lbl_passe = ctk.CTkLabel(
                    frame_topo, 
                    text=" ★ VIP ", 
                    font=ctk.CTkFont(size=12, weight="bold"), 
                    text_color="#FFD700", # Dourado
                    fg_color="#4B4000",   # Fundo dourado escuro
                    corner_radius=6
                )
            elif "ANUAL" in tipo_passe:
                lbl_passe = ctk.CTkLabel(
                    frame_topo, 
                    text=" 🏷 PASSE ANUAL ", 
                    font=ctk.CTkFont(size=12, weight="bold"), 
                    text_color="#38bdf8", # Azul claro
                    fg_color="#0c4a6e",   # Azul escuro 
                    corner_radius=6
                )
            else:
                lbl_passe = ctk.CTkLabel(
                    frame_topo, 
                    text=" NORMAL ", 
                    font=ctk.CTkFont(size=12), 
                    text_color="#A0A0A0", 
                    fg_color="#1F1D2B", 
                    corner_radius=6
                )
            lbl_passe.pack(side="right")

            # Base do Card
            frame_base = ctk.CTkFrame(card, fg_color="transparent")
            frame_base.pack(fill="x", padx=15, pady=(2, 8))
            
            tem_cartao = "Sim" if hasattr(v, 'cartao') and v.cartao else "Não"
            info_texto = f"CPF: {v.cpf}  •  Idade: {v.idade} anos  •  Nasc: {v.data_nascimento}  •  E-mail: {v.email}   •  Possui Cartão: {tem_cartao}"
            lbl_info = ctk.CTkLabel(frame_base, text=info_texto, font=ctk.CTkFont(size=12), text_color="#A0A0A0") # Texto secundário mais suave
            lbl_info.pack(side="left")