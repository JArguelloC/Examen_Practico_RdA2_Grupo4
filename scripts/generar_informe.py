"""Genera docs/informe/Informe_Tecnico_EcoTrip2026.pdf (HTML -> PDF con Chrome/Edge headless).

Uso: python scripts/generar_informe.py
Las capturas se leen de docs/evidencias/ (ver nombres en EVIDENCIAS). Si falta alguna se deja un recuadro.
"""
import base64
import html
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "informe"
EVID = RAIZ / "docs" / "evidencias"
REPO_URL = "https://github.com/JArguelloC/Examen_Practico_RdA2_Grupo4"

INTEGRANTES = [
    ("James Argüello", "Configuración base, modelos y DataStore"),
    ("Wismar Benítez", "EcoTripViewModel y SavedStateHandle"),
    ("Carlos Galarza", "Pantalla de formulario (Material Design 3)"),
    ("Mateo Morales", "Navegación type-safe y pantalla de resumen"),
    ("Ángel Loor", "QA, pruebas de resiliencia e informe técnico"),
]

EVIDENCIAS = [
    ("01-formulario-vertical.png",
     "Figura 2. Formulario de viaje con datos válidos (modo vertical, emulador API 36)."),
    ("02-rotacion-horizontal.png",
     "Figura 3. Prueba de rotación: el formulario conserva los datos en modo horizontal."),
    ("04a-process-death-antes.png",
     "Figura 4. Muerte de proceso, antes: formulario lleno con «No conservar actividades» activo."),
    ("04-process-death-despues.png",
     "Figura 5. Muerte de proceso, después: el proceso fue terminado (am kill) y todos los campos se restauraron."),
    ("05a-material-you-formulario-naranja.png",
     "Figura 6. Formulario con Color Dinámico tras cambiar el fondo de pantalla a naranja."),
    ("06-material-you-resumen.png",
     "Figura 7. Pantalla de Resumen de Ruta con Color Dinámico tras cambiar el fondo de pantalla."),
]

CODIGO = [
    "app/build.gradle.kts",
    "gradle/libs.versions.toml",
    "app/src/main/java/com/example/myapplication/MainActivity.kt",
    "app/src/main/java/com/example/myapplication/data/model/PreferenciaViaje.kt",
    "app/src/main/java/com/example/myapplication/data/local/EcoTripDataStore.kt",
    "app/src/main/java/com/example/myapplication/ui/state/FormularioUiState.kt",
    "app/src/main/java/com/example/myapplication/ui/viewmodel/EcoTripViewModel.kt",
    "app/src/main/java/com/example/myapplication/navigation/Routes.kt",
    "app/src/main/java/com/example/myapplication/navigation/EcoTripNavHost.kt",
    "app/src/main/java/com/example/myapplication/ui/screens/FormularioScreen.kt",
    "app/src/main/java/com/example/myapplication/ui/screens/ResumenScreen.kt",
    "app/src/androidTest/java/com/example/myapplication/ResilienciaTest.kt",
]

CSS = """
@page { size: A4; margin: 2.54cm; }
body { font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 2; color: #000; }
h1 { font-size: 12pt; font-weight: bold; text-align: center; margin: 0; page-break-before: always; }
h2 { font-size: 12pt; font-weight: bold; margin: 0; }
h3 { font-size: 12pt; font-weight: bold; font-style: italic; margin: 0; }
p { margin: 0; text-indent: 1.27cm; text-align: left; }
.portada { text-align: center; page-break-after: always; }
.portada p { text-indent: 0; text-align: center; }
.sin-salto { page-break-before: auto; }
table { border-collapse: collapse; width: 100%; line-height: 1.3; margin: 0.4cm 0; font-size: 11pt; }
th, td { border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 4px 6px; text-align: left; vertical-align: top; }
.tabla-t { font-weight: bold; text-indent: 0; line-height: 1.3; }
.tabla-n { font-style: italic; text-indent: 0; line-height: 1.3; margin-bottom: 4px; }
figure { margin: 0.5cm 0; text-align: center; page-break-inside: avoid; }
figure img { max-height: 9.5cm; max-width: 100%; border: 1px solid #999; }
figcaption { font-size: 11pt; line-height: 1.3; font-style: italic; }
.falta { border: 1px dashed #c00; color: #c00; padding: 2cm 0; line-height: 1.3; font-size: 11pt; }
pre { font-family: Consolas, 'Courier New', monospace; font-size: 7.5pt; line-height: 1.25; white-space: pre-wrap;
      word-break: break-word; border: 1px solid #bbb; padding: 6px; background: #fafafa; }
.codigo-t { font-weight: bold; text-indent: 0; line-height: 1.3; font-size: 10pt; margin-top: 8px; }
.diagrama { font-family: Consolas, monospace; font-size: 7.5pt; line-height: 1.2; white-space: pre; text-indent: 0; overflow: hidden;
            border: 1px solid #000; padding: 8px; margin: 0.4cm 0; }
.ref { padding-left: 1.27cm; text-indent: -1.27cm; }
"""


