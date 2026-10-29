import pygame
import sys
import os
import json
import math

# ============================================================================
# Sección 1 configuración
# ============================================================================

ANCHO_PANTALLA = 1280
ALTO_PANTALLA  = 720
FPS            = 60

#Suelo
SUELO = 620

COLOR_LLAVE = (0, 0, 0)   #Chroma Key

#--Tamaño "de fábrica" de las hojas de sprites de 4 fotogramas
#Casi todos los personajes (Benjamín, el caballo, los soldados, Arapoty,
#el Coronel) vienen en hojas de este tamaño. Cruz es la excepción y usa
#su propio tamaño de origen (ver CompaneroCruz), pero como todos se
#normalizan por ALTO_VIS_PERSONAJE, terminan midiendo igual en pantalla.
ANCHO_CUADRO_PERSONAJE   = 400
ALTO_CUADRO_PERSONAJE    = 396
ANCHO_CUADRO_CHICHA_FINAL = 400
ALTO_CUADRO_CHICHA_FINAL  = 393

# Escala "de referencia" con la que se calcula el tamaño estándar de
# personaje en pantalla (ver ALTO_VIS_PERSONAJE más abajo).
ESCALA_GAMEPLAY = 0.35

# Escala específica para la sala del Coronel (personajes más grandes)
ESCALA_SALA_CORONEL = 0.45

# Tamaño visible ESTÁNDAR de personaje en gameplay. TODOS los personajes
# (Benjamín, el caballo montado y solo, Cruz, los soldados, el Coronel)
# se cargan pidiéndole a HojaSprites que los escale a esta altura
# (alto_destino=ALTO_VIS_PERSONAJE), sin importar el tamaño original de
# su hoja: así se evita que algunos se vean más grandes o más chicos.
ANCHO_VIS_PERSONAJE = int(ANCHO_CUADRO_PERSONAJE * ESCALA_GAMEPLAY)
ALTO_VIS_PERSONAJE  = int(ALTO_CUADRO_PERSONAJE  * ESCALA_GAMEPLAY)

# Altura estándar específica para el caballo (montado y solo). Un
# caballo es más alto que una persona de pie, así que forzarlo a
# ALTO_VIS_PERSONAJE lo hace ver chico. FACTOR_TAMANIO_CABALLO es el
# único número que hay que tocar para agrandarlo/achicarlo: probá con
# otros valores (1.3, 1.6, 1.8...) hasta que se vea bien con tu arte.
FACTOR_TAMANIO_CABALLO = 2.2
ALTO_VIS_CABALLO = int(ALTO_VIS_PERSONAJE * FACTOR_TAMANIO_CABALLO)

# Offset vertical para alinear el caballo con el suelo (las patas)
# Este valor ajusta cuántos píxeles se "hunde" el caballo en el suelo
# para que las patas toquen correctamente la línea SUELO
OFFSET_Y_CABALLO = 25

#--Estado de salud y honor
SALUD_MAXIMA  = 100
SALUD_INICIAL = 60
HONOR_MAXIMO  = 100

#--Sigilo (Fase 3b: fortín interior)
VELOCIDAD_INFILTRACION    = 160.0   # px/seg, Benjamín a pie, sigiloso
DANIO_POR_DETECCION       = 10
LIMITE_SOSPECHA_CENTINELA = 2.0     # segundos expuesto antes de ser detectado

#--Movimiento por los mundos panorámicos (litoral, campamento, fortín)
MARGEN_CAM_X           = ANCHO_PANTALLA // 2   # la cámara centra a Benjamín
MARGEN_LLEGADA_BORDE   = 60                    # qué tan cerca del borde derecho "cuenta" como llegar
VELOCIDAD_MONTADO      = 220.0   # px/seg, Benjamín a caballo (más rápido)
VELOCIDAD_A_PIE        = 140.0   # px/seg, Benjamín caminando

#--Combate con soldados y boleadora (Fase 3a: entrada del fortín)
VELOCIDAD_SOLDADO_PATRULLA = 70.0
DISTANCIA_ATAQUE_SOLDADO   = 70
DANIO_SOLDADO               = 8
VELOCIDAD_BOLEADORA         = 480.0
COOLDOWN_LANZAMIENTO        = 0.5
IMPACTOS_PARA_DERRIBAR      = 2   # golpes de boleadora necesarios para derribar a un soldado

# Coordenada X donde debe estar el jugador para iniciar el combate en el fortín
X_INICIO_COMBATE_FORTIN = 1200

#--Combate con el Coronel (Fase 4: sala del Coronel)
VIDA_CORONEL_MAXIMA      = 4    # golpes necesarios para derrotar al Coronel
DANIO_ATAQUE_CORONEL     = 100  # daño instantáneo si el Coronel toca al jugador

#--Ancho de cada mundo panorámico (uno por escena/ruta). Cuando el ancho
#de una escena es igual al ancho de pantalla, la cámara queda fija (es
#el caso de la sala del Coronel): no hace falta un caso especial.
ANCHO_MUNDO_LITORAL         = 2200
ANCHO_MUNDO_CAMPAMENTO      = 1800
ANCHO_MUNDO_FORTIN_ENTRADA  = 2000
ANCHO_MUNDO_FORTIN_INTERIOR = 1800
ANCHO_MUNDO_SALA_CORONEL    = ANCHO_PANTALLA

#Guardar partida
ARCHIVO_GUARDADO = "partida.json"

# --Rutas de pantallas
RUTA_FONDO_MENU     = r"Media\Pantallas\fondo_menu.png"
RUTA_PANTALLA_CARGA = r"Media\Pantallas\pantalla_carga.jpeg"

# --Fondos de cada escena/ruta del Capítulo 3
RUTA_FONDO_ATARDECER       = r"Media\Paisajes\final_cine.png"
RUTA_FONDO_LITORAL         = r"Media\Paisajes\litoral.png"
RUTA_FONDO_CAMPAMENTO      = r"Media\Paisajes\campamento_litoral.png"
RUTA_FONDO_FORTIN_ENTRADA  = r"Media\Paisajes\fortin_exterior.png"
RUTA_FONDO_FORTIN_INTERIOR = r"Media\Paisajes\fortin_interior.png"
RUTA_FONDO_SALA_CORONEL    = r"Media\Paisajes\sala_coronel.png"

# --Benjamín / Chicha: spritesheets
RUTA_CHICHA_NORMAL    = r"Media\Npc_Personajes\chicha.png"
RUTA_CHICHA_SENTADO   = r"Media\Npc_Personajes\chicha_cineFinal.png"
RUTA_CHICHA_ATAQUE    = r"Media\Npc_Personajes\chicha_ataque.png"
RUTA_BENJAMIN_CABALLO = r"Media\Npc_Personajes\chicha_montando.png"
RUTA_CABALLO_SOLO     = r"Media\Npc_Personajes\caballo.png"

# --Cruz (compañero opcional, condicionado a la decisión del Capítulo 1)
RUTA_CRUZ_LIBRE = r"Media\Npc_Personajes\cruz.png"

# --Arapoty (NPC guaraní que enseña las mezclas en el campamento)
RUTA_ARAPOTY = r"Media\Npc_Personajes\arapoty.png"

# --Coronel Ibáñez (enfrentamiento final, en la sala del Coronel)
RUTA_CORONEL = r"Media\Npc_Personajes\coronel_marchando.png"

# --Soldados (entrada del fortín)
RUTA_SOLDADO_AVANCE = r"Media\Npc_Personajes\soldado.png"
RUTA_SOLDADO_CAIDO  = r"Media\Npc_Personajes\NPC_caido.png"

# --Boleadora
RUTA_BOLEADORA = r"Media\Objetos\boleadora.png"

# --Música
RUTA_MUSICA_MENU     = r"Media\Musica\Menú_juego.mp3"
RUTA_MUSICA_JUEGO    = r"Media\Musica\Explorar.ogg"
RUTA_MUSICA_DECISION = r"Media\Musica\Decisión.ogg"
RUTA_MUSICA_FINAL    = r""

# ============================================================================
# Sección 2 paleta de colores
# ============================================================================

COLOR_BLANCO        = (255, 255, 255)
COLOR_NEGRO         = (  0,   0,   0)
COLOR_TIERRA        = (101,  67,  33)
COLOR_TIERRA_BORDE  = (160, 110,  60)
COLOR_VERDE_VIDA    = ( 60, 180,  60)
COLOR_ROJO_DANIO    = (200,  40,  40)
COLOR_HONOR_ORO     = (218, 165,  32)
COLOR_CAJA_DLG      = ( 12,   8,   4, 215)
COLOR_OVERLAY_INTRO = (  0,   0,   0, 190)

# ============================================================================
# Sección 3 utilidades generales
# ============================================================================

def _quitar_fondo_solido(superficie: pygame.Surface) -> pygame.Surface:
    
    mascaras = superficie.get_masks()
    tiene_alfa_real = mascaras[3] != 0

    if tiene_alfa_real:
        return superficie.convert_alpha()

    superficie = superficie.convert()
    superficie.set_colorkey(COLOR_LLAVE)
    return superficie


def cargar_imagen(ruta: str, escala: tuple = None) -> pygame.Surface:

    if not ruta or not os.path.exists(ruta):
        if ruta:
            print(f"[Asset no encontrado] {ruta}")
        ancho, alto = escala if escala else (64, 64)
        ph = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        ph.fill((40, 40, 40, 200))
        pygame.draw.rect(ph, (220, 0, 220), ph.get_rect(), 3)
        return ph
    try:
        imagen = pygame.image.load(ruta)
        imagen = _quitar_fondo_solido(imagen)
    except pygame.error as err:
        print(f"[Error al cargar imagen] {ruta} {err}")
        ancho, alto = escala if escala else (64, 64)
        ph = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        ph.fill((40, 40, 40, 200))
        pygame.draw.rect(ph, (220, 0, 220), ph.get_rect(), 3)
        return ph
    if escala:
        # pygame.transform.scale() puede perder el colorkey de la
        # superficie original: lo guardamos antes y lo reaplicamos
        # después de escalar (fix del bug de invisibilidad).
        colorkey = imagen.get_colorkey()
        imagen = pygame.transform.scale(imagen, escala)
        if colorkey is not None:
            imagen.set_colorkey(colorkey)
    return imagen


def reproducir_musica(ruta: str, volumen: float = 0.5) -> None:
    if not ruta or not os.path.exists(ruta):
        return
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)
    except Exception:
        pass


def reproducir_sonido(ruta: str, volumen: float = 0.6):
    if not ruta or not os.path.exists(ruta):
        return None
    try:
        sonido = pygame.mixer.Sound(ruta)
        sonido.set_volume(volumen)
        return sonido
    except Exception:
        return None


def dibujar_texto_envuelto(pantalla, texto, fuente, color, x, y, ancho_max) -> int:

    palabras     = texto.split(" ")
    linea        = ""
    desplaz_y    = 0
    interlineado = fuente.get_linesize() + 2
    for palabra in palabras:
        prueba = linea + palabra + " "
        if fuente.size(prueba)[0] > ancho_max and linea:
            pantalla.blit(fuente.render(linea.rstrip(), True, color), (x, y + desplaz_y))
            desplaz_y += interlineado
            linea      = palabra + " "
        else:
            linea = prueba
    if linea.strip():
        pantalla.blit(fuente.render(linea.rstrip(), True, color), (x, y + desplaz_y))
        desplaz_y += interlineado
    return desplaz_y


def dibujar_caja(pantalla, rect, color_fondo, color_borde, grosor=2, radio=6):  # Dialogo

    sup = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(sup, color_fondo, sup.get_rect(), border_radius=radio)
    pantalla.blit(sup, rect.topleft)
    pygame.draw.rect(pantalla, color_borde, rect, grosor, border_radius=radio)


# ============================================================================
# Sección 4 hoja de sprite sheets
# ============================================================================

