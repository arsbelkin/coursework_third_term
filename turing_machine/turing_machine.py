from tape import DoubleLinkedList
import json


class TuringMachine:
    def __init__(self, tape=DoubleLinkedList(), path_to_file="data.json") -> None:
        self.tape = tape  # лента
        self.data = self.__load_data(path_to_file)  # данные
        self.alphabet = self.data["alphabet"]  # алфавит
        self.word = self.data["word"]  # слово
        self.condition = self.data[
            "start_condition"
        ]  # состояние(при инициализации стартовое состояние)
        self.pointer = self.data[
            "start_pointer"
        ]  # позиция курсора(при инициализации стартовое положение)
        self.conditions = self.data["conditions"]  # массив состояний и инструкций

        self.__set_word(self.word)  # запись слова в ленту

        # TODO: удалить
        self.__min = 0
        self.__max = len(self.word)

    def __load_data(self, path_to_file) -> dict:
        "функция для загрузки данных из файла"
        with open(path_to_file) as file:
            data = json.load(file)
        return data

    def __set_word(self, word) -> None:
        # self.tape.push_front()
        for elem in word:
            self.tape.push_back(elem)
        # self.tape.push_back()

    def print_tape(self):
        pos = str(self.tape).find(self.tape[self.pointer].value)
        self.tape.print_list()
        print(" " * pos + "x")

    def next_step(self) -> None:
        condition = self.conditions[int(self.condition[1::])]
        # symbol = (
        #     self.tape[self.pointer].value if 0 <= self.pointer < len(self.word) else "empty"
        # )
        symbol = self.tape[self.pointer].value
        command = condition["commands"][symbol].split()

        if len(command) == 1:
            if command[0] == "!":
                self.tape.print_list()
                return False
            else:
                if command[0] == "L":
                    self.pointer -= 1
                    if self.pointer < 0:
                        self.tape.push_front("empty")
                        self.pointer = 0
                elif command[0] == "R":
                    self.pointer += 1
                    if self.pointer > self.tape.len - 1:
                        self.tape.push_back("empty")
                        self.pointer -= 1
        else:
            new_symbol, new_pointer, new_condition = command

            if new_symbol != "_":
                self.tape[self.pointer].value = new_symbol

            if new_pointer == "L":
                self.pointer -= 1
                if self.pointer < 0:
                    self.tape.push_front("empty")
                    self.pointer = 0
            elif new_pointer == "R":
                self.pointer += 1
                if self.pointer > self.tape.len - 1:
                    self.tape.push_back("empty")
                    self.pointer -= 1

            if new_condition != "!":
                self.condition = new_condition
            else:
                self.condition = self.data[
            "start_condition"
        ] 
                self.tape.print_list()
                return False
        
        return True
            
    def run(self):
        flag = True
        while flag:
            flag = self.next_step()
        #print(self.tape.print_list())


tm = TuringMachine()

tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()
tm.run()

# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()

# tm.next_step()
# print(tm.pointer)
# print(tm.condition)
# # tm.print_tape()
# tm.tape.print_list()
