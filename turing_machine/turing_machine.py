from tape import DoubleLinkedList
import json


class TuringMachine:
    def __init__(self, tape=DoubleLinkedList, path_to_file=None) -> None:
        self.tape = tape() # лента
        self.data = self.__load_data(path_to_file) if path_to_file is not None else dict()# данные
        self.alphabet = self.data["alphabet"] if path_to_file is not None else None # алфавит
        self.word = self.data["word"] if path_to_file is not None else None # слово
        self.condition = self.data[
            "start_condition"
        ] if path_to_file is not None else None # состояние(при инициализации стартовое состояние)
        self.pointer = self.data[
            "start_pointer"
        ] if path_to_file is not None else None # позиция курсора(при инициализации стартовое положение)
        self.conditions = self.data["conditions"] if path_to_file is not None else None # массив состояний и инструкций

        if path_to_file is not None:
            self.__set_word(self.word)  # запись слова в ленту

    def __load_data(self, path_to_file) -> dict:
        """Загрузка данных из JSON-файла."""
        with open(path_to_file) as file:
            data = json.load(file)
        data["path_to_file"] = path_to_file  # Сохраняем путь к файлу
        return data

    def get_states(self):
        if self.condition is not None:
            return [state["condition"] for state in self.conditions]
        else:
            return ""
    
    def get_alphabet(self):
        return self.alphabet if self.alphabet is not None else ""

    def __set_word(self, word) -> None:
        for elem in word:
            self.tape.push_back(elem)

    def step(self) -> bool:
        condition = self.conditions[int(self.condition[1::])]
        symbol = self.tape[self.pointer].value
        command = condition["commands"][symbol].split()

        if len(command) == 1:
            if command[0] == "!":
                return False
            else:
                if command[0] == "L":
                    self.pointer -= 1
                    if self.pointer < 0:
                        self.tape.push_front("_")
                        self.pointer = 0
                elif command[0] == "R":
                    self.pointer += 1
                    if self.pointer > self.tape.len - 1:
                        self.tape.push_back("_")
                        self.pointer -= 1
        else:
            new_symbol, new_pointer, new_condition = command

            if new_symbol != "_":
                self.tape[self.pointer].value = new_symbol

            if new_pointer == "L":
                self.pointer -= 1
                if self.pointer < 0:
                    self.tape.push_front("_")
                    self.pointer = 0
            elif new_pointer == "R":
                self.pointer += 1
                if self.pointer > self.tape.len - 1:
                    self.tape.push_back("_")
                    self.pointer -= 1

            if new_condition != "!":
                self.condition = new_condition
            else:
                self.condition = self.data[
            "start_condition"
        ] 
                return False
        
        return True
            
    def run(self):
        flag = True
        while flag:
            flag = self.step()
