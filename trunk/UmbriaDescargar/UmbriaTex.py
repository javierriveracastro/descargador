# coding=utf-8
"""
Pasa unha partida de Umbria a un ficheiro .tex
"""

import codecs


def genera_tex(nombre_archivo):
    """
    Genera el fichero .text

    @param nombre_archivo: Nombre del archivo
    """
    fichero = codecs.open(nombre_archivo, "w", "utf-8")
    fichero.write('\\documentclass[a4paper,11pt]{book}\n'
                  "\\title{Descargador Umbria}\n"
                  "\usepackage[spanish]{babel}\n"
                  "\usepackage[utf8]{inputenc}")
    fichero.close()
