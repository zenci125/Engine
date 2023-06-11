import Lib.Exceptions.EngineException as enex


class GameConfiguration:
    def __init__(self, filepath = None):
        if filepath is None or filepath == "":
            self.filepath = None
            file = open("config/config.txt", "r")

        else:
            self.filepath = filepath
            file = open(self.filepath, "r")

        self.configuration = dict()
        a = file.readlines()

        for item in a:
            self.configuration[item.split(': ')[0]] = (item.split(': ')[1]).split("\n")[0]

        file.close()

    def set_variable(self, var, value = None):
        self.configuration.update({var: value})

    def get_variable(self, var):
        return self.configuration.get(var)

    def execute_file(self, filepath):
        a = filepath
        try:
            file = open(a, "r")
            for item in file.readlines():
                self.configuration[item.split(': ')[0]] = (item.split(': ')[1]).split("\n")[0]
            file.close()
        except:
            raise enex.EngineException(enex.EngineException.NOT_FOUND_FILE)

    def save(self, filepath = None):
        try:
            if filepath is None:
                filepath = self.filepath
                file = open(filepath, "w")
                for key in self.configuration.keys():
                    file.write(f"{key}: {self.configuration[key]}\n")
                file.close()
        except:
            raise enex.EngineException(enex.EngineException.NOT_FOUND_FILE)

    def __getitem__(self, item):
        return self.get_variable(item)

    def __setitem__(self, key, value):
        self.set_variable(key, value)