def esc(t):
    return html.escape(t)


def figura(nombre, pie):
    ruta = EVID / nombre
    if ruta.exists():
        b64 = base64.b64encode(ruta.read_bytes()).decode()
        return f'<figure><img src="data:image/png;base64,{b64}"><figcaption>{esc(pie)}</figcaption></figure>'
    print(f"AVISO: falta la captura docs/evidencias/{nombre}", file=sys.stderr)
    return (f'<figure><div class="falta">[Falta captura: docs/evidencias/{esc(nombre)}]</div>'
            f'<figcaption>{esc(pie)}</figcaption></figure>')


DIAGRAMA = """   +--------------------------------------------+
   |  Composables: FormularioScreen / Resumen   |
   +--------------------------------------------+
        |  eventos            ^  StateFlow<
        |  (onDestinoChange)  |  FormularioUiState>
        v                     |
   +--------------------------------------------+
   |   EcoTripViewModel (fuente unica de verdad)|
   +--------------------------------------------+
        |                                  |
        | estado temporal                  | preferencias
        v                                  v
   +--------------------+        +----------------------+
   |  SavedStateHandle  |        |   EcoTripDataStore   |
   |  destino, dias,    |        |   (disco) expone     |
   |  modo grupal,      |        |   Flow<Preferencia   |
   |  nombre, transporte|        |   Viaje>             |
   |  (muerte proceso)  |        +----------+-----------+
   +--------------------+                   |
                                            v
                                 +----------------------+
                                 |   PreferenciaViaje   |
                                 |  data class (val)    |
                                 +----------------------+"""


def cuerpo():
    p = []
    # Portada
    p.append('<div class="portada">')
    p.append('<p><b>Universidad / Facultad (completar)</b></p><p>Carrera de Ingeniería (completar)</p><br><br>')
    p.append('<p><b>Informe Técnico: Resiliencia del Estado en Android con Jetpack Compose</b></p>')
    p.append('<p><b>Aplicación EcoTrip 2026</b></p><br>')
    p.append('<p>Examen Práctico RdA-2 · Grupo 4</p><br>')
    for n, r in INTEGRANTES:
        p.append(f'<p>{esc(n)}</p>')
    p.append('<br><p>Asignatura (completar)</p><p>Docente (completar)</p><p>Octubre de 2026</p>')
    p.append('</div>')

    # Introducción
    p.append('<h1 class="sin-salto">Introducción</h1>')
    p.append("""<p>En Android, la interfaz de usuario vive en componentes cuyo ciclo de vida no controla el desarrollador. Una
rotación de pantalla destruye y recrea la <i>Activity</i>; la presión de memoria puede terminar el proceso completo
mientras la aplicación está en segundo plano. Cuando el estado reside únicamente en variables de la UI, cualquiera de
estos eventos borra lo que el usuario había escrito. A este fenómeno se le denomina volatilidad del estado.</p>
<p>EcoTrip 2026 es una aplicación de planificación de viajes sostenibles que sirve como caso de estudio. Su formulario
captura destino, días de duración, modalidad grupal, nombre del viajero, medio de transporte y preferencia de baja huella
de carbono. El objetivo es que cada dato sobreviva al nivel de persistencia que le corresponde: memoria, proceso o disco.
Este informe describe la arquitectura adoptada, las pruebas de resiliencia ejecutadas en el emulador API 36 (Android 16)
y la justificación técnica de la navegación fuertemente tipada.</p>""")

    # Arquitectura
    p.append('<h1>Arquitectura implementada</h1>')
    p.append("""<p>La aplicación sigue el patrón de flujo unidireccional de datos (UDF) en tres capas. El código está escrito
al 100&nbsp;% con Jetpack Compose y Material Design 3, sin vistas XML ni <i>findViewById</i>. El proyecto usa Java 21,
<i>compileSdk</i> y <i>targetSdk</i> 36, y centraliza las dependencias en el catálogo <i>libs.versions.toml</i>.</p>""")
    p.append('<h2>Componentes y responsabilidades</h2>')
    p.append("""<p class="tabla-t">Tabla 1</p><p class="tabla-n">Niveles de persistencia por componente</p>
<table><tr><th>Componente</th><th>Rol</th><th>Sobrevive a rotación</th><th>Sobrevive a muerte de proceso</th><th>Sobrevive a cierre total</th></tr>
<tr><td><i>PreferenciaViaje</i> (data class)</td><td>Modelo inmutable (<i>val</i>) de las preferencias globales</td><td>—</td><td>—</td><td>—</td></tr>
<tr><td>ViewModel (<i>StateFlow</i>)</td><td>Fuente única de verdad de la UI</td><td>Sí</td><td>No</td><td>No</td></tr>
<tr><td><i>SavedStateHandle</i></td><td>Destino, días y modo grupal</td><td>Sí</td><td>Sí</td><td>No</td></tr>
<tr><td>DataStore (Preferences)</td><td>Nombre, transporte y baja huella</td><td>Sí</td><td>Sí</td><td>Sí</td></tr></table>""")
    p.append('<h2>Diagrama conceptual</h2>')
    p.append(f'<p class="tabla-n">Figura 1. Interacción entre PreferenciaViaje, ViewModel, SavedStateHandle y DataStore.</p>'
             f'<div class="diagrama">{esc(DIAGRAMA)}</div>')
    p.append("""<p>La UI (<i>FormularioScreen</i>) no guarda lógica: recibe un <i>FormularioUiState</i> y emite eventos, aplicando
<i>state hoisting</i>. El ViewModel actualiza el estado de forma atómica con <i>MutableStateFlow.update</i> y, para los tres
campos temporales, escribe además en el <i>SavedStateHandle</i>, que el sistema serializa en un <i>Bundle</i> antes de matar
el proceso. Al reconstruirse, el ViewModel lee esos valores como estado inicial. Los datos que deben ser permanentes pasan por
<i>EcoTripDataStore</i>, que expone un <i>Flow&lt;PreferenciaViaje&gt;</i> y escribe con una corrutina (<i>edit</i>) sin
bloquear el hilo principal. DataStore se prefiere sobre SharedPreferences por su API asíncrona basada en corrutinas, su
consistencia transaccional y el manejo explícito de errores de E/S.</p>
<p>La validación se realiza en el ViewModel: los días se interpretan con <i>toIntOrNull()</i> y se rechazan valores vacíos,
no numéricos o menores o iguales a cero; un destino en blanco también genera error. La navegación al resumen solo ocurre si
ambos campos son válidos.</p>""")
    p.append(f'<h2>Repositorio</h2><p>Código fuente disponible públicamente en: <a href="{REPO_URL}">{REPO_URL}</a></p>')

    # Evidencias
    p.append('<h1>Evidencias de pruebas de resiliencia</h1>')
    p.append("""<p>Las pruebas se ejecutaron en el emulador Pixel 8 con Android 16 (API 36). Además de las pruebas manuales, el
proyecto incluye pruebas instrumentadas (<i>ResilienciaTest</i>) que recrean la Activity y verifican la restauración del
<i>SavedStateHandle</i>. Para la muerte de proceso se activó «No conservar actividades», se envió la app a segundo plano
y se terminó el proceso con <i>adb shell am kill</i>: el identificador de proceso cambió (7008 → 7174), lo que confirma que
el proceso fue recreado y no solo la Activity. Para el Color Dinámico se aplicó un fondo de pantalla naranja desde el
selector del sistema y se reabrió la app: la paleta pasó de azul a naranja sin cambios de código.</p>
<p>Durante la primera ejecución de la prueba de muerte de proceso se detectó un defecto: destino, días y modo grupal se
restauraban, pero el nombre, el transporte y la bandera de baja huella volvían a sus valores por defecto, porque solo se
guardaban en DataStore al pulsar el botón de guardar. Se corrigió registrando también esos tres campos en el
<i>SavedStateHandle</i> y dándoles prioridad sobre el valor del disco al iniciar. Las capturas de este informe corresponden
a la versión corregida.</p>""")
    for nombre, pie in EVIDENCIAS:
        p.append(figura(nombre, pie))
    p.append("""<p class="tabla-t">Tabla 2</p><p class="tabla-n">Resultados de las pruebas</p>
<table><tr><th>Prueba</th><th>Procedimiento</th><th>Resultado</th></tr>
<tr><td>Rotación</td><td>Llenar formulario y rotar vertical ↔ horizontal</td><td>OK. Los cinco campos conservan su valor</td></tr>
<tr><td>Muerte de proceso</td><td>Activar «No conservar actividades», enviar la app a segundo plano, <i>am kill</i> y regresar</td><td>OK tras la corrección (falló antes con 3 de 6 campos)</td></tr>
<tr><td>Material You</td><td>Cambiar el fondo de pantalla a naranja y reabrir la app</td><td>OK. La paleta de la UI cambió a tonos naranja</td></tr>
<tr><td>Instrumentadas</td><td><i>./gradlew connectedDebugAndroidTest</i></td><td>OK. 6 de 6 pruebas aprobadas</td></tr></table>""")

    # Type safety
    p.append('<h1>Navegación fuertemente tipada frente a Strings y Bundles</h1>')
    p.append("""<p>En el esquema clásico, cada destino se identificaba con una cadena (<i>"resumen/{destino}/{dias}"</i>) y los
argumentos viajaban como texto o dentro de un <i>Bundle</i>. Ese diseño traslada al tiempo de ejecución errores que el
compilador no puede ver:</p>
<p>1. <b>Rutas mal escritas.</b> Un error tipográfico en la cadena de una ruta solo se descubre al navegar, con un
<i>IllegalArgumentException</i> por destino inexistente.</p>
<p>2. <b>Claves de argumento inconsistentes.</b> Quien escribe la clave <i>"dias"</i> y quien lee <i>"duracion"</i>
obtiene <i>null</i> o un valor por defecto, sin aviso del compilador.</p>
<p>3. <b>Tipos no verificados.</b> Los argumentos de ruta llegan como <i>String</i> y requieren conversiones manuales; un
<i>"abc"</i> donde se espera un entero produce <i>NumberFormatException</i> o un <i>ClassCastException</i> al leer el
<i>Bundle</i>.</p>
<p>4. <b>Argumentos obligatorios ausentes.</b> Nada impide omitir un parámetro al construir la ruta.</p>
<p>Con Navigation Compose 2.8 las rutas son clases <i>@Serializable</i>. En EcoTrip, <i>ResumenRoute</i> es una
<i>data class</i> con seis campos tipados (<i>diasDuracion: Int</i>, <i>soloBajaHuella: Boolean</i>, etc.). El destino se
declara con <i>composable&lt;ResumenRoute&gt;</i>, se invoca con <i>navController.navigate(ResumenRoute(...))</i> y los
argumentos se recuperan con <i>backStackEntry.toRoute&lt;ResumenRoute&gt;()</i>. La serialización y deserialización las
genera el plugin de <i>kotlinx.serialization</i> en tiempo de compilación, de modo que:</p>
<p>• No existen cadenas de ruta que escribir a mano: el tipo es el identificador.</p>
<p>• Faltar un argumento o pasar un tipo incorrecto es un error de compilación, no un <i>crash</i>.</p>
<p>• Renombrar o añadir un campo se propaga a todos los puntos de uso mediante el compilador y el IDE.</p>
<p>• La conversión de tipos ocurre en un único lugar controlado por la librería.</p>
<p>Es importante precisar el alcance: el tipado fuerte elimina los fallos de estructura, nombre y tipo, pero no los de
valor. Por eso EcoTrip valida los datos en el ViewModel antes de navegar. Para la higiene del <i>back stack</i>, el
retorno desde el resumen usa <i>popUpTo&lt;FormularioRoute&gt;</i> con <i>launchSingleTop = true</i>, evitando
formularios duplicados en la pila.</p>""")

    # Conclusiones
    p.append('<h1>Conclusiones y recomendaciones</h1>')
    p.append("""<p>Los resultados de las pruebas de resiliencia (Tabla 2) respaldan la
estrategia de separar el estado por su ciclo de vida: ViewModel para la recomposición y rotación, <i>SavedStateHandle</i>
para la muerte de proceso y DataStore para la persistencia permanente. La navegación tipada reduce la superficie de errores
en tiempo de ejecución y concentra los restantes en la validación de valores.</p>
<p>Recomendaciones de ingeniería:</p>
<p>1. Registrar en <i>SavedStateHandle</i> todo campo de entrada, aunque también tenga destino en DataStore. La prueba de
muerte de proceso demostró que lo que solo vive en memoria o en un almacenamiento que se escribe «al guardar» se pierde
antes de guardar. Esta recomendación ya fue aplicada en la versión entregada.</p>
<p>2. Mantener Espresso actualizado: con la versión 3.6.1 las pruebas instrumentadas fallan en Android 16 por la
eliminación de <i>InputManager.getInstance</i>; se corrigió subiendo a 3.7.0 en el catálogo de versiones.</p>
<p>3. Incorporar pruebas unitarias del ViewModel con un <i>DataStore</i> inyectable mediante una interfaz, para ejecutarlas
sin dispositivo.</p>
<p>4. Incluir la prueba de «No conservar actividades» en la lista de verificación de cada entrega, ya que es la forma más
barata de detectar estado perdido.</p>
<p>5. Pasar a la pantalla de resumen solo un identificador o recuperar los datos desde una única fuente, en lugar de
copiar seis campos en la ruta, si el modelo crece.</p>""")

    # Referencias
    p.append('<h1>Referencias</h1>')
    refs = [
        "Android Developers. (s. f.). <i>Save UI states</i>. Google. https://developer.android.com/topic/libraries/architecture/saving-states",
        "Android Developers. (s. f.). <i>Type safety in Kotlin DSL and Navigation Compose</i>. Google. https://developer.android.com/guide/navigation/design/type-safety",
        "Android Developers. (s. f.). <i>DataStore</i>. Google. https://developer.android.com/topic/libraries/architecture/datastore",
        "Android Developers. (s. f.). <i>Dynamic color</i> (Material Design 3). Google. https://developer.android.com/develop/ui/views/theming/dynamic-colors",
    ]
    for r in refs:
        p.append(f'<p class="ref">{r}</p>')

    # Anexo
    p.append('<h1>Anexo. Código fuente de la aplicación</h1>')
    for rel in CODIGO:
        ruta = RAIZ / rel
        if not ruta.exists():
            print(f"AVISO: no existe {rel}", file=sys.stderr)
            continue
        p.append(f'<p class="codigo-t">{esc(rel)}</p><pre>{esc(ruta.read_text(encoding="utf-8"))}</pre>')
    return "\n".join(p)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    html_path = SALIDA / "informe.html"
    html_path.write_text(
        f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Informe Técnico EcoTrip 2026</title>'
        f'<style>{CSS}</style></head><body>{cuerpo()}</body></html>', encoding="utf-8")
    pdf = SALIDA / "Informe_Tecnico_EcoTrip2026.pdf"
    navegadores = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    exe = next((n for n in navegadores if Path(n).exists()), None)
    if not exe:
        sys.exit("No se encontró Chrome ni Edge; abre informe.html e imprime a PDF.")
    subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", html_path.as_uri()], check=True)
    print(f"PDF generado: {pdf}")


if __name__ == "__main__":
    main()
