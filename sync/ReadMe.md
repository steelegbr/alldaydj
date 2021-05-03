# Sync for AllDay DJ

Syncronises another playout system into AllDay DJ.

## Installation

pyodbc is a key requirement for this application. [There are some required steps for installing this](https://github.com/mkleehammer/pyodbc/wiki/Install). As a starting point, you may need to install the Python3 dev headers:

    sudo apt install python3.9-dev
    sudo apt install unixodbc-dev

On Ubuntu, you will need unixODBC drivers. Details can be found at [here](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#ubuntu17).

If you're connecting to an old version of SQL server, you will need to [downgrade the TLS connection](https://github.com/microsoft/msphpsql/issues/1021#issuecomment-520943561).