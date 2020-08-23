package com.example.rormanslamp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;


import java.io.OutputStream;
import java.util.UUID;

@SuppressWarnings("WeakerAccess")
public class ThreadBluetooth extends Thread{
    private final OutputStream mmOutStream;
    private BluetoothSocket socket;
    private boolean connect;

    //Call this from the main activity to create a connection
    public ThreadBluetooth(String MAC_Bluetooth, BluetoothAdapter bluetoothAdapter) throws Exception{
        OutputStream tmpOut;
        UUID uuid = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");

        BluetoothDevice bluetoothDevice = bluetoothAdapter.getRemoteDevice(MAC_Bluetooth);

        socket = bluetoothDevice.createRfcommSocketToServiceRecord(uuid);

        socket.connect();

        connect = true;

        tmpOut = socket.getOutputStream();

        mmOutStream = tmpOut;

    }

    // Call this from the main activity to take connection status
    public boolean getConnect(){
        return connect;
    }

    // Call this from the main activity to send data to the remote device.
    public void write(String msg) throws Exception{
        byte[] byte_msg = msg.getBytes();
            mmOutStream.write(byte_msg );
    }

    // Call this from the main activity to close connection
    public void close_socket() throws Exception{
       if(connect){
               socket.close();
               connect = false;
       }
    }
}
