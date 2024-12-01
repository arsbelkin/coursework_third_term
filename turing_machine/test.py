from tape import DoubleLinkedList
import json


class TuringMachine:
    def __init__(self, path_to_file=None):
        self.tape = DoubleLinkedList()
        self.data = dict()
        self.path_to_file = path_to_file
        self.alphabet = ""
        self.word = ""
        self.rules = None
        self.states = set()
        self.currentCondition = None
        self.pointer = None

        self.__load_data(path_to_file=path_to_file)
        self.__set_data()
        self.__set_word()
    
    def __load_data(self, path_to_file) -> None:
        if path_to_file is not None:
            with open(path_to_file) as file:
                self.data = json.load(file)
    
    def __set_data(self)->None:
        if len(self.data):
            self.alphabet = self.data["alphabet"]
            self.word = self.data["word"]
            self.rules = self.data["conditions"]
            self.states = self.get_states()
            self.currentCondition = self.data["start_condition"]
            self.pointer = self.data["start_pointer"]
    
    def __set_word(self) -> None:
        if len(self.word):
            for char in self.word:
                self.tape.push_back(char)

    def get_rules(self)->str:
        rules = ""
        if self.rules is not None:
            for cond in self.rules:
                rules += f"{cond["condition"]}, "
                for key, value in cond["commands"].items():
                    rules += f"{key}: "
                    rules += f"{value}\n"
        return rules

    def get_states(self)->set:
        if self.rules is not None:
            return (cond.get("condition", "") for cond in self.rules)
        else:
            return self.states
    
    def step(self)->bool:
        self.currentCondition = self.rules[int(self.currentCondition[1::])]
        symbol = self.tape[self.pointer].value
        command = self.currentCondition["commands"][symbol].split()

        new_symbol, move, new_condition = command

        if new_symbol != "_":
            self.tape[self.pointer].value = new_symbol

        if move == "L":
            self.pointer -= 1
            if self.pointer < 0:
                self.tape.push_front("_")
                self.pointer = 0
        elif move == "R":
            self.pointer += 1
            if self.pointer > self.tape.len - 1:
                self.tape.push_back("_")
                self.pointer -= 1
        
        if new_condition != "!":
            self.currentCondition = new_condition
        else:
            self.currentCondition = self.data.get("start_condition", "q0")
            return False
        
        return True
    
    def run(self)->None:
        flag = True
        while flag:
            flag = self.step()
    