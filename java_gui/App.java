package java_gui;

import javax.swing.SwingUtilities;

public class App {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            // Inicia la aplicación cargando la pantalla de Login
            new LoginFrame().setVisible(true);
        });
    }
}