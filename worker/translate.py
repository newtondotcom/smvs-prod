import argostranslate.package
import argostranslate.translate

from_code = "fr"
to_code = "en"


def check_package_installed(from_code, to_code):
    langages = argostranslate.package.get_installed_packages()
    for langage in langages:
        if langage.from_code == from_code and langage.to_code == to_code:
            return True


def install_package(from_code, to_code):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code,
            available_packages,
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())


def translate(text, from_code):
    to_code = "en"
    if from_code != "en":
        if not check_package_installed(from_code, to_code):
            install_package(from_code, to_code)
        translatedText = argostranslate.translate.translate(text, from_code, to_code)
        return translatedText
    return text
