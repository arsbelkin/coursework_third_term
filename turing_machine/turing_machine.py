from tape import DoubleLinkedList
import json


class TuringMachine:
    def __init__(self, path_to_file=None):
        self.tape = DoubleLinkedList()
        self.data = dict()
        self.path_to_file = path_to_file
        self.alphabet = ""
        self.word = ""
        self.rules = dict()
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

    def __set_data(self) -> None:
        if len(self.data):
            self.alphabet = self.data["alphabet"]
            self.word = self.data["word"]
            self.load_rules()
            self.states = self.get_states()
            self.currentCondition = self.data["start_condition"]
            self.pointer = self.data["start_pointer"]

    def __set_word(self) -> None:
        if len(self.word):
            for char in self.word:
                self.tape.push_back(char)

    def load_rules(self):
        if len(self.data):
            self.rules = self.data["conditions"]

    def save(self, file):
        self.data["alphabet"] = self.alphabet
        self.data["word"] = str(self.tape)
        json.dump(self.data, file)

    def get_rules(self) -> str:
        rules = ""
        if len(self.rules):
            for cond in self.rules.values():
                for key, value in cond["commands"].items():
                    rules += f"{cond["condition"]}, "
                    rules += f"{key}:"
                    rules += f"{value}\n"
        return rules

    def get_states(self) -> set:
        if len(self.rules):
            return (cond.get("condition", "") for cond in self.rules.values())
        else:
            return self.states

    def set_rules(self, new_rules: str) -> bool:
        self.data["conditions"] = {}

        for line in new_rules.split("\n"):
            parts = line.split(":")
            key = tuple(map(str.strip, parts[0].split(",")))
            value = tuple(map(str.strip, parts[1].split()))

            if "conditions" not in self.data:
                self.data["conditions"] = {}

            if key[0] not in self.data["conditions"]:
                self.data["conditions"][key[0]] = {}
                self.data["conditions"][key[0]]["condition"] = key[0]

            if "commands" not in self.data["conditions"][key[0]]:
                self.data["conditions"][key[0]]["commands"] = {}

            if key[1] not in self.data["conditions"][key[0]]["commands"]:
                self.data["conditions"][key[0]]["commands"][key[1]] = {}
            self.data["conditions"][key[0]]["commands"][
                key[1]
            ] = f"{value[0]} {value[1]} {value[2]}"

    def step(self) -> bool:
        self.currentRule = self.rules.get(
            self.currentCondition, self.rules.get(self.data["start_condition"], None)
        )
        symbol = self.tape[self.pointer].value
        command = self.currentRule["commands"][symbol].split()

        new_symbol, move, new_condition = command

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

        if new_condition != "!":
            self.currentCondition = new_condition
        else:
            self.currentCondition = self.data.get("start_condition", "q0")
            return False

        return True

    def run(self) -> None:
        flag = True
        while flag:
            flag = self.step()
