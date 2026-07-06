import edge_tts
import asyncio
import pygame
import tempfile
import os

VOICE = "en-US-JennyNeural"


async def generate_audio(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)


def speak(text):

    filename = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    ).name

    asyncio.run(generate_audio(text, filename))

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    pygame.mixer.music.unload()

    try:
        os.remove(filename)
    except PermissionError:
        pass