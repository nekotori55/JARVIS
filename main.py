import pyaudio
import pygame
import struct
import wave

###################################################################################
pygame.init()
window_size = (1000, 800)

background_color = (10, 10, 10)
left_channel_color = (100, 180, 255)
right_channel_color = (255, 100, 100)

audio_file = wave.open("Rusty K - Dark Eyes.wav", "rb")  # 2 different channels
# audio_file = wave.open("Rusty K - Dark Eyes1.wav", "rb") # 1 channel
# audio_file = wave.open("Rusty K - Dark Eyes2.wav", "rb") # 2 identical channels

format = audio_file.getsampwidth()  # глубина звука
channels = audio_file.getnchannels()  # количество каналов
rate = audio_file.getframerate()  # частота дискретизации
n_frames = audio_file.getnframes()  # кол-во отсчетов

print("Глубина звука:", format)
print("Кол-во каналов:", channels)
print("Частота дискретизации:", rate)
print("Количество фреймов:", n_frames)

audio = pyaudio.PyAudio()  # Подключение к аудиокарте

out_stream = audio.open(format=format, channels=channels,
                        rate=rate // 2, output=True)  # Поток динамика


window = pygame.display.set_mode(window_size)
pygame.display.set_caption("JARVIZ")
sf = pygame.Surface(window_size)
sf.fill(background_color)
window.blit(sf, (0, 0))

samples_per_second = 1000

max_height = 400
left_offset = 200
right_offset = 500

multiplier = 0.01

while True:
    samples = audio_file.readframes(samples_per_second)
    values = list(struct.unpack("<" + str(samples_per_second * channels) + "h", samples))

    ## Отрисовка
    sf.fill(background_color)

    for i in range(0, len(values) - 2, 2):
        pygame.draw.line(sf, left_channel_color, (i * window_size[0] // samples_per_second, values[i] * multiplier + left_offset),
                         (i * window_size[0] // samples_per_second + 1, values[i + channels] * multiplier + left_offset))
    #
    for i in range(1, len(values) - 2, 2):
        pygame.draw.line(sf, right_channel_color, (i * window_size[0] // samples_per_second, values[i] * multiplier + right_offset),
                         (i * window_size[0] // samples_per_second + 1, values[i + channels] * multiplier + right_offset))

    window.blit(sf, (0, 0))

    pygame.display.update()

    out_stream.write(samples)  # отправляем на динамик
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            audio.terminate()
            quit()

    # sleep(10)
