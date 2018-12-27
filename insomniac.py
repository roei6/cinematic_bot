import os
import ctypes


class Insomniac:
    """
    Prevent OS sleep/hibernate in windows; code from:
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx
    """
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self):
        pass

    def __enter__(self):
        self.inhibit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.uninhibit()

    def inhibit(self):
        if os.name == 'nt':
            print("Preventing Windows from going to sleep")
            ctypes.windll.kernel32.SetThreadExecutionState(
                Insomniac.ES_CONTINUOUS |
                Insomniac.ES_SYSTEM_REQUIRED)

    def uninhibit(self):
        if os.name == 'nt':
            print("Allowing Windows to go to sleep")
            ctypes.windll.kernel32.SetThreadExecutionState(
                Insomniac.ES_CONTINUOUS)
