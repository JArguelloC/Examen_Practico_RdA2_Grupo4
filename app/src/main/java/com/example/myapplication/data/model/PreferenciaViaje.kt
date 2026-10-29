package com.example.myapplication.data.model

import kotlinx.serialization.Serializable

enum class TipoTransporte {
    TREN,
    BICICLETA,
    VEHICULO_ELECTRICO
}

@Serializable
data class PreferenciaViaje(
    val nombreViajero: String = "",
    val transporteSeleccionado: TipoTransporte = TipoTransporte.TREN,
    val soloBajaHuella: Boolean = false
)