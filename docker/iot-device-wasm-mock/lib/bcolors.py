
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @classmethod
    def print_header(cls, string):
        print(cls.HEADER + str(string) + cls.ENDC)
    
    @classmethod
    def print_blue(cls, string):
        print(cls.OKBLUE + str(string) + cls.ENDC)
    
    @classmethod
    def print_cyan(cls, string):
        print(cls.OKCYAN + str(string) + cls.ENDC)
    
    @classmethod
    def print_green(cls, string):
        print(cls.OKGREEN + str(string) + cls.ENDC)
    
    @classmethod
    def print_warning(cls, string):
        print(cls.WARNING + str(string) + cls.ENDC)

    @classmethod
    def print_fail(cls, string):
        print(cls.FAIL + str(string) + cls.ENDC)

    @classmethod
    def print_bold(cls, string):
        print(cls.BOLD + str(string) + cls.ENDC)

    @classmethod
    def print_underline(cls, string):
        print(cls.UNDERLINE + str(string) + cls.ENDC)
