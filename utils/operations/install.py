from .base_operation import BaseOperation
from .arguments.package_name_argument import PackageNameArgument


class InstallOperation(BaseOperation):
    def __init__(self):
        super().__init__()
        self.names = ["install"]
        self.arguments = (PackageNameArgument(),)
        self.help = "Install package on your computer"

    def execute(self, arguments: dict) -> None:
        print("install arguments is", arguments)
