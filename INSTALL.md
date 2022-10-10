# Installation

This is the installations you need to follow in order to train models. If you
only want to run tts with the ecomputed models just use `pip install TTS`.

## Manual installation

```sh
git clone --recurse-submodules -j8 https://github.com/raquelpanapalen/PAE-YOV.git
cd PAE-YOV
python3 -m venv .yov-venv
source .yov-venv/bin/activate
cd TTS
make install
```

## Server installation
On the server we need to install a specific CUDA version (v.11.X),
since the lower versions do not support the required CUDA capability (`sm_86`,
Ampere architecture).

```sh
git clone --recurse-submodules -j8 https://github.com/raquelpanapalen/PAE-YOV.git
cd PAE-YOV
python3 -m venv .yov-venv
source .yov-venv/bin/activate
pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
cd TTS
make install
```

