# Server notifiche

## Specifiche

* Server in ascolto sulla porta `30123` TCP per raccogliere notifiche che sono stringhe di testo, ogni connessione rappresenta una notifica (troncare a 300 caratteri massimo).
* Trovare a quale cliente appartiene la notifica in base a ricerca case insensitive di una label (tabella `customers` campo `notification_label`)  nel testo della notifica
* Salvare la notifica su DB Sql con ID cliente di appartenenza.
* Incrementare contatore notifiche giornaliero per cliente.
* Il salvataggio della notifica e l’incremento del contatore devono essere eseguiti in modo atomico. Ogni connessione deve durare il meno possibile e non dev’essere dipendente dai tempi di I/O wait del DB.
* Il servizio deve scrivere log su file con diversi tipi di verbosità:
  * **INFO**: con descrizione sintetica delle azioni intraprese.
  * **DEBUG**: con query ed eventuali dump di dati utili a ricercare possibili bug.
  * **ERROR**: in caso di errori imprevisti.
* In caso di conflitti (notifica contenente più di una label) la notifica dovrà essere salvata su DB senza campo `id_customer` valorizzato.

## Database

Il DB dovrà essere un file Sqlite3 con nome di file a piacere, di seguito la struttura.

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    notification_label TEXT NOT NULL UNIQUE
);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    body TEXT NOT NULL,
    id_customer INTEGER,
    FOREIGN KEY (id_customer) REFERENCES customers(id)
);

CREATE TABLE notification_counters (
    id_customer INTEGER NOT NULL,
    num INTEGER NOT NULL DEFAULT 0,
    day DATE NOT NULL,
    PRIMARY KEY (id_customer, day),
    FOREIGN KEY (id_customer) REFERENCES customers(id)
);

INSERT INTO customers VALUES
    (1, 'Yvonne Nash', 'Los Angeles'),
    (2, 'Justin Wright', 'Jeddah'),
    (3, 'Thomas Hamilton', 'Bangkok'),
    (4, 'Lily Lee', 'Casablanca'),
    (5, 'Angela Davies', 'Addis Ababa'),
    (6, 'Dan Skinner', 'Lahore'),
    (7, 'Dylan Butler', 'Kinshasa'),
    (8, 'Carl Reid', 'Dhaka'),
    (9, 'Jasmine Rampling', 'Karachi'),
    (10, 'Amelia Ross', 'Abidjan')
;
```
