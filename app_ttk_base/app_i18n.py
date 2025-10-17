from app_utils import load_json
from pathlib import Path

class I18N:
    """
    Manage internationalization of an application.

    Attributes:
        translations_file (str or Path) : the pathname of the file which stores the translations.
        current_lang (str) : the current language to use.
        defined_langs (list[str]) : the list of the defined languages.
    """

    def __init__(self, translations_file:None|str|Path, translations_default:dict=None, lang:str="en"):
        """
        The constructor.
        :param translations_file: the pathname of the file which stores the translations.
        :param translations_default: a default translations dictionary.
        :param lang: the current language to use.
        """
        self.translations_file = translations_file
        self.current_lang = ""
        if translations_file :
            self.translations=load_json(translations_file, translations_default)
        else :
            self.translations = translations_default
        self.defined_langs = self.get_langs()
        self.set_current_lang(lang)

    def t(self, key: str) -> str:
        """
        Get the translation associated to the given key for the current language.
        :param key: the key.
        :return: the translation.
        """
        result=None
        if key in self.translations[self.current_lang] :
            result = self.translations[self.current_lang][key]
        return result if result is not None else key

    def set_current_lang(self, lang:str):
        """
        Try to set the current language. If the lang argument is not in the defined languages,
        the current language is not changed.
        :param lang: the language to set.
        """
        if lang in self.defined_langs :
            self.current_lang = lang

    def nb_lang(self)->int:
        """
        Compute the number of defined languages in the translations dictionary.
        :return: the number of defined languages.
        """
        if self.translations :
            return sum(1 for v in self.translations.values() if len(v)>0 )
        else :
            return 0

    def get_langs(self)->list:
        """
        Get the list of defined languages in the translations dictionary.
        :return: the list of defined languages.
        """
        if self.translations :
            return [k for k, v in self.translations.items() if len(v)>0 ]
        else :
            return []

if __name__ == "__main__":
    # Some tests and examples
    APP_DIR = Path(__file__).resolve().parent
    I18N_PATH = APP_DIR / "translations.json"
    i18n=I18N(I18N_PATH)
    print(i18n.nb_lang())
    print(i18n.get_langs())
    print(i18n.t("menu.about"))
    i18n.set_current_lang("fr")
    print(i18n.t("menu.about"))
