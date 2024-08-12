
**Progetto**: Sto sviluppando un ecosistema di applicazioni Django destinato a piccole e medie imprese (PMI). Il progetto è strutturato in tre livelli principali:

1. **Progetto Base**: Include le funzionalità fondamentali e le app generiche necessarie per l'intero ecosistema.

2. **Tier 1**: App business generiche come CRM, ERP e altre che si basano sul Progetto Base e forniscono funzionalità di base comuni a molte imprese. Esempi includono:
   - **Gestione degli Ordini e dell'Inventario**: Gestisce le vendite, gli ordini e l'inventario.
   - **Gestione dei Punti di Vendita (PDV)**: Include la gestione delle sedi fisiche e dei magazzini.
   - **Sistema di Prenotazione Eventi**: Gestisce prenotazioni e registrazioni per eventi aziendali.
   - **Sistema di Contabilità Base**: Fornisce funzionalità per la gestione delle finanze aziendali.

3. **Tier 2**: App business specifiche per settori verticali, estendendo le funzionalità delle app di Tier 1 e personalizzate per esigenze particolari. Esempi includono:
   - **Sistema di Prenotazione per Ristoranti**: Estensione del CRM per gestire prenotazioni tavoli e ordini al ristorante.
   - **Gestione dei Magazzini Avanzata**: Estensione del sistema di gestione dei magazzini con funzionalità avanzate come tracciamento dettagliato delle spedizioni e delle scorte.
   - **Sistema di Gestione degli Eventi per Hotel**: Estensione del sistema di prenotazione eventi per gestire conferenze e altre attività specifiche per hotel.
   - **Modulo di Analisi Avanzata per E-Commerce**: Estensione del sistema di gestione degli ordini con reportistica e analisi dettagliata delle vendite.

### **Tecnologie e Infrastruttura**

- **Framework**: Django
- **Database**:
  - **Default**: Database principale usato come data lake per i dati grezzi.
  - **Gold**: Database per la business intelligence, contenente dati aggregati e raffinati.
- **Containerizzazione**: Utilizzo di Docker e Docker Compose:
  - **Sviluppo**: Include la creazione delle immagini, inclusa quella per Nginx, e gestisce l'ambiente di sviluppo.
  - **Produzione**: Utilizza i container dal GitHub Container Registry (GHCR) e gestisce il deployment; Nginx è configurato e gestito direttamente sul server di produzione.
- **CI/CD**: Utilizzo di GitHub Actions per l'automazione del flusso di lavoro, inclusi creazione delle immagini Docker e deployment su servizi IaaS (Digital Ocean Droplet). È previsto un futuro passaggio a PaaS per semplificare il deployment e creare soluzioni agnostiche al vendor.

### **Struttura del Progetto**

**1. Logging App**
   - **Scopo**: Registra e aggrega i log delle richieste HTTP e degli errori.
   - **Struttura Aggiornata**:
     - **File e Directory**:
       - `models/`: Contiene `base.py` e `aggregated.py` per i modelli di log.
       - `tasks/`: Contiene `aggregate_access_logs.py` e `aggregate_error_logs.py` per le attività di aggregazione dei log.
       - `views/`: Contiene `base.py` e `aggregated.py` per le visualizzazioni dei log.

**2. Website App**
   - **Scopo**: Gestisce il frontend del sito e attualmente funziona come un semplice CMS.
   - **Modifiche Pianificate**:
     - Rimuovere modelli non necessari e mantenere l'app focalizzata sul rendering di pagine HTML statiche o quasi statiche.
   - **Risultato Atteso**: Un'app semplificata e pronta per future espansioni CMS.

**3. Backoffice App**
   - **Scopo**: Fornisce strumenti di gestione backend e visualizzazione dei dati.
   - **Modifiche Pianificate**:
     - Modularizzare l'app e integrare nuovi strumenti di visualizzazione dei dati provenienti da Gold BI.
   - **Risultato Atteso**: Un backoffice aggiornato, modulare e ben integrato con Gold BI.

**4. Gold BI**
   - **Scopo**: Gestisce i flussi ETL e le attività di pianificazione utilizzando Django Q. VIENE ESTESA CON LE SCHEDULAZIONI DELLE TASK delle altre app.
   - **Risultato Atteso**: Un sistema ETL funzionante con pianificazione delle tasks gestita tramite Django Q.

### Struttura filesystem

DjangoForge/
├── config
│   ├── db.cfg
│   └── gold.cfg
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── docs
│   ├── CODE_OF_CONDUCT.md
│   ├── README.md
│   ├── _config.yml
│   ├── assets
│   │   └── img
│   └── prompt.md
├── manager.sh
├── nginx
│   ├── nginx.conf
│   └── nginx.dev.conf
└── src
    ├── Dockerfile
    ├── backoffice
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── templates
    │   │   └── backoffice
    │   │       ├── backoffice_base.html
    │   │       ├── contact_page.html
    │   │       ├── create_group.html
    │   │       ├── gallery_page.html
    │   │       ├── group_list.html
    │   │       ├── image_page.html
    │   │       ├── opening_hours_page.html
    │   │       └── push_info.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── base
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── gold_bi
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── apps.py
    │   ├── docs
    │   │   ├── README.md
    │   │   └── assets
    │   │       └── images
    │   ├── signals.py
    │   ├── tasks_scheduler.py
    │   └── tests.py
    ├── logging_app
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── docs
    │   │   ├── README.md
    │   │   ├── _config.yml
    │   │   └── assets
    │   ├── forms.py
    │   ├── middleware.py
    │   ├── models
    │   │   ├── __init__.py
    │   │   ├── aggregated.py
    │   │   └── base.py
    │   ├── tasks
    │   │   ├── __init__.py
    │   │   ├── aggregate_access_logs.py
    │   │   └── aggregate_error_logs.py
    │   ├── templates
    │   │   └── logging_app
    │   │       ├── AElist.html
    │   │       ├── accordion.html
    │   │       ├── graphs.html
    │   │       ├── log_list.html
    │   │       └── request_log_detail.html
    │   ├── tests.py
    │   ├── urls.py
    │   └── views
    │       ├── __init__.py
    │       ├── aggregated.py
    │       └── base.py
    ├── manage.py
    ├── requirements.txt
    └── website
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── docs
        │   └── README.md
        ├── forms.py
        ├── models.py
        ├── static
        │   ├── favicon
        │   │   ├── 16DjangoForge.ico
        │   │   ├── 48DjangoForge.ico
        │   │   └── bee.ico
        │   ├── icons
        │   └── pwa
        │       └── icons
        ├── templates
        │   ├── registration
        │   │   ├── login.html
        │   │   ├── logout.html
        │   │   └── password_reset.html
        │   └── website
        │       ├── base.html
        │       ├── footer.html
        │       ├── landing.html
        │       └── navbar.html
        ├── tests.py
        ├── urls.py
        └── views.py

33 directories, 82 files


### **Milestone**

3. **Milestone 3: Modularizzazione e Aggiornamento della Backoffice App**
   - **Durata**: 5 giorni
   - **Obiettivo**: Modularizzare l'app e integrare nuovi strumenti di visualizzazione dei dati da Gold BI.
   - **Output**: Backoffice app aggiornata e modulare.

4. **Milestone 4: Semplificazione e Preparazione della Website App**
   - **Durata**: 3 giorni
   - **Obiettivo**: Rimuovere i modelli non necessari e preparare l'app per future espansioni CMS.
   - **Output**: Website app semplificata e migliorata.

