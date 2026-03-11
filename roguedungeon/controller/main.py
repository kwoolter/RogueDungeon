from . cmd_controller import RDCLI

def run():
    print("Controller GUI running...")


def run_cli():
    print("Controller CLI running...")
    c = RDCLI()
    c.run()

