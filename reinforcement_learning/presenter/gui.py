import tkinter as tk

import dearpygui.dearpygui as dpg


class Gui:
    def __init__(self):
        self.width, self.height = self.__get_current_screen_geometry()
        self.setup()

    def setup(self):
        dpg.create_context()
        dpg.show_debug()
        dpg.show_metrics()
        dpg.show_item_registry()
        dpg.create_viewport(title="Reinforcement Learning", width=self.width, height=self.height)
        dpg.setup_dearpygui()

    def run(self):
        dpg.show_viewport()
        dpg.maximize_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def __get_current_screen_geometry(self):
        root = tk.Tk()
        root.withdraw()
        return root.winfo_screenwidth(), root.winfo_screenheight()

    def __del__(self):
        dpg.destroy_context()


if __name__ == '__main__':
    gui = Gui()
    gui.run()
