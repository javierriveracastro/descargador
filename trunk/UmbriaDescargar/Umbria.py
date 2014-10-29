# coding=utf-8
"""
API para conectarse a Umbria
"""

import urllib2
import urllib
import socket
import datetime
import tempfile
import random
from bs4 import BeautifulSoup
from PyQt4 import QtGui

URL_BASE = "http://www.comunidadumbria.com/"
PAGINA_INICIAL = "%sfront" % URL_BASE
URL_PORTADA = URL_BASE + "partida/%s"
HTTP_TIMEOUT = 60


def logea(usuario, contrasena):
    """
    Devuelve un opener de urllib2, ya logeado en Umbria o None si hay un error

    @param usuario: Usuario a logear
    @param contrasena: Contaseña del usuario
    """
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(),
                                  urllib2.ProxyHandler())
    try:
        opener.open(PAGINA_INICIAL, None, HTTP_TIMEOUT)
        datos = opener.open(PAGINA_INICIAL, urllib.urlencode(
            {'ACCESO': usuario, 'CLAVE': contrasena}),
            HTTP_TIMEOUT).read()
    except (urllib2.URLError, socket.timeout):
        opener = None  # Si hay un error, no vale el opener.
        datos = ''
        print "%s: Error al intentar autentificar" % \
            datetime.datetime.now()
    if 'value="Entrar"' in datos:
        opener = None
    return opener


def descarga_imagen(url_imageg):
    """
    Descarga una imagen de Umbria, no realiza autentificación

    @param url_imageg: cadena con la url de la imagen
    @return: Objeto fichero con la imagen
    """
    conexion = urllib.urlopen(url_imageg)
    temporal = tempfile.NamedTemporaryFile(delete=False)
    temporal.write(conexion.read())
    nombre_fichero = temporal.name
    conexion.close()
    temporal.close()
    return nombre_fichero


class Post(object):
    """
    Calse que representa un post
    """

    def __init__(self, html):
        """
        Genera el objeto que representa el post a partir del html
        """
        self.escritor = html.find("div", class_="pj").string
        self.avatar = html.find("img", class_="fotoAvatar")['src']
        self.texto = html.find("div", class_="texto")
        self.notas = html.find("div", class_="notas")


class Escena(object):
    """
    Clase que representa una escena
    """

    def __init__(self, titulo, url, descripcion, partida):
        # noinspection PyArgumentEqualDefault
        self.titulo = titulo
        self.url = URL_BASE + url[:-7]  # Eliminamos el ?__Pg=1
        self.descripcion = descripcion
        self.partida = partida

    def posts(self):
        """
        Obtiene los post de una escena como una lista de objetos post
        """
        # Descargar la primera pagina
        html_pagina_actual = self.partida.leer_pagina("%s?__Pg=1" % self.url)
        interpretada = BeautifulSoup(html_pagina_actual)
        # Calcular el número de paginas de la escena
        paginador = interpretada.find("ul", class_="paginador")
        if paginador is None:
            paginas = 1
        else:
            elementos_pag = paginador.find_all("a")
            url_ultima = elementos_pag[-1]["href"]
            trozos = url_ultima.split("=")
            paginas = int(trozos[-1])
        # Cargar pagina a pagina
        posts = []
        for pagina_siguiente in range(2, paginas + 2):
            html_posts = interpretada("div", class_="mensaje")
            for html_post in html_posts:
                posts.append(Post(html_post))
            if pagina_siguiente <= paginas:
                html_pagina_actual = self.partida.leer_pagina("%s?__Pg=%s" % (
                    self.url, pagina_siguiente))
                interpretada = BeautifulSoup(html_pagina_actual)
        return posts


class Partida(object):
    """
    Clase que representa una partida
    """

    def __init__(self, codigo, usuario, contrasena):
        """
        @param codigo: Codigo de la partida en Umbria
        @param usuario: Usuario en umbria
        @param contrasena: idem.
        """
        progreso = QtGui.QProgressDialog('Cargando partida', 'Cancelar', 1, 5)
        progreso.show()
        self.codigo = codigo
        self.usuario = usuario
        self.contrasena = contrasena
        self.opener = None
        self._imagenes = {}
        self.escenas_seleccionadas = []
        progreso.setValue(1)
        progreso.setLabelText("Cargando la portada")
        # noinspection PyArgumentList
        QtGui.QApplication.processEvents()
        html_portada = self.leer_pagina(URL_PORTADA % self.codigo)
        progreso.setValue(2)
        progreso.setLabelText("Interpretando la portsada")
        # noinspection PyArgumentList
        QtGui.QApplication.processEvents()
        sopa = BeautifulSoup(html_portada)
        titulo = sopa.find("h2", "tituloPartida")
        self.titulo = titulo.string
        progreso.setValue(3)
        progreso.setLabelText("Interpretando escenas")
        # noinspection PyArgumentList
        QtGui.QApplication.processEvents()
        self.escenas = []
        escenas = sopa.find_all("a", "tituloEscena")
        for escena in escenas:
            descripcion = escena.parent.parent.find("div", "textoEscena")
            self.escenas.append(Escena(escena.string, escena['href'],
                                       descripcion, self))
        progreso.setValue(4)
        progreso.setLabelText("Interpretando descripciones")
        # noinspection PyArgumentList
        QtGui.QApplication.processEvents()
        # El primer h4 es la introducción
        tag_actual = sopa.find("h4")
        resultados = []
        actual = ""
        for tag in tag_actual.next_siblings:
            try:
                if tag.name == "h4":
                    resultados.append(actual)
                    actual = ""
                else:
                    actual += str(tag)
            except AttributeError:
                pass  # Probablemente blancos
        resultados.append(actual)
        self.introduccion, self.sinopsis, self.notas = resultados
        self.url_portada = sopa.find("img", "portadaPartida")['src']
        progreso.setValue(5)

    def leer_pagina(self, direccion):
        """
        Lee una pagina de Umbria

        @param direccion: Direccion a leer
        @return: codigo HTML de la pagina
        """
        if self.opener is None:
            self.opener = logea(self.usuario, self.contrasena)
        return self.opener.open(direccion, None, HTTP_TIMEOUT).read()

    def imagen(self, url):
        """
        Devuelve un fichero con una imagen

        @param url: Url de la imagen
        """
        if url not in self._imagenes:
            self._imagenes[url] = descarga_imagen(url)
        return self._imagenes[url]


class EscenaPruebas(Escena):
    """
    Version de pruebas de la escena
    """

    def posts(self):
        """
        Devuelve varios post falsos
        """
        random.seed()
        posts = []
        for post in range(0, random.randrange(5, 15)):
            posts.append(Post(BeautifulSoup(
                '<div class="mensaje" id="msj10667358">'
                '<div class="avatar">'
                '<a href="/comunidad/companeros/13377" target="_blank"'
                ' class="linkAvatar">'
                '<img width="90" height="120"'
                ' src="http://www.comunidadumbria.com/imgs/usuarios/'
                '526bc08847bcf.png" title="sergut" alt="sergut"'
                ' class="fotoAvatar" /></a></div>'
                '<div class="fecha">23/01/2014, 17:14</div>'
                '<div class="pj">sergut</div>'
                '<div class="texto"><blockquote><p>Errrr... Sopa, '
                'hay dos ex-PJs libres, un bardo y un viejo mercenario '
                '(aunque este quiz&aacute; haya muerto). Si quieres '
                'hacerte un PJ nuevo </p></blockquote>'
                '<p>Empezar sin equipo es lo menos que le vamos a pedir'
                ' a un personaje que quiera ser parte del grupo '
                'm&aacute;s disfuncional de la historia. :-D</p></div>'
                '<div class="notas" id="notas10667358">'
                '<h3>Notas de juego</h3>'
                '<p>Watabuinegui consup... %s<br />Hey!</p>'
                '</div>' % post)))
        return posts


class PartidaPruebas(Partida):
    """
    Version de pruebas de una partida
    """

    # noinspection PyMissingConstructor
    def __init__(self, codigo, usuario, contrasena):
        """
        Genera una partida para hacer pruebas de layout sin tener que descargar
        datos reales

        @param codigo: Da igual
        @param usuario: Tampoco lo usamos, es para mantener la firma
        @param contrasena: Lo mismo
        """
        self.codigo = codigo
        self.usuario = usuario
        self.contrasena = contrasena
        self.opener = None
        self.titulo = "Partida de prueba"
        self.url_portada = ""
        self.escenas_seleccionadas = []
        self.escenas = [
            EscenaPruebas(
                "Off Topic Prubas", "", BeautifulSoup(
                    u"<div>Esto es la <em>descripcion</em> del Offtopic<p>"
                    u"<strong>negritas</strong></p><p><em>italicas</em></p>"
                    u"<p><u><a href='http://media/e.jpg'>subrayado</a></u></p>"
                    u"<p><strike>tachado</strike></p>"
                    u"<p><em><strong>negritalicas</strong></em></p>"
                    u"<p><strong><u><strike><em>tojunto</strike></em>"
                    u"</u></strong></p>" u"<img src='1'></div>"), self),
            EscenaPruebas("Cosas", "", BeautifulSoup(
                "<div><p>Con dos parrafos</p>" "<p>La ostia</p></div>"), self)]
        self.introduccion = u'Esto es una introducción de prueba, ' \
                            u'intentaremos que sea algo largo, para que no ' \
                            u'sea una sola linea, lo que significa que voy ' \
                            u'a tener que escribir varias chorradas. ' \
                            u'Y en varias frases. Que bonito es usar puntos. ' \
                            u'Supongo que con esto llegará'
        self.sinopsis = u'Pues nada, es solo una partida para ver como ' \
                        u'quedan las cosas sin necesidad de cargar datos ' \
                        u'reales de la web, que lleva un rato'
        self.notas = u'Larararararra'

    def imagen(self, url):
        """
        Devuelve siempre la misma imagen

        @param url: Lo ignora
        """
        return "UmbriaDescargar/media/alyan_logo.png"
