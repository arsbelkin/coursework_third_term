from test import TuringMachine
import tkinter as tk
from tkinter import messagebox, filedialog, ttk


class TuringMachineGUI:
    CELL_SIZE = 50  # Размер ячейки на ленте

    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Эмулятор машины Тьюринга")

        self.tm = TuringMachine()  # Экземпляр TuringMachine
        self.running = False  # Флаг выполнения

        self.create_interface()

    def create_interface(self):
        """Создаёт элементы интерфейса."""
        config_frame = tk.Frame(self.master)
        config_frame.pack(pady=10)

        # Лента
        self.canvas = tk.Canvas(self.master, height=100, bg="white")
        self.canvas.pack(fill=tk.X, pady=10)
        self.cells = []

        # Панель управления
        control_frame = tk.Frame(self.master)
        control_frame.pack(pady=10)

        self.load_button = tk.Button(control_frame, text="Загрузить конфигурацию", command=self.load_configuration)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.settings_button = tk.Button(control_frame, text="Настройки", command=self.open_settings)
        self.settings_button.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(control_frame, text="Полный запуск", state=tk.DISABLED, command=self.run_machine)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(control_frame, text="Остановить", state=tk.DISABLED, command=self.stop_machine)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.step_button = tk.Button(control_frame, text="Шаг", state=tk.DISABLED, command=self.perform_step)
        self.step_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(control_frame, text="Сброс", state=tk.DISABLED, command=self.reset_machine)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.master, text="Статус: Ожидание конфигурации")
        self.status_label.pack()

    def update_ui_buttons(self, running=False, loaded=False):
        """Обновляет состояние кнопок в зависимости от текущего состояния."""
        self.run_button.config(state=tk.NORMAL if loaded and not running else tk.DISABLED)
        self.step_button.config(state=tk.NORMAL if loaded and not running else tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL if loaded else tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL if running else tk.DISABLED)

    def open_settings(self):
        """Открывает окно настроек."""
        if not self.tm:
            messagebox.showwarning("Ошибка", "Сначала загрузите или создайте машину.")
            return

        settings_window = tk.Toplevel(self.master)
        settings_window.title("Настройки машины Тьюринга")
        settings_window.geometry("600x400")

        tab_control = ttk.Notebook(settings_window)

        # Вкладка "Алфавит"
        alphabet_tab = ttk.Frame(tab_control)
        tab_control.add(alphabet_tab, text="Алфавит")

        tk.Label(alphabet_tab, text="Введите символы алфавита через запятую:").pack(pady=10)
        alphabet_entry = tk.Entry(alphabet_tab, width=50)
        alphabet_entry.pack(pady=5)
        alphabet_entry.insert(0, ",".join(self.tm.get_alphabet()))

        def save_alphabet():
            new_alphabet = alphabet_entry.get().split(",")
            if new_alphabet:
                self.tm.alphabet = [s.strip() for s in new_alphabet if s.strip()]
                messagebox.showinfo("Успех", "Алфавит обновлён!")

        tk.Button(alphabet_tab, text="Сохранить", command=save_alphabet).pack(pady=10)

        # Вкладка "Слово"
        word_tab = ttk.Frame(tab_control)
        tab_control.add(word_tab, text="Слово")

        tk.Label(word_tab, text="Введите начальное слово:").pack(pady=10)
        word_entry = tk.Entry(word_tab, width=50)
        word_entry.pack(pady=5)

        # Проверка содержимого ленты перед вставкой в поле
        if self.tm.tape.head:
            word_entry.insert(0, "".join(str(self.tm.tape)))

        def save_word():
            new_word = word_entry.get().strip()

            # Проверка, чтобы все символы в слове были из алфавита
            if any((char not in self.tm.alphabet and char!="_") for char in new_word):
                messagebox.showerror("Ошибка", "В слово можно вводить только символы из алфавита!")
                return

            if new_word:
                self.tm.tape.clear()
                for char in new_word:
                    self.tm.tape.push_back(char)
                self.update_tape_display()
                messagebox.showinfo("Успех", "Слово обновлено!")

        tk.Button(word_tab, text="Сохранить", command=save_word).pack(pady=10)

        # Вкладка "Состояния"
        states_tab = ttk.Frame(tab_control)
        tab_control.add(states_tab, text="Состояния")

        tk.Label(states_tab, text="Введите состояния через запятую:").pack(pady=10)
        states_entry = tk.Entry(states_tab, width=50)
        states_entry.pack(pady=5)
        states_entry.insert(0, ",".join(self.tm.get_states()))

        tk.Label(states_tab, text="Начальное состояние:").pack(pady=10)
        start_state_entry = tk.Entry(states_tab, width=50)
        start_state_entry.pack(pady=5)
        start_state_entry.insert(0, self.tm.data.get("start_condition", ""))

        tk.Label(states_tab, text="Финальные состояния через запятую:").pack(pady=10)
        final_states_entry = tk.Entry(states_tab, width=50)
        final_states_entry.pack(pady=5)
        ##final_states_entry.insert(0, ",".join(self.tm.final_states))

        def save_states():
            new_states = states_entry.get().split(",")
            new_start_state = start_state_entry.get().strip()
            new_final_states = final_states_entry.get().split(",")

            if new_states and new_start_state:
                self.tm.states = [s.strip() for s in new_states if s.strip()]
                self.tm.condition = new_start_state
                self.tm.final_states = {s.strip() for s in new_final_states if s.strip()}
                messagebox.showinfo("Успех", "Состояния обновлены!")

        tk.Button(states_tab, text="Сохранить", command=save_states).pack(pady=10)

        # Вкладка "Правила"
        rules_tab = ttk.Frame(tab_control)
        tab_control.add(rules_tab, text="Правила")

        tk.Label(rules_tab, text="Введите правила переходов:").pack(pady=10)
        rules_text = tk.Text(rules_tab, height=10, width=60)
        rules_text.pack(pady=5)

        # Отображаем текущие правила
        # rules_display = "\n".join(
        #     f"{state}, {symbol} -> {new_state}, {new_symbol}, {direction}"
        #     for (state, symbol), (new_state, new_symbol, direction) in self.tm.transition_function.items()
        # )
        # rules_text.insert(1.0, rules_display)

        def save_rules():
            new_rules = rules_text.get(1.0, tk.END).strip()
            try:
                self.tm.transition_function.clear()
                for line in new_rules.split("\n"):
                    parts = line.split("->")
                    key = tuple(map(str.strip, parts[0].split(",")))
                    value = tuple(map(str.strip, parts[1].split(",")))
                    self.tm.transition_function[key] = value
                messagebox.showinfo("Успех", "Правила обновлены!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Некорректный формат правил: {str(e)}")

        tk.Button(rules_tab, text="Сохранить", command=save_rules).pack(pady=10)

        tab_control.pack(expand=1, fill="both")

    def load_configuration(self):
        """Загрузка конфигурации из файла JSON."""
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filename:
            return
        try:
            # Загружаем новую конфигурацию
            self.tm = TuringMachine(path_to_file=filename)
            self.update_tape_display()

            # Обновляем состояние интерфейса
            self.update_ui_buttons(loaded=True)
            self.status_label.config(text="Конфигурация загружена.")
            self.master.geometry(f"{max(self.tm.tape.len * self.CELL_SIZE + 100, 800)}x250")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить конфигурацию: {str(e)}")

    def update_tape_display(self):
        """Обновление отображения ленты на экране."""
        if not self.tm:
            return
        self.canvas.delete("all")
        self.cells = []

        current_node = self.tm.tape.head
        index = 0
        while current_node:
            x_start = index * self.CELL_SIZE
            x_end = x_start + self.CELL_SIZE
            rect = self.canvas.create_rectangle(x_start, 20, x_end, 70, fill="white", outline="black")
            text = self.canvas.create_text((x_start + x_end) // 2, 45, text=current_node.value, font=("Arial", 14))
            self.cells.append((rect, text))
            if index == self.tm.pointer:
                self.canvas.itemconfig(rect, fill="lightblue")
            current_node = current_node.next
            index += 1

    def perform_step(self):
        """Выполнение одного шага."""
        if not self.tm:
            return
        try:
            result = self.tm.step()
            self.update_tape_display()
            if not result:
                self.update_ui_buttons(loaded=True)
                messagebox.showinfo("Финал", "Работа завершена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def run_machine(self):
        """Полный запуск машины."""
        if not self.tm:
            return
        self.running = True
        self.update_ui_buttons(running=True)

        def step_through():
            if not self.running:
                self.update_ui_buttons(loaded=True)
                return
            try:
                result = self.tm.step()
                self.update_tape_display()
                if not result:
                    self.running = False
                    self.update_ui_buttons(loaded=True)
                    messagebox.showinfo("Финал", "Работа завершена.")
                else:
                    self.master.after(500, step_through)
            except Exception as e:
                self.running = False
                self.update_ui_buttons(loaded=True)
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

        step_through()

    def stop_machine(self):
        """Останавливает выполнение машины."""
        self.running = False
        self.status_label.config(text="Выполнение остановлено.")
        self.update_ui_buttons(loaded=True)

    def reset_machine(self):
        """Сброс машины к начальному состоянию."""
        if not self.tm:
            return
        try:
            self.tm = TuringMachine()
            self.update_tape_display()
            self.update_ui_buttons(loaded=False)
            self.status_label.config(text="Машина сброшена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сбросить машину: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = TuringMachineGUI(root)
    root.mainloop()
