import customtkinter as ctk

class TelaFila(ctk.CTkFrame):
    def __init__(self, master, servico):
        super().__init__(master)
        self.servico = servico

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(self, text="Fila Virtual - Entrada", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=10)

        # --- FORMULÁRIO ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.entry_cpf = ctk.CTkEntry(self.frame_form, placeholder_text="CPF do Visitante", width=200)
        self.entry_cpf.grid(row=0, column=0, padx=10, pady=10)
        self.entry_cpf.bind("<KeyRelease>", self.limitar_cpf)

        # NOVIDADE: Adicionamos o "command=self.atualizar_lista_fila" para atualizar a tela se você mudar a atração!
        self.combo_atracao = ctk.CTkComboBox(self.frame_form, values=["Nenhuma atração cadastrada"], width=220, command=self.atualizar_lista_fila)
        self.combo_atracao.grid(row=0, column=1, padx=10, pady=10)

        self.btn_adicionar = ctk.CTkButton(self.frame_form, text="Adicionar à Fila", command=self.entrar_na_fila)
        self.btn_adicionar.grid(row=1, column=0, columnspan=2, pady=15)

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", text_color="green")
        self.lbl_mensagem.grid(row=2, column=0, columnspan=2)

        # --- NOVIDADE: VISUALIZAÇÃO DA FILA (O QUE FALTAVA!) ---
        self.lbl_lista = ctk.CTkLabel(self, text="Fila Atual da Atração:", font=("Arial", 16, "bold"))
        self.lbl_lista.pack(pady=(20, 0))

        self.caixa_texto_lista = ctk.CTkTextbox(self, height=200)
        self.caixa_texto_lista.pack(pady=10, padx=20, fill="both", expand=True)
        self.caixa_texto_lista.configure(state="disabled")
        # -------------------------------------------------------

        self.carregar_atracoes()

    def limitar_cpf(self, event):
        texto = self.entry_cpf.get()
        if len(texto) > 11:
            self.entry_cpf.delete(11, "end")

    def carregar_atracoes(self):
        atracoes = self.servico.listar_atracoes()
        if atracoes:
            nomes = [a.nome for a in atracoes]
            self.combo_atracao.configure(values=nomes)
            self.combo_atracao.set(nomes[0])
            self.atualizar_lista_fila() # NOVIDADE: Já mostra a fila da primeira atração ao abrir a tela

    def entrar_na_fila(self):
        cpf = self.entry_cpf.get()
        nome_atracao = self.combo_atracao.get()

        if not cpf or nome_atracao == "Nenhuma atração cadastrada":
            self.lbl_mensagem.configure(text="Preencha o CPF e escolha uma atração válida!", text_color="red")
            return

        cpf_limpo = "".join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            self.lbl_mensagem.configure(text="Erro: O CPF precisa ter exatos 11 números!", text_color="red")
            return
            
        cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

        msg = self.servico.adicionar_visitante_na_fila(cpf_formatado, nome_atracao)
        
        if "Erro" in msg:
            self.lbl_mensagem.configure(text=msg, text_color="red")
        else:
            self.lbl_mensagem.configure(text=msg, text_color="green")
            self.entry_cpf.delete(0, 'end')
            self.atualizar_lista_fila() # NOVIDADE: Atualiza a listagem assim que a pessoa entra com sucesso!

    # --- NOVIDADE: FUNÇÃO QUE BUSCA A FILA E ESCREVE NA TELA ---
    def atualizar_lista_fila(self, escolha=None):
        nome_atracao = self.combo_atracao.get()
        
        self.caixa_texto_lista.configure(state="normal")
        self.caixa_texto_lista.delete("1.0", "end")

        if nome_atracao == "Nenhuma atração cadastrada":
            self.caixa_texto_lista.configure(state="disabled")
            return

        atracoes = self.servico.listar_atracoes()
        for a in atracoes:
            if a.nome == nome_atracao:
                # Pega a lista do seu arquivo fila_prioridade.py
                fila_atual = a.fila_virtual.listar_fila()
                
                if not fila_atual:
                    self.caixa_texto_lista.insert("end", "A fila está vazia no momento.\n")
                else:
                    for posicao, pessoa in enumerate(fila_atual, 1):
                        self.caixa_texto_lista.insert("end", f"{posicao}º lugar: {pessoa}\n")
                break

        self.caixa_texto_lista.configure(state="disabled")