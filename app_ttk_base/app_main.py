import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app_config import ConfigManager
from app_dlg import PreferencesDialog
from app_i18n import I18N
from pathlib import Path

# Install these modules :
#   tkinter-tooltip 3.1.2
from tktooltip import ToolTip

# Applications file paths
APP_DIR = Path(__file__).resolve().parent
I18N_PATH = APP_DIR / "translations.json"
CONFIG_PATH = APP_DIR / "config.json"
DATA_PATH = APP_DIR / "data_app"

class AppMain :
    """
    The main class of the application, which stores the root window.
    Attributes:
        root (tk.Tk): The main application window.
        config (app_config.ConfigManager) : the configuration manager of the application.
        i18n (app_i18n.I18N) : the translations manager of the application.
        appearance (str) : the appearance of the application (ttk theme).
        theme (str) : the color theme of the application (ttk theme).
        pw_horizontal (ttk.PanedWindow) : the main panel of the application.
        left_frame (ttk.Frame) : the frame on left part on the main paned window.
        main_frame (ttk.Frame) : the main frame, which is the right part on the main paned window.
    """

    CONFIG_DEFAULTS = {
        "language": "fr",
        "appearance_mode": "Azure",
        "color_theme": "dark",
        "geometry": "1024x640+100+80",
        "separator_pos": None,
        "appearances" : {
            "Azure" : ["light","dark"],
            "Forest" : ["light","dark"]
        }
    }

    def __init__(self, title:str):
        """
        The constructor of the class AppMain.
        :param title: the application's title.
        """
        self.root = tk.Tk()
        self.root.title(title)
        # Configuration (include preferences)
        self.config=ConfigManager(CONFIG_PATH, AppMain.CONFIG_DEFAULTS)
        # Internationalization (translations)
        self.i18n=I18N(I18N_PATH, lang=self.config.get("language"))
        # Sets window size
        self.root.geometry(self.config.get("geometry"))
        # Menu bar
        self.menubar=self._create_menu()
        # Toolbar
        self.toolbar=self._create_toolbar()
        # Main view based on PanedWindow
        self.pw_horizontal = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.pw_horizontal.pack(fill=tk.BOTH, expand=True)
        self.left_frame = self._create_left_frame()
        self.main_frame = self._create_main_frame()
        self.pw_horizontal.add(self.left_frame, weight=1)
        self.pw_horizontal.add(self.main_frame, weight=3)
        pos = self.config.get("separator_pos")
        if pos is not None:
            self.pw_horizontal.update()
            self.pw_horizontal.sashpos(0, int(pos))
        # Bind window close to save settings
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Set appearance and theme
        self.appearance = self.config.get("appearance_mode")
        self.theme = self.config.get("color_theme")
        self._set_appearance()
        # Sets the application's icon
        icon_app = tk.PhotoImage(file=DATA_PATH / 'icons/transport-public.png')
        self.root.iconphoto(False, icon_app)
        # Run the UI loop
        self.root.mainloop()

    def _set_appearance(self):
        """
        Sets the current theme's appearance and color.
        """
        if self.appearance=="Azure":
            # Look at  : https://github.com/rdbende/Azure-ttk-theme
            self.root.tk.call("source", DATA_PATH / "themes/azure/azure.tcl")
            self.root.tk.call("set_theme", self.theme)
        elif self.appearance=="Forest":
            # Look at  : https://github.com/rdbende/Forest-ttk-theme
            self.root.tk.call("source", DATA_PATH / f"themes/forest/forest-{self.theme}.tcl")
            ttk.Style().theme_use(f"forest-{self.theme}")

    def _change_appearance(self):
        """
        Changes dynamically the application theme's appearance and color.
        """
        old_appear=self.config.get("appearance_mode")
        old_theme=self.config.get("color_theme")
        if self.appearance!=old_appear:
            self._set_appearance()
        elif self.theme!=old_theme :
            if self.appearance == "Azure":
                self.root.tk.call("set_theme", self.theme)
            elif self.appearance=="Forest":
                self.root.tk.call("source", DATA_PATH / f"themes/forest/forest-{self.theme}.tcl")
                ttk.Style().theme_use(f"forest-{self.theme}")

        self.config.set("appearance_mode", self.appearance)
        self.config.set("color_theme", self.theme)

    def _create_menu(self)->tk.Menu:
        """
        Creates the application's main menu.
        :return: the menu bar
        """
        menubar = tk.Menu(self.root)
        # Menu File
        self.file_menu = tk.Menu(menubar, tearoff=False)
        self.file_menu.add_command(label=self.i18n.t("menu.exit"), command=self.on_close)
        menubar.add_cascade(label=self.i18n.t("menu.file"), menu=self.file_menu)
        # Menu Help
        self.help_menu = tk.Menu(menubar, tearoff=False)
        self.help_menu.add_command(label=self.i18n.t("menu.prefs"), command=self.open_preferences)
        self.help_menu.add_separator()
        self.help_menu.add_command(label=self.i18n.t("menu.about"), command=self.show_about)
        menubar.add_cascade(label=self.i18n.t("menu.help"), menu=self.help_menu)

        self.root.config(menu=menubar)
        return menubar

    def _create_toolbar(self)->ttk.Frame:
        """
        Creates the application's toolbar.
        :return: the toolbar.
        """
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.exit_icon = tk.PhotoImage(file=DATA_PATH / 'icons/porte-de-sortie-24.png')
        btn_exit=ttk.Button(toolbar, image=self.exit_icon, padding=0, command=self.on_close)
        btn_exit.grid(row=0, column=0, padx=5, pady=5)
        ToolTip(btn_exit, msg=self.i18n.t("menu.exit"), delay=0.5)
        return toolbar

    def _create_left_frame(self)->ttk.Frame:
        """
        Creates the left frame inside the main paned window.
        :return: left frame.
        """
        left_frame = ttk.Frame(self.pw_horizontal, relief="sunken")
        # Add widgets here
        label = ttk.Label(left_frame, text="Enter a value here :")
        label.pack(side=tk.TOP, pady=5, padx=5, anchor="w")
        entry = ttk.Entry(left_frame)
        entry.pack(side=tk.TOP, pady=2, padx=10, anchor="w")
        return left_frame

    def _create_main_frame(self)->ttk.Frame:
        """
        Creates the main frame inside the main paned window.
        :return: the main frame.
        """
        main_frame = ttk.Frame(self.pw_horizontal, relief="sunken")
        # Add widgets here
        canvas = tk.Canvas(main_frame, bg="pale green")
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_text(30, 30, text="Main surface", anchor="w", font=("Ariel", 20, "italic"))
        return main_frame

    def _rebuild_texts(self):
        """
        Rebuilds all the texts of the application, using the current language.
        """
        self.menubar.entryconfigure(1, label=self.i18n.t("menu.file"))
        self.file_menu.entryconfigure(0, label=self.i18n.t("menu.exit"))
        self.menubar.entryconfigure(2, label=self.i18n.t("menu.help"))
        self.help_menu.entryconfigure(0, label=self.i18n.t("menu.prefs"))
        self.help_menu.entryconfigure(2, label=self.i18n.t("menu.about"))

    # -------------------------
    # Commands
    # -------------------------
    def open_preferences(self):
        """
        Opens the preferences dialog box, and changes language and theme if not cancelled.
        """
        dialog = PreferencesDialog(self.root, self.config, self.i18n)
        if dialog.result:
            params = dialog.result
            if params["language"]!=self.i18n.current_lang :
                self.i18n.set_current_lang(params["language"])
                self._rebuild_texts()
            if params["appearance"]!=self.appearance or params["theme"]!=self.theme :
                self.appearance=params["appearance"]
                self.theme=params["theme"]
                self._change_appearance()

    def show_about(self):
        """
        Opens the 'about' dialog box.
        """
        messagebox.showinfo(title=self.i18n.t("about.title"), message=self.i18n.t("about.message"), parent=self.root)

    def on_close(self):
        """
        Saves the current configuration, then close the application.
        """
        x=self.root.winfo_x()
        y=self.root.winfo_y()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.config.set("geometry", f"{width}x{height}+{x}+{y}")
        self.config.set("language", self.i18n.current_lang)
        self.config.set("separator_pos", self.pw_horizontal.sashpos(0))
        # Save configuration and close
        self.config.save()
        print("Configuration saved...")
        self.root.destroy()

if __name__ == "__main__":
    app=AppMain("Example Tkinter App")
