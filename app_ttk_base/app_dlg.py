from tkinter import simpledialog, ttk
import tkinter as tk

class PreferencesDialog(simpledialog.Dialog):
    """
    The Preferences dialog box.

    Attributes:
        config (app_config.ConfigManager) : the configuration manager of the parent application.
        i18n (app_i18n.I18N) : the translations manager of the parent application.
        language_var (tk.StringVar) : the variable used with the language choice combobox.
        appearance_var (tk.StringVar) : the variable used with the appearance choice combobox.
        theme_var (tk.StringVar) : the variable used with the theme choice combobox.
        result (dict) : dictionary used to return the user's choices.
    """

    def __init__(self, parent, config, i18n):
        """
        The constructor of PreferencesDialog class.
        :param parent: the parent window.
        :param config: the configuration manager of the application.
        :param i18n: the internationalization manager of the application.
        """
        self.i18n=i18n
        self.config=config
        self.language_var = tk.StringVar(value=i18n.current_lang)
        self.appearance_var = tk.StringVar(value=config.get("appearance_mode"))
        self.theme_var = tk.StringVar(value=config.get("color_theme"))
        self.cb_language=None # Instanciation in body()
        self.cb_appear=None # Instanciation in body()
        self.cb_theme=None # Instanciation in body()
        self.result=None # Instanciation in apply()
        super().__init__(parent, title=i18n.t("prefs.title"))

    def body(self, master):
        ttk.Label(master, text=self.i18n.t("prefs.language")+" :").grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)
        ttk.Label(master, text=self.i18n.t("prefs.appearance")+" :").grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
        ttk.Label(master, text=self.i18n.t("prefs.theme")+" :").grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)

        self.cb_language=ttk.Combobox(master, textvariable=self.language_var, state = "readonly",
                     values=self.i18n.get_langs())
        self.cb_language.grid(row=0, column=1, padx=5, pady=5)
        self.cb_appear=ttk.Combobox(master, textvariable=self.appearance_var, state = "readonly",
                     values=list(self.config.get("appearances").keys()))
        self.cb_appear.grid(row=1, column=1, padx=5, pady=5)
        self.cb_appear.bind("<<ComboboxSelected>>", self.on_appearance_changed)
        self.cb_theme=ttk.Combobox(master, textvariable=self.theme_var, state = "readonly",
                     values=self.config.get("appearances")[self.config.get("appearance_mode")])
        self.cb_theme.grid(row=2, column=1, padx=5, pady=5)

        return None

    def on_appearance_changed(self, event=None):
        """Update the list of available themes when appearance changes."""
        appear = self.appearance_var.get()
        themes=self.config.get("appearances")[appear]
        self.cb_theme["values"]=themes
        self.cb_theme.set(themes[0])

    def apply(self):
        self.result = {
            "language": self.language_var.get(),
            "appearance": self.appearance_var.get(),
            "theme": self.theme_var.get(),
        }