class HojaSprites:

    def __init__(self, ruta: str, ancho_cuadro: int = None, alto_cuadro: int = None,
                 escala: float = ESCALA_GAMEPLAY, alto_destino: int = None,
                 fotogramas: int = 4):
        

        self._cache_frames = {}

        # Tamaño de emergencia para el placeholder cuando ni siquiera
        # se pudo cargar el archivo (y por lo tanto tampoco se puede
        # auto-detectar el tamaño real de cuadro).
        ancho_emergencia = ancho_cuadro or ANCHO_CUADRO_PERSONAJE
        alto_emergencia  = alto_cuadro  or ALTO_CUADRO_PERSONAJE

        if not ruta or not os.path.exists(ruta):
            if ruta:
                print(f"[HojaSprites] No encontrado: {ruta}")
            self._hoja = self._placeholder(ancho_emergencia, alto_emergencia)
        else:
            try:
                hoja_cruda = pygame.image.load(ruta)
                self._hoja = _quitar_fondo_solido(hoja_cruda)
            except pygame.error as err:
                print(f"[HojaSprites] Error: {ruta} -> {err}")
                self._hoja = self._placeholder(ancho_emergencia, alto_emergencia)

        # Auto-detección: si no se especificó el tamaño de cuadro, se
        # calcula a partir de la hoja realmente cargada (ancho total /
        # cantidad de fotogramas, alto total de la hoja).
        if ancho_cuadro is None:
            ancho_cuadro = max(1, math.floor(self._hoja.get_width() / fotogramas))
        if alto_cuadro is None:
            alto_cuadro = self._hoja.get_height()

        self.ancho_cuadro = ancho_cuadro
        self.alto_cuadro  = alto_cuadro

        if alto_destino is not None:
            # Escala automática: todos los personajes que usen
            # alto_destino terminan midiendo lo mismo en pantalla, sin
            # importar la resolución de su hoja original.
            self.escala = alto_destino / alto_cuadro
        else:
            self.escala = escala

        # math.floor() calcula cuántos cuadros de "ancho_cuadro" píxeles
        # entran exactamente en el ancho total de la hoja. Esta misma
        # clase se usa para TODOS los personajes (Benjamín, el caballo,
        # los soldados, Cruz, Arapoty, el Coronel), así que trocear acá
        # con math alcanza para cualquier spritesheet nuevo de 4
        # fotogramas que se agregue al proyecto.
        self.total_cuadros = max(1, math.floor(self._hoja.get_width() / ancho_cuadro))

    @staticmethod
    def _placeholder(ancho, alto):
        sup = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        sup.fill((40, 40, 40, 220))
        pygame.draw.rect(sup, (220, 0, 220), sup.get_rect(), 2)
        return sup

    def obtener_frame(self, indice: int) -> pygame.Surface:
        indice = indice % self.total_cuadros
        if indice in self._cache_frames:
            return self._cache_frames[indice]

        # División exacta con math.floor para ubicar el cuadro "indice"
        # dentro de la hoja, sin depender de que el ancho total sea
        # múltiplo perfecto de ancho_cuadro.
        x_recorte = math.floor(indice * self.ancho_cuadro)
        x_recorte = min(x_recorte, max(0, self._hoja.get_width() - self.ancho_cuadro))
        rect_recorte = pygame.Rect(x_recorte, 0, self.ancho_cuadro, self.alto_cuadro)

        try:
            cuadro = self._hoja.subsurface(rect_recorte).copy()
        except ValueError:
            cuadro = self._placeholder(self.ancho_cuadro, self.alto_cuadro)

        ancho_final = int(self.ancho_cuadro * self.escala)
        alto_final  = int(self.alto_cuadro  * self.escala)

        # pygame.transform.scale() puede perder el colorkey del cuadro
        # original: lo guardamos antes y lo reaplicamos después de
        # escalar (fix del bug de invisibilidad de Benjamín/boleadora).
        colorkey = cuadro.get_colorkey()
        cuadro_escalado = pygame.transform.scale(cuadro, (ancho_final, alto_final))
        if colorkey is not None:
            cuadro_escalado.set_colorkey(colorkey)

        self._cache_frames[indice] = cuadro_escalado
        return cuadro_escalado


# ============================================================================
# Sección 5 guardado y carga de partida
# ============================================================================

