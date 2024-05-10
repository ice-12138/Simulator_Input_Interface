from PyQt5.QtWidgets import QApplication

from simulation_parameter.para_choose_window import select_para_main
from simulation_parameter.edit_para_window import edit_para_main

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = select_para_main.MyApplication()
    ui.show()
    sys.exit(app.exec_())
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui = edit_para_main.MyApplication()
#     ui.show()
#     sys.exit(app.exec_())
