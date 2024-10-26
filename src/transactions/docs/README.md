# Transactions App - Applicazione di Gestione Finanziaria

Benvenuti nell'applicazione Transactions! Questa applicazione Django è progettata per aiutarti a gestire le tue finanze personali. Con Transactions, puoi tenere traccia delle tue entrate, spese, asset e debiti, tutto in un'unica piattaforma facile da usare.

## Panoramica delle Funzionalità

- **Gestione Conti**: Crea e gestisci conti bancari e denaro contante.
- **Registrazione Transazioni**: Registra entrate e spese con categorie personalizzabili.
- **Tracciamento Saldi**: Visualizza l'andamento dei saldi nel tempo con un sistema di log dettagliato.
- **Supporto per Entrate e Spese Ricorrenti**: Configura entrate e spese ricorrenti per una gestione automatizzata.

## Come Utilizzare l'App

### Requisiti

- Python 3.7 o versioni successive
- Django 3.1 o versioni successive
- Pacchetti Python aggiuntivi elencati in `requirements.txt`

### Installazione

1. Clona il repository dell'app:
```bash
   git clone https://github.com/leoBitto/transactions.git
```

Naviga nella directory del progetto:
```bash
cd transactions
```

Crea un ambiente virtuale (consigliato) e attivalo:
```bash
python3 -m venv venv
source venv/bin/activate
```

Installa i requisiti:
```bash
pip install -r requirements.txt
```

Applica le migrazioni:
```python 
 manage.py migrate
```


Avvia il server di sviluppo:
```python 
manage.py runserver
```


Accedi all'app nel tuo browser all'indirizzo http://localhost:8000.


Contributi
Se vuoi contribuire all'applicazione Transactions, sentiti libero di aprire un problema o inviare una richiesta pull nel repository GitHub: https://github.com/leoBitto/transactions

Licenza
L'applicazione è distribuita con licenza MIT. Consulta il file LICENSE per ulteriori dettagli.



# Financial Management Application

## Introduzione

Questa applicazione è progettata per gestire i conti correnti e il contante, tenendo traccia delle transazioni finanziarie e mantenendo un registro dello storico dei saldi. L'app consente di registrare entrate, spese e altre transazioni in modo flessibile, supportando diversi tipi di fondi come conti bancari e denaro contante.

### Funzionalità Principali
- Creazione e gestione di conti bancari e contanti.
- Registrazione di transazioni finanziarie (entrate e spese).
- Tracciamento delle modifiche dei saldi nel tempo attraverso un sistema di log.
- Supporto per categorie di entrate e spese personalizzate.

## Modelli

### FundBase
`FundBase` è un modello astratto che fornisce una struttura comune per rappresentare un fondo finanziario, come un conto bancario o denaro contante. Include campi per il saldo (`balance`), la data di apertura (`start_date`) e la data di chiusura (`end_date`).

### BankAccount
`BankAccount` eredita da `FundBase` ed è utilizzato per rappresentare conti bancari specifici. Oltre ai campi base, include il tipo di conto (`account_type`), il nome dell'istituto bancario (`institution`) e il tasso d'interesse (`interest_rate`).

### Cash
`Cash` eredita da `FundBase` ed è utilizzato per rappresentare denaro contante. Include un campo aggiuntivo per la descrizione (`description`).

### FundLog
`FundLog` tiene traccia delle modifiche del saldo per qualsiasi tipo di fondo (`BankAccount` o `Cash`). Utilizza un `GenericForeignKey` per collegarsi dinamicamente al modello specifico di fondo.

### Transaction
`Transaction` rappresenta una transazione finanziaria generica. Può essere collegata a qualsiasi tipo di fondo (`BankAccount` o `Cash`) tramite una `GenericForeignKey`.

### Income
`Income` è un'estensione di `Transaction` per rappresentare entrate finanziarie. Ogni entrata è associata a una categoria (`IncomeCategory`).

### Expenditure
`Expenditure` è un'estensione di `Transaction` per rappresentare spese finanziarie. Ogni spesa è associata a una categoria (`ExpenseCategory`).

### Relazioni tra Modelli
I modelli `Income` e `Expenditure` ereditano da `Transaction` e sono collegati a categorie specifiche tramite relazioni `ForeignKey`. I modelli `BankAccount` e `Cash` sono collegati al log tramite `GenericForeignKey`.

### Esempi di Utilizzo
Di seguito un esempio di come creare e collegare un conto bancario e registrare una transazione:

```python
# Creare un nuovo conto bancario
bank_account = BankAccount.objects.create(
    balance=1000.00,
    start_date=date.today(),
    account_type='savings',
    institution='Bank XYZ',
    interest_rate=1.5
)

# Creare una nuova transazione di entrata
income_category = IncomeCategory.objects.create(name='Salary', description='Monthly salary')
income = Income.objects.create(
    date=date.today(),
    amount=500.00,
    related_fund=ContentType.objects.get_for_model(bank_account),
    object_id=bank_account.id,
    type=income_category
)
```

## Signal e Logging

### Signal `log_fund_change`
Il signal `log_fund_change` è collegato ai modelli `BankAccount` e `Cash`. Viene attivato ogni volta che un fondo viene aggiornato (non creato) e crea un nuovo record in `FundLog` per registrare il cambiamento del saldo.

### Gestione del Logging
Il modello `FundLog` utilizza un `GenericForeignKey` per collegarsi dinamicamente a qualsiasi tipo di fondo (`BankAccount` o `Cash`). Questo sistema di logging consente di tracciare l'andamento del saldo nel tempo, offrendo uno storico dettagliato delle operazioni sui fondi.

---

## Form

Questa sezione descrive i moduli di form utilizzati nell'applicazione per gestire conti bancari, denaro contante, entrate e spese, e per la gestione di trasferimenti e spese ricorrenti.


### BankAccountForm

Il `BankAccountForm` è utilizzato per creare e aggiornare i record di conti bancari. I campi del modulo includono:

- **balance**: Il saldo attuale del conto bancario.
- **start_date**: La data di apertura del conto.
- **end_date**: La data di chiusura del conto (opzionale).
- **account_type**: Il tipo di conto (es. risparmio, corrente).
- **institution**: Il nome dell'istituto bancario.
- **interest_rate**: Il tasso d'interesse del conto (opzionale).

#### Validazione
Il modulo verifica che la data di chiusura sia successiva alla data di apertura. Se non è così, viene aggiunto un errore al campo `end_date`.

### CashForm

Il `CashForm` è utilizzato per creare e aggiornare i record di denaro contante. I campi del modulo includono:

- **balance**: Il saldo attuale del denaro contante.
- **start_date**: La data di inizio del registro del contante.
- **end_date**: La data di fine del registro del contante (opzionale).
- **description**: Una descrizione opzionale del contante.

#### Validazione
Il modulo verifica che la data di fine sia successiva alla data di inizio. Se non è così, viene aggiunto un errore al campo `end_date`.

### IncomeForm

Il `IncomeForm` è utilizzato per registrare entrate finanziarie. I campi del modulo includono:

- **date**: La data dell'entrata.
- **time**: L'ora dell'entrata (opzionale).
- **amount**: L'importo dell'entrata.
- **description**: Una descrizione opzionale dell'entrata.
- **type**: La categoria dell'entrata.
- **related_fund**: Il fondo a cui è associata l'entrata.

#### Validazione
Il modulo verifica che l'importo sia positivo. Inoltre, verifica che il fondo associato sia valido e che l'ID dell'oggetto esista.

### ExpenditureForm

Il `ExpenditureForm` è utilizzato per registrare spese finanziarie. I campi del modulo includono:

- **date**: La data della spesa.
- **time**: L'ora della spesa (opzionale).
- **amount**: L'importo della spesa.
- **description**: Una descrizione opzionale della spesa.
- **type**: La categoria della spesa.
- **related_fund**: Il fondo a cui è associata la spesa.

#### Validazione
Il modulo verifica che l'importo sia positivo. Inoltre, verifica che il fondo associato sia valido e che l'ID dell'oggetto esista.

### TransferFundsForm

Il `TransferFundsForm` è utilizzato per trasferire fondi tra conti o tra denaro contante. I campi del modulo includono:

- **amount**: L'importo del trasferimento.
- **source_fund**: Il fondo di origine del trasferimento.
- **destination_fund**: Il fondo di destinazione del trasferimento.
- **commission**: Una commissione opzionale associata al trasferimento.

#### Validazione
Il modulo verifica che il fondo di origine e quello di destinazione non siano lo stesso. Inoltre, controlla che l'importo sia maggiore di zero e che ci siano fondi sufficienti nel fondo di origine per coprire l'importo e la commissione.

### RecurringIncomeForm

Il `RecurringIncomeForm` è utilizzato per impostare entrate ricorrenti. I campi del modulo includono:

- **amount**: L'importo dell'entrata ricorrente.
- **frequency**: La frequenza dell'entrata (giornaliera, settimanale, mensile, annuale).
- **start_date**: La data di inizio dell'entrata ricorrente.
- **end_date**: La data di fine dell'entrata ricorrente (opzionale).
- **description**: Una descrizione opzionale dell'entrata.
- **income_type**: La categoria dell'entrata.
- **related_fund**: Il fondo a cui è associata l'entrata ricorrente.

#### Validazione
Il modulo verifica che la data di fine sia successiva alla data di inizio.

### RecurringExpenseForm

Il `RecurringExpenseForm` è utilizzato per impostare spese ricorrenti. I campi del modulo includono:

- **amount**: L'importo della spesa ricorrente.
- **frequency**: La frequenza della spesa (giornaliera, settimanale, mensile, annuale).
- **start_date**: La data di inizio della spesa ricorrente.
- **end_date**: La data di fine della spesa ricorrente (opzionale).
- **description**: Una descrizione opzionale della spesa.
- **expenditure_type**: La categoria della spesa.
- **related_fund**: Il fondo a cui è associata la spesa ricorrente.

#### Validazione
Il modulo verifica che la data di fine sia successiva alla data di inizio.





















