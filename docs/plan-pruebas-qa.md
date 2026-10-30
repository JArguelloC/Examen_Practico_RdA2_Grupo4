# Plan de pruebas QA – EcoTrip 2026

Responsable: Ángel Loor · Rama: `feature/qa-resilience-docs`
Dispositivo: Emulador Android API 36 (Android 16). Guardar las capturas en `docs/evidencias/`.

## Pruebas automatizadas

`app/src/androidTest/.../ResilienciaTest.kt` (requiere emulador o dispositivo):

```
./gradlew connectedDebugAndroidTest
```

| Prueba | Qué verifica |
|---|---|
| `rotacion_conservaDestinoYDias` | Tras recrear la Activity, destino y días siguen en pantalla |
| `procesoMuerto_viewModelRestauraFormularioDesdeSavedStateHandle` | El ViewModel reconstruye el formulario desde `SavedStateHandle` |
| `savedStateHandle_seActualizaConCadaCambioDelFormulario` | Cada cambio se escribe en el `SavedStateHandle` |
| `validacion_diasInvalidosGeneranError` | `abc`, `0` y vacío dan error; `5` no |
| `validacion_destinoVacioGeneraError` | Destino en blanco da error |

## Pruebas manuales obligatorias

### 1. Rotación
1. Abrir la app. Escribir nombre, destino «Quito», días «4», activar «Viaje grupal».
2. Rotar vertical → horizontal → vertical (botones de rotación del emulador, con auto-rotate activo).
3. **Esperado:** todos los campos conservan su valor.
4. Evidencia: `01-rotacion-vertical.png`, `02-rotacion-horizontal.png`.

### 2. Muerte de proceso
1. Ajustes → Opciones de desarrollador → activar **«No conservar actividades»** (*Don't keep activities*).
2. Abrir la app y llenar destino, días y «Viaje grupal».
3. Pulsar Home (la Activity se destruye) y volver desde recientes.
4. **Esperado:** destino, días y modo grupal siguen intactos.
5. Alternativa más estricta: con la app en segundo plano, `adb shell am kill com.example.myapplication` y reabrir desde recientes.
6. Comprobar además que nombre, transporte y «baja huella» persisten tras **cerrar la app por completo** (DataStore, disco).
7. Evidencia: `03-process-death-antes.png`, `04-process-death-despues.png`.

### 3. Material You
1. Pantalla de inicio → fondo de pantalla → elegir una imagen con color dominante distinto (p. ej. azul y luego naranja).
2. Abrir la app (Android 12+ con `dynamicColor` activo).
3. **Esperado:** cambian `TopAppBar`, tarjetas y superficies según el fondo.
4. Evidencia: `05-material-you-fondo-A.png`, `06-material-you-fondo-B.png` (formulario y resumen en ambos).

### Extra: navegación
- Formulario → Resumen → flecha atrás: no se duplica el Formulario en el back stack.
- Guardar con campos vacíos: aparecen errores y no navega.

## Registro de resultados

| # | Prueba | Fecha | Resultado | Evidencia |
|---|---|---|---|---|
| 1 | Rotación | | ☐ OK ☐ Falla | |
| 2 | Muerte de proceso | | ☐ OK ☐ Falla | |
| 3 | Material You | | ☐ OK ☐ Falla | |
| 4 | Tests instrumentados | | ☐ OK ☐ Falla | |
| 5 | Navegación / back stack | | ☐ OK ☐ Falla | |

## Hallazgos de la QA
- **Corregido.** La primera prueba real de muerte de proceso mostró que nombre, transporte y «baja huella» se perdían (solo se guardaban en DataStore al pulsar el FAB). Ahora también se registran en `SavedStateHandle` y prevalecen sobre el disco al iniciar.
- **Corregido.** Espresso 3.6.1 falla en Android 16 (`InputManager.getInstance`); se subió a 3.7.0 en `libs.versions.toml`.

## Resultados (ejecutados en Pixel 8 API 36)
Rotación OK · Muerte de proceso OK (PID 7008 → 7174 tras `am kill`) · Material You OK (fondo naranja) · `connectedDebugAndroidTest` 6/6 OK.
