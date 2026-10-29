package com.example.myapplication.ui.state

import com.example.myapplication.data.model.TipoTransporte

data class FormularioUiState(
    // Persistencia permanente (DataStore)
    val nombreViajero: String = "",
    val transporteSeleccionado: TipoTransporte = TipoTransporte.TREN,
    val soloBajaHuella: Boolean = false,

    // Persistencia de proceso (SavedStateHandle)
    val destino: String = "",
    val diasDuracionTexto: String = "",
    val esViajeGrupal: Boolean = false,

    // Feedback de validación
    val errorDestino: String? = null,
    val errorDias: String? = null
)