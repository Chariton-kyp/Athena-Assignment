# TechFlow Data Automation - Demo Script

**Διάρκεια:** 7-10 λεπτά

---

## Εισαγωγή

> "Γεια σας, είμαι ο Χαρίτων Κυπραίος και σας παρουσιάζω το TechFlow Data Automation Project."

> "Η TechFlow είναι μια IT εταιρεία με 50-100 υπαλλήλους. Αυτή τη στιγμή ξοδεύουν περίπου 18 ώρες την εβδομάδα σε χειροκίνητη καταχώρηση δεδομένων από φόρμες επικοινωνίας, emails πελατών και τιμολόγια."

> "Η λύση αυτοματοποιεί την εξαγωγή αυτών των δεδομένων, αλλά - και αυτό είναι το κλειδί - **δίνει πλήρη έλεγχο στον χρήστη** πριν την τελική αποθήκευση. Τίποτα δεν αποθηκεύεται χωρίς ρητή έγκριση."

---

## Γλώσσα Εφαρμογής

> "Η εφαρμογή υποστηρίζει πλήρως Ελληνικά και Αγγλικά. Χρησιμοποιείται η βιβλιοθήκη `next-intl` για internationalization. Με ένα κλικ στο header αλλάζει γλώσσα και όλα τα κείμενα, labels, μηνύματα, ακόμα και τα error messages μεταφράζονται αυτόματα."

---

## Dashboard

> "Ξεκινώντας από το Dashboard βλέπουμε μια πλήρη επισκόπηση του συστήματος."

> "Στο πάνω μέρος έχουμε τέσσερα stats cards που δείχνουν σε πραγματικό χρόνο:
> - Το **σύνολο των εγγραφών** που υπάρχουν στο σύστημα
> - Πόσες **εκκρεμούν** για έλεγχο, δηλαδή περιμένουν τον χρήστη να τις εγκρίνει ή απορρίψει
> - Πόσες έχουν **εγκριθεί** και είναι έτοιμες για εξαγωγή
> - Πόσες έχουν **απορριφθεί** ως spam ή λανθασμένα δεδομένα"

> "Παρακάτω έχουμε δύο γραφήματα:
> - Το πρώτο είναι ένα **donut chart** που δείχνει την κατανομή ανά κατάσταση - ποσοστό pending, approved, rejected. Αυτό δίνει άμεσα μια εικόνα του workload.
> - Το δεύτερο είναι ένα **bar chart** που δείχνει πόσες εγγραφές έχουμε ανά τύπο: φόρμες επικοινωνίας, emails, τιμολόγια."

> "Κάτω δεξιά υπάρχουν **quick action buttons** που οδηγούν απευθείας στις εκκρεμείς εγγραφές, ώστε ο χρήστης να ξεκινήσει αμέσως τον έλεγχο."

---

## AI Semantic Search

> "Ένα από τα πιο ενδιαφέροντα features είναι το **Semantic Search**."

> "Χρησιμοποιούμε **Hybrid Search** που συνδυάζει δύο τεχνικές:
> - **Semantic similarity** με **pgvector** - που είναι ένα extension της PostgreSQL για vector operations
> - **Lexical search** με **tsvector** για ακριβές matching λέξεων"

> "Τα embeddings δημιουργούνται από το μοντέλο **EmbeddingGemma-300M** - είναι μια **ελαφριά παραλλαγή** του Gemma ειδικά σχεδιασμένη για embeddings. Τα vectors **αποθηκεύονται μόνιμα στη PostgreSQL** στον πίνακα `document_embeddings` και γίνεται cosine similarity search με τον pgvector operator."

> "Αυτό σημαίνει ότι μπορώ να ψάξω για 'τιμολόγιο digital agency' και να βρω σχετικά αποτελέσματα ακόμα κι αν δεν περιέχουν ακριβώς αυτές τις λέξεις. Λειτουργεί και στα Ελληνικά και στα Αγγλικά."

---

## Extraction - Εξαγωγή Δεδομένων

> "Στη σελίδα Extraction βλέπουμε τα raw data που μπορούμε να επεξεργαστούμε."

