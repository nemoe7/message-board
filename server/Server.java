package server;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketAddress;
import java.net.SocketException;
import java.util.HashMap;

import util.MyJSON;

public class Server extends Thread {

    private DatagramSocket ds;
    private byte[] receive = new byte[65535];
    private DatagramPacket packet = null;

    private int port;
    private HashMap<SocketAddress, Client> clientMap = new HashMap<>();
    private HashMap<String, Client> handleMap = new HashMap<>();

    public Server(int port) {

        this.port = port;

        try {
            ds = new DatagramSocket(port);
        } catch (SocketException e) {
            e.printStackTrace();
            System.exit(-1);
        }
    }

    @Override
    public void run() {
        System.out.println("Server: Listening on port " + port);
        try {
            while (true) {
                packet = new DatagramPacket(receive, receive.length);
                ds.receive(packet);

                SocketAddress sa = packet.getSocketAddress();
                MyJSON json = new MyJSON(data(receive).toString());
                String command = json.get("command");

                if (command.equals("join")) { // Client connects
                    if (!clientMap.containsKey(sa)) { // Check if client is already connected
                        Client c = new Client(packet);
                        clientMap.put(sa, c);
                        System.out.println("Server: New client connected at " + c + ".");
                    } else { // Error otherwise
                        error(clientMap.get(sa), "Client already connected.");
                    }
                } else { // If a client is not connecting, it's information will be used;
                    Client c = clientMap.get(sa);
                    System.out.println("Server: New packet received from " + c + ":");
                    if (command.equals("leave")) { // Client disconnects
                        System.out.println("        Client invoked 'leave'.");
                        clientMap.remove(sa); // Remove mappings
                        handleMap.remove(c.getHandle()); // Remove mappings
                        System.out.println("        Client disconnected " + c + ".");
                    } else if (command.equals("register")) { // Client registers new handle
                        String handle = json.get("handle");
                        System.out.println("        Client invoked 'handle' with parameter '" + handle + "'.");
                        if (c.getHandle().equals("") && !handleMap.containsKey(handle)) { // Check if client has associated handle or handle is already taken
                            c.setHandle(handle);
                            handleMap.put(handle, c);
                            System.out.println("Server: Client at " + sa + " registered new alias " + handle);
                        } else { // Error otherwise
                            error(c, "Registration failed. Handle or alias already exists.");
                        }
                    } else { // This block handles json with message attribute
                        String message = json.get("message");
                        if (command.equals("all")) { // Client sends to all
                            System.out.println("        Client invoked 'all' with parameter '" + message + "'.");
                            all(c, json);
                        } else if (command.equals("msg")) { // Client sends to one
                            Client from = c;
                            Client to = handleMap.get(json.get("handle"));
                            System.out.println("        Client invoked 'msg' to '" + to + "'");
                            if (to != null) {
                                MyJSON fromJSON = (MyJSON) json.clone();
                                json.put("message", "[From " + from.getHandle() + "]: " + message);
                                fromJSON.put("message", "[To " + to.getHandle() + "]: " + message);
                                send(to, json);
                                send(from, fromJSON);
                            } else {
                                error(c, "Handle or alias not found.");
                            }
                        }
                    }
                }

                receive = new byte[65535];

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void send(Client c, MyJSON json) {
        InetAddress address = c.getAddress();
        int port = c.getPort();
        byte buf[] = json.toString().getBytes();

        DatagramPacket send = new DatagramPacket(buf, buf.length, address, port);
        try {
            ds.send(send);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void error(Client c, String message) {
        MyJSON json = new MyJSON();
        json.put("command", "error");
        json.put("message", "Error: " + message);
        send(c, json);
    }

    private void all(Client c, MyJSON json) {
        json.put("message", c.getHandle() + ": " + json.get("message"));
        for (Client client : clientMap.values()) {
            send(client, json);
        }
    }

    public static StringBuilder data(byte[] a)
    {
        if (a == null)
            return null;
        StringBuilder ret = new StringBuilder();
        int i = 0;
        while (a[i] != 0)
        {
            ret.append((char) a[i]);
            i++;
        }
        return ret;
    }
}
