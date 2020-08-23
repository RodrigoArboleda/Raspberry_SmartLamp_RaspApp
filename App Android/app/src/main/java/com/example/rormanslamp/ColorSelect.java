package com.example.rormanslamp;

import android.bluetooth.BluetoothAdapter;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

import top.defaults.colorpicker.ColorPickerView;

public class ColorSelect extends AppCompatActivity {

    private ThreadBluetooth bluetoothThread = null;

    private String color_text = null;

    private static final int INITIAL_COLOR = 0xFFFFFFFF;


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        Intent intent = getIntent();
        String MAC_Bluetooth = intent.getStringExtra("MAC_Bluetooth");

        BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_color_select);

        try {
            bluetoothThread = new ThreadBluetooth(MAC_Bluetooth, bluetoothAdapter);
        }catch (Exception erro){
            Toast.makeText(getApplicationContext(), "Erro ao iniciar conexão.", Toast.LENGTH_LONG).show();
            finish();
        }

        final Button sendButton = findViewById(R.id.sendMsg);

        final ColorPickerView colorPickerView = findViewById(R.id.colorPicker);

        if(bluetoothThread != null && bluetoothThread.getConnect()){
            sendButton.setOnClickListener(v -> {
                try {
                    if (color_text != null){
                        bluetoothThread.write(color_text);
                    }
                    else {
                        Toast.makeText(getApplicationContext(), "Cor não definida.", Toast.LENGTH_LONG).show();
                    }
                }catch (Exception erro){
                    Toast.makeText(getApplicationContext(), "Falha na conexão.", Toast.LENGTH_LONG).show();
                    finish();
                }
            });
        }

        colorPickerView.subscribe((color, fromUser, shouldPropagate) -> color_text = colorHex(color));
        colorPickerView.setInitialColor(INITIAL_COLOR);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (bluetoothThread != null){
            try {
                bluetoothThread.write("quit000000");
                bluetoothThread.close_socket();
            }catch (Exception erro){
                Toast.makeText(getApplicationContext(), "Erro ao encerrar conexão.", Toast.LENGTH_LONG).show();
            }
        }
    }

    private String colorHex(int color) {
        int a = Color.alpha(color);
        int r = Color.red(color);
        int g = Color.green(color);
        int b = Color.blue(color);
        return String.format(Locale.getDefault(), "0x%02X%02X%02X%02X", a, r, g, b);
    }
}