> "Έχουμε **τρεις τύπους πηγών** από τα παρεχόμενα dummy data:
> - **5 HTML φόρμες επικοινωνίας**
> - **10 email αρχεία σε μορφή .eml**
> - **10 HTML τιμολόγια** - τα sample data είναι HTML, αλλά το σύστημα υποστηρίζει και **PDF parsing** με τη βιβλιοθήκη pdfplumber"

> "Για κάθε αρχείο μπορεί να γίνει preview για να δούμε τα raw data, και μετά να πατήσουμε Εξαγωγή. Το backend χρησιμοποιεί **BeautifulSoup** για HTML parsing, **pdfplumber** για PDF, και **regex patterns** για να κάνει extract τα πεδία."

> "Όταν κάνουμε εξαγωγή, η εγγραφή δημιουργείται με status **Pending** - δεν πάει απευθείας στο Google Sheets. Πρέπει πρώτα να την ελέγξει και να την εγκρίνει ο χρήστης."

---

## Εγγραφές - Records Page

> "Η σελίδα Εγγραφές είναι το κέντρο του **Human-in-the-Loop workflow**."

> "Βλέπουμε έναν πίνακα με όλες τις εγγραφές. Κάθε γραμμή δείχνει:
> - Το **όνομα αρχείου** προέλευσης
> - Τον **τύπο** - form, email, invoice
> - Την **κατάσταση** - pending, approved, rejected, edited
> - Το **confidence score** - πόσο σίγουρο είναι το σύστημα για την ακρίβεια της εξαγωγής
> - Την **ημερομηνία** δημιουργίας
> - Και τα **action buttons** για κάθε εγγραφή"

> "Στο πάνω μέρος έχουμε **φίλτρα** για να δούμε μόνο τις pending ή μόνο τα invoices."

---

## Approve, Edit, Reject - Μεμονωμένες Ενέργειες

> "Κάθε εγγραφή με status Pending έχει τρία action buttons."

> "Το **Approve** - πράσινο ✓ - εγκρίνει την εγγραφή. Αυτό σημαίνει ότι ο χρήστης επιβεβαίωσε ότι τα δεδομένα είναι σωστά και μπορούν να αποθηκευτούν μόνιμα."

> "Το **Edit** - μολύβι - ανοίγει ένα dialog όπου μπορώ να διορθώσω τα δεδομένα πριν την έγκριση. Αν το OCR ή το parsing έκανε κάποιο λάθος, π.χ. γράφει λάθος όνομα ή αριθμό, το διορθώνω εδώ. Μετά την αποθήκευση η κατάσταση γίνεται **Edited** και μπορώ να την εγκρίνω."

> "Το **Reject** - κόκκινο ✗ - απορρίπτει την εγγραφή. Ζητάει αιτιολογία - π.χ. 'Spam email', 'Duplicate', 'Invalid data'. Αυτό είναι σημαντικό για **audit trail** - να ξέρουμε γιατί απορρίφθηκε κάτι."

---

## Bulk Actions - Μαζικές Ενέργειες

> "Για high-volume workflows υπάρχουν και **μαζικές ενέργειες**."

> "Κάθε γραμμή έχει ένα checkbox. Μπορούμε να επιλέξουμε μεμονωμένες εγγραφές ή να πατήσουμε το checkbox στην κεφαλίδα για **Select All**."

> "Όταν επιλέξουμε εγγραφές, εμφανίζεται μια action bar με:
> - **Bulk Approve** - εγκρίνει όλες τις επιλεγμένες μαζί
> - **Bulk Reject** - απορρίπτει όλες τις επιλεγμένες μαζί"

> "Αυτό είναι πολύ χρήσιμο όταν έχεις εκατοντάδες εγγραφές. Αντί να κάνεις κλικ ένα-ένα, κάνεις review, επιλέγεις τα σωστά, και μαζική έγκριση."

---

## Ρυθμίσεις Εξαγωγής

> "Το σύστημα δίνει **τρεις επιλογές** για τον τρόπο εξαγωγής δεδομένων."

> "**Χειροκίνητη** - η default. Ο χρήστης πατάει το κουμπί Εξαγωγή όποτε θέλει."

