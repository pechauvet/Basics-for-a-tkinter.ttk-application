# Basics-for-a-tkinter.ttk-application
A windowed application skeleton coded with tkinter, which includes configuration management, internationalization, theme selection, etc. The application is functional but does nothing concrete: its purpose is to provide some basics for developing an interface in Python.

### Objective
This application skeleton illustrates a number of generic features, such as the ability to preserve the configuration between user sessions, the ability to choose its appearance (ttk styles), the language to use. The content of the main window is based on a PanedWindow widget, with two frames whose separation is adjustable, a menu, a toolbar (button with icon and tooltip). A dialog box, which inherits from simpledialog.Dialog, allows you to modify preferences (theme, language). It is intended for introductory course on development of python applications and tkinter.  
The application is deliberately limited and without concrete application, focusing on a few functionalities, to facilitate the understanding of the code and its appropriation for real projects.

### Third-party components
First of all, to illustrate the possibility of having a "modern" visual for a tkinter application, I used [rdbende](https://github.com/rdbende)'s ttk themes: azure and forest. 

- Azure theme : https://github.com/rdbende/Azure-ttk-theme
- Forest theme : https://github.com/rdbende/Forest-ttk-theme

For the tooltip example in the toolbat (button exit), I used the tkinter-tooltip module version 3.1.2 (see https://pypi.org/project/tkinter-tooltip/). It is necessary to install this module to run the application.

### Application project structure
- data_app : directory with icons and themes
- > icons : sub-directory containing the icons used by the application
- > themes : sub-directory containing the themes used by the application
- app_main.py : main class with tk root window
- app_config.py : configuration management class
- app_i18n.py : internationalization management class
- app_dlg : dialog box classes (PreferencesDialog class)
- app_utils : utility functions
- config.json : File containing the last saved configuration of the application
- translations.json : File containing translations in different languages ​​(currently en and fr)

