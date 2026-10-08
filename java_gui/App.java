package java_gui;

import javax.swing.*;

public class App {
    public static void main(String[] args) {
        // Activa el Look and Feel nativo del sistema operativo (Windows)
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            System.out.println("No se pudo cargar el estilo nativo: " + e.getMessage());
        }

        SwingUtilities.invokeLater(() -> {
            new LoginFrame().setVisible(true);
        });
    }
}