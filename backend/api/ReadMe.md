# AllDay DJ FastAPI

The FastAPI with Firestore implementation of the AllDay DJ backend.

## Firebase

You may need to refresh the environment variables if it doesn't load:

    $env:FIREBASE_CREDENTIALS="/path/to/file.json"
    $env:ALLDAYDJ_BUCKET="addj-test-bucket"
    $env:ALLDADYJ_TOPIC_VALIDATE="validate-audio"

### Emulator

To use the firebase emulator, you'll need some extra environement variables:

    $env:FIRESTORE_EMULATOR_HOST="localhost:8080"
    $env:FIREBASE_STORAGE_EMULATOR_HOST="localhost:9199"

You may need to build the functions before attempting to run the emulators:

    npm run build

##

Testing the backend API can be done with a call to:

    pytest

## Search

To allow the generation of search terms to ignore stop words, NLTK must have collection of stopwords for the language. Downloads can be triggered from the CLI:

    python -m nltk.downloader stopwords