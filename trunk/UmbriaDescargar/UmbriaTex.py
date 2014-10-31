# coding=utf-8
"""
Pasa unha partida de Umbria a un ficheiro .tex
"""

import codecs

# TODO: Pedir un directorio en vez de un ficheiro
# TODO: Descargas as imaxes o directorio
# TODO: Incluir as imaxes no .text


def html2latex(el):
    """
    Intenta convertir un documento en HTML a LaTex

    @param el: Arbol BeatifulSoup a convertir
    """
    try:
        contenidos = el.contents
    except AttributeError:
        # Estamos al final del arbol
        return unicode(el)
    else:
        resul = u''
        # Diversos tags tienen que hacer diversas cosas
        if el.name == u'em':
            resul += "\\emph{"
        elif el.name == u'strong':
            resul += "\\textbf{"
        elif el.name == u'u':
            resul += '\\underline{'
        elif el.name == u'strike':
            resul += '\\sout{'
        for elemento in contenidos:
            resul += html2latex(elemento)
        if el.name in (u'em', u'strong', u'u', u'strike'):
            resul += "}"
        if el.name in (u'div', u'p'):
            resul += "\n\n"
        return resul


def genera_escena(escena):
    """
    Genera una escena como docmento de text

    @param escena: escena de Umbria que queremos generar
    """
    tex = "\\chapter{{%s}}\n" % escena.titulo
    tex += "%s\n" % html2latex(escena.descripcion)
    return tex


def genera_tex(nombre_archivo, partida):
    """
    Genera el fichero .text

    @param nombre_archivo: Nombre del archivo
    @param partida: Partida descargada
    """
    fichero = codecs.open(nombre_archivo, "w", "utf-8")
    fichero.write('\\documentclass[a4paper,11pt]{book}\n'
                  "\\usepackage[spanish]{babel}\n"
                  "\\usepackage[utf8x]{inputenc}\n"
                  "\\usepackage{ulem}\n"
                  "\\author{Comunidad Umbria}\n"
                  "\\title{%s}\n\n"
                  "\\begin{document}\n"
                  "\\maketitle\n" % partida.titulo)
    fichero.write("\\frontmatter\n")
    fichero.write(u"\\chapter{Introduccion}\n%s\n" % html2latex(
        partida.introduccion))
    fichero.write(u"\\chapter{Sinopsis}\n%s\n" % html2latex(partida.sinopsis))
    fichero.write(u"\\chapter{Notas}\n%s\n" % html2latex(partida.notas))
    fichero.write("\\mainmatter\n")
    for escena in partida.escenas:
        fichero.write(genera_escena(escena))
    fichero.write("\\end{document}\n")
    fichero.close()
