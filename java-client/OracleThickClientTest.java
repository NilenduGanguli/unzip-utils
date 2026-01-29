import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Properties;

public class OracleThickClientTest {
    public static void main(String[] args) {
        String jdbcUrl = "jdbc:oracle:oci:@//oracle-server:1521/FREEPDB1";
        String user = "unzip_user";
        String password = "YourStrong!Passw0rd";

        System.out.println("Starting Oracle Thick Client Test...");
        System.out.println("URL: " + jdbcUrl);

        try {
            // Explicitly load the driver to verify it's on classpath
            Class.forName("oracle.jdbc.OracleDriver");

            Properties props = new Properties();
            props.setProperty("user", user);
            props.setProperty("password", password);

            Connection conn = DriverManager.getConnection(jdbcUrl, props);
            System.out.println("Connected successfully via OCI Driver!");

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT 'Hello from Oracle DB - ' || version FROM v$instance");
            
            while (rs.next()) {
                System.out.println("Query Result: " + rs.getString(1));
            }
            
            rs.close();
            stmt.close();
            conn.close();
        } catch (Exception e) {
            System.err.println("Connection failed:");
            e.printStackTrace();
        }
        
        // Keep alive for a bit
        try { Thread.sleep(50000); } catch (InterruptedException e) {}
    }
}