def guardar_partida(partida: dict, nombre_escena: str) -> None:

    datos = {
        "capitulo":          nombre_escena,
        "honor":             partida["honor"],
        "salud":             partida["salud"],
        "inventario":        partida["inventario"],
        "plantas_conocidas": partida["plantas_conocidas"],
        "decisiones":        partida["decisiones"],
    }
    try:
        with open(ARCHIVO_GUARDADO, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print(f"[Guardado] {ARCHIVO_GUARDADO}")
    except Exception as err:
        print(f"[Error al guardar] {err}")


def cargar_partida():
    if not os.path.exists(ARCHIVO_GUARDADO):
        return None
    try:
        with open(ARCHIVO_GUARDADO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as err:
        print(f"[Error al cargar] {err}")
        return None


# ============================================================================
# Sección 6 gestor y estado de partida
# ============================================================================

class GestorEscenas:

    def __init__(self, pantalla: pygame.Surface):
        self.pantalla      = pantalla
        self._mapa         = {}
        self.escena_actual = None
        self.nombre_escena = "menu"
        self.partida = {
            "honor":             60,
            "salud":             SALUD_INICIAL,
            "inventario":        [],
            "plantas_conocidas": [],
            "decisiones":        {},
        }

    def registrar(self, nombre: str, clase) -> None:
        self._mapa[nombre] = clase

    def cambiar(self, nombre: str, **argumentos) -> None:
        if nombre not in self._mapa:
            raise KeyError(f"Escena '{nombre}' no registrada.")
        self.nombre_escena = nombre
        self.escena_actual = self._mapa[nombre](self, **argumentos)

    def sumar_honor(self, delta: int) -> None:
        self.partida["honor"] = max(0, min(HONOR_MAXIMO,
                                           self.partida["honor"] + delta))

    def aplicar_guardado(self, datos: dict) -> None:
        for clave in ("honor", "salud", "inventario",
                      "plantas_conocidas", "decisiones"):
            if clave in datos:
                self.partida[clave] = datos[clave]


class EscenaBase:  # Base de todas las escenas

    def __init__(self, gestor: GestorEscenas):
        self.gestor = gestor

    def manejar_evento(self, evento: pygame.event.Event) -> None:
        pass

    def actualizar(self, dt: float) -> None:
        pass

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pass


# ============================================================================
# Sección 7 sistema de dialogo
# ============================================================================

class LineaDialogo:
    def __init__(self, hablante: str, texto: str):
        self.hablante = hablante
        self.texto    = texto


class Opcion:
    def __init__(self, texto: str, efecto_honor: int = 0, resultado: str = ""):
        self.texto        = texto
        self.efecto_honor = efecto_honor
        self.resultado    = resultado


class SistemaDialogo:

    RELLENO    = 22
    ALTO_CAJA  = 210
    MARGEN_INF = 18
    VEL_CHARS  = 2

    def __init__(self):
        self.activo            = False
        self._lineas           = []
        self._opciones         = []
        self._indice           = 0
        self._chars            = 0
        self._tick              = 0
        self._modo_opciones    = False
        self._seleccion        = 0
        self._callback_cerrar  = None

        self._fn = pygame.font.SysFont("Arial", 18, bold=True)
        self._ft = pygame.font.SysFont("Arial", 17)
        self._fo = pygame.font.SysFont("Arial", 16)
        self._fp = pygame.font.SysFont("Arial", 13)

    def iniciar(self, lineas: list, opciones: list = None,
                callback_cerrar=None) -> None:
        self._lineas           = lineas
        self._opciones         = opciones or []
        self._indice           = 0
        self._chars            = 0
        self._tick              = 0
        self._modo_opciones    = False
        self._seleccion        = 0
        self._callback_cerrar  = callback_cerrar
        self.activo            = True

    def cerrar(self) -> None:
        self.activo = False

    def actualizar(self, dt: float) -> None:
        if not self.activo or self._modo_opciones:
            return
        self._tick += 1
        if self._tick % 2 == 0:
            self._chars = min(self._chars + self.VEL_CHARS,
                              len(self._lineas[self._indice].texto))

    def procesar_evento(self, evento: pygame.event.Event):

        if not self.activo:
            return None

        if self._modo_opciones and evento.type == pygame.MOUSEBUTTONDOWN:
            return self._click_opcion(evento.pos)

        if evento.type != pygame.KEYDOWN:
            return None
        if self._modo_opciones:
            return self._navegar(evento.key)
        if evento.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
            self._avanzar()
        return None

    def _avanzar(self) -> None:
        linea = self._lineas[self._indice]
        if self._chars < len(linea.texto):
            self._chars = len(linea.texto)
            return
        self._indice += 1
        if self._indice >= len(self._lineas):
            if self._opciones:
                self._modo_opciones = True
                self._seleccion     = 0
            else:
                self.activo = False
                cb = self._callback_cerrar
                self._callback_cerrar = None
                if cb:
                    cb()
        else:
            self._chars = 0
            self._tick  = 0

    def _navegar(self, tecla):
        if tecla == pygame.K_UP:
            self._seleccion = max(0, self._seleccion - 1)
        elif tecla == pygame.K_DOWN:
            self._seleccion = min(len(self._opciones) - 1, self._seleccion + 1)
        elif tecla in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
            elegida     = self._opciones[self._seleccion]
            self.activo = False
            return elegida
        return None

    def _click_opcion(self, pos_mouse):
        y0   = ALTO_PANTALLA - self.ALTO_CAJA - self.MARGEN_INF
        caja = pygame.Rect(self.RELLENO, y0,
                           ANCHO_PANTALLA - self.RELLENO * 2, self.ALTO_CAJA)
        p = self.RELLENO
        for i, _ in enumerate(self._opciones):
            y_op = caja.y + p + 38 + i * 36
            rect_opcion = pygame.Rect(caja.x + p - 4, y_op - 4,
                                      caja.width - p * 2 + 8, 32)
            if rect_opcion.collidepoint(pos_mouse):
                elegida     = self._opciones[i]
                self.activo = False
                return elegida
        return None

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if not self.activo:
            return
        y0   = ALTO_PANTALLA - self.ALTO_CAJA - self.MARGEN_INF
        caja = pygame.Rect(self.RELLENO, y0,
                           ANCHO_PANTALLA - self.RELLENO * 2, self.ALTO_CAJA)
        dibujar_caja(pantalla, caja, COLOR_CAJA_DLG, COLOR_TIERRA_BORDE, 2, 8)
        if self._modo_opciones:
            self._dibujar_opciones(pantalla, caja)
        else:
            self._dibujar_linea(pantalla, caja)

    def _dibujar_linea(self, pantalla, caja):
        p     = self.RELLENO
        linea = self._lineas[self._indice]
        nombre_s = self._fn.render(linea.hablante, True, COLOR_HONOR_ORO)
        pantalla.blit(nombre_s, (caja.x + p, caja.y + p))
        sep_y = caja.y + p + nombre_s.get_height() + 4
        pygame.draw.line(pantalla, COLOR_TIERRA_BORDE,
                         (caja.x + p, sep_y), (caja.right - p, sep_y), 1)
        texto_vis = linea.texto[:self._chars]
        dibujar_texto_envuelto(pantalla, texto_vis, self._ft, COLOR_BLANCO,
                               caja.x + p, sep_y + 8, caja.width - p * 2)
        if self._chars >= len(linea.texto):
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                pista = self._fp.render(" Espacio", True, (175, 175, 175))
                pantalla.blit(pista, (caja.right - pista.get_width() - p,
                                      caja.bottom - pista.get_height() - p))

    def _dibujar_opciones(self, pantalla, caja):
        p   = self.RELLENO
        tit = self._fn.render("¿Qué haces?", True, COLOR_HONOR_ORO)
        pantalla.blit(tit, (caja.x + p, caja.y + p))
        for i, op in enumerate(self._opciones):
            y_op   = caja.y + p + 38 + i * 36
            es_sel = (i == self._seleccion)
            if es_sel:
                r = pygame.Rect(caja.x + p - 4, y_op - 4,
                                caja.width - p * 2 + 8, 32)
                dibujar_caja(pantalla, r, (*COLOR_TIERRA, 180),
                             COLOR_HONOR_ORO, 1, 4)
            color = COLOR_HONOR_ORO if es_sel else COLOR_BLANCO
            pref  = "> " if es_sel else "  "
            pantalla.blit(self._fo.render(pref + op.texto, True, color),
                          (caja.x + p + 6, y_op))
        op_a = self._opciones[self._seleccion]
        if op_a.efecto_honor != 0:
            signo = "+" if op_a.efecto_honor > 0 else ""
            col   = COLOR_VERDE_VIDA if op_a.efecto_honor > 0 else COLOR_ROJO_DANIO
            h_txt = self._fp.render(f"Honor: {signo}{op_a.efecto_honor}", True, col)
            pantalla.blit(h_txt, (caja.right - h_txt.get_width() - p,
                                  caja.bottom - h_txt.get_height() - p))


# ============================================================================
# Sección 8 ayudas de pantalla
# ============================================================================

def _dibujar_intro_textual(pantalla, titulo, paginas, pagina, f_tit, f_ital, f_ctrl):
    overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
    overlay.fill(COLOR_OVERLAY_INTRO)
    pantalla.blit(overlay, (0, 0))
    tit = f_tit.render(titulo, True, COLOR_HONOR_ORO)
    pantalla.blit(tit, (ANCHO_PANTALLA // 2 - tit.get_width() // 2, 90))
    if pagina < len(paginas):
        for i, linea in enumerate(paginas[pagina].split("\n")):
            s = f_ital.render(linea, True, COLOR_BLANCO)
            pantalla.blit(s, (ANCHO_PANTALLA // 2 - s.get_width() // 2, 268 + i * 40))
    pista = f_ctrl.render("[Espacio] continuar", True, (140, 140, 140))
    pantalla.blit(pista, (ANCHO_PANTALLA // 2 - pista.get_width() // 2, ALTO_PANTALLA - 52))


def _dibujar_fundido(pantalla, timer, duracion, texto, fuente):
    progreso = 1.0 - timer / duracion
    alpha    = int(255 * max(0.0, min(1.0, progreso)))
    ov = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    ov.set_alpha(alpha)
    ov.fill(COLOR_NEGRO)
    pantalla.blit(ov, (0, 0))
    if alpha > 100:
        sup = fuente.render(texto, True, COLOR_HONOR_ORO)
        sup.set_alpha(alpha)
        pantalla.blit(sup, (ANCHO_PANTALLA // 2 - sup.get_width() // 2,
                            ALTO_PANTALLA  // 2))


def _dibujar_etiqueta_capitulo(pantalla, fuente, titulo, region):
    txt   = fuente.render(f"{titulo}  ·  {region}", True, (200, 195, 185))
    fondo = pygame.Surface((txt.get_width() + 16, txt.get_height() + 6), pygame.SRCALPHA)
    fondo.fill((0, 0, 0, 130))
    x = ANCHO_PANTALLA // 2 - fondo.get_width() // 2
    pantalla.blit(fondo, (x, 3))
    pantalla.blit(txt,   (x + 8, 6))


# ============================================================================
# Sección 9 menu principal (imagen limpia + zonas invisibles)
# ============================================================================

class MenuPrincipal(EscenaBase):

    ZONAS_BOTONES = [
        ("empezar", pygame.Rect(90, 440, 270, 50)),   # ajustar a "Comenzar"
        ("cargar",  pygame.Rect(90, 502, 270, 50)),   # ajustar a "Cargar partida"
        ("salir",   pygame.Rect(90, 564, 270, 50)),   # ajustar a "Salir"
    ]

    def __init__(self, gestor: GestorEscenas):
        super().__init__(gestor)
        self._fondo          = cargar_imagen(RUTA_FONDO_MENU, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self._tiene_guardado = os.path.exists(ARCHIVO_GUARDADO)
        self._mostrar_debug  = False   # True para ver Rects invisibles en rojo
        reproducir_musica(RUTA_MUSICA_MENU)

    def manejar_evento(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for accion, rect in self.ZONAS_BOTONES:
                if rect.collidepoint(evento.pos):
                    self._ejecutar(accion)
                    break
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self._ejecutar("empezar")
            elif evento.key == pygame.K_ESCAPE:
                self._ejecutar("salir")

    def _ejecutar(self, accion: str) -> None:
        if accion == "empezar":
            self.gestor.cambiar("capitulo_3")
        elif accion == "cargar":
            datos = cargar_partida()
            if datos:
                self.gestor.aplicar_guardado(datos)
                self.gestor.cambiar("capitulo_3")
        elif accion == "salir":
            pygame.quit()
            sys.exit()

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.blit(self._fondo, (0, 0))
        if self._mostrar_debug:
            for _, rect in self.ZONAS_BOTONES:
                pygame.draw.rect(pantalla, (255, 0, 0), rect, 2)


# ============================================================================
# Sección 10 cámara horizontal (reutilizable por cualquier escena/ruta)
# ============================================================================

class Camara:
    

    def __init__(self, ancho_mundo: int = ANCHO_PANTALLA):
        self.ancho_mundo = ancho_mundo
        self.desplaz_x   = 0

    def actualizar(self, pos_jugador_x: float) -> None:
        objetivo       = pos_jugador_x - MARGEN_CAM_X
        limite         = max(0, self.ancho_mundo - ANCHO_PANTALLA)
        self.desplaz_x = max(0, min(objetivo, limite))

    def aplicar_x(self, x_mundo: float) -> int:
        return int(x_mundo - self.desplaz_x)


# ============================================================================
# Sección 10bis gestor de fondos múltiples (niveles/zonas + capas)
# ============================================================================

class SegmentoFondo:
    

    __slots__ = ("imagen", "x_mundo", "ancho")

    def __init__(self, imagen: pygame.Surface, x_mundo: float, ancho: int):
        self.imagen  = imagen
        self.x_mundo = x_mundo
        self.ancho   = ancho


class GestorFondos:
    

    def __init__(self, ancho_pantalla: int = ANCHO_PANTALLA):
        self._ancho_pantalla = ancho_pantalla
        self._niveles = {}          # nombre_nivel -> {nombre_capa: [tramos]}
        self.nivel_actual = None

    def registrar_nivel(self, nombre_nivel: str, capas: dict,
                        ancho_tramo: int, alto: int = ALTO_PANTALLA) -> None:
        
        capas_cargadas = {}
        for nombre_capa, rutas in capas.items():
            tramos = []
            for indice, ruta in enumerate(rutas):
                imagen = cargar_imagen(ruta, (ancho_tramo, alto))
                x_mundo = indice * ancho_tramo
                tramos.append(SegmentoFondo(imagen, x_mundo, ancho_tramo))
            capas_cargadas[nombre_capa] = tramos

        self._niveles[nombre_nivel] = capas_cargadas
        if self.nivel_actual is None:
            self.nivel_actual = nombre_nivel

    def cambiar_nivel(self, nombre_nivel: str) -> None:
        
        if nombre_nivel not in self._niveles:
            raise KeyError(f"Nivel de fondo '{nombre_nivel}' no registrado.")
        self.nivel_actual = nombre_nivel

    def ancho_mundo_actual(self) -> int:
        
        capas = self._niveles.get(self.nivel_actual, {})
        if not capas:
            return self._ancho_pantalla
        return max(sum(tramo.ancho for tramo in tramos) for tramos in capas.values())

    def dibujar(self, pantalla: pygame.Surface, camara: Camara) -> None:
        
        capas = self._niveles.get(self.nivel_actual)
        if not capas:
            return

        for tramos in capas.values():
            for tramo in tramos:
                x_pantalla = camara.aplicar_x(tramo.x_mundo)

                # Descarte visual (culling): un tramo es visible si su
                # rango en pantalla [x_pantalla, x_pantalla + ancho] se
                # superpone con el rango visible [0, ancho_pantalla].
                # No alcanza con mirar solo el borde izquierdo del
                # tramo (ese era un bug del código anterior).
                visible = (x_pantalla + tramo.ancho > 0
                          and x_pantalla < self._ancho_pantalla)
                if visible:
                    pantalla.blit(tramo.imagen, (x_pantalla, 0))


# ============================================================================
# Sección 11 centinela, soldado, boleadora, Cruz, Arapoty, Coronel
# ============================================================================

class Centinela:
    

    ANCHO_CAJA = int(ANCHO_VIS_PERSONAJE * 0.55)
    ALTO_CAJA  = ALTO_VIS_PERSONAJE

    def __init__(self, x: int, y: int, limite_izq: int, limite_der: int):
        self.x_mundo = float(x)
        self._limite_izq = limite_izq
        self._limite_der = limite_der
        self._velocidad = 60.0
        self._direccion = 1

        # Sprite del soldado para centinela
        self._hoja = HojaSprites(RUTA_SOLDADO_AVANCE, ancho_cuadro=400, alto_cuadro=396,
                                alto_destino=ALTO_VIS_PERSONAJE)
        self._cuadro = 0
        self._timer_anim = 0.0

        # Rect de colisión basado en el tamaño del sprite
        self.rect = pygame.Rect(
            int(self.x_mundo) + (ANCHO_VIS_PERSONAJE - self.ANCHO_CAJA) // 2,
            SUELO - self.ALTO_CAJA,
            self.ANCHO_CAJA, self.ALTO_CAJA
        )

        self.rect_vision = pygame.Rect(0, 0, 160, 100)
        self.tiempo_sospecha = 0.0
        self._color_vision = (255, 255, 255, 60)

    def actualizar(self, dt: float) -> None:
        self.x_mundo += self._velocidad * self._direccion * dt
        if self.x_mundo >= self._limite_der:
            self._direccion = -1
        elif self.x_mundo <= self._limite_izq:
            self._direccion = 1

        # Actualizar rect de colisión
        self.rect.x = int(self.x_mundo) + (ANCHO_VIS_PERSONAJE - self.ANCHO_CAJA) // 2

        # Actualizar animación
        self._timer_anim += dt
        if self._timer_anim >= 0.18:
            self._timer_anim = 0.0
            self._cuadro = (self._cuadro + 1) % 4

        self.rect_vision.y = self.rect.y
        if self._direccion == 1:
            self.rect_vision.left = self.rect.right
        else:
            self.rect_vision.right = self.rect.left

    def detectar(self, rect_jugador: pygame.Rect, jugador_oculto: bool, dt: float) -> bool:
        expuesto = self.rect_vision.colliderect(rect_jugador) and not jugador_oculto

        if expuesto:
            self.tiempo_sospecha += dt
        else:
            self.tiempo_sospecha -= dt * 2.0

        self.tiempo_sospecha = max(0.0, min(self.tiempo_sospecha, LIMITE_SOSPECHA_CENTINELA))

        if self.tiempo_sospecha <= 0:
            self._color_vision = (255, 255, 255, 60)
            return False
        elif self.tiempo_sospecha < LIMITE_SOSPECHA_CENTINELA:
            self._color_vision = (255, 255, 0, 120)
            return False
        else:
            self._color_vision = (255, 0, 0, 150)
            return True

    def reiniciar_sospecha(self) -> None:
        self.tiempo_sospecha = 0.0
        self._color_vision = (255, 255, 255, 60)

    def dibujar(self, pantalla: pygame.Surface, camara: Camara) -> None:
        frame = self._hoja.obtener_frame(self._cuadro)
        
        # Voltear sprite según dirección
        if self._direccion == -1:  # Mirando a la izquierda
            frame = pygame.transform.flip(frame, True, False)

        x_pan = camara.aplicar_x(self.x_mundo)
        y_pan = SUELO - ALTO_VIS_PERSONAJE
        pantalla.blit(frame, (x_pan, y_pan))

        # Cono de visión invisible (no se dibuja)
        # vision_pantalla = pygame.Rect(camara.aplicar_x(self.rect_vision.x), self.rect_vision.y,
        #                               self.rect_vision.width, self.rect_vision.height)
        # sup_vision = pygame.Surface((vision_pantalla.width, vision_pantalla.height), pygame.SRCALPHA)
        # sup_vision.fill(self._color_vision)
        # pantalla.blit(sup_vision, vision_pantalla.topleft)

        if self.tiempo_sospecha > 0:
            porcentaje  = self.tiempo_sospecha / LIMITE_SOSPECHA_CENTINELA
            barra_ancho = 40
            pygame.draw.rect(pantalla, COLOR_NEGRO, (x_pan, self.rect.y - 15, barra_ancho, 8))
            pygame.draw.rect(pantalla, (255, 255, 0),
                             (x_pan, self.rect.y - 15, barra_ancho * porcentaje, 8))


class Soldado:
    

    ANCHO_CAJA = int(ANCHO_VIS_PERSONAJE * 0.55)
    ALTO_CAJA  = ALTO_VIS_PERSONAJE

    def __init__(self, x_mundo: float):
        self.x_mundo   = float(x_mundo)
        self.estado    = "avanzando"   # avanzando | tambaleando | caido
        self.activo    = True
        self.impactos  = 0

        self._hoja_avance = HojaSprites(RUTA_SOLDADO_AVANCE, ancho_cuadro=400, alto_cuadro=396,
                                        alto_destino=ALTO_VIS_PERSONAJE)
        self._hoja_caido  = HojaSprites(RUTA_SOLDADO_CAIDO, ancho_cuadro=400, alto_cuadro=393,
                                        alto_destino=ALTO_VIS_PERSONAJE)
        self._cuadro     = 0
        self._timer_anim = 0.0

        self.rect = pygame.Rect(
            int(self.x_mundo) + (ANCHO_VIS_PERSONAJE - self.ANCHO_CAJA) // 2,
            SUELO - self.ALTO_CAJA,
            self.ANCHO_CAJA, self.ALTO_CAJA
        )

    def actualizar(self, dt: float, objetivo_x: float) -> bool:
        hizo_contacto = False

        if self.estado in ("avanzando", "tambaleando"):
            velocidad = VELOCIDAD_SOLDADO_PATRULLA * (0.35 if self.estado == "tambaleando" else 1.0)
            if self.x_mundo > objetivo_x:
                self.x_mundo -= velocidad * dt
            else:
                self.x_mundo += velocidad * dt
            self.rect.x = int(self.x_mundo) + (ANCHO_VIS_PERSONAJE - self.ANCHO_CAJA) // 2

            if self.estado == "avanzando" and abs(self.x_mundo - objetivo_x) <= DISTANCIA_ATAQUE_SOLDADO:
                hizo_contacto = True

            self._timer_anim += dt
            if self._timer_anim >= 0.18:
                self._timer_anim = 0.0
                self._cuadro = (self._cuadro + 1) % 4

        elif self.estado == "caido":
            self._timer_anim += dt
            if self._timer_anim >= 0.18:
                self._timer_anim = 0.0
                if self._cuadro < 3:
                    self._cuadro += 1

        return hizo_contacto

    def recibir_impacto(self) -> None:
        self.impactos += 1
        if self.impactos >= IMPACTOS_PARA_DERRIBAR:
            self.estado      = "caido"
            self._cuadro     = 0
            self._timer_anim = 0.0
        else:
            self.estado = "tambaleando"

    def dibujar(self, pantalla: pygame.Surface, camara: Camara) -> None:
        if not self.activo:
            return
        hoja  = self._hoja_caido if self.estado == "caido" else self._hoja_avance
        frame = hoja.obtener_frame(self._cuadro)
        x_pan = camara.aplicar_x(self.x_mundo)
        y_pan = SUELO - ALTO_VIS_PERSONAJE
        if self.estado == "tambaleando":
            if (pygame.time.get_ticks() // 150) % 2 == 0:
                frame = frame.copy()
                frame.set_alpha(140)
        pantalla.blit(frame, (x_pan, y_pan))


class Boleadora:
    

    ANCHO = 68
    ALTO  = 68

    def __init__(self, x_mundo: float, direccion: int, ancho_mundo: int):
        self.x_mundo     = float(x_mundo)
        self.direccion   = direccion
        self.activo      = True
        self._ancho_mundo = ancho_mundo
        self._imagen     = cargar_imagen(RUTA_BOLEADORA, (self.ANCHO, self.ALTO))
        self.rect = pygame.Rect(int(self.x_mundo), SUELO - 120, self.ANCHO, self.ALTO)

    def actualizar(self, dt: float) -> None:
        self.x_mundo += VELOCIDAD_BOLEADORA * self.direccion * dt
        self.rect.x   = int(self.x_mundo)
        if self.x_mundo < -100 or self.x_mundo > self._ancho_mundo + 100:
            self.activo = False

    def dibujar(self, pantalla: pygame.Surface, camara: Camara) -> None:
        if not self.activo:
            return
        x_pan = camara.aplicar_x(self.x_mundo)
        pantalla.blit(self._imagen, (x_pan, self.rect.y))


class CompaneroCruz:
    

    def __init__(self):
        # alto_destino=ALTO_VIS_PERSONAJE: la hoja de Cruz viene en una
        # resolución distinta a la de Benjamín (516x512 contra 400x396),
        # así que normalizamos por altura para que mida exactamente lo
        # mismo en pantalla que el resto de los personajes.
        self._hoja = HojaSprites(RUTA_CRUZ_LIBRE, ancho_cuadro=516, alto_cuadro=512,
                                 alto_destino=ALTO_VIS_PERSONAJE)
        self._cuadro     = 0
        self._timer_anim = 0.0
        self._fuente     = pygame.font.SysFont("Arial", 13)

    def actualizar(self, dt: float, en_movimiento: bool = False) -> None:
        self._timer_anim += dt
        intervalo = 0.13 if en_movimiento else 0.5
        if self._timer_anim >= intervalo:
            self._timer_anim = 0.0
            if en_movimiento:
                self._cuadro = (self._cuadro % 3) + 1
            else:
                self._cuadro = 0

    def dibujar(self, pantalla: pygame.Surface, x_mundo: float,
                camara: Camara = None, oculto: bool = False) -> None:
        frame = self._hoja.obtener_frame(self._cuadro)
        if oculto:
            # Se agacha en la cobertura junto con Benjamín: se atenúa y
            # no muestra su cartel de nombre, igual que hace Chicha.
            frame = frame.copy()
            frame.set_alpha(140)

        x_pan = camara.aplicar_x(x_mundo) if camara else int(x_mundo)
        y_pan = SUELO - frame.get_height()
        pantalla.blit(frame, (x_pan, y_pan))

        if oculto:
            return

        etq   = self._fuente.render("Cruz", True, COLOR_BLANCO)
        ex    = x_pan + frame.get_width() // 2 - etq.get_width() // 2
        ey    = y_pan - 16
        fondo = pygame.Surface((etq.get_width() + 8, etq.get_height() + 4), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 145))
        pantalla.blit(fondo, (ex - 4, ey - 2))
        pantalla.blit(etq,   (ex, ey))


class Arapoty:
    

    ANCHO_CAJA = int(ANCHO_VIS_PERSONAJE * 0.6)
    ALTO_CAJA  = ALTO_VIS_PERSONAJE

    def __init__(self, x_mundo: float):
        self.x_mundo = float(x_mundo)
        self.nombre  = "Arapoty"
        self.activo  = True

        # Usar auto-detección de tamaño para evitar bugs con dimensiones incorrectas
        self._hoja        = HojaSprites(RUTA_ARAPOTY,
                                        alto_destino=ALTO_VIS_PERSONAJE)
        self._cuadro       = 0
        self._timer_anim   = 0.0
        self._fuente       = pygame.font.SysFont("Arial", 13)

        # Obtener el primer frame para calcular dimensiones reales
        frame_inicial = self._hoja.obtener_frame(0)
        ancho_real = frame_inicial.get_width()
        alto_real = frame_inicial.get_height()

        self.rect = pygame.Rect(
            int(self.x_mundo),
            SUELO - alto_real,
            ancho_real, alto_real
        )

    def actualizar(self, dt: float) -> None:
        self._timer_anim += dt
        if self._timer_anim >= 0.5:
            self._timer_anim = 0.0
            self._cuadro = (self._cuadro + 1) % 4

    def cerca_de(self, rect_jugador: pygame.Rect, dist: int = 110) -> bool:
        return self.rect.colliderect(rect_jugador.inflate(dist, dist))

    def dibujar(self, pantalla: pygame.Surface, camara: Camara, mostrar_pista: bool = False) -> None:
        if not self.activo:
            return
        frame = self._hoja.obtener_frame(self._cuadro)
        x_pan = camara.aplicar_x(self.x_mundo)
        y_pan = SUELO - frame.get_height()
        pantalla.blit(frame, (x_pan, y_pan))

        etq   = self._fuente.render(f"▼ {self.nombre}", True, COLOR_BLANCO)
        ex    = x_pan + frame.get_width() // 2 - etq.get_width() // 2
        ey    = y_pan - 18
        fondo = pygame.Surface((etq.get_width() + 8, etq.get_height() + 4), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 145))
        pantalla.blit(fondo, (ex - 4, ey - 2))
        pantalla.blit(etq,   (ex, ey))

        if mostrar_pista:
            pista = self._fuente.render("[E] Hablar", True, COLOR_HONOR_ORO)
            px = x_pan + frame.get_width() // 2 - pista.get_width() // 2
            py = ey - 18
            fondo2 = pygame.Surface((pista.get_width() + 8, pista.get_height() + 4), pygame.SRCALPHA)
            fondo2.fill((0, 0, 0, 165))
            pantalla.blit(fondo2, (px - 4, py - 2))
            pantalla.blit(pista, (px, py))


class Coronel:
    

    ANCHO_CAJA = int(ANCHO_VIS_PERSONAJE * 0.6)
    ALTO_CAJA  = ALTO_VIS_PERSONAJE

    def __init__(self, x_mundo: float):
        self.x_mundo = float(x_mundo)
        # Usar escala más grande para la sala del Coronel
        alto_destino_coronel = int(ALTO_CUADRO_PERSONAJE * ESCALA_SALA_CORONEL)
        # Usar auto-detección de tamaño para evitar bugs con dimensiones incorrectas
        self._hoja   = HojaSprites(RUTA_CORONEL,
                                   alto_destino=alto_destino_coronel)
        self._cuadro     = 0
        self._timer_anim = 0.0
        
        # Sistema de combate
        self.vida = VIDA_CORONEL_MAXIMA
        self.esta_combatiendo = False
        self._velocidad_ataque = 180.0  # px/seg, velocidad de carga hacia el jugador
        self._atacando = False
        self._timer_ataque = 0.0
        self._cooldown_ataque = 0.0

        # Obtener el primer frame para calcular dimensiones reales
        frame_inicial = self._hoja.obtener_frame(0)
        ancho_real = frame_inicial.get_width()
        alto_real = frame_inicial.get_height()

        self.rect = pygame.Rect(
            int(self.x_mundo),
            SUELO - alto_real,
            ancho_real, alto_real
        )

    def actualizar(self, dt: float, x_jugador: float) -> bool:
        
        self._timer_anim += dt
        if self._timer_anim >= 0.6:
            self._timer_anim = 0.0
            self._cuadro = (self._cuadro + 1) % 4

        daño_instantaneo = False

        if self.esta_combatiendo:
            # Cooldown entre ataques
            if self._cooldown_ataque > 0:
                self._cooldown_ataque -= dt
            else:
                # Iniciar carga hacia el jugador
                if not self._atacando:
                    self._atacando = True
                    self._timer_ataque = 0.0

                # Moverse hacia el jugador durante el ataque
                if self._atacando:
                    self._timer_ataque += dt
                    if self.x_mundo > x_jugador:
                        self.x_mundo -= self._velocidad_ataque * dt
                    else:
                        self.x_mundo += self._velocidad_ataque * dt

                    # Verificar colisión con el jugador
                    self.rect.x = int(self.x_mundo)
                    rect_jugador = pygame.Rect(int(x_jugador), SUELO - ALTO_VIS_PERSONAJE,
                                            int(ANCHO_VIS_PERSONAJE * 0.5), ALTO_VIS_PERSONAJE)
                    
                    if self.rect.colliderect(rect_jugador):
                        daño_instantaneo = True
                        self._atacando = False
                        self._cooldown_ataque = 1.5  # Cooldown después de un ataque
                        # Volver a posición original
                        self.x_mundo = float(self._posicion_original)
                    elif self._timer_ataque >= 1.0:  # Duración del ataque
                        self._atacando = False
                        self._cooldown_ataque = 0.8
                        # Volver a posición original
                        self.x_mundo = float(self._posicion_original)

        return daño_instantaneo

    def recibir_golpe(self) -> bool:
        
        self.vida -= 1
        return self.vida <= 0

    def iniciar_combate(self):
        
        self.esta_combatiendo = True
        self._posicion_original = self.x_mundo  # Guardar posición original

    def dibujar(self, pantalla: pygame.Surface, camara: Camara) -> None:
        frame = self._hoja.obtener_frame(self._cuadro)
        # Mira hacia la izquierda, hacia donde entra Benjamín
        frame = pygame.transform.flip(frame, True, False)
        x_pan = camara.aplicar_x(self.x_mundo)
        y_pan = SUELO - frame.get_height()
        pantalla.blit(frame, (x_pan, y_pan))

        # Dibujar barra de vida si está combatiendo
        if self.esta_combatiendo:
            barra_ancho = 60
            barra_alto = 8
            x_barra = x_pan + frame.get_width() // 2 - barra_ancho // 2
            y_barra = y_pan - 20
            
            # Fondo negro
            pygame.draw.rect(pantalla, COLOR_NEGRO, (x_barra, y_barra, barra_ancho, barra_alto))
            # Barra de vida roja
            vida_porcentaje = self.vida / VIDA_CORONEL_MAXIMA
            pygame.draw.rect(pantalla, COLOR_ROJO_DANIO, 
                           (x_barra, y_barra, barra_ancho * vida_porcentaje, barra_alto))
            # Borde
            pygame.draw.rect(pantalla, COLOR_BLANCO, (x_barra, y_barra, barra_ancho, barra_alto), 1)


# ============================================================================
# Sección 12 sistema de botánica (mini-juego de mezcla de plantas)
# ============================================================================

class MenuBotanico:
    

    RECETAS = {
        tuple(sorted(["Yerba Mate", "Burrito"])): "Mate Calmante",
        tuple(sorted(["Uña de Gato", "Yerba Mate"])): "Infusión Sanadora",
    }

    def __init__(self, ancho_pantalla: int, alto_pantalla: int, inventario: list):
        self._fuente = pygame.font.SysFont("Georgia", 20)
        self.inventario = inventario  # lista de nombres (strings)
        self._ranuras = []
        self._mensaje = "Arapoty te enseña: elegí dos plantas para combinarlas."

        self._rect_panel = pygame.Rect(ancho_pantalla // 2 - 250,
                                       alto_pantalla // 2 - 150, 500, 300)
        self._rect_boton = pygame.Rect(self._rect_panel.centerx - 75,
                                       self._rect_panel.bottom - 60, 150, 40)
        self._rect_boton_cerrar = pygame.Rect(self._rect_panel.right - 60, self._rect_panel.top + 10, 50, 30)
        self._rects_inventario = []
        self._rect_ranura1 = pygame.Rect(self._rect_panel.x + 100,
                                         self._rect_panel.y + 100, 100, 100)
        self._rect_ranura2 = pygame.Rect(self._rect_panel.x + 300,
                                         self._rect_panel.y + 100, 100, 100)

    def manejar_evento(self, evento: pygame.event.Event) -> None:
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return
        pos_raton = evento.pos

        # Botón cerrar
        if self._rect_boton_cerrar.collidepoint(pos_raton):
            return "cerrar"

        if self._rect_boton.collidepoint(pos_raton):
            self._intentar_mezcla()
            return

        for rect, item in self._rects_inventario:
            if rect.collidepoint(pos_raton):
                if len(self._ranuras) < 2:
                    self._ranuras.append(item)
                    self.inventario.remove(item)
                    self._mensaje = f"Añadiste {item}."
                else:
                    self._mensaje = "Las ranuras están llenas."
                return

        if self._rect_ranura1.collidepoint(pos_raton) and len(self._ranuras) >= 1:
            self.inventario.append(self._ranuras.pop(0))
            self._mensaje = "Planta devuelta al inventario."
            return

        if self._rect_ranura2.collidepoint(pos_raton) and len(self._ranuras) == 2:
            self.inventario.append(self._ranuras.pop(1))
            self._mensaje = "Planta devuelta al inventario."
            return

    def _intentar_mezcla(self) -> None:
        if len(self._ranuras) < 2:
            self._mensaje = "Necesitás 2 ingredientes para mezclar."
            return

        clave = tuple(sorted(self._ranuras))
        if clave in self.RECETAS:
            resultado = self.RECETAS[clave]
            self._mensaje = f"¡Éxito! Preparaste: {resultado}"
            self.inventario.append(resultado)
            self._ranuras.clear()
        else:
            self._mensaje = "Esa mezcla no combina. Probá con otras plantas."
            self.inventario.extend(self._ranuras)
            self._ranuras.clear()

    def dibujar(self, pantalla: pygame.Surface) -> None:
        sombra = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 150))
        pantalla.blit(sombra, (0, 0))

        dibujar_caja(pantalla, self._rect_panel, (30, 35, 20, 230), COLOR_TIERRA_BORDE, 3, 10)

        # Título
        tit = self._fuente.render("Mortero de Arapoty", True, COLOR_HONOR_ORO)
        msg = self._fuente.render(self._mensaje, True, COLOR_BLANCO)
        pantalla.blit(tit, (self._rect_panel.centerx - tit.get_width() // 2, self._rect_panel.y + 15))
        pantalla.blit(msg, (self._rect_panel.centerx - msg.get_width() // 2, self._rect_panel.y + 50))

        # Botón cerrar
        color_boton_cerrar = (180, 60, 60) if self._rect_boton_cerrar.collidepoint(pygame.mouse.get_pos()) else (150, 50, 50)
        pygame.draw.rect(pantalla, color_boton_cerrar, self._rect_boton_cerrar, border_radius=5)
        texto_cerrar = self._fuente.render("X", True, COLOR_BLANCO)
        pantalla.blit(texto_cerrar, (self._rect_boton_cerrar.centerx - texto_cerrar.get_width() // 2,
                                     self._rect_boton_cerrar.centery - texto_cerrar.get_height() // 2))

        pygame.draw.rect(pantalla, (55, 60, 35), self._rect_ranura1, border_radius=5)
        pygame.draw.rect(pantalla, (55, 60, 35), self._rect_ranura2, border_radius=5)

        if len(self._ranuras) >= 1:
            t1 = self._fuente.render(self._ranuras[0], True, COLOR_BLANCO)
            pantalla.blit(t1, (self._rect_ranura1.centerx - t1.get_width() // 2,
                              self._rect_ranura1.centery - t1.get_height() // 2))
        if len(self._ranuras) == 2:
            t2 = self._fuente.render(self._ranuras[1], True, COLOR_BLANCO)
            pantalla.blit(t2, (self._rect_ranura2.centerx - t2.get_width() // 2,
                              self._rect_ranura2.centery - t2.get_height() // 2))

        signo = self._fuente.render("+", True, COLOR_HONOR_ORO)
        pantalla.blit(signo, (self._rect_panel.centerx - signo.get_width() // 2,
                              self._rect_ranura1.centery - signo.get_height() // 2))

        color_boton = (95, 80, 45) if self._rect_boton.collidepoint(pygame.mouse.get_pos()) else (70, 60, 35)
        pygame.draw.rect(pantalla, color_boton, self._rect_boton, border_radius=5)
        pygame.draw.rect(pantalla, COLOR_HONOR_ORO, self._rect_boton, 2, border_radius=5)
        tb = self._fuente.render("Mezclar", True, COLOR_BLANCO)
        pantalla.blit(tb, (self._rect_boton.centerx - tb.get_width() // 2,
                          self._rect_boton.centery - tb.get_height() // 2))

        t_inv = self._fuente.render("Tu inventario:", True, COLOR_HONOR_ORO)
        pantalla.blit(t_inv, (self._rect_panel.x + 20, self._rect_panel.bottom + 10))

        self._rects_inventario.clear()
        x_obj = self._rect_panel.x + 20
        for i, item in enumerate(self.inventario):
            r_item = pygame.Rect(x_obj + (i * 130), self._rect_panel.bottom + 40, 120, 30)
            self._rects_inventario.append((r_item, item))
            pygame.draw.rect(pantalla, (70, 70, 70), r_item, border_radius=4)
            t_obj = self._fuente.render(item, True, COLOR_BLANCO)
            pantalla.blit(t_obj, (r_item.centerx - t_obj.get_width() // 2,
                                 r_item.centery - t_obj.get_height() // 2))

class MenuInventario:
    
    
    # Efectos de las yerbas/objetos
    EFECTOS_OBJETOS = {
        "Mate Calmante": {"vida": 25, "mensaje": "Recuperaste 25 vida con el mate calmante."},
        "Infusión Sanadora": {"vida": 30, "mensaje": "Recuperaste 30 vida con la infusión sanadora."},
        "Yerba Mate": {"vida": 10, "mensaje": "Masticaste yerba mate. +10 vida."},
        "Burrito": {"vida": 10, "mensaje": "Masticaste burrito. +10 vida."},
        "Uña de Gato": {"vida": 10, "mensaje": "Masticaste uña de gato. +10 vida."},
        "Boldo": {"vida": 10, "mensaje": "Masticaste boldo. +10 vida."},
    }
    
    def __init__(self, ancho_pantalla: int, alto_pantalla: int, inventario: list, salud_maxima: int):
        self._fuente = pygame.font.SysFont("Georgia", 18)
        self.inventario = inventario
        self._salud_maxima = salud_maxima
        self._mensaje = "Selecciona un objeto para consumirlo."
        self._vida_recuperada = 0
        
        self._rect_panel = pygame.Rect(ancho_pantalla // 2 - 250,
                                       alto_pantalla // 2 - 200, 500, 400)
        self._rect_boton_cerrar = pygame.Rect(self._rect_panel.right - 60, self._rect_panel.top + 10, 50, 30)
        self._rects_inventario = []
        
    def manejar_evento(self, evento: pygame.event.Event) -> None:
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return
        
        pos_raton = evento.pos
        
        # Botón cerrar
        if self._rect_boton_cerrar.collidepoint(pos_raton):
            return "cerrar"
        
        # Click en objetos del inventario
        for rect, item in self._rects_inventario:
            if rect.collidepoint(pos_raton):
                self._consumir_objeto(item)
                return
        
        return None
    
    def _consumir_objeto(self, item: str) -> None:
        
        if item in self.EFECTOS_OBJETOS:
            efecto = self.EFECTOS_OBJETOS[item]
            if item in self.inventario:
                self.inventario.remove(item)
                self._mensaje = efecto["mensaje"]
                self._vida_recuperada = efecto["vida"]
            else:
                self._mensaje = "Ya no tienes ese objeto."
                self._vida_recuperada = 0
        else:
            self._mensaje = "Ese objeto no se puede consumir."
            self._vida_recuperada = 0
    
    def obtener_vida_recuperada(self) -> int:
        
        if hasattr(self, '_vida_recuperada'):
            vida = self._vida_recuperada
            self._vida_recuperada = 0
            return vida
        return 0
    
    def obtener_salud_recuperada(self, item: str) -> int:
        
        if item in self.EFECTOS_OBJETOS:
            return self.EFECTOS_OBJETOS[item].get("vida", 0)
        return 0
    
    def dibujar(self, pantalla: pygame.Surface, salud_actual: int) -> None:
        sombra = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 150))
        pantalla.blit(sombra, (0, 0))
        
        dibujar_caja(pantalla, self._rect_panel, (30, 35, 20, 230), COLOR_TIERRA_BORDE, 3, 10)
        
        # Título
        tit = self._fuente.render("Inventario", True, COLOR_HONOR_ORO)
        pantalla.blit(tit, (self._rect_panel.centerx - tit.get_width() // 2, self._rect_panel.y + 15))
        
        # Salud actual
        salud_texto = self._fuente.render(f"Salud: {salud_actual}", True, COLOR_VERDE_VIDA)
        pantalla.blit(salud_texto, (self._rect_panel.x + 20, self._rect_panel.y + 50))
        
        # Mensaje
        msg = self._fuente.render(self._mensaje, True, COLOR_BLANCO)
        pantalla.blit(msg, (self._rect_panel.centerx - msg.get_width() // 2, self._rect_panel.y + 80))
        
        # Botón cerrar
        color_boton = (180, 60, 60) if self._rect_boton_cerrar.collidepoint(pygame.mouse.get_pos()) else (150, 50, 50)
        pygame.draw.rect(pantalla, color_boton, self._rect_boton_cerrar, border_radius=5)
        texto_cerrar = self._fuente.render("X", True, COLOR_BLANCO)
        pantalla.blit(texto_cerrar, (self._rect_boton_cerrar.centerx - texto_cerrar.get_width() // 2,
                                     self._rect_boton_cerrar.centery - texto_cerrar.get_height() // 2))
        
        # Inventario
        t_inv = self._fuente.render("Tu inventario:", True, COLOR_HONOR_ORO)
        pantalla.blit(t_inv, (self._rect_panel.x + 20, self._rect_panel.y + 120))
        
        self._rects_inventario.clear()
        x_obj = self._rect_panel.x + 20
        y_obj = self._rect_panel.y + 150
        
        for i, item in enumerate(self.inventario):
            r_item = pygame.Rect(x_obj + (i % 2) * 220, y_obj + (i // 2) * 50, 200, 40)
            self._rects_inventario.append((r_item, item))
            
            color_item = (70, 100, 70) if item in self.EFECTOS_OBJETOS else (70, 70, 70)
            color_item_hover = (90, 120, 90) if item in self.EFECTOS_OBJETOS else (90, 90, 90)
            
            color_actual = color_item_hover if r_item.collidepoint(pygame.mouse.get_pos()) else color_item
            pygame.draw.rect(pantalla, color_actual, r_item, border_radius=4)
            
            t_obj = self._fuente.render(item, True, COLOR_BLANCO)
            pantalla.blit(t_obj, (r_item.centerx - t_obj.get_width() // 2,
                                 r_item.centery - t_obj.get_height() // 2))
        
        if not self.inventario:
            vacio = self._fuente.render("Inventario vacío", True, (150, 150, 150))
            pantalla.blit(vacio, (self._rect_panel.centerx - vacio.get_width() // 2, self._rect_panel.y + 200))

class MenuAyuda:
    
    
    def __init__(self, ancho_pantalla: int, alto_pantalla: int):
        self._fuente = pygame.font.SysFont("Georgia", 16)
        self._fuente_titulo = pygame.font.SysFont("Georgia", 24, bold=True)
        
        self._rect_panel = pygame.Rect(ancho_pantalla // 2 - 300,
                                       alto_pantalla // 2 - 250, 600, 500)
        self._rect_boton_cerrar = pygame.Rect(self._rect_panel.right - 60, self._rect_panel.top + 10, 50, 30)
        
        self._controles = [
            ("Movimiento", "Flechas / A-D: Moverse"),
            ("Caballo", "H/M: Subir o bajar del caballo"),
            ("Boleadora", "Espacio/Z: Lanzar boleadora"),
            ("Centinela", "Abajo/S: Esconderse tras la mesa"),
            ("Atacar", "Espacio: Atacar (en combate)"),
        ]
    
    def manejar_evento(self, evento: pygame.event.Event) -> bool:
        
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return True
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self._rect_boton_cerrar.collidepoint(evento.pos):
                return True
        
        return False
    
    def dibujar(self, pantalla: pygame.Surface) -> None:
        sombra = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 150))
        pantalla.blit(sombra, (0, 0))
        
        dibujar_caja(pantalla, self._rect_panel, (30, 35, 20, 230), COLOR_TIERRA_BORDE, 3, 10)
        
        # Título
        tit = self._fuente_titulo.render("Controles y Movimientos", True, COLOR_HONOR_ORO)
        pantalla.blit(tit, (self._rect_panel.centerx - tit.get_width() // 2, self._rect_panel.y + 15))
        
        # Botón cerrar
        color_boton = (180, 60, 60) if self._rect_boton_cerrar.collidepoint(pygame.mouse.get_pos()) else (150, 50, 50)
        pygame.draw.rect(pantalla, color_boton, self._rect_boton_cerrar, border_radius=5)
        texto_cerrar = self._fuente.render("X", True, COLOR_BLANCO)
        pantalla.blit(texto_cerrar, (self._rect_boton_cerrar.centerx - texto_cerrar.get_width() // 2,
                                     self._rect_boton_cerrar.centery - texto_cerrar.get_height() // 2))
        
        # Controles
        y_inicio = self._rect_panel.y + 60
        for categoria, accion in self._controles:
            cat_texto = self._fuente.render(f"{categoria}:", True, COLOR_HONOR_ORO)
            acc_texto = self._fuente.render(accion, True, COLOR_BLANCO)
            
            pantalla.blit(cat_texto, (self._rect_panel.x + 20, y_inicio))
            pantalla.blit(acc_texto, (self._rect_panel.x + 20, y_inicio + 25))
            
            y_inicio += 60


# Plantas de la selva que Arapoty entrega al comenzar el tutorial botánico
PLANTAS_ARAPOTY_INICIALES = ["Yerba Mate", "Burrito", "Uña de Gato", "Boldo"]


# ============================================================================
# TEXTOS DE LA CINEMÁTICA NARRATIVA DE ARAPOTY
# ----------------------------------------------------------------------------
# Tus textos de la historia van aquí. Esta lista se reproduce como el
# "Modo Cinemática" apenas Benjamín aprende a hacer las mezclas: la
# acción se pausa y cada elemento de la lista aparece como una línea de
# diálogo, una debajo de la otra, en el mismo cuadro de texto que usan
# el resto de las conversaciones del capítulo.
#
# Podés agregar, quitar o reescribir estas líneas libremente. Por
# defecto todas las habla "Arapoty"; si en algún momento querés que
# hable Chicha (o cualquier otro personaje), armá esa línea directo
# como LineaDialogo("Chicha", "...") dentro de
# _iniciar_cinematica_historia() en vez de agregarla a esta lista.
# ============================================================================
TEXTOS_CINEMATICA_ARAPOTY = [
    "Hace no mucho donde ahora se ubica ese fortin vivia mi gente, mi pueblo.",
    "Pero ese coronel nos arrebato las tierras como si nada y no nos tuvo piedad.",
    "Puedo llevarte hasta la entrada del fortin y tu podrias enfrentarlo.",
]


# ============================================================================
# Sección 13 Capítulo 3 — estructura de escenas por fases
# ============================================================================

class CapituloLitoral(EscenaBase):
    

    TITULO = "Capítulo 3 El fortín del Coronel"
    REGION = "Litoral entrerriano · 1870"
    NOMBRE = "capitulo_3"

    ESTADO_INTRO           = "intro"
    ESTADO_LITORAL         = "litoral"
    ESTADO_CAMPAMENTO      = "campamento"
    ESTADO_FORTIN_ENTRADA  = "fortin_entrada"
    ESTADO_FORTIN_INTERIOR = "fortin_interior"
    ESTADO_SALA_CORONEL    = "sala_coronel"
    ESTADO_RESUELTO        = "resuelto"

    # Estados que se mueven por un mundo panorámico con cámara propia
    # (a diferencia de ESTADO_INTRO/ESTADO_RESUELTO, que son pantallas
    # fijas de texto/fundido).
    _ESTADOS_CON_MUNDO = (ESTADO_LITORAL, ESTADO_CAMPAMENTO,
                          ESTADO_FORTIN_ENTRADA, ESTADO_FORTIN_INTERIOR,
                          ESTADO_SALA_CORONEL)

    # Ancho/alto visual de Benjamín, reutilizando el spritesheet estándar
    ANCHO_CHICHA = ANCHO_VIS_PERSONAJE
    ALTO_CHICHA  = ALTO_VIS_PERSONAJE

    def __init__(self, gestor: GestorEscenas):
        super().__init__(gestor)

        self.estado_juego  = self.ESTADO_INTRO
        self._pagina_intro = 0

        # --Fondos: TODOS los niveles del capítulo se cargan y
        # pre-escalan de una sola vez acá, antes de que arranque el
        # bucle principal (ver _registrar_fondos). Cambiar de escena
        # después, con _cargar_escena(), es instantáneo.
        self._registrar_fondos()

        self._dialogo             = SistemaDialogo()
        self._plantas_selva       = []
        self._menu_botanico       = None
        self._menu_ayuda          = None
        self._decision_final      = None
        self._tutorial_completado = False   # True tras la cinemática con Arapoty
        self._combate_coronel_activo = False  # True cuando se enfrenta al Coronel
        self._capturado_por_coronel = False  # True cuando el Coronel captura al jugador
        self._timer_captura = 0.0  # Temporizador para la pantalla de captura

        # --Sprites de Benjamín: caminando, a caballo, atacando. El
        # caballo solo (sin jinete) se usa cuando Benjamín se baja.
        #
        # RUTA_CHICHA_NORMAL ya se sabe que mide 400x393 por cuadro,
        # así que se lo indicamos a mano. Los otros tres son sprites
        # más nuevos del proyecto (ataque, caballo montado, caballo
        # solo) y no conviene asumirles un tamaño fijo: si el archivo
        # real no mide exactamente 400x396 por cuadro, el recorte
        # fallaba y se veía el placeholder gris con borde magenta. Al
        # no pasarles ancho_cuadro/alto_cuadro, HojaSprites detecta
        # solo el tamaño real de cada hoja (ver __init__).
        self._hoja_chicha  = HojaSprites(RUTA_CHICHA_NORMAL, ancho_cuadro=400, alto_cuadro=393,
                                         alto_destino=ALTO_VIS_PERSONAJE)
        self._hoja_ataque  = HojaSprites(RUTA_CHICHA_ATAQUE,
                                         alto_destino=ALTO_VIS_PERSONAJE)
        self._hoja_caballo = HojaSprites(RUTA_BENJAMIN_CABALLO,
                                         alto_destino=ALTO_VIS_CABALLO)
        self._hoja_caballo_solo = HojaSprites(RUTA_CABALLO_SOLO,
                                              alto_destino=ALTO_VIS_CABALLO)
        
        # Versiones especiales para la sala del Coronel (más grandes)
        alto_destino_sala_coronel = int(ALTO_CUADRO_PERSONAJE * ESCALA_SALA_CORONEL)
        self._hoja_chicha_sala  = HojaSprites(RUTA_CHICHA_NORMAL, ancho_cuadro=400, alto_cuadro=393,
                                               alto_destino=alto_destino_sala_coronel)
        self._hoja_ataque_sala  = HojaSprites(RUTA_CHICHA_ATAQUE,
                                               alto_destino=alto_destino_sala_coronel)

        self._cuadro_chicha     = 0
        self._timer_anim_chicha = 0.0
        self._mirando_der       = True
        self._en_movimiento     = False
        self._montado           = True   # Benjamín arranca YA MONTADO (Fase 1)

        # --Animación de ataque (al lanzar la boleadora)
        self._atacando      = False
        self._cuadro_ataque = 0
        self._timer_ataque  = 0.0
        self._vel_ataque    = 0.09

        # --Posición de Benjamín en el "mundo" de la escena activa, y
        # rect genérico usado para todas las detecciones de cercanía
        # (NPC, soldados, centinelas, matorrales). Se reconfigura cada
        # vez que se carga una escena nueva (ver _cargar_escena()).
        self._x_mundo          = 100.0
        self._ancho_mundo_actual = ANCHO_PANTALLA
        self._camara            = Camara(ANCHO_PANTALLA)
        self._rect_mundo = pygame.Rect(int(self._x_mundo), SUELO - self.ALTO_CHICHA,
                                       int(self.ANCHO_CHICHA * 0.5), self.ALTO_CHICHA)
        self._jugador_oculto = False

        # --Combate en la entrada del fortín (Fase 3a)
        self._soldados                = []
        self._boleadoras              = []
        self._cooldown_lanzamiento    = 0.0
        self._combate_resuelto        = False
        self._timer_trans_combate     = 0.0

        # --Sigilo en el interior del fortín (Fase 3b), se arma recién
        # cuando se carga esa escena (ver _configurar_fortin_interior)
        self._centinelas       = []
        self._zonas_cobertura  = []
        self._rect_meta        = None

        # --NPCs de las distintas escenas
        self._arapoty = Arapoty(700)
        self._coronel = None   # se crea al entrar a la sala del Coronel

        # --Cruz: acompaña a Benjamín si en el Capítulo 1 se decidió liberarlo
        self._tiene_cruz = bool(
            gestor.partida.get("decisiones", {}).get("libero_cruz", False))
        self._companero_cruz = CompaneroCruz() if self._tiene_cruz else None

        self._timer_transicion = 0.0

        # --Mensajes temporales en pantalla (reemplazo liviano del HUD)
        self._mensaje       = ""
        self._timer_mensaje = 0.0

        self._f_tit    = pygame.font.SysFont("Georgia", 28, bold=True)
        self._f_ital   = pygame.font.SysFont("Georgia", 20, italic=True)
        self._f_ctrl   = pygame.font.SysFont("Arial",   15)
        self._f_texto  = pygame.font.SysFont("Arial",   18)
        self._f_stats  = pygame.font.SysFont("Arial",   14)
        self._f_fund   = pygame.font.SysFont("Georgia", 22, italic=True)
        self._f_etq    = pygame.font.SysFont("Arial",   13)

        reproducir_musica(RUTA_MUSICA_JUEGO)

    # ------------------------------------------------------------------
    # Carga de escenas: el corazón de la estructura por fases
    # ------------------------------------------------------------------

    def _registrar_fondos(self) -> None:
        
        self._fondos = GestorFondos(ANCHO_PANTALLA)
        self._fondos.registrar_nivel(
            self.ESTADO_LITORAL, {"fondo": [RUTA_FONDO_LITORAL]}, ANCHO_MUNDO_LITORAL)
        self._fondos.registrar_nivel(
            self.ESTADO_CAMPAMENTO, {"fondo": [RUTA_FONDO_CAMPAMENTO]}, ANCHO_MUNDO_CAMPAMENTO)
        self._fondos.registrar_nivel(
            self.ESTADO_FORTIN_ENTRADA, {"fondo": [RUTA_FONDO_FORTIN_ENTRADA]}, ANCHO_MUNDO_FORTIN_ENTRADA)
        self._fondos.registrar_nivel(
            self.ESTADO_FORTIN_INTERIOR, {"fondo": [RUTA_FONDO_FORTIN_INTERIOR]}, ANCHO_MUNDO_FORTIN_INTERIOR)
        self._fondos.registrar_nivel(
            self.ESTADO_SALA_CORONEL, {"fondo": [RUTA_FONDO_SALA_CORONEL]}, ANCHO_MUNDO_SALA_CORONEL)

    def _cargar_escena(self, estado: str, x_inicial: float = 100.0) -> None:
        
        self.estado_juego        = estado
        self._fondos.cambiar_nivel(estado)
        self._ancho_mundo_actual = self._fondos.ancho_mundo_actual()
        self._x_mundo            = x_inicial
        self._camara             = Camara(self._ancho_mundo_actual)
        self._rect_mundo.x       = int(self._x_mundo)
        self._jugador_oculto     = False

    def _llego_al_borde(self) -> bool:
        
        limite = self._ancho_mundo_actual - self.ANCHO_CHICHA - MARGEN_LLEGADA_BORDE
        return self._x_mundo >= limite

    # ------------------------------------------------------------------
    # Mensajes temporales
    # ------------------------------------------------------------------

    def _mostrar_mensaje(self, texto: str) -> None:
        self._mensaje       = texto
        self._timer_mensaje = 3.0

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------

    def manejar_evento(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F5:
            self._guardar_rapido()
            return

        # Mientras Chicha está hablando (lore, cinemática, monólogos,
        # encuentro con el Coronel), todos los eventos van al sistema
        # de diálogo y se pausa el resto de la lógica de la escena.
        if self._dialogo.activo:
            resultado = self._dialogo.procesar_evento(evento)
            if resultado and self.estado_juego == self.ESTADO_SALA_CORONEL:
                self._resolver_decision_coronel(resultado)
            return

        # Menú de ayuda (Tab): muestra los controles disponibles y se
        # puede abrir/cerrar en cualquier momento del capítulo (salvo
        # durante un diálogo, ya filtrado más arriba).
        if self._menu_ayuda:
            if self._menu_ayuda.manejar_evento(evento):
                self._alternar_menu_ayuda()
            return

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_TAB:
            self._alternar_menu_ayuda()
            return

        if self.estado_juego == self.ESTADO_INTRO:
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._pagina_intro += 1
                if self._pagina_intro >= len(_INTRO_CAP3):
                    # Fase 1: Benjamín ya está montado (ver __init__).
                    self._cargar_escena(self.ESTADO_LITORAL)

        elif self.estado_juego == self.ESTADO_CAMPAMENTO and self._menu_botanico:
            self._menu_botanico.manejar_evento(evento)
            if "Mate Calmante" in self._plantas_selva:
                for nombre in self._plantas_selva:
                    if nombre not in self.gestor.partida["plantas_conocidas"]:
                        self.gestor.partida["plantas_conocidas"].append(nombre)
                self._iniciar_cinematica_historia()

        elif self.estado_juego == self.ESTADO_CAMPAMENTO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_o and self._tutorial_completado:
                    # Abrir menú botánico después del tutorial
                    self._plantas_selva = list(PLANTAS_ARAPOTY_INICIALES)
                    self._menu_botanico = MenuBotanico(ANCHO_PANTALLA, ALTO_PANTALLA, self._plantas_selva)
                elif evento.key == pygame.K_e and not self._tutorial_completado:
                    self._intentar_hablar_arapoty()

        elif self.estado_juego in (self.ESTADO_LITORAL, self.ESTADO_FORTIN_ENTRADA):
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_h, pygame.K_m):
                    self._alternar_montura()
                elif evento.key in (pygame.K_SPACE, pygame.K_z) and self.estado_juego == self.ESTADO_FORTIN_ENTRADA:
                    self._lanzar_boleadora()

        elif self.estado_juego == self.ESTADO_SALA_CORONEL and self._combate_coronel_activo:
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_z):
                self._atacar_coronel()

    # ------------------------------------------------------------------
    # Actualización
    # ------------------------------------------------------------------

    def actualizar(self, dt: float) -> None:
        if self._timer_mensaje > 0:
            self._timer_mensaje -= dt

        # Mientras hay un diálogo/cinemática en pantalla, se pausa la
        # lógica de movimiento, combate y sigilo de la escena actual.
        if self._dialogo.activo:
            self._dialogo.actualizar(dt)
            return

        if self.estado_juego == self.ESTADO_LITORAL:
            self._actualizar_mundo_libre(dt)
            if not self._llego_al_borde():
                return
            self._cargar_escena(self.ESTADO_CAMPAMENTO)
            self._mostrar_mensaje("Campamento a la vista. Buscá a Arapoty (E para hablar).")

        elif self.estado_juego == self.ESTADO_CAMPAMENTO:
            self._actualizar_mundo_libre(dt)
            self._arapoty.actualizar(dt)

        elif self.estado_juego == self.ESTADO_FORTIN_ENTRADA:
            self._actualizar_fortin_entrada(dt)

        elif self.estado_juego == self.ESTADO_FORTIN_INTERIOR:
            self._actualizar_fortin_interior(dt)

        elif self.estado_juego == self.ESTADO_SALA_CORONEL:
            if self._coronel:
                if self._combate_coronel_activo:
                    # Permitir movimiento del jugador durante el combate
                    self._actualizar_mundo_libre(dt)
                    daño = self._coronel.actualizar(dt, self._x_mundo)
                    if daño:
                        self._capturado_por_coronel = True
                        self._timer_captura = 0.0
                        self._combate_coronel_activo = False
                else:
                    self._coronel.actualizar(dt, self._x_mundo)
            
            # Manejar pantalla de captura
            if self._capturado_por_coronel:
                self._timer_captura += dt
                if self._timer_captura >= 3.0:
                    self._capturado_por_coronel = False
                    self._sincronizar_partida()
                    self.estado_juego = self.ESTADO_RESUELTO
                    self._timer_transicion = 3.0

        elif self.estado_juego == self.ESTADO_RESUELTO:
            self._timer_transicion -= dt
            if self._timer_transicion <= 0:
                self.gestor.cambiar("fin_demo")

    # --Movimiento genérico por cualquier mundo panorámico (litoral,
    #   campamento, fortín): mueve a Benjamín, actualiza la cámara, la
    #   animación y a Cruz. Cada escena llama a esto y después agrega
    #   su propia lógica particular (NPC, soldados, sigilo).

    def _actualizar_mundo_libre(self, dt: float) -> None:
        teclas = pygame.key.get_pressed()
        velocidad = VELOCIDAD_MONTADO if self._montado else VELOCIDAD_A_PIE

        movimiento_x = 0.0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            movimiento_x -= velocidad * dt
            self._mirando_der = False
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            movimiento_x += velocidad * dt
            self._mirando_der = True

        self._en_movimiento = movimiento_x != 0
        self._x_mundo = max(0.0, min(self._ancho_mundo_actual - self.ANCHO_CHICHA,
                                     self._x_mundo + movimiento_x))
        self._camara.actualizar(self._x_mundo)
        self._rect_mundo.x = int(self._x_mundo)

        self._actualizar_animacion_benjamin(dt)

        if self._companero_cruz:
            self._companero_cruz.actualizar(dt, self._en_movimiento)

    def _actualizar_animacion_benjamin(self, dt: float) -> None:
        
        if self._atacando:
            self._timer_ataque += dt
            if self._timer_ataque >= self._vel_ataque:
                self._timer_ataque = 0.0
                self._cuadro_ataque += 1
                if self._cuadro_ataque >= 4:
                    self._atacando      = False
                    self._cuadro_ataque = 0
            return

        self._timer_anim_chicha += dt
        if self._timer_anim_chicha >= 0.13:
            self._timer_anim_chicha = 0.0
            self._cuadro_chicha = (self._cuadro_chicha % 3) + 1 if self._en_movimiento else 0

    def _iniciar_animacion_ataque(self) -> None:
        self._atacando      = True
        self._cuadro_ataque = 0
        self._timer_ataque  = 0.0

    # --Fase 2: interacción con Arapoty (campamento)

    def _intentar_hablar_arapoty(self) -> None:
        if self._tutorial_completado:
            return
        if self._arapoty.cerca_de(self._rect_mundo):
            self._iniciar_dialogo_lore()

    # --Montar / desmontar (litoral, campamento, entrada del fortín)

    def _alternar_montura(self) -> None:
        self._montado = not self._montado
        self._cuadro_chicha = 0
        if self._montado:
            self._mostrar_mensaje("Subís a Yanis. Te movés más rápido.")
        else:
            self._mostrar_mensaje("Bajás del caballo. Yanis te espera cerca.")

    def _atacar_coronel(self) -> None:
        
        if not self._combate_coronel_activo:
            return

        self._iniciar_animacion_ataque()
        derrotado = self._coronel.recibir_golpe()
        
        if derrotado:
            self._combate_coronel_activo = False
            self._mostrar_mensaje("¡Derrotaste al Coronel!")
            self._sincronizar_partida()
            self.estado_juego = self.ESTADO_RESUELTO
            self._timer_transicion = 3.0
        else:
            golpes_restantes = self._coronel.vida
            self._mostrar_mensaje(f"¡Golpe! El Coronel necesita {golpes_restantes} golpes más.")

    # --Fase 3a: entrada del fortín (soldados + boleadora)

    def _lanzar_boleadora(self) -> None:
        if self._cooldown_lanzamiento > 0:
            return
        direccion = 1 if self._mirando_der else -1
        x_inicio  = self._x_mundo + (self.ANCHO_CHICHA if direccion > 0 else 0)
        self._boleadoras.append(Boleadora(x_inicio, direccion, self._ancho_mundo_actual))
        self._cooldown_lanzamiento = COOLDOWN_LANZAMIENTO
        self._iniciar_animacion_ataque()

    def _iniciar_combate_fortin(self) -> None:
        
        # Mover al jugador a la coordenada específica de combate
        self._x_mundo = float(X_INICIO_COMBATE_FORTIN)
        self._camara.actualizar(self._x_mundo)
        self._rect_mundo.x = int(self._x_mundo)
        
        base_x = self._x_mundo + 500
        self._soldados = [
            Soldado(base_x),
            Soldado(base_x + 220),
            Soldado(base_x + 440),
        ]
        self._combate_resuelto = False
        self._montado          = False
        self._mostrar_mensaje(
            "¡Soldados en la entrada!  Espacio: boleadora")

    def _actualizar_fortin_entrada(self, dt: float) -> None:
        if self._combate_resuelto:
            self._timer_trans_combate -= dt
            if self._timer_trans_combate <= 0:
                self._configurar_fortin_interior()
            return

        self._actualizar_mundo_libre(dt)

        if self._cooldown_lanzamiento > 0:
            self._cooldown_lanzamiento -= dt

        for soldado in self._soldados:
            contacto = soldado.actualizar(dt, self._x_mundo)
            if contacto and soldado.estado == "avanzando":
                self.gestor.partida["salud"] = max(0, self.gestor.partida["salud"] - DANIO_SOLDADO)
                soldado.recibir_impacto()
                self._mostrar_mensaje(f"¡Recibiste un golpe!  -{DANIO_SOLDADO} vida")

        for boleadora in self._boleadoras:
            boleadora.actualizar(dt)
            if boleadora.activo:
                for soldado in self._soldados:
                    if soldado.estado != "caido" and boleadora.rect.colliderect(soldado.rect):
                        soldado.recibir_impacto()
                        boleadora.activo = False
                        if soldado.estado == "caido":
                            self._mostrar_mensaje("¡Soldado derribado!")
                        else:
                            self._mostrar_mensaje("¡Impacto! El soldado se tambalea...")
                        break

        self._boleadoras = [b for b in self._boleadoras if b.activo]

        if (self._soldados and not self._combate_resuelto
                and all(s.estado == "caido" for s in self._soldados)):
            self._combate_resuelto    = True
            self._timer_trans_combate = 3.0
            self._mostrar_mensaje("El camino al interior del fortín está libre...")

    # --Fase 3b: interior del fortín (sigilo)

    def _configurar_fortin_interior(self) -> None:
        self._cargar_escena(self.ESTADO_FORTIN_INTERIOR)
        self._montado = False

        self._centinelas = [
            Centinela(700, SUELO - self.ALTO_CHICHA, 500, 1300),
        ]
        self._zonas_cobertura = [
            pygame.Rect(800, SUELO - self.ALTO_CHICHA, 225, self.ALTO_CHICHA),  # Más ancho, extendido a la izquierda
        ]
        self._mostrar_mensaje("Flechas/A-D moverte  ·  Abajo/S para esconderse tras la mesa")

    def _actualizar_fortin_interior(self, dt: float) -> None:
        teclas = pygame.key.get_pressed()

        movimiento_x = 0.0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            movimiento_x -= VELOCIDAD_INFILTRACION * dt
            self._mirando_der = False
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            movimiento_x += VELOCIDAD_INFILTRACION * dt
            self._mirando_der = True

        self._en_movimiento = movimiento_x != 0
        self._x_mundo = max(0.0, min(self._ancho_mundo_actual - self.ANCHO_CHICHA,
                                     self._x_mundo + movimiento_x))
        self._camara.actualizar(self._x_mundo)
        self._rect_mundo.x = int(self._x_mundo)

        self._actualizar_animacion_benjamin(dt)

        # Cobertura: mantener Abajo o C dentro de un matorral para ocultarse
        en_zona = any(zona.colliderect(self._rect_mundo) for zona in self._zonas_cobertura)
        self._jugador_oculto = en_zona and (teclas[pygame.K_DOWN] or teclas[pygame.K_s])

        # Cruz se mueve junto con Benjamín y se agacha en la cobertura
        # apenas Benjamín se oculta, para no ser visto por los centinelas.
        if self._companero_cruz:
            self._companero_cruz.actualizar(dt, self._en_movimiento)

        for guardia in self._centinelas:
            guardia.actualizar(dt)
            if guardia.detectar(self._rect_mundo, self._jugador_oculto, dt):
                self._x_mundo = max(0.0, self._x_mundo - 220.0)
                self._rect_mundo.x = int(self._x_mundo)
                self.gestor.partida["salud"] = max(0, self.gestor.partida["salud"] - DANIO_POR_DETECCION)
                self._mostrar_mensaje(f"¡Te vieron!  -{DANIO_POR_DETECCION} vida")
                for otro in self._centinelas:
                    otro.reiniciar_sospecha()

        if self._llego_al_borde():
            self._iniciar_sala_coronel()

    # --Fase 4: sala del Coronel

    def _iniciar_sala_coronel(self) -> None:
        self._cargar_escena(self.ESTADO_SALA_CORONEL, x_inicial=150.0)
        self._coronel = Coronel(self._ancho_mundo_actual - 260)
        self._iniciar_encuentro_coronel()

    # ------------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------------

    def dibujar(self, pantalla: pygame.Surface) -> None:
        if self.estado_juego in self._ESTADOS_CON_MUNDO:
            self._fondos.dibujar(pantalla, self._camara)

        if self.estado_juego == self.ESTADO_INTRO:
            pantalla.fill(COLOR_NEGRO)
            _dibujar_intro_textual(pantalla, self.TITULO, _INTRO_CAP3,
                                   self._pagina_intro, self._f_tit, self._f_ital, self._f_ctrl)
            return

        if self.estado_juego == self.ESTADO_LITORAL:
            self._dibujar_benjamin_mundo(pantalla)
            if self._companero_cruz:
                self._companero_cruz.dibujar(pantalla, self._x_mundo - 90, self._camara)
            self._dibujar_stats(pantalla)
            aviso = self._f_texto.render(
                "Flechas/A-D cabalgar  ·  H/M: subir o bajar del caballo",
                True, COLOR_BLANCO)
            pantalla.blit(aviso, (20, 20))

        elif self.estado_juego == self.ESTADO_CAMPAMENTO:
            self._arapoty.dibujar(
                pantalla, self._camara,
                mostrar_pista=(not self._tutorial_completado
                              and self._arapoty.cerca_de(self._rect_mundo)))
            if self._menu_botanico:
                self._menu_botanico.dibujar(pantalla)
            else:
                self._dibujar_benjamin_mundo(pantalla)
                if self._companero_cruz:
                    self._companero_cruz.dibujar(pantalla, self._x_mundo - 90, self._camara)
                self._dibujar_stats(pantalla)
                aviso_txt = ("Flechas/A-D moverte  ·  H/M: caballo  ·  E: hablar con Arapoty"
                            if not self._tutorial_completado else
                            "Flechas/A-D moverte  ·  H/M: caballo  ·  O: menú mezclas")
                aviso = self._f_texto.render(aviso_txt, True, COLOR_BLANCO)
                pantalla.blit(aviso, (20, 20))

        elif self.estado_juego == self.ESTADO_FORTIN_ENTRADA:
            for soldado in self._soldados:
                soldado.dibujar(pantalla, self._camara)
            for boleadora in self._boleadoras:
                boleadora.dibujar(pantalla, self._camara)
            self._dibujar_benjamin_mundo(pantalla)
            if self._companero_cruz:
                self._companero_cruz.dibujar(pantalla, self._x_mundo - 90, self._camara)
            self._dibujar_stats(pantalla)

            aviso = self._f_texto.render(
                "Flechas/A-D avanzar  ·  Espacio: boleadora",
                True, COLOR_BLANCO)
            pantalla.blit(aviso, (20, 20))

            if self._combate_resuelto:
                _dibujar_fundido(pantalla, self._timer_trans_combate, 3.0,
                                 "El camino al interior del fortín está libre...", self._f_fund)

        elif self.estado_juego == self.ESTADO_FORTIN_INTERIOR:
            # Zonas de cobertura invisibles (no se dibujan)
            # for zona in self._zonas_cobertura:
            #     zona_pantalla = pygame.Rect(self._camara.aplicar_x(zona.x), zona.y,
            #                                 zona.width, zona.height)
            #     pygame.draw.rect(pantalla, (40, 90, 40), zona_pantalla, border_radius=4)

            for guardia in self._centinelas:
                guardia.dibujar(pantalla, self._camara)

            if self._companero_cruz:
                if self._jugador_oculto:
                    x_cruz = self._x_mundo + self.ANCHO_CHICHA // 2 - 40
                else:
                    x_cruz = self._x_mundo - 90
                self._companero_cruz.dibujar(pantalla, x_cruz, self._camara, oculto=self._jugador_oculto)

            self._dibujar_benjamin_mundo(pantalla)
            self._dibujar_stats(pantalla)

            hud_txt = self._f_texto.render(
                "Flechas/A-D moverte  ·  Abajo/S en la mesa para ocultarte",
                True, COLOR_BLANCO)
            pantalla.blit(hud_txt, (20, 20))

        elif self.estado_juego == self.ESTADO_SALA_CORONEL:
            if self._coronel:
                self._coronel.dibujar(pantalla, self._camara)
            self._dibujar_benjamin_mundo(pantalla)
            self._dibujar_stats(pantalla)
            
            if self._combate_coronel_activo:
                aviso = self._f_texto.render(
                    "Espacio: atacar al Coronel  ·  ¡Evita que te toque!",
                    True, COLOR_HONOR_ORO)
                pantalla.blit(aviso, (20, 20))
            
            # Pantalla de captura
            if self._capturado_por_coronel:
                overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
                overlay.fill(COLOR_NEGRO)
                overlay.set_alpha(255)
                pantalla.blit(overlay, (0, 0))
                
                texto_captura = self._f_tit.render("¡FUISTE CAPTURADO!", True, COLOR_ROJO_DANIO)
                texto_sub = self._f_ital.render("El Coronel Ibáñez te ha atrapado...", True, COLOR_BLANCO)
                
                pantalla.blit(texto_captura, (ANCHO_PANTALLA // 2 - texto_captura.get_width() // 2, ALTO_PANTALLA // 2 - 30))
                pantalla.blit(texto_sub, (ANCHO_PANTALLA // 2 - texto_sub.get_width() // 2, ALTO_PANTALLA // 2 + 20))

        if self.estado_juego == self.ESTADO_RESUELTO:
            texto_fundido = ("Chicha decidió enfrentar al Coronel..."
                             if self._decision_final == "enfrentar"
                             else "Chicha se alejó del fortín sin decir nada...")
            _dibujar_fundido(pantalla, self._timer_transicion, 3.0, texto_fundido, self._f_fund)

        # El sistema de diálogo se dibuja encima de cualquier escena
        # mientras esté activo: cubre el lore de Arapoty, el "Modo
        # Cinemática" y el encuentro/decisión con el Coronel.
        if self._dialogo.activo:
            self._dialogo.dibujar(pantalla)

        if self._timer_mensaje > 0:
            self._dibujar_mensaje(pantalla)

        _dibujar_etiqueta_capitulo(pantalla, self._f_etq, self.TITULO, self.REGION)

        # El menú de ayuda (Tab) se dibuja por encima de todo lo demás.
        if self._menu_ayuda:
            self._menu_ayuda.dibujar(pantalla)

    def _dibujar_benjamin_mundo(self, pantalla: pygame.Surface) -> None:
        
        offset_y = 0  # Offset vertical para alinear con el suelo
        
        # Usar hojas especiales para la sala del Coronel (personajes más grandes)
        hoja_ataque_actual = self._hoja_ataque_sala if self.estado_juego == self.ESTADO_SALA_CORONEL else self._hoja_ataque
        hoja_chicha_actual = self._hoja_chicha_sala if self.estado_juego == self.ESTADO_SALA_CORONEL else self._hoja_chicha
        
        if self._atacando:
            frame = hoja_ataque_actual.obtener_frame(self._cuadro_ataque)
        elif self._montado:
            frame = self._hoja_caballo.obtener_frame(self._cuadro_chicha)
            offset_y = OFFSET_Y_CABALLO  # Aplicar offset para caballo montado
        else:
            if self.estado_juego in (self.ESTADO_LITORAL, self.ESTADO_CAMPAMENTO,
                                     self.ESTADO_FORTIN_ENTRADA):
                # Desmontado en una zona "de caballo": Yanis espera cerca.
                frame_caballo = self._hoja_caballo_solo.obtener_frame(0)
                x_caballo = self._camara.aplicar_x(self._x_mundo - 70)
                y_caballo = SUELO - frame_caballo.get_height() + OFFSET_Y_CABALLO
                pantalla.blit(frame_caballo, (x_caballo, y_caballo))
            frame = hoja_chicha_actual.obtener_frame(self._cuadro_chicha)

        if not self._mirando_der:
            frame = pygame.transform.flip(frame, True, False)

        if self._jugador_oculto:
            frame = frame.copy()
            frame.set_alpha(140)   # Benjamín se atenúa mientras está oculto

        x_pan = self._camara.aplicar_x(self._x_mundo)
        x_pan += (self.ANCHO_CHICHA - frame.get_width()) // 2
        y_pan = SUELO - frame.get_height() + offset_y
        pantalla.blit(frame, (x_pan, y_pan))

    def _dibujar_stats(self, pantalla: pygame.Surface) -> None:
        txt = self._f_stats.render(
            f"Vida: {self.gestor.partida['salud']} / {SALUD_MAXIMA}   "
            f"Honor: {self.gestor.partida['honor']} / {HONOR_MAXIMO}",
            True, COLOR_BLANCO)
        pantalla.blit(txt, (20, ALTO_PANTALLA - 34))

    def _dibujar_mensaje(self, pantalla: pygame.Surface) -> None:
        prog  = min(1.0, self._timer_mensaje / 3.0)
        alpha = int(min(255, 255 * min(prog * 3, 1)))
        sup   = self._f_texto.render(self._mensaje, True, COLOR_HONOR_ORO)
        sup.set_alpha(alpha)
        pantalla.blit(sup, ((ANCHO_PANTALLA - sup.get_width()) // 2, 48))

    # ------------------------------------------------------------------
    # Diálogo de presentación con Arapoty (Fase 2)
    # ------------------------------------------------------------------

    def _iniciar_dialogo_lore(self) -> None:
        lineas_lore = [
            LineaDialogo("Arapoty",
                "Benjamín llega a caballo. Bienvenido al campamento, forastero."),
            LineaDialogo("Arapoty",
                "Ese fortin es del coronel."),
            LineaDialogo("Arapoty",
                "Antes de ir hacia allá, tenés que aprender a usar las hierbas de la selva."),
        ]

        def al_cerrar_lore():
            self._plantas_selva = list(PLANTAS_ARAPOTY_INICIALES)
            self._menu_botanico  = MenuBotanico(ANCHO_PANTALLA, ALTO_PANTALLA, self._plantas_selva)

        self._dialogo.iniciar(lineas_lore, callback_cerrar=al_cerrar_lore)

    # --Modo Cinemática (historia personalizable, ver TEXTOS_CINEMATICA_ARAPOTY)

    def _alternar_menu_ayuda(self) -> None:
        
        if self._menu_ayuda is None:
            self._menu_ayuda = MenuAyuda(ANCHO_PANTALLA, ALTO_PANTALLA)
        else:
            self._menu_ayuda = None

    def _iniciar_cinematica_historia(self) -> None:
        
        lineas = [LineaDialogo("Arapoty", texto) for texto in TEXTOS_CINEMATICA_ARAPOTY]

        def al_cerrar():
            self._finalizar_cinematica()

        self._dialogo.iniciar(lineas, callback_cerrar=al_cerrar)

    def _finalizar_cinematica(self) -> None:
        
        self._tutorial_completado = True
        self._menu_botanico       = None
        self._cargar_escena(self.ESTADO_FORTIN_ENTRADA)
        self._iniciar_combate_fortin()

    # --Encuentro final con el Coronel Ibáñez (Fase 4)

    def _iniciar_encuentro_coronel(self) -> None:
        reproducir_musica(RUTA_MUSICA_DECISION)

        lineas = [
            LineaDialogo("Coronel Ibáñez",
                "Así que hasta aquí llegaste, gaucho. No pensé que el litoral te dejara pasar."),
            LineaDialogo("Chicha", "Coronel..."),
            LineaDialogo("Coronel Ibáñez",
                "Todavía podés entregarte. Esto termina distinto "
                "si no me obligás a perseguirte hasta el sur."),
            LineaDialogo("Chicha", "Tengo que decidir ahora mismo qué voy a hacer."),
        ]
        opciones = [
            Opcion("Enfrentarlo cara a cara.",
                   efecto_honor=+15, resultado="enfrentar"),
            Opcion("Huir sin decir nada.",
                   efecto_honor=-5, resultado="huir"),
        ]
        self._dialogo.iniciar(lineas, opciones)

    def _resolver_decision_coronel(self, opcion: Opcion) -> None:
        self.gestor.sumar_honor(opcion.efecto_honor)
        self.gestor.partida.setdefault("decisiones", {})["enfrento_coronel"] = (
            opcion.resultado == "enfrentar")
        self._decision_final = opcion.resultado

        if opcion.resultado == "enfrentar":
            self._mostrar_mensaje("¡El Coronel ataca!  Espacio: atacar")
            self._coronel.iniciar_combate()
            self._combate_coronel_activo = True
        else:
            self._mostrar_mensaje("Te fuiste en silencio.  -5 Honor")
            self._sincronizar_partida()
            self.estado_juego      = self.ESTADO_RESUELTO
            self._timer_transicion = 3.0

    # ------------------------------------------------------------------
    # Guardado
    # ------------------------------------------------------------------

    def _sincronizar_partida(self) -> None:
        self.gestor.partida.setdefault("decisiones", {})

    def _guardar_rapido(self) -> None:
        self._sincronizar_partida()
        guardar_partida(self.gestor.partida, self.NOMBRE)
        self._mostrar_mensaje("Partida guardada  [F5]")


# Textos de apertura del capítulo
_INTRO_CAP3 = [
    "Litoral entrerriano, 1870.",
    "Benjamín deja atrás las llanuras del oeste,\nsiguiendo el rumor de un campamento guaraní\nescondido entre la selva.",
    "Allí lo espera Arapoty, una curandera\nque conoce estas tierras mejor que\nel propio Coronel.",
    "Pero más adelante, tras la espesura,\nse alza el fortín de piedra que una vez\nfue el hogar de su pueblo.",
]


# ============================================================================
# Sección 14 fin demo
# ============================================================================

class FinDemo(EscenaBase):
    # Pantalla dividida
    # Izquierda: Chicha spritesheet
    # Derecha: texto con titulo "Fin del Capítulo 3", plantas recolectadas y decisiones.
    # Tecla Espacio,Enter,Escape para volver al menú principal.

    ESCALA_ESCENA_FINAL = 0.65
    ANCHO_CHICHA_FINAL  = int(ANCHO_CUADRO_CHICHA_FINAL * ESCALA_ESCENA_FINAL)
    ALTO_CHICHA_FINAL   = int(ALTO_CUADRO_CHICHA_FINAL  * ESCALA_ESCENA_FINAL)

    # Volver al menú
    RECT_BOTON_VOLVER = pygame.Rect(ANCHO_PANTALLA - 230, ALTO_PANTALLA - 60, 200, 44)

    def __init__(self, gestor: GestorEscenas):
        super().__init__(gestor)

        self._fondo = cargar_imagen(RUTA_FONDO_ATARDECER, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self._hoja_sentado = HojaSprites(RUTA_CHICHA_SENTADO,
                                         ANCHO_CUADRO_CHICHA_FINAL,
                                         ALTO_CUADRO_CHICHA_FINAL,
                                         self.ESCALA_ESCENA_FINAL)
        self._cuadro      = 0
        self._timer_anim  = 0.0
        self._vel_anim    = 1.25   # Animacion lenta

        self._honor       = gestor.partida["honor"]
        self._salud       = gestor.partida["salud"]
        self._plantas     = gestor.partida["plantas_conocidas"]
        self._decisiones  = gestor.partida["decisiones"]

        self._f_titulo = pygame.font.SysFont("Georgia", 34, bold=True)
        self._f_stat   = pygame.font.SysFont("Arial",   17)
        self._f_sub    = pygame.font.SysFont("Arial",   15)
        self._f_ctrl   = pygame.font.SysFont("Arial",   13)

        reproducir_musica(RUTA_MUSICA_FINAL)

    def manejar_evento(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.gestor.cambiar("menu")
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.RECT_BOTON_VOLVER.collidepoint(evento.pos):
                self.gestor.cambiar("menu")

    def actualizar(self, dt: float) -> None:
        self._timer_anim += dt
        if self._timer_anim >= self._vel_anim:
            self._timer_anim = 0.0
            self._cuadro = (self._cuadro + 1) % 4   # Bucle de respiracion/poncho

    def dibujar(self, pantalla: pygame.Surface) -> None:
        pantalla.blit(self._fondo, (0, 0))

        # Mitad izquierda: Chicha sentado mirando el atardecer
        frame = self._hoja_sentado.obtener_frame(self._cuadro)
        x_chicha = ANCHO_PANTALLA // 4 - frame.get_width() // 2
        y_chicha = SUELO - frame.get_height()
        pantalla.blit(frame, (x_chicha, y_chicha))

        # Mitad derecha: panel de estadísticas
        panel_x = ANCHO_PANTALLA // 2 + 20
        panel_w = ANCHO_PANTALLA // 2 - 60
        panel = pygame.Rect(panel_x, 60, panel_w, ALTO_PANTALLA - 140)
        dibujar_caja(pantalla, panel, (10, 6, 2, 210), COLOR_TIERRA_BORDE, 2, 10)

        tit = self._f_titulo.render("Fin del Capítulo 3", True, COLOR_HONOR_ORO)
        pantalla.blit(tit, (panel.x + 24, panel.y + 22))

        y_actual = panel.y + 80

        for txt in [
            f"Honor acumulado:   {self._honor} / {HONOR_MAXIMO}",
            f"Vida al terminar:  {self._salud} / {SALUD_MAXIMA}",
        ]:
            pantalla.blit(self._f_stat.render(txt, True, COLOR_BLANCO), (panel.x + 24, y_actual))
            y_actual += 28

        y_actual += 10
        pygame.draw.line(pantalla, COLOR_TIERRA_BORDE,
                         (panel.x + 24, y_actual), (panel.right - 24, y_actual), 1)
        y_actual += 20

        pantalla.blit(self._f_stat.render("Plantas conocidas:", True, COLOR_HONOR_ORO),
                      (panel.x + 24, y_actual))
        y_actual += 26
        if self._plantas:
            for nombre_planta in self._plantas:
                pantalla.blit(self._f_sub.render(f"{nombre_planta}", True, (180, 220, 160)),
                              (panel.x + 36, y_actual))
                y_actual += 22
        else:
            pantalla.blit(self._f_sub.render("Ninguna planta recolectada.", True, (170, 150, 150)),
                          (panel.x + 36, y_actual))
            y_actual += 22

        y_actual += 14
        pygame.draw.line(pantalla, COLOR_TIERRA_BORDE,
                         (panel.x + 24, y_actual), (panel.right - 24, y_actual), 1)
        y_actual += 20

        pantalla.blit(self._f_stat.render("Decisiones tomadas:", True, COLOR_HONOR_ORO),
                      (panel.x + 24, y_actual))
        y_actual += 26
        if self._decisiones:
            for clave, valor in self._decisiones.items():
                etiqueta = clave.replace("_", " ").capitalize()
                resultado = "Sí" if valor else "No"
                pantalla.blit(
                    self._f_sub.render(f"- {etiqueta}: {resultado}", True, (220, 200, 180)),
                    (panel.x + 36, y_actual))
                y_actual += 22
        else:
            pantalla.blit(self._f_sub.render("Sin decisiones registradas.", True, (170, 150, 150)),
                          (panel.x + 36, y_actual))
            y_actual += 22

        ctrl = self._f_ctrl.render("(Espacio / Enter / Clic)  volver al menu principal",
                                   True, (170, 160, 145))
        pantalla.blit(ctrl, (panel.x + 24, panel.bottom - 30))


# ============================================================================
# Sección 15 principal
# ============================================================================

def main():
    pygame.init()
    pygame.mixer.init()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Los Hijos de Nadie: Capítulo 3 — El fortín del Coronel")
    reloj = pygame.time.Clock()

    gestor = GestorEscenas(pantalla)
    gestor.registrar("menu",       MenuPrincipal)
    gestor.registrar("capitulo_3", CapituloLitoral)
    gestor.registrar("fin_demo",   FinDemo)
    gestor.cambiar("menu")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # F9 carga la última partida guardada
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F9:
                datos = cargar_partida()
                if datos:
                    gestor.aplicar_guardado(datos)
                    gestor.cambiar("capitulo_3")
                continue

            gestor.escena_actual.manejar_evento(evento)

        dt = reloj.tick(FPS) / 1000.0
        gestor.escena_actual.actualizar(dt)
        gestor.escena_actual.dibujar(pantalla)
        pygame.display.flip()


if __name__ == "__main__":
    main()