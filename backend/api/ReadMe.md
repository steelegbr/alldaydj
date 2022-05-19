# AllDay DJ FastAPI

The FastAPI with Firestore implementation of the AllDay DJ backend.

## Root Path

In order to support the split routing between front and back end, you need to set the root path:

    uvicorn main:app --root-path /api

You may need to refresh the environment variables if it doesn't load:

    $env:FIREBASE_CREDENTIALS="/path/to/file.json"