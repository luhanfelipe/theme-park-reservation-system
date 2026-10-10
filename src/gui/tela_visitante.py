import customtkinter as ctk

class TelaVisitante(ctk.CTkFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master)
        
        # O "master" é o frame_principal lá do main.py
        # O "servico" é o ParqueService que vai salvar os dados
        self.servico = servico 

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self, 
            text="⬅ Voltar", 
            width=80, 
            height=32,
            fg_color="transparent", 
            border_width=1, 
            border_color="#4b5563",
            hover_color="#374151",
            command=comando_voltar
        )
        self.btn_voltar.place(x=20, y=15)

        # --- TÍTULO DA TELA ---
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text="👤 Cadastro de Visitantes", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # --- FORMULÁRIO DE CADASTRO ---
        self.frame_form = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#374151")
        self.frame_form.pack(pady=10, padx=20, anchor="center")

        # --- LINHA 0: Nome e Idade ---
        # Campo Nome
        self.lbl_nome = ctk.CTkLabel(self.frame_form, text="Nome do Visitante:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_nome.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 2))
        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: Maria Silva", width=220)
        self.entry_nome.grid(row=1, column=0, padx=15, pady=(0, 10))

        # Campo Idade
        self.lbl_idade = ctk.CTkLabel(self.frame_form, text="Idade:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_idade.grid(row=0, column=1, sticky="w", padx=15, pady=(12, 2))
        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 25", width=220)
        self.entry_idade.grid(row=1, column=1, padx=15, pady=(0, 10))

        # --- LINHA 1: CPF e Data de Nascimento ---
        # Campo CPF
        self.lbl_cpf = ctk.CTkLabel(self.frame_form, text="CPF (só números):", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_cpf.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_cpf = ctk.CTkEntry(self.frame_form, placeholder_text="00000000000", width=220)
        self.entry_cpf.grid(row=3, column=0, padx=15, pady=(0, 10))
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)

        # Campo Data de Nascimento
        self.lbl_data = ctk.CTkLabel(self.frame_form, text="Data de Nasc. (DDMMAAAA):", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_data.grid(row=2, column=1, sticky="w", padx=15, pady=(5, 2))
        self.entry_data = ctk.CTkEntry(self.frame_form, placeholder_text="01012000", width=220)
        self.entry_data.grid(row=3, column=1, padx=15, pady=(0, 10))
        self.entry_data.bind("<KeyRelease>", self.limitar_data)

        # --- LINHA 2: E-mail e Passe ---
        # Campo E-mail
        self.lbl_email = ctk.CTkLabel(self.frame_form, text="E-mail:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_email.grid(row=4, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_email = ctk.CTkEntry(self.frame_form, placeholder_text="exemplo@email.com", width=220)
        self.entry_email.grid(row=5, column=0, padx=15, pady=(0, 10))

        # Campo Tipo de Passe
        self.lbl_passe = ctk.CTkLabel(self.frame_form, text="Tipo de Passe:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_passe.grid(row=4, column=1, sticky="w", padx=15, pady=(5, 2))
        self.combo_passe = ctk.CTkComboBox(
            self.frame_form, 
            values=["Normal", "Passe Anual", "VIP"], 
            width=220
        )
        self.combo_passe.grid(row=5, column=1, padx=15, pady=(0, 10))
        self.combo_passe.set("Normal")

        # --- BOTÃO DE AÇÃO (Verde de Confirmação) ---
        self.btn_salvar = ctk.CTkButton(
            self.frame_form, 
            text=" ✓ Salvar Visitante", 
            fg_color="#10b981", 
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            width=200,
            command=self.salvar_visitante
        )
        self.btn_salvar.grid(row=6, column=0, columnspan=2, pady=(15, 10))

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_mensagem.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        # --- LISTAGEM DE VISITANTES ---
        self.lbl_lista = ctk.CTkLabel(self, text=" 👤 Visitantes Cadastrados", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_lista.pack(pady=(15, 5))

        self.frame_lista = ctk.CTkScrollableFrame(self, height=220, fg_color="transparent")
        self.frame_lista.pack(pady=5, padx=20, fill="both", expand=True)

        # Carrega a lista inicial de visitantes
        self.atualizar_lista()

    def limitar_cpf(self, event):
        texto = self.entry_cpf.get()
        if len(texto) > 11:
            self.entry_cpf.delete(11, "end")

    def limitar_data(self, event):
        texto = self.entry_data.get()
        if len(texto) > 8:
            self.entry_data.delete(8, "end")

    def salvar_visitante(self):
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        cpf = self.entry_cpf.get()
        data = self.entry_data.get()
        email = self.entry_email.get()
        passe = self.combo_passe.get()

        if not nome or not idade or not cpf:
            self.lbl_mensagem.configure(text="⚠ Preencha pelo menos Nome, Idade e CPF!", text_color="#f87171")
            return

        cpf_limpo = "".join(filter(str.isdigit, cpf))
        data_limpa = "".join(filter(str.isdigit, data))

        if len(cpf_limpo) == 11:
            cpf = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        
        if len(data_limpa) == 8:
            data = f"{data_limpa[:2]}/{data_limpa[2:4]}/{data_limpa[4:]}"

        msg = self.servico.cadastrar_visitante(nome, idade, cpf, data, email, passe)
        self.lbl_mensagem.configure(text=f"✓ {msg}", text_color="#34d399")

        # Limpar os campos
        self.entry_nome.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_cpf.delete(0, 'end')
        self.entry_data.delete(0, 'end')
        self.entry_email.delete(0, 'end')
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
                text_color="#9ca3af"
            )
            lbl_vazio.pack(pady=30)
            return

        for v in visitantes:
            card = ctk.CTkFrame(self.frame_lista, corner_radius=10, border_width=1, border_color="#374151")
            card.pack(pady=4, padx=5, fill="x")

            # Topo do Card
            frame_topo = ctk.CTkFrame(card, fg_color="transparent")
            frame_topo.pack(fill="x", padx=15, pady=(8, 2))

            lbl_nome = ctk.CTkLabel(frame_topo, text=v.nome, font=ctk.CTkFont(size=15, weight="bold"), text_color="#60a5fa")
            lbl_nome.pack(side="left")

            # Formatando as badges de prioridade com fundo
            tipo_passe = str(v.tipo_passe).upper()
            if "VIP" in tipo_passe:
                lbl_passe = ctk.CTkLabel(
                    frame_topo, 
                    text=" ★ VIP ", 
                    font=ctk.CTkFont(size=12, weight="bold"), 
                    text_color="#fef08a", 
                    fg_color="#854d0e", 
                    corner_radius=6
                )
            elif "ANUAL" in tipo_passe:
                lbl_passe = ctk.CTkLabel(
                    frame_topo, 
                    text=" 🏷 PASSE ANUAL ", 
                    font=ctk.CTkFont(size=12, weight="bold"), 
                    text_color="#bbf7d0", 
                    fg_color="#166534", 
                    corner_radius=6
                )
            else:
                lbl_passe = ctk.CTkLabel(
                    frame_topo, 
                    text=" NORMAL ", 
                    font=ctk.CTkFont(size=12), 
                    text_color="#e5e7eb", 
                    fg_color="#374151", 
                    corner_radius=6
                )
            lbl_passe.pack(side="right")

            # Base do Card
            frame_base = ctk.CTkFrame(card, fg_color="transparent")
            frame_base.pack(fill="x", padx=15, pady=(2, 8))
            
            info_texto = f"CPF: {v.cpf}  •  Idade: {v.idade} anos  •  Nasc: {v.data_nascimento}  •  E-mail: {v.email}"
            lbl_info = ctk.CTkLabel(frame_base, text=info_texto, font=ctk.CTkFont(size=12), text_color="#9ca3af")
            lbl_info.pack(side="left")