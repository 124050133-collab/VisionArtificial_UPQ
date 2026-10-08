package java_gui;

import javax.swing.*;
import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

public class ProcessFrame extends JFrame {
    private String rutaImagenOriginal;
    private String rutaImagenProcesada;
    private JLabel lblVisor;
    private JComboBox<String> comboFiltros;
    private JSlider sliderGamma;
    private JButton btnAplicar;
    private JButton btnGuardarBD;
    private JButton btnSepararCapas;

    private static final String PYTHON_PATH = "C:\\Users\\pablo\\AppData\\Local\\Programs\\Python\\Python311\\python.exe";
    private static final String BRIDGE_PATH = "c:/Examen_IA/VisionArtificial_UPQ/python_backend/main_bridge.py";

    public ProcessFrame(String rutaImagen) {
        this.rutaImagenOriginal = rutaImagen;
        this.rutaImagenProcesada = rutaImagen;

        setTitle("Sistema de Visión Artificial - Preprocesamiento");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        lblVisor = new JLabel("", SwingConstants.CENTER);
        mostrarImagen(rutaImagenOriginal);
        add(lblVisor, BorderLayout.CENTER);

        JPanel panelControles = new JPanel();
        panelControles.setLayout(new BoxLayout(panelControles, BoxLayout.Y_AXIS));
        panelControles.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        panelControles.add(new JLabel("Filtro / Proceso:"));
        String[] opciones = {"Original", "Grises", "Gamma", "Negativo", "Histograma", "SegmentarRojo", "SegmentarVerde", "SegmentarAzul"};
        comboFiltros = new JComboBox<>(opciones);
        panelControles.add(comboFiltros);

        panelControles.add(Box.createVerticalStrut(10));
        panelControles.add(new JLabel("Ajuste Gamma (0.1 - 3.0):"));
        sliderGamma = new JSlider(1, 30, 8);
        panelControles.add(sliderGamma);

        panelControles.add(Box.createVerticalStrut(15));
        btnAplicar = new JButton("Aplicar Filtro");
        panelControles.add(btnAplicar);

        panelControles.add(Box.createVerticalStrut(15));
        btnGuardarBD = new JButton("Guardar en BD (Matriz Píxeles)");
        panelControles.add(btnGuardarBD);

        panelControles.add(Box.createVerticalStrut(15));
        btnSepararCapas = new JButton("Ver Separación de Capas");
        panelControles.add(btnSepararCapas);

        add(panelControles, BorderLayout.EAST);

        btnAplicar.addActionListener(e -> aplicarProceso());
        btnGuardarBD.addActionListener(e -> guardarEnBaseDatos());
        btnSepararCapas.addActionListener(e -> mostrarCapas());
    }

    private String normalizarRuta(String ruta) {
        if (ruta == null || ruta.isEmpty()) return "";
        return new File(ruta).getAbsolutePath().replace("\\", "/");
    }

    private void aplicarProceso() {
        String seleccion = (String) comboFiltros.getSelectedItem();
        if ("Original".equals(seleccion)) {
            rutaImagenProcesada = rutaImagenOriginal;
            mostrarImagen(rutaImagenOriginal);
            return;
        }

        try {
            String rutaOrigenAbs = normalizarRuta(rutaImagenOriginal);
            String rutaSalidaAbs = normalizarRuta("temp_procesada.jpg");
            double valGamma = sliderGamma.getValue() / 10.0;

            ProcessBuilder pb = new ProcessBuilder(
                PYTHON_PATH, 
                BRIDGE_PATH, 
                "procesar", 
                rutaOrigenAbs, 
                seleccion, 
                rutaSalidaAbs, 
                String.valueOf(valGamma)
            );

            Process p = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(p.getErrorStream()));

            String respuesta = reader.readLine();

            StringBuilder sbError = new StringBuilder();
            String errLine;
            while ((errLine = errorReader.readLine()) != null) {
                sbError.append(errLine).append("\n");
            }

            if (respuesta != null && respuesta.contains("\"status\": \"ok\"")) {
                rutaImagenProcesada = rutaSalidaAbs;
                mostrarImagen(rutaImagenProcesada);
            } else {
                String detalle = sbError.length() > 0 ? sbError.toString() : (respuesta != null ? respuesta : "Sin respuesta de Python");
                JOptionPane.showMessageDialog(this, "Error de Python:\n" + detalle, "Error al Aplicar Filtro", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error en Java: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void guardarEnBaseDatos() {
        try {
            String rutaProcesadaAbs = normalizarRuta(rutaImagenProcesada);
            String tipo = (String) comboFiltros.getSelectedItem();

            ProcessBuilder pb = new ProcessBuilder(PYTHON_PATH, BRIDGE_PATH, "guardar_bd", rutaProcesadaAbs, tipo);
            Process p = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(p.getErrorStream()));

            String respuesta = reader.readLine();

            StringBuilder sbError = new StringBuilder();
            String errLine;
            while ((errLine = errorReader.readLine()) != null) {
                sbError.append(errLine).append("\n");
            }

            if (respuesta != null && respuesta.contains("\"status\": \"ok\"")) {
                JOptionPane.showMessageDialog(this, "Imagen descompuesta y guardada correctamente en BD por píxel (RGB).", "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } else {
                String detalle = sbError.length() > 0 ? sbError.toString() : (respuesta != null ? respuesta : "Sin respuesta de Python");
                JOptionPane.showMessageDialog(this, "Error al guardar en BD:\n" + detalle, "Error", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error en Java: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void mostrarCapas() {
        try {
            String rutaOrigenAbs = normalizarRuta(rutaImagenOriginal);
            String carpetaCapas = normalizarRuta("capas_out");

            ProcessBuilder pb = new ProcessBuilder(PYTHON_PATH, BRIDGE_PATH, "separar_capas", rutaOrigenAbs, carpetaCapas);
            Process p = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(p.getErrorStream()));

            String respuesta = reader.readLine();

            if (respuesta != null && respuesta.contains("\"status\": \"ok\"")) {
                JFrame frameCapas = new JFrame("Separación de Capas (R, G, B, M, Y, C)");
                frameCapas.setLayout(new GridLayout(2, 3));
                frameCapas.setSize(900, 600);

                String[] nombres = {"Rojo", "Verde", "Azul", "Magenta", "Amarillo", "Cian"};
                for (String c : nombres) {
                    String rutaCapa = carpetaCapas + "/capa_" + c + ".jpg";
                    ImageIcon icon = new ImageIcon(rutaCapa);
                    Image img = icon.getImage().getScaledInstance(280, 250, Image.SCALE_SMOOTH);
                    JLabel lbl = new JLabel(c, new ImageIcon(img), JLabel.CENTER);
                    lbl.setVerticalTextPosition(JLabel.BOTTOM);
                    lbl.setHorizontalTextPosition(JLabel.CENTER);
                    frameCapas.add(lbl);
                }
                frameCapas.setVisible(true);
            } else {
                String errLine = errorReader.readLine();
                JOptionPane.showMessageDialog(this, "Error al generar capas: " + (errLine != null ? errLine : "Error desconocido"), "Error", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error al generar capas: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void mostrarImagen(String ruta) {
        ImageIcon icon = new ImageIcon(ruta);
        Image img = icon.getImage().getScaledInstance(520, 420, Image.SCALE_SMOOTH);
        lblVisor.setIcon(new ImageIcon(img));
    }
}