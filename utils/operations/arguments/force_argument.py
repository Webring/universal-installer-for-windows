import os

from .base_argument import *


class ForceArgument(BaseArgument):
    def __init__(self):
        self.names = ["-f", "--force"]
        self.help = "Consent to force remove"
        self.action = 'store_const'
        self.const = True
        self.dest = "force"
