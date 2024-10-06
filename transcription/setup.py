from setuptools import setup, find_packages

setup(
    name='transcription-tools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai-whisper',
    ],
    entry_points={
        'console_scripts': [
            'transcribe=transcription_tools.cli:main',
        ],
    },
)
