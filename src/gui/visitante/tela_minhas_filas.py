import customtkinter as ctk

class TelaMinhasFilas(ctk.CTkScrollableFrame):

    COR_BOTAO_VERMELHO = "#ef4444"
    COR_HOVER_VERMELHO = "#7f1d1d"

    def __init__(self, master, servico, cpf_visitante, comando_voltar):
        super().__init__(master, fg_color="transparent")
        
        # Ocultar a barra de rolagem visual (Magia Premium)
        self._scrollbar.grid_forget()

        self.servico = servico
        self.cpf_visitante = cpf_visitante

        # Cores
        COR_FUNDO_VIDRO = "#2A2D3E"
        COR_BORDA_NEON = "#5A52D5"
        COR_TEXTO = "#FFFFFF"
        COR_TEXTO_SEC = "#A0A0A0"

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self, text="⬅ Voltar ao Menu", width=120, height=32,
            fg_color="transparent", border_width=1, border_color=COR_BORDA_NEON,
            hover_color=COR_FUNDO_VIDRO, text_color=COR_TEXTO, command=comando_voltar
        )
        self.btn_voltar.pack(anchor="nw", padx=20, pady=(20, 0))

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="📋 Minhas Reservas e Filas", 
            font=ctk.CTkFont(size=24, weight="bold"), text_color=COR_TEXTO
        )
        self.lbl_titulo.pack(pady=(15, 5))
        
        self.lbl_subtitulo = ctk.CTkLabel(
            self, text="Acompanhe o status das suas aventuras.", 
            font=ctk.CTkFont(size=14), text_color=COR_TEXTO_SEC
        )
        self.lbl_subtitulo.pack(pady=(0, 15))

        # --- LISTA DE RESERVAS ---
        # Frame normal, pois quem faz scroll é a tela inteira
        self.frame_lista = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.carregar_reservas()

    def carregar_reservas(self):
        # Limpa a tela para recarregar
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        # Consome os métodos criados na Issue 10
        reservas = self.servico.listar_reservas_do_visitante(self.cpf_visitante)
        visitante = self.servico.buscar_visitante_por_cpf(self.cpf_visitante)
        tipo_passe = str(getattr(visitante, 'tipo_passe', 'Normal')).upper()

        if not reservas:
            lbl_vazio = ctk.CTkLabel(self.frame_lista, text="Você ainda não possui nenhuma reserva.", font=ctk.CTkFont(slant="italic", size=14), text_color="#A0A0A0")
            lbl_vazio.pack(pady=40)
            return

        # Mostra as reservas (invertido para a mais recente aparecer primeiro)
        for r in reversed(reservas):
            card = ctk.CTkFrame(self.frame_lista, corner_radius=10, fg_color="#252836", border_width=1, border_color="#374151")
            card.pack(pady=8, fill="x")

            # TOPO DO CARD: Nome e Status
            frame_topo = ctk.CTkFrame(card, fg_color="transparent")
            frame_topo.pack(fill="x", padx=15, pady=(12, 5))

            lbl_atracao = ctk.CTkLabel(frame_topo, text=r.nome_atracao, font=ctk.CTkFont(size=18, weight="bold"), text_color="#FFFFFF")
            lbl_atracao.pack(side="left")

            if r.status == "Ativa":
                cor_status = "#34d399"
                bg_status = "#064e3b"
            elif r.status == "Cancelada":
                cor_status = "#fca5a5"
                bg_status = "#7f1d1d"
            else: # Concluída
                cor_status = "#94a3b8"
                bg_status = "#1e293b"

            lbl_status = ctk.CTkLabel(frame_topo, text=f" {r.status.upper()} ", font=ctk.CTkFont(size=11, weight="bold"), text_color=cor_status, fg_color=bg_status, corner_radius=6)
            lbl_status.pack(side="right")

            # MEIO DO CARD: Horário e Destaque VIP
            frame_meio = ctk.CTkFrame(card, fg_color="transparent")
            frame_meio.pack(fill="x", padx=15, pady=5)

            lbl_horario = ctk.CTkLabel(frame_meio, text=f"🕒 Horário: {r.horario}", font=ctk.CTkFont(size=14), text_color="#A0A0A0")
            lbl_horario.pack(side="left")

            if r.status == "Ativa":
                if "VIP" in tipo_passe:
                    lbl_passe = ctk.CTkLabel(frame_meio, text=" ★ Atendimento Prioritário VIP ", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFD700")
                    lbl_passe.pack(side="right")
                elif "ANUAL" in tipo_passe:
                    lbl_passe = ctk.CTkLabel(frame_meio, text=" 🏷 Passe Anual ", font=ctk.CTkFont(size=12, weight="bold"), text_color="#38bdf8")
                    lbl_passe.pack(side="right")

            # BASE DO CARD: Botão Cancelar (Aparece apenas se a reserva estiver Ativa)
            if r.status == "Ativa":
                frame_base = ctk.CTkFrame(card, fg_color="transparent")
                frame_base.pack(fill="x", padx=15, pady=(5, 12))
                
                btn_cancelar = ctk.CTkButton(
                    frame_base,
                    text="✗ Cancelar Reserva",
                    width=130,
                    height=28,
                    fg_color="transparent",
                    border_width=1,
                    border_color=self.COR_BOTAO_VERMELHO,
                    text_color=self.COR_BOTAO_VERMELHO,
                    hover_color=self.COR_HOVER_VERMELHO,
                    command=lambda cod=r.codigo: self.cancelar_reserva(cod)
                )
                btn_cancelar.pack(side="right")
            else:
                # Dá um espaçamento no fim do card se não houver botão
                ctk.CTkFrame(card, height=10, fg_color="transparent").pack()

    def cancelar_reserva(self, codigo):
        # Consome o método do serviço
        self.servico.cancelar_reserva(codigo)
        # Recarrega a tela para mostrar a alteração imediatamente
        self.carregar_reservas()