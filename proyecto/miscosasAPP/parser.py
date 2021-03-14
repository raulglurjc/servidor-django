#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class YTHandler(ContentHandler):

    def __init__(self):
        self.inEntry = False  # Para saber si estamos dentro de entry
        self.inContent = False  # Si tenemos contenido que queremos leer
        self.inMediaGroup = False
        self.inAuthor = False
        self.content = ""
        self.title = ""
        self.link = ""
        self.videoId = ""
        self.fotoVideo = ""
        self.nombreCanal = ""
        self.enlaceCanal = ""
        self.fecha = ""
        self.descripcion = ""
        self.alimentador = ""
        self.alimentadorId = ""
        self.nombreAcortado = ""

    def startElement(self, name, attrs):
        if name == 'entry':
            self.inEntry = True

        elif self.inEntry:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
            elif name == 'yt:videoId':
                self.inContent = True
            elif name == 'media:group':
                self.inMediaGroup = True
            elif name == 'author':
                self.inAuthor = True
            elif name == 'published':
                self.inContent = True
            elif name == 'yt:channelId':
                self.inContent = True
        if self.inMediaGroup:
            if name == 'media:thumbnail':
                self.fotoVideo = attrs.get('url')
            if name ==  'media:description':
                self.inContent = True
        if self.inAuthor:
            if name == 'name':
                self.inContent = True
            elif name == 'uri':
                self.inContent = True

    def endElement(self, name):
        if name == 'entry':
            from .models import Item, Alimentador
            self.inEntry = False

            if self.alimentador == "":
                try:
                    a = Alimentador.objects.get(tipo_alimentador="youtube", clave= self.alimentadorId, nombre=self.nombreCanal, url=self.enlaceCanal)

                except Alimentador.DoesNotExist:
                    a = Alimentador(tipo_alimentador="youtube", clave= self.alimentadorId, nombre=self.nombreCanal, url=self.enlaceCanal)
                    a.save()

                self.alimentador = a

            try:
                i = Item.objects.get(nombre=self.title, enlace=self.link, clave=self.videoId,
                                            media=self.fotoVideo, info=self.descripcion,
                                            alimentador=self.alimentador)
            except Item.DoesNotExist:
                newItem = Item(nombre=self.title, enlace=self.link, clave=self.videoId,
                                            media=self.fotoVideo, info=self.descripcion,
                                            alimentador=self.alimentador)
                newItem.save()

        elif name == 'media:group':
            self.inMediaGroup = False

        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == 'yt:videoId':
                self.videoId = self.content
                self.content = ""
                self.inContent = False
            elif name == 'name':
                self.nombreCanal = self.content
                self.content = ""
                self.inContent = False
            elif name == 'uri':
                self.enlaceCanal = self.content
                self.content = ""
                self.inContent = False
            elif name == 'published':
                self.fecha = self.content
                self.content = ""
                self.inContent = False
            elif name == 'media:description':
                self.descripcion = self.content
                self.content = ""
                self.inContent = False
            elif name == 'yt:channelId':
                self.alimentadorId = self.content
                self.content = ""
                self.inContent = False

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars

#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class LastfmHandler(ContentHandler):

    def __init__(self):
        self.inEntry = False
        self.inContent = False
        self.imagenbuena  = False
        self.content = ""
        self.alimentador = ""
        self.tituloAlimentador = ""
        self.enlaceAlimentador = ""
        self.alimentadorId = ""
        self.tituloItem = ""
        self.enlaceItem = ""
        self.clave = ""
        self.media = ""

    def startElement(self, name, attrs):
        if name == 'artist':
            self.inEntry = True
        elif self.inEntry:
            if name == 'name':
                self.inContent = True
            if name == 'url':
                self.inContent = True

        elif self.inEntry == False:
            if name == 'name':
                self.inContent = True
            elif name == 'url':
                self.inContent = True
            elif name == 'image' and attrs.get('size') == 'extralarge' :
                self.inContent = True
                self.imagenbuena = True


    def endElement(self, name):
        if name == 'artist':
            self.inEntry = False

        elif self.inEntry:
            if name == 'name':
                self.tituloAlimentador = self.content
                self.content = ""
                self.inContent = False

            if name == 'url':
                self.enlaceAlimentador = self.content
                self.content = ""
                self.inContent = False

        elif self.inEntry == False:

            if name == 'name':
                self.tituloItem = self.content
                self.content = ""
                self.inContent = False

            elif name == 'url':
                self.enlaceItem = self.content
                self.content = ""
                self.inContent = False

            elif name == 'image':
                if self.imagenbuena:
                    self.media = self.content
                    self.content = ""
                    self.inContent = False
                    self.imagenbuena = False

                    from .models import Item, Alimentador
                    if self.alimentador == "":
                        try:
                            a = Alimentador.objects.get(tipo_alimentador="lastfm", clave=self.tituloAlimentador, nombre=self.tituloAlimentador,
                                                        url=self.enlaceAlimentador)
                        except Alimentador.DoesNotExist:
                            a = Alimentador(tipo_alimentador="lastfm", clave=self.tituloAlimentador, nombre=self.tituloAlimentador,
                                                        url=self.enlaceAlimentador)
                            a.save()

                        self.alimentador = a

                    try:
                        i = Item.objects.get(nombre=self.tituloItem, enlace=self.enlaceItem, clave=self.tituloItem,
                                             media=self.media, alimentador=self.alimentador)
                    except Item.DoesNotExist:
                        newItem = Item(nombre=self.tituloItem, enlace=self.enlaceItem, clave=self.tituloItem,
                                       media=self.media, alimentador=self.alimentador)
                        newItem.save()

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars
