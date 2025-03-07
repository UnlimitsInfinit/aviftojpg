import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess

class AVIFtoJPGConverter:
    def __init__(self, master):
        self.master = master
        master.title("Conversor AVIF para JPG")
        master.geometry("400x350")

        # Botão para selecionar arquivos
        self.select_button = tk.Button(
            master, 
            text="Selecionar Arquivos AVIF", 
            command=self.select_files
        )
        self.select_button.pack(pady=10)

        # Listbox para mostrar arquivos selecionados
        self.files_listbox = tk.Listbox(master, width=50, height=5)
        self.files_listbox.pack(pady=10)

        # Habilitar arrastar e soltar
        self.files_listbox.drop_target_register(DND_FILES)
        self.files_listbox.dnd_bind('<<Drop>>', self.drop_files)

        # Botão para selecionar pasta de destino
        self.destination_button = tk.Button(
            master, 
            text="Selecionar Pasta de Destino", 
            command=self.select_destination
        )
        self.destination_button.pack(pady=10)

        # Label para mostrar destino
        self.destination_label = tk.Label(
            master, 
            text="Nenhuma pasta de destino selecionada", 
            wraplength=350
        )
        self.destination_label.pack(pady=10)

        # Botão de conversão
        self.convert_button = tk.Button(
            master, 
            text="Converter para JPG", 
            command=self.convert_to_jpg,
            state=tk.DISABLED
        )
        self.convert_button.pack(pady=10)

        # Variáveis para armazenar arquivos e destino
        self.selected_files = []
        self.destination_folder = ""

    def select_files(self):
        # Abre diálogo para seleção de arquivos AVIF
        files = filedialog.askopenfilenames(
            title="Selecione arquivos AVIF", 
            filetypes=[
                ("Arquivos AVIF", "*.avif"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if files:
            self.add_files_to_list(files)

    def drop_files(self, event):
        # Obtém os arquivos arrastados
        files = self.master.tk.splitlist(event.data)
        self.add_files_to_list(files)

    def add_files_to_list(self, files):
        # Limpa lista anterior
        self.files_listbox.delete(0, tk.END)
        
        # Adiciona arquivos à lista
        self.selected_files = list(files)
        for file in files:
            self.files_listbox.insert(tk.END, os.path.basename(file))
        
        # Habilita conversão se destino estiver selecionado
        if self.destination_folder:
            self.convert_button.config(state=tk.NORMAL)

    def select_destination(self):
        # Abre diálogo para seleção da pasta de destino
        folder = filedialog.askdirectory(
            title="Selecione pasta de destino"
        )
        
        if folder:
            self.destination_folder = folder
            self.destination_label.config(
                text=f"Destino: {folder}"
            )
            if self.selected_files:
                self.convert_button.config(state=tk.NORMAL)

    def convert_to_jpg(self):
        # Verifica se há arquivos e destino selecionados
        if not self.selected_files or not self.destination_folder:
            messagebox.showerror(
                "Erro", 
                "Selecione arquivos e pasta de destino"
            )
            return

        # Contador de conversões
        conversoes_sucesso = 0
        conversoes_erro = 0
        erros_detalhados = []

        for avif_path in self.selected_files:
            current_filename = os.path.basename(avif_path)
            try:
                print(f"Tentando converter: {current_filename}")

                # Gera o caminho de destino
                base_name = os.path.splitext(current_filename)[0]
                jpg_path = os.path.join(
                    self.destination_folder, 
                    f"{base_name}.jpg"
                )
                
                # Usa ffmpeg para converter
                subprocess.run(
                    ['ffmpeg', '-i', avif_path, jpg_path],
                    check=True
                )
                conversoes_sucesso += 1
                print(f"Convertido com sucesso: {jpg_path}")

            except subprocess.CalledProcessError as e:
                conversoes_erro += 1
                erros_detalhados.append(f"{current_filename}: {str(e)}")
                print(f"Erro ao converter {current_filename}: {str(e)}")

        # Mensagem final
        if conversoes_sucesso > 0:
            mensagem_sucesso = f"{conversoes_sucesso} arquivo(s) convertido(s) com sucesso!"
            if conversoes_erro > 0:
                mensagem_sucesso += f"\n{conversoes_erro} arquivo(s) falharam."
            messagebox.showinfo("Conversão Concluída", mensagem_sucesso)

            # Mostra detalhes dos erros, se houver
            if erros_detalhados:
                erro_detalhado = "\n".join(erros_detalhados)
                messagebox.showwarning("Detalhes dos Erros", erro_detalhado)
        else:
            messagebox.showerror("Erro", "Nenhum arquivo foi convertido.")

# Inicializa a aplicação
def main():
    root = TkinterDnD.Tk()  # Use TkinterDnD.Tk para habilitar arrastar e soltar
    app = AVIFtoJPGConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
