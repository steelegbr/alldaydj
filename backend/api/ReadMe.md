# AllDay DJ FastAPI

The FastAPI with Firestore implementation of the AllDay DJ backend.

## Firebase

You may need to refresh the environment variables if it doesn't load:

    $env:FIREBASE_CREDENTIALS="/path/to/file.json"

### Emulator

To use the firebase emulator, you'll need some extra environement variables:

    $env:FIRESTORE_EMULATOR_HOST="localhost:9099"
    $env:FIREBASE_STORAGE_EMULATOR_HOST="localhost:9199"

## Search

To allow the generation of search terms to ignore stop words, NLTK must have collection of stopwords for the language. Downloads can be triggered from the CLI:

    python -m nltk.downloader stopwords