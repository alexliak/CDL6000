# CLD6000 Design Document Generator

Ένα εργαλείο Python για την αυτόματη δημιουργία τεχνικής τεκμηρίωσης του συστήματος ταξινόμησης νομικών εγγράφων CLD6000.

## 📋 Περιεχόμενα

- [Προαπαιτούμενα](#προαπαιτούμενα)
- [Εγκατάσταση](#εγκατάσταση)
- [Χρήση](#χρήση)
- [Δομή Project](#δομή-project)
- [Συνεισφορά](#συνεισφορά)
- [Άδεια](#άδεια)

## 🔧 Προαπαιτούμενα

- Python 3.7 ή νεότερη έκδοση
- Windows OS (για το default path D:/)

Το script μπορεί να τρέξει απευθείας χωρίς virtual environment, καθώς χρησιμοποιεί μόνο built-in βιβλιοθήκες της Python:
- `os`
- `datetime`

## 💻 Εγκατάσταση

1. Κλωνοποιήστε το repository:
```bash
git clone https://github.com/YourUsername/cld6000-design-doc-generator.git
cd cld6000-design-doc-generator
```

2. (Προαιρετικό) Δημιουργία virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

## 🚀 Χρήση

1. Απλή εκτέλεση:
```bash
python create_design_document.py
```

2. Το script θα:
   - Δημιουργήσει τον φάκελο D:/ αν δεν υπάρχει
   - Παράξει το αρχείο `cld6000-optical-design-proposal.md`
   - Επαληθεύσει ότι όλες οι απαιτούμενες ενότητες υπάρχουν
   - Εμφανίσει μηνύματα προόδου

3. Έλεγχος επιτυχίας:
   - Επιβεβαιώστε ότι το αρχείο δημιουργήθηκε στο D:/
   - Ελέγξτε τα μηνύματα του terminal για τυχόν σφάλματα
   - Ανοίξτε το .md αρχείο για να επιβεβαιώσετε το περιεχόμενο

## 📁 Δομή Project

```
cld6000-design-doc-generator/
│
├── create_design_document.py   # Κύριο script
├── README.md                  # Αυτό το αρχείο
└── requirements.txt           # (Προαιρετικό) Εξαρτήσεις
```

## 🤝 Συνεισφορά

1. Fork το Project
2. Δημιουργήστε νέο branch (`git checkout -b feature/AmazingFeature`)
3. Commit τις αλλαγές σας (`git commit -m 'Add some AmazingFeature'`)
4. Push στο Branch (`git push origin feature/AmazingFeature`)
5. Ανοίξτε ένα Pull Request

## ⚠️ Σημαντικές Σημειώσεις

### Τροποποίηση Path
Αν θέλετε να αλλάξετε το path εξόδου, τροποποιήστε τη μεταβλητή `doc_path` στη συνάρτηση `create_design_doc()`:

```python
doc_path = "YOUR_PREFERRED_PATH/cld6000-optical-design-proposal.md"
```

### Debugging
- Τα μηνύματα λάθους είναι αναλυτικά και εμφανίζονται στο terminal
- Ελέγξτε τα δικαιώματα εγγραφής στον φάκελο προορισμού
- Επιβεβαιώστε ότι το path είναι έγκυρο για το σύστημά σας

## 📝 Άδεια

Distributed under the MIT License. Δείτε το `LICENSE` για περισσότερες πληροφορίες.

---

✨ **Δημιουργήθηκε με αγάπη από την ομάδα του CLD6000** ✨

*Σημείωση: Αυτό το εργαλείο είναι μέρος του project CLD6000 για την αυτοματοποιημένη ταξινόμηση νομικών εγγράφων.*