package com.example.myapplication.data.local

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.example.myapplication.data.model.PreferenciaViaje
import com.example.myapplication.data.model.TipoTransporte
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "ecotrip_preferences")

class EcoTripDataStore(private val context: Context) {

    companion object {
        val KEY_NOMBRE_VIAJERO = stringPreferencesKey("key_nombre_viajero")
        val KEY_TIPO_TRANSPORTE = stringPreferencesKey("key_tipo_transporte")
        val KEY_SOLO_BAJA_HUELLA = booleanPreferencesKey("key_solo_baja_huella")
    }

    val preferenciaViajeFlow: Flow<PreferenciaViaje> = context.dataStore.data
        .catch { exception ->
            if (exception is IOException) {
                emit(emptyPreferences())
            } else {
                throw exception
            }
        }
        .map { preferences ->
            val nombre = preferences[KEY_NOMBRE_VIAJERO] ?: ""
            val transporteStr = preferences[KEY_TIPO_TRANSPORTE] ?: TipoTransporte.TREN.name
            val transporte = try {
                TipoTransporte.valueOf(transporteStr)
            } catch (e: IllegalArgumentException) {
                TipoTransporte.TREN
            }
            val bajaHuella = preferences[KEY_SOLO_BAJA_HUELLA] ?: false

            PreferenciaViaje(
                nombreViajero = nombre,
                transporteSeleccionado = transporte,
                soloBajaHuella = bajaHuella
            )
        }

    suspend fun guardarPreferenciasGlobales(preferencia: PreferenciaViaje) {
        context.dataStore.edit { preferences ->
            preferences[KEY_NOMBRE_VIAJERO] = preferencia.nombreViajero
            preferences[KEY_TIPO_TRANSPORTE] = preferencia.transporteSeleccionado.name
            preferences[KEY_SOLO_BAJA_HUELLA] = preferencia.soloBajaHuella
        }
    }
}