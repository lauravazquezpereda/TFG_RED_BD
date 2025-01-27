import sqlite3
import cv2
import time
from fer import FER
from fer.utils import draw_annotations
from bd import create_database

def analyze_video(video_source, video_name):
    # Crear tabla para el video en la base de datos
    table_name = create_database(video_name)

    conn = sqlite3.connect('emotions.db')
    c = conn.cursor()

    # Configurar detector FER y captura de video
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara")
        return

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fin del video o error en la captura")
            break

        # Recortar la región donde está tu cara
        frame_height, frame_width, _ = frame.shape
        crop_x_start = int(1177 / 1920 * frame_width)  # Aproximadamente el 61% del ancho
        crop_y_start = int(662 / 1080 * frame_height)  # Aproximadamente el 61% de la altura
        # Recortar el área donde está tu cara
        cropped_frame = frame[crop_y_start:, crop_x_start:]

        # Detectar emociones solo en el área recortada
        emotions = detector.detect_emotions(cropped_frame)

        if emotions:
            for face in emotions:
                timestamp = time.time() - start_time
                for emotion, confidence in face['emotions'].items():
                    if confidence > 0.5:  # Filtrar emociones con confianza significativa
                        c.execute(f'''
                            INSERT INTO {table_name} (timestamp, emotion)
                            VALUES (?, ?)
                        ''', (timestamp, emotion))

        # Dibujar las emociones detectadas (opcional)
        cropped_frame = draw_annotations(cropped_frame, emotions)

        # Mostrar el área recortada en lugar del fotograma completo
        cv2.imshow("Video", cropped_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Presionar 'q' para salir
            break

    # Guardar cambios y liberar recursos
    conn.commit()
    conn.close()
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    video_source = "prueba1.mp4"  # Ruta al archivo de video grabado
    video_name = "prueba1"  # Nombre para identificar el video en la base de datos
    analyze_video(video_source, video_name)
