## Entradas
- URL de YouTube (vía CLI o Telegram).
- `GEMINI_API_KEY` (Google Generative AI).
- `TELEGRAM_BOT_TOKEN` (Opcional, para modo Bot).
- `WEBHOOK_URL` (Opcional, para Google Sheets).

## Salidas
- Post impreso en consola.
- Mensaje de Telegram con el post generado (modo Bot).
- Propuesta interactiva para generar infografía (modo Bot).
- Texto estructurado de infografía generado por Gemini.
- Archivo local: `.tmp/posts_linkedin.xlsx`.

## Lógica y Pasos
...
1. **Transcripción**: 
    - Extraer el ID del video.
    - Usar `transcript_service.py` para obtener el texto (vía `youtube-transcript-api`).
    - Soporte para `cookies.txt` si hay restricciones.

2. **Generación con IA**:
    - Enviar el transcript COMPLETO a Gemini (sin recortes de 15k).
    - Modelo: `models/gemini-3-flash-preview` (o versión estable disponible).

3. **Escritura Local (Excel)**:
    - Guardar en `.tmp/posts_linkedin.xlsx`.
    - Gestión de errores: Si el archivo está abierto, el sistema reintenta y notifica al usuario.

## Restricciones y Casos Borde
- **Tokens de Gemini**: Aprovechar la ventana de contexto extendida (1M+ tokens).
- **Acceso a Excel**: Si se recibe `PermissionError`, cerrar el archivo y el reintento automático lo procesará.

## Historial de Aprendizaje
- [2026-04-08] - Refactorización de Core: Se renombró `apify_yt.py` a `transcript_service.py`.
- [2026-04-08] - Optimización de IA: Se eliminó el límite de 15k caracteres y se actualizó el modelo a Gemini 3 Flash.
- [2026-04-08] - Resiliencia: Se añadió manejo de `PermissionError` para archivos Excel abiertos.
