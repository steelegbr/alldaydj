# AllDay DJ FastAPI

The FastAPI with Firestore implementation of the AllDay DJ backend.

## Firebase

You may need to refresh the environment variables if it doesn't load:

    $env:FIREBASE_CREDENTIALS="/path/to/file.json"

## Search

To allow the generation of search terms to ignore stop words, NLTK must have collection of stopwords for the language. Downloads can be triggered from the CLI:

    python -m nltk.downloader stopwords