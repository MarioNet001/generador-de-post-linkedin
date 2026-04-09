# 🛰️ Pulsing Cassini

**YouTube a LinkedIn con Superpoderes de IA.**

## 📋 Resumen del Proyecto

**Pulsing Cassini** es una solución "todo en uno" diseñada para creadores de contenido y profesionales del marketing. Su objetivo es maximizar el valor de los videos de YouTube transformándolos automáticamente en múltiples formatos de redes sociales de alta calidad en cuestión de segundos.

### ¿Qué es?
Es un asistente inteligente que automatiza el flujo de trabajo de "repurpose" de contenido. Toma un video de YouTube y lo convierte en activos listos para publicar, eliminando horas de trabajo manual de redacción y diseño.

### ¿Cómo lo hace?
1.  **Ingesta**: El sistema recibe una URL de YouTube a través de Telegram o CLI.
2.  **Extracción**: Utiliza APIs de bajo nivel para obtener la transcripción completa del video, sorteando bloqueos mediante el uso de cookies.
3.  **Procesamiento (IA)**: Envía el texto a **Google Gemini 3 Flash**, quien actúa como un copywriter senior para redactar un post de LinkedIn con ganchos efectivos.
4.  **Diseño Visual**: Gemini genera código estructural SVG que el sistema convierte en una infografía PNG profesional.
5.  **Persistencia**: Guarda automáticamente cada post en un archivo Excel local para mantener un historial organizado.

## ✨ Características

- 📝 **Transcripción Automática**: Obtiene el contenido de cualquier video de YouTube (incluyendo reintentos por bloqueo).
- 🤖 **Generación de Posts**: Crea contenido de LinkedIn con ganchos potentes y estructura profesional.
- 🎨 **Infografías Visuales**: Genera infografías en formato vectorial (SVG) y las convierte a imagen (PNG).
- 💾 **Historial Local**: Guarda todos los posts generados en un archivo Excel automático.
- 🤖 **Bot de Telegram**: Interfaz amigable para realizar todo el proceso desde el móvil.

## 💎 Economía de Tokens (Optimización)

Para maximizar la eficiencia y reducir el consumo de la API de Gemini, el sistema implementa:
- **Unified Content Bundle**: Genera el post de LinkedIn, el resumen y el código SVG en una única transacción de tokens.
- **Smart Slicing**: Trunca automáticamente videos largos, priorizando el inicio (Hooks) y el final (Conclusiones) para mantener el contexto esencial sin desperdiciar tokens.
- **Noise Filtering**: Limpia muletillas (`[Música]`, `[Aplausos]`, etc.) y optimiza el texto antes de enviarlo a la IA.

## 🚀 Instalación Rápida

1.  **Clonar el repo**:
    ```bash
    git clone https://github.com/tu-usuario/pulsing-cassini.git
    cd pulsing-cassini
    ```

2.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar variables**:
    Copia `.env.example` a `.env` y completa tus claves:
    - `GEMINI_API_KEY`: Obtenida en [Google AI Studio](https://aistudio.google.com/).
    - `TELEGRAM_BOT_TOKEN`: Obtenida vía [@BotFather](https://t.me/botfather).

4.  **Cookies (Importante)**:
    Para evitar bloqueos de YouTube, exporta tus cookies desde el navegador (formato Mozilla/Netscape) a un archivo llamado `cookies.txt` en la raíz del proyecto.

## 🛠️ Uso

### Bot de Telegram (Recomendado)
```bash
python bot.py
```

### Línea de Comandos (CLI)
```bash
python main.py "https://www.youtube.com/watch?v=..."
```

## 🏗️ Estructura del Proyecto

- `src/`: Núcleo del sistema (IA, Transcripción, Almacenamiento).
- `bot.py`: Punto de entrada del Bot de Telegram.
- `main.py`: Punto de entrada de la CLI.
- `.tmp/`: Carpeta para archivos temporales e historial Excel.

## 📄 Licencia

MIT - Hecho con ❤️ por Antigravity.
