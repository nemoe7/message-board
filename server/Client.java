package server;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

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
    public void start() {
        Scanner scanner = new Scanner(System.in);
        String handle = "";
        while (true) {
            try {
                System.out.print("Enter command (join/register/msg/all/leave): ");
                String command = scanner.nextLine();
                MyJSON json = new MyJSON();
                if (command.equals("?")) {
                    System.out.print("Command List:\n")
                    System.out.print("/join - Connect to server application\n")
                    System.out.print("/leave - Disconnect to server application\n")
                    System.out.print("/register - Register a unique handle or alias\n")
                    System.out.print("/all - Send message to all\n")
                    System.out.print("/msg - Send direct message to a single handle\n")
                }
                else if (command.equals("join")) {
                    json.put("command", "join");
                    send(json);
                } else if (command.equals("register")) {
                    if (!handle.equals("")) {
                        System.out.println("You already have a handle: " + handle);
                        continue;
                    }
                    System.out.print("Enter handle: ");
                    handle = scanner.nextLine();
                    json.put("command", "register");
                    json.put("handle", handle);
                    send(json);
                } else if (command.equals("msg")) {
                    if (handle.equals("")) {
                        System.out.println("You must register a handle first.");
                        continue;
                    }
                    System.out.print("Enter recipient handle: ");
                    String to = scanner.nextLine();
                    System.out.print("Enter message: ");
                    String message = scanner.nextLine();
                    json.put("command", "msg");
                    json.put("handle", to);
                    json.put("message", message);
                    send(json);
                } else if (command.equals("all")) {
                    if (handle.equals("")) {
                        System.out.println("You must register a handle first.");
                        continue;
                    }
                    System.out.print("Enter message: ");
                    String message = scanner.nextLine();
                    json.put("command", "all");
                    json.put("message", message);
                    send(json);
                } else if (command.equals("leave")) {
                    json.put("command", "leave");
                    send(json);
                    break;
                } else {
                    System.out.println("Invalid command.");
                    continue;
                }
                receive();
            } catch (SocketTimeoutException e) {
                System.out.println("Server not responding.");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        scanner.close();
    }

    private void send(MyJSON json) throws IOException {
        byte[] buf = json.toString().getBytes();
        DatagramPacket sendPacket = new DatagramPacket(buf, buf.length, serverAddress, serverPort);
        ds.send(sendPacket);
    }

    private void receive() throws IOException {
        byte[] buf = new byte[65535];
        DatagramPacket receivePacket = new DatagramPacket(buf, buf.length);
        ds.receive(receivePacket);
        MyJSON json = new MyJSON(new String(receivePacket.getData(), 0, receivePacket.getLength()));
        String command = json.get("command");
        if (command.equals("join")) {
            String handle = json.get("handle");
            System.out.println("Joined with handle: " + handle);
        } else if (command.equals("error")) {
            String message = json.get("message");
            System.out.println("Error: " + message);
        } else if (command.equals("msg")) {
            String from = json.get("From");
            String message = json.get(message);
            String to = json.get(to);
            Sytem.out.println("[" + from + to + "]: " + message);
        }
    }
}
