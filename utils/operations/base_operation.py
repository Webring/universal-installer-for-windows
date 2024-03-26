class BaseOperation:
    def __init__(self):
        self.names = []
        self.result = {"success": False}
        self.arguments = []
        self.help = "This operation do nothing"
    def execute(self, *args, **kwargs) -> None:
        pass