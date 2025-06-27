import threading
import globals
import sys
from utils.file_operations import check_data_file
from utils.handle_signals import handle_signals


def run_app() -> None:
    globals.window.show()
    sys.exit(globals.app.exec_())


def main() -> None:
    handle_signals()
    threading.Thread(target=check_data_file).start()
    run_app()


if __name__ == "__main__":
    main()
