# TODO: Simple list of todo's and/or questions

## Databases
- [X] Make a script for database processing.
- [X] `helena_cat`: So some processing (VAD, level normalization, etc).
- [ ] Make script to validate/complete metadata files. During our recording
      some metadata files where not saved correctly, leaving "gaps".

## Models & Vocoders
- [X] Train a vocoder (Trained hifigan with ljspeech).
- [ ] **Not going to happen since we are not capable of using the Tacotron2
      model** Train a model with the `ca_es_female` database with Tacotron2.
- [X] Train a model with the `ca_es_female` database with VITS.
- [X] Train a model with the `ca_es_female` database with GlowTTS.
- [ ] Train a vocoder with the `ca_es_female` database with hifigan [Working on it].

## Github
- [ ] Transfer main repo to the `paeyovupc` account ([link](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository)).

## Questions
- [ ] Find out which sample rate to use (16000, 22050, others?¿)
- [ ] Is it needed to train a model before the vocoder?
- [ ] Can vocoders be trained separately of models?
