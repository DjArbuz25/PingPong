import pytest
from pathlib import Path
import os
import psutil

def test_directory_exists():
    assert os.path.exists('gluhoy-stuk.wav'),'файл no существует'
    assert os.path.exists('pukane-11.wav'), 'файл no существует'



def test_system_requeiments():
    assert os.cpu_count() >= 2
    memory = psutil.virtual_memory()
    available_memory = memory.available
    available_memory_gb = available_memory / (1024 * 1024 * 1024)
    assert available_memory_gb > 0.4
        # проверить требовия пк: озу:2гб, количество ядер:2