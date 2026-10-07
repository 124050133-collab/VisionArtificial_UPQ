package java_gui;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class LoginFrame extends JFrame {
    private JTextField txtUsuario;
    private JPasswordField txtContrasena;
    private JButton btnLogin;
    private JButton btnRegistrar;

    // Ruta al ejecutable de Python y al script bridge
    private static final String PYTHON_PATH = "C:\\Users\\pablo\\AppData\\Local\\Programs\\Python\\Python311\\python.exe";
    private static final String BRIDGE_PATH = "c:/Examen_IA/VisionArtificial_UPQ/python_backend/main_bridge.py";

    public LoginFrame() {
        setTitle("Sistema de Visión Artificial - Login");
        setSize(400, 250);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new GridBagLayout());

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8, 8, 8, 8);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // Usuario
        gbc.gridx = 0; gbc.gridy = 0;
        add(new JLabel("Usuario:"), gbc);
        
        gbc.gridx = 1; gbc.gridy = 0;
        txtUsuario = new JTextField(15);
        add(txtUsuario, gbc);

        // Contraseña
        gbc.gridx = 0; gbc.gridy = 1;
        add(new JLabel("Contraseña:"), gbc);

        gbc.gridx = 1; gbc.gridy = 1;
        txtContrasena = new JPasswordField(15);
        add(txtContrasena, gbc);

        // Botón Login
        gbc.gridx = 0; gbc.gridy = 2;
        btnLogin = new JButton("Iniciar Sesión");
        add(btnLogin, gbc);

        // Botón Registro
        gbc.gridx = 1; gbc.gridy = 2;
        btnRegistrar = new JButton("Registrarse");
        add(btnRegistrar, gbc);

        // Evento Iniciar Sesión
        btnLogin.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ejecutarLogin();
            }
        });

        // Evento Registro
        btnRegistrar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                ejecutarRegistro();
            }
        });
    }

    private void ejecutarLogin() {
        String usuario = txtUsuario.getText().trim();
        String contrasena = new String(txtContrasena.getPassword()).trim();

        if (usuario.isEmpty() || contrasena.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Por favor llena todos los campos.", "Advertencia", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            ProcessBuilder pb = new ProcessBuilder(PYTHON_PATH, BRIDGE_PATH, "login", usuario, contrasena);
            Process p = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String respuesta = reader.readLine();

            if (respuesta != null && respuesta.contains("\"status\": \"ok\"")) {
                JOptionPane.showMessageDialog(this, "¡Bienvenido al Sistema!", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                
                // --- LÍNEA CLAVE: Abre la ventana principal ---
                new MainFrame().setVisible(true);
                
                // Cierra la ventana de Login actual
                this.dispose(); 
            } else {
                JOptionPane.showMessageDialog(this, "Credenciales incorrectas.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error de comunicación con Python: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void ejecutarRegistro() {
        String usuario = txtUsuario.getText().trim();
        String contrasena = new String(txtContrasena.getPassword()).trim();

        if (usuario.isEmpty() || contrasena.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Ingresa un usuario y contraseña para registrarte.", "Advertencia", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            // Se envía: comando, nombre, ap_pat, ap_mat, usuario, contraseña
            ProcessBuilder pb = new ProcessBuilder(PYTHON_PATH, BRIDGE_PATH, "registrar", "Usuario", "Demo", "UPQ", usuario, contrasena);
            Process p = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String respuesta = reader.readLine();

            if (respuesta != null && respuesta.contains("\"status\": \"ok\"")) {
                JOptionPane.showMessageDialog(this, "¡Bienvenido al Sistema!", "Éxito", JOptionPane.INFORMATION_MESSAGE);
                
                // --- AGREGAR ESTA LÍNEA PARA ABRIR EL MAINFRAME ---
                new MainFrame().setVisible(true);
                
                this.dispose(); // Cierra la pantalla de Login
            } else {
                JOptionPane.showMessageDialog(this, "Credenciales incorrectas.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error de comunicación con Python: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new LoginFrame().setVisible(true);
        });
    }
}