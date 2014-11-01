# coding=utf-8
"""
Pasa unha partida de Umbria a un ficheiro .tex
"""

# TODO: Os saltos de lineas dentro das italicas e similares dan problemas
# TODO: Subindices/texto pequeño
# TODO: Tablas
# TODO: Lineas horizontales
# TODO: Listas sin orden
# TODO: Listas ordenadas
# TODO: Enlaces
# TODO: Tabla de contenidos

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
                      "\\usepackage[utf8]{inputenc}\n"
                      "\\usepackage{ulem}\n"
                      "\\usepackage{graphicx}\n"
                      "\\usepackage[official]{eurosym}\n"
                      "\\DeclareUnicodeCharacter{00A0}{~}\n"
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
        for escena in partida.escenas_seleccionadas:
            fichero.write(self.genera_escena(escena))
        fichero.write("\\end{document}\n")
        fichero.close()

    def descarga_imagen(self, url):
        """
        Descarga unha imaxen se non a temos

        @param url: url da imaxen
        @return: Nome do ficheiro da imaxen
        """
        if url not in self.imagenes:
            self.imagenes[url] = descarga_imagen(url, self.directorio)
        return self.imagenes[url]

    def html2latex(self, el):
        """
        Intenta convertir un documento en HTML a LaTex

        @param el: Arbol BeatifulSoup a convertir
        """
        try:
            contenidos = el.contents
        except AttributeError:
            # Estamos al final del arbol
            # Sustituit caracteres especiales en Latex
            el = el.replace(u'&', u'\\&')
            el = el.replace(u'^', u'\\textasciicircum')
            el = el.replace(u'"', u"''")
            el = el.replace(u'%', u'\\%')
            el = el.replace(u'€', u'\\euro{}')
            el = el.replace(u'_', u'\\_')
            el = el.replace(u'►', u'-')
            el = el.replace(u'$', u'\\$')
            el = el.replace(u'¬', u'$\\neg$')
            el = el.replace(u'#', u'\\#')
            el = el.replace(u'[', u'$[$')
            el = el.replace(u']', u'$]$')
            el = el.replace(u':\\', u'.: \\')
            el = el.replace(u'´', u"'")
            return unicode(el)
        else:
            resul = u''
            # Diversos tags tienen que hacer diversas cosas
            if el.name == u'em':
                resul += "\\textit{"
            elif el.name == u'strong':
                resul += "\\textbf{"
            elif el.name == u'u':
                resul += '\\underline{'
            elif el.name == u'strike':
                resul += '\\sout{'
            elif el.name == u'blockquote':
                resul += '\\begin{quotation} \\textquotedblleft\n'
            elif el.name == u'img':
                nombre_imagen = self.descarga_imagen(el['src'])
                if nombre_imagen:
                    resul += '\\includegraphics[width=\\textwidth]{%s}\n\n' % \
                        nombre_imagen
            elif el.name == u'br':
                resul += '\\\\ '
            for elemento in contenidos:
                resul += self.html2latex(elemento)
            if el.name in (u'em', u'strong', u'u', u'strike'):
                resul += "}"
            elif el.name in (u'div', u'p'):
                resul += "\n\n"
            elif el.name == u'blockquote':
                resul += '\\textquotedblright \\end{quotation}\n'
            return resul

    def genera_escena(self, escena):
        """
        Genera una escena como docmento de text

        @param escena: escena de Umbria que queremos generar
        """
        tex = "\\chapter{%s}\n" % escena.titulo
        tex += "%s\n" % self.html2latex(escena.descripcion)
        for post in escena.posts():
            tex += "\\section*{%s}\n" % post.escritor
            tex += "\\includegraphics[width=1.5cm]{%s}\n" % \
                self.descarga_imagen(post.avatar)
            tex += self.html2latex(post.texto)
            if post.notas:
                tex += "\\subsection*{Notas}\n"
                tex += self.html2latex(post.notas)
        return tex
