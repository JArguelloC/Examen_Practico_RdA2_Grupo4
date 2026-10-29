package com.example.myapplication.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Place
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.myapplication.data.model.TipoTransporte
import com.example.myapplication.navigation.ResumenRoute
import com.example.myapplication.ui.theme.MyApplicationTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResumenScreen(
    route: ResumenRoute,
    onVolver: () -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        modifier = modifier,
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            TopAppBar(
                title = { Text("Resumen de ruta") },
                navigationIcon = {
                    IconButton(onClick = onVolver) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Volver al formulario"
                        )
                    }
                }
            )
        }
    ) { innerPadding ->
        BoxWithConstraints(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            val wideLayout = maxWidth >= 600.dp
            Column(
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(
                        text = "Tu viaje está listo",
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.onSurface,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Revisa los detalles de tu próxima aventura.",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }

                DestinationCard(
                    destino = route.destino,
                    diasDuracion = route.diasDuracion
                )

                if (wideLayout) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalAlignment = Alignment.Top
                    ) {
                        TravelerCard(
                            nombreViajero = route.nombreViajero,
                            esViajeGrupal = route.esViajeGrupal,
                            modifier = Modifier.weight(1f)
                        )
                        TransportCard(
                            transporte = route.transporte,
                            soloBajaHuella = route.soloBajaHuella,
                            modifier = Modifier.weight(1f)
                        )
                    }
                } else {
                    TravelerCard(
                        nombreViajero = route.nombreViajero,
                        esViajeGrupal = route.esViajeGrupal
                    )
                    TransportCard(
                        transporte = route.transporte,
                        soloBajaHuella = route.soloBajaHuella
                    )
                }
            }
        }
    }
}

@Composable
private fun DestinationCard(
    destino: String,
    diasDuracion: Int,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer,
            contentColor = MaterialTheme.colorScheme.onPrimaryContainer
        ),
        shape = RoundedCornerShape(24.dp)
    ) {
        Row(
            modifier = Modifier.padding(20.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Filled.Place,
                contentDescription = null
            )
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = destino.ifBlank { "Destino sin especificar" },
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.SemiBold
                )
                Text(
                    text = "$diasDuracion ${if (diasDuracion == 1) "día" else "días"}",
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }
    }
}

@Composable
private fun TravelerCard(
    nombreViajero: String,
    esViajeGrupal: Boolean,
    modifier: Modifier = Modifier
) {
    DetailCard(
        title = "Viajero",
        icon = Icons.Filled.Person,
        modifier = modifier
    ) {
        DetailLine(
            label = "Nombre",
            value = nombreViajero.ifBlank { "No especificado" }
        )
        StatusIndicator(
            label = "Modalidad",
            value = if (esViajeGrupal) "Grupal" else "Individual"
        )
    }
}

@Composable
private fun TransportCard(
    transporte: String,
    soloBajaHuella: Boolean,
    modifier: Modifier = Modifier
) {
    DetailCard(
        title = "Movilidad sostenible",
        icon = Icons.Filled.Info,
        modifier = modifier
    ) {
        DetailLine(
            label = "Transporte",
            value = transporte.toTransportLabel()
        )
        StatusIndicator(
            label = "Rutas de baja huella",
            value = if (soloBajaHuella) "Activado" else "Desactivado"
        )
    }
}

@Composable
private fun DetailCard(
    title: String,
    icon: ImageVector,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        border = CardDefaults.outlinedCardBorder(),
        shape = RoundedCornerShape(20.dp)
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary
                )
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleLarge,
                    color = MaterialTheme.colorScheme.onSurface,
                    fontWeight = FontWeight.SemiBold
                )
            }
            content()
        }
    }
}

@Composable
private fun DetailLine(
    label: String,
    value: String
) {
    Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurface
        )
    }
}

@Composable
private fun StatusIndicator(
    label: String,
    value: String
) {
    Surface(
        color = MaterialTheme.colorScheme.secondaryContainer,
        contentColor = MaterialTheme.colorScheme.onSecondaryContainer,
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 10.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = value,
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

private fun String.toTransportLabel(): String = when (this) {
    TipoTransporte.TREN.name -> "Tren"
    TipoTransporte.BICICLETA.name -> "Bicicleta"
    TipoTransporte.VEHICULO_ELECTRICO.name -> "Vehículo eléctrico"
    else -> "No especificado"
}

@Preview(showBackground = true, widthDp = 390, heightDp = 800)
@Composable
private fun ResumenScreenPreview() {
    MyApplicationTheme(dynamicColor = false) {
        ResumenScreen(
            route = ResumenRoute(
                nombreViajero = "Mateo Morales",
                transporte = TipoTransporte.TREN.name,
                soloBajaHuella = true,
                destino = "Parque Nacional Cotopaxi",
                diasDuracion = 3,
                esViajeGrupal = true
            ),
            onVolver = {}
        )
    }
}
