package util;
import java.util.HashMap;
import java.util.Set;

public class MyJSON extends HashMap<String, Object>{

    public MyJSON() {
        super();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("{");
        Set<String> keySet = this.keySet();
        for (int i = 0; i < keySet().size(); i++) {
            sb.append("\"" + keySet.toArray()[i] + "\":\"" + this.get(keySet.toArray()[i]) + "\"");
            if (i < keySet().size() - 1) {
                sb.append(", ");
            }
        }
        sb.append("}");
        return sb.toString();
    }

    public static MyJSON parseString(String s) {
        MyJSON json = new MyJSON();
        String[] remove = {"{", "}"};
        for (String string : remove) {
            s = s.replace(string, "");
        }
        String[] kvp = s.split(", ");
        for (String string : kvp) {
            String k = string.split(":")[0].replace("\"", "");
            String v = string.split(":")[1].replace("\"", "");
            json.put(k, v);
        }
        return json;
    }

    public static void main(String[] args) {
        System.out.println(MyJSON.parseString("{\"test\":\"a thing\", \"this\":\"12345\"}"));
    }
}