# Ρύθμιση Google Sheets Integration

Αυτός ο οδηγός εξηγεί πώς να ρυθμίσετε τη σύνδεση με Google Sheets για το σύστημα TechFlow.

---

## Σύνοψη

Το σύστημα χρησιμοποιεί **Service Account** για πρόσβαση στα Google APIs. Χρειάζεστε:
1. Δημιουργία Service Account στο Google Cloud Console
2. Ενεργοποίηση Sheets και Drive APIs
3. Λήψη του JSON αρχείου κλειδιού
4. Κοινοποίηση του spreadsheet με το Service Account email

---

## Οδηγίες Βήμα-Βήμα

### 1. Ρύθμιση Google Cloud Console

1. Μεταβείτε στο [Google Cloud Console](https://console.cloud.google.com/)
2. Δημιουργήστε **Νέο Project** (π.χ. "TechFlow Automation")
3. Ενεργοποιήστε τα APIs:
   - Πηγαίνετε στο **APIs & Services > Library**
   - Αναζητήστε **"Google Sheets API"** και ενεργοποιήστε το
   - Αναζητήστε **"Google Drive API"** και ενεργοποιήστε το

### 2. Δημιουργία Service Account

1. Πηγαίνετε στο **IAM & Admin > Service Accounts**
2. Πατήστε **+ CREATE SERVICE ACCOUNT**
3. Δώστε όνομα (π.χ. `techflow-bot`)
4. Δώστε ρόλο **Editor** (Project > Editor)
5. Πατήστε **Done**

### 3. Δημιουργία Credentials

1. Κάντε κλικ στο Service Account που δημιουργήσατε
2. Πηγαίνετε στην καρτέλα **Keys**
3. Πατήστε **ADD KEY > Create new key**
4. Επιλέξτε **JSON**
5. Το αρχείο θα κατέβει αυτόματα
6. **Μετονομάστε** το αρχείο σε `google-sheets-credentials.json`

### 4. Τοποθέτηση Credentials

Τοποθετήστε το αρχείο `google-sheets-credentials.json` στον φάκελο:
```
Part_B_Implementation/backend/credentials/
```

> **Σημείωση**: Ο φάκελος `credentials` είναι στο `.gitignore` για ασφάλεια.

### 5. Ρύθμιση Spreadsheet

Για να λειτουργήσει η σύνδεση, πρέπει να δημιουργήσετε ένα spreadsheet χειροκίνητα:

1. Δημιουργήστε ένα νέο Google Sheet
2. **Κοινοποιήστε** το sheet με το Service Account email (π.χ. `techflow-bot@project-id.iam.gserviceaccount.com`) ως **Editor**
3. Αντιγράψτε το **Spreadsheet ID** από το URL:
   `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_ΕΔΩ/edit`
4. Ενημερώστε το `.env`:
   ```bash
   GOOGLE_SPREADSHEET_ID=το_id_του_spreadsheet
   ```

> **Σημαντικό**: Το Spreadsheet ID είναι υποχρεωτικό. Η εφαρμογή δεν δημιουργεί αυτόματα νέο spreadsheet.

---

## Αντιμετώπιση Προβλημάτων

| Σφάλμα | Λύση |
|--------|------|
| **Error 403 (Permission Denied)** | Κοινοποιήσατε το sheet με το Service Account email; |
| **Error 404 (Not Found)** | Είναι σωστό το Spreadsheet ID; |
| **API Not Enabled** | Ενεργοποιήσατε και τα δύο APIs (Sheets + Drive); |

---

## Σημείωση Ασφαλείας

⚠️ **ΜΗΝ κάνετε commit το JSON αρχείο στο Git!**

Ο φάκελος `backend/credentials/` έχει δικό του `.gitignore` που:
- ✅ **Αγνοεί** όλα τα credential αρχεία (π.χ. `google-sheets-credentials.json`)
- ✅ **Επιτρέπει** μόνο: `README.md`, `.gitignore`, `*.example.json`

Για επαλήθευση, τρέξτε: `git check-ignore -v backend/credentials/google-sheets-credentials.json`

---

**TechFlow Solutions - Data Automation Platform**
