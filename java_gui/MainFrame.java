package java_gui;

import javax.swing.*;
import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

public class MainFrame extends JFrame {
    private JLabel lblImagen;
    private JButton btnBuscar;
    private JButton btnCamara;
    private JButton btnProcesar;
    private JButton btnLimpiar;
    private String rutaImagenActual = "";

    private static final String PYTHON_PATH = "C:\\Users\\pablo\\AppData\\Local\\Programs\\Python\\Python311\\python.exe";
    private static final String BRIDGE_PATH = "c:/Examen_IA/VisionArtificial_UPQ/python_backend/main_bridge.py";

    public MainFrame() {
        setTitle("Sistema de Visión Artificial - Captura y Carga");
        setSize(700, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        // Panel superior para botones
        JPanel panelBotones = new JPanel();
        btnBuscar = new JButton("Buscar Foto Local");
        btnCamara = new JButton("Encender Cámara / Tomar Foto");
        btnLimpiar = new JButton("Limpiar");
        btnProcesar = new JButton("Preprocesamiento >>");

        panelBotones.add(btnBuscar);
        panelBotones.add(btnCamara);
        panelBotones.add(btnLimpiar);
        panelBotones.add(btnProcesar);

        add(panelBotones, BorderLayout.NORTH);

        // Visor de Imagen al centro
        lblImagen = new JLabel("No hay imagen cargada", SwingConstants.CENTER);
        lblImagen.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        add(lblImagen, BorderLayout.CENTER);

        // Eventos con expresiones lambda (sin necesidad de ActionListener explícito)
        btnBuscar.addActionListener(e -> buscarFotoLocal());
        btnCamara.addActionListener(e -> tomarFotoCamara());
        btnLimpiar.addActionListener(e -> limpiarVista());
        btnProcesar.addActionListener(e -> abrirPreprocesamiento());
    }

    private void buscarFotoLocal() {
        JFileChooser fileChooser = new JFileChooser();
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            rutaImagenActual = selectedFile.getAbsolutePath();
            mostrarImagen(rutaImagenActual);
        }
    }

    private void tomarFotoCamara() {
        try {
            String rutaTemp = "captura_temp.jpg";
            ProcessBuilder pb = new ProcessBuilder(PYTHON_PATH, BRIDGE_PATH, "capturar_foto", rutaTemp);
            Process p = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String respuesta = reader.readLine();

            if (respuesta != null && respuesta.contains("\"status\": \"ok\"")) {
                rutaImagenActual = new File(rutaTemp).getAbsolutePath();
                mostrarImagen(rutaImagenActual);
                JOptionPane.showMessageDialog(this, "Foto tomada con éxito.", "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "No se pudo acceder a la cámara.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error al invocar la cámara: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void mostrarImagen(String ruta) {
        ImageIcon icon = new ImageIcon(ruta);
        Image img = icon.getImage().getScaledInstance(500, 350, Image.SCALE_SMOOTH);
        lblImagen.setIcon(new ImageIcon(img));
        lblImagen.setText("");
    }

    private void limpiarVista() {
        rutaImagenActual = "";
        lblImagen.setIcon(null);
        lblImagen.setText("No hay imagen cargada");
    }

    private void abrirPreprocesamiento() {
        if (rutaImagenActual.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Primero selecciona o toma una foto.", "Advertencia", JOptionPane.WARNING_MESSAGE);
            return;
        }
        new ProcessFrame(rutaImagenActual).setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new MainFrame().setVisible(true);
        });
    }
}