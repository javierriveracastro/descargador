# coding=utf-8
"""
Pasa unha partida de Umbria a un ficheiro .tex
"""

import codecs

from Umbria import descarga_imagen


class GeneradorText(object):
    """
    Clase que xenera un tex de unha partida
    """

    def __init__(self, nombre_dir, partida):
        """
        Genera el fichero .text

        @param nombre_dir: Nombre del archivo
        @param partida: Partida descargada
        """
        self.imagenes = {}
        self.directorio = nombre_dir
        fichero = codecs.open(nombre_dir + "/partida.tex", "w", "utf-8")
        fichero.write('\\documentclass[a4paper,11pt]{book}\n'
                      "\\usepackage[spanish]{babel}\n"
                      "\\usepackage[utf8x]{inputenc}\n"
                      "\\usepackage{ulem}\n"
                      "\\usepackage{graphicx}\n"
                      "\\author{Comunidad Umbria}\n"
                      "\\title{%s}\n\n"
                      "\\begin{document}\n"
                      "\\maketitle\n" % partida.titulo)
        fichero.write("\\frontmatter\n")
        fichero.write(u"\\chapter{Introduccion}\n%s\n" % self.html2latex(
            partida.introduccion))
        fichero.write(u"\\chapter{Sinopsis}\n%s\n" % self.html2latex(
            partida.sinopsis))
        fichero.write(u"\\chapter{Notas}\n%s\n" % self.html2latex(
            partida.notas))
        fichero.write("\\mainmatter\n")
        for escena in partida.escenas:
            fichero.write(self.genera_escena(escena))
        fichero.write("\\end{document}\n")
        fichero.close()

    def html2latex(self, el):
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
            elif el.name == u'img':
                nombre_imagen = self.imagenes.get(el['src'], descarga_imagen(
                    el['src'], self.directorio))
                resul += '\\includegraphics[width=\\textwidth]{%s}\n\n' % \
                    nombre_imagen
            for elemento in contenidos:
                resul += self.html2latex(elemento)
            if el.name in (u'em', u'strong', u'u', u'strike'):
                resul += "}"
            if el.name in (u'div', u'p'):
                resul += "\n\n"
            return resul

    def genera_escena(self, escena):
        """
        Genera una escena como docmento de text

        @param escena: escena de Umbria que queremos generar
        """
        tex = "\\chapter{{%s}}\n" % escena.titulo
        tex += "%s\n" % self.html2latex(escena.descripcion)
        return tex
