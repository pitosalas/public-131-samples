class Reporter:
    def __init__(self):
        self.trace: list[str] = []
        pass

    def info(self, scenario: str, algo: str, file_name: str):
        self.scenario = scenario
        self.algo = algo
        self.file_name = file_name
        
    def add_trace(self, step):
        self.trace.append(step)

    def report(self):
        print("----------------------------------------")
        print(f"SCENARIO: {self.scenario}")
        print(f"   Starting Conditions")
        print(f"      Memory Manager: {self.algo}")
        print(f"      Script file: {self.file_name}")
        print(f"   Trace:")
        for step in self.trace:
            print(f"       {step}")
        print("***S Real Memory")
        print("* TODO: Print memory state")