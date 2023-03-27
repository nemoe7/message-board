package server;

import java.net.DatagramPacket;
import java.net.InetAddress;

public class Client extends Thread {

    private String handle = "";
    private InetAddress address;
    private int port;

    public Client(DatagramPacket packet) {
        this.address = packet.getAddress();
        this.port = packet.getPort();
    }

    public String getHandle() {
        return this.handle;
    }

    public void setHandle(String handle) {
        this.handle = handle;
    }

    public InetAddress getAddress() {
        return this.address;
    }

    public int getPort() {
        return this.port;
    }

    @Override
    public String toString() {
        if (handle.equals("")) {
            return this.address + "/" + this.port;
        } else {
            return this.handle + " (" + this.address + "/" + this.port + ")";
        }
    }
}
