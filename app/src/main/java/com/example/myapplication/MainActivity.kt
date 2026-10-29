package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myapplication.navigation.EcoTripNavHost
import com.example.myapplication.ui.theme.MyApplicationTheme
import com.example.myapplication.ui.viewmodel.EcoTripViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                val ecoTripViewModel: EcoTripViewModel = viewModel(
                    factory = EcoTripViewModel.factory(application)
                )
                EcoTripNavHost(viewModel = ecoTripViewModel)
            }
        }
    }
}