> "**Αυτόματη σε Excel** - μετά από κάθε bulk approve, κατεβαίνει αυτόματα ένα Excel αρχείο με τις εγκεκριμένες εγγραφές."

> "**Αυτόματος συγχρονισμός στο Google Sheets** - κάθε φορά που εγκρίνεται μια εγγραφή, συγχρονίζεται στο background με το Google Sheet."

> "Υπάρχει επίσης η επιλογή **Συμπερίληψη Απορριφθέντων** - αν θέλουμε τα rejected records να συμπεριλαμβάνονται στο Excel για audit purposes."

---

## Εξαγωγή σε Αρχείο

> "Το Export Dialog δίνει τρία formats:"

> "**CSV** - απλό comma-separated για εισαγωγή οπουδήποτε."

> "**Excel (.xlsx)** - με formatting, headers, έτοιμο για χρήση."

> "**JSON** - για integrations με άλλα συστήματα ή APIs."

> "Και πάλι υπάρχει η επιλογή να συμπεριλάβουμε τα rejected για πλήρες audit trail."

---

## Google Sheets Integration

> "Το Google Sheets integration είναι πλήρες."

> "Χρησιμοποιούμε **Service Account** για authentication - δεν χρειάζεται ο χρήστης να κάνει login με τον Google λογαριασμό του."

> "Η αρχική ρύθμιση γίνεται **μία φορά** από τον διαχειριστή - δημιουργία Service Account στο Google Cloud και κοινοποίηση του spreadsheet. Υπάρχει **step-by-step οδηγός** στο documentation."

> "Τα δεδομένα οργανώνονται αυτόματα σε **ξεχωριστά sheets**:
> - Ένα sheet για Contacts από τις φόρμες
> - Ένα sheet για Emails
> - Ένα sheet για Invoices"

> "Κάθε sheet έχει τα κατάλληλα columns για τον τύπο δεδομένων. Τα invoices έχουν ποσά, ΦΠΑ, ημερομηνίες. Τα emails έχουν subject, body, sender."

---

## Technical Overview

> "Τεχνικά, η αρχιτεκτονική είναι:
> - **Backend:** FastAPI με async SQLAlchemy και PostgreSQL 16
> - **AI:** pgvector extension για vector similarity, EmbeddingGemma-300M για embeddings
> - **Frontend:** Next.js 15 με App Router, TypeScript, TailwindCSS, Shadcn UI
> - **Infrastructure:** Docker Compose με multi-stage builds"

> "Τα tests είναι με pytest και έχουμε πάνω από 80% code coverage. Υπάρχουν unit tests, integration tests για τα API endpoints, και end-to-end tests για critical flows."

---

## Κλείσιμο

> "Συνοψίζοντας, αυτό που κάναμε είναι ένα σύστημα που:
> - Αυτοματοποιεί το **90%** της χειροκίνητης δουλειάς
> - Δίνει **πλήρη έλεγχο** στον άνθρωπο για το τελικό αποτέλεσμα
> - Υποστηρίζει **bulk operations** για high volume
> - Έχει **AI-powered search** για εύκολη αναζήτηση
> - Εξάγει σε **πολλαπλά formats** - Excel, CSV, JSON, Google Sheets"

> "Η φιλοσοφία είναι **Human-in-the-Loop**: η τεχνητή νοημοσύνη κάνει τη βαριά δουλειά, αλλά ο άνθρωπος έχει τον τελικό λόγο."

> "Ευχαριστώ πολύ για τον χρόνο σας."

---

## Checklist πριν την Εγγραφή

- [ ] Docker containers running (`docker compose --profile prod up`)
- [ ] Frontend: http://localhost:7002
- [ ] Backend: http://localhost:7000/docs
- [ ] Database με 25 records (extracted & ready)
- [ ] Google Sheets credentials configured (see `docs/GOOGLE_SHEETS_SETUP.md`)
- [ ] Spreadsheet shared with Service Account email
- [ ] Test sync to Google Sheets works
- [ ] Excel export test
- [ ] Language switcher test (EL/EN)
- [ ] Mic check
- [ ] Screen recording software ready
