from tape import DoubleLinkedList
import json


class TuringMachine:
    def __init__(self, tape=DoubleLinkedList(), path_to_file="data.json") -> None:
        self.tape = tape  # лента
        self.data = self.__load_data(path_to_file)  # данные
        self.alphabet = self.data["alphabet"]  # алфавит
        self.word = self.data["word"]  # слово
        self.start_condition = self.data["start_condition"]  # стартовое состояние
        self.start_pointer = self.data[ "start_pointer"]  # стартовая позиция
        self.conditions = self.data["conditions"]  # состояния

        self.__set_word(self.word)
    
    def __load_data(self, path_to_file) -> dict:
        "функция для загрузки данных из файла"
        with open(path_to_file) as file:
            data = json.load(file)
        return data
    
    def __set_word(self, word) -> None:
        self.tape.push_front()
        for elem in word:
            self.tape.push_back(elem)
        self.tape.push_back()

    def print_tape(self):
        pos = str(self.tape).find(self.word[self.start_pointer])
        self.tape.print_list()
        print(" "*pos + "x")






tm = TuringMachine()

tm.print_tape()
