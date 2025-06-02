# CLD6000: Natural Language Processing for Legal Documents

## Project Scope Definition and Boundaries

This project focuses exclusively on Natural Language Processing (NLP) techniques and their application to legal documents, specifically avoiding classification tasks which are reserved for the dissertation project. 

### What This Project IS:
- Text extraction and processing
- Entity recognition
- Feature engineering
- Document structure analysis
- NLP pipeline development

### What This Project is NOT:
- Document classification
- Predictive modeling
- Legal taxonomy development
- Multi-label classification
- Classification evaluation metrics

## Technical Implementation

### 1. Document Processing Pipeline
```python
def process_legal_document(pdf_path):
    """
    Process legal documents using NLP techniques.
    Focuses on extraction and processing, NOT classification.
    """
    # Document loading
    raw_text = load_pdf(pdf_path)
    
    # Text preprocessing
    clean_text = preprocess_text(raw_text)
    
    # NLP analysis
    nlp_features = extract_nlp_features(clean_text)
    
    return nlp_features
```

### 2. Core NLP Components
- Tokenization
- Lemmatization
- Part-of-speech tagging
- Named entity recognition
- Dependency parsing

### 3. Dataset Selection
Using EUR-Lex subset (2000 documents) focusing on:
- Document structure
- Legal terminology
- Entity relationships
- Linguistic patterns

### 4. Development Tools
- spaCy
- NLTK
- PyPDF2
- Basic transformers for feature extraction

## Deliverables
1. NLP processing pipeline
2. Feature extraction framework
3. Document analysis tools
4. Technical documentation

## Important Note
This project deliberately excludes classification tasks to avoid overlap with the dissertation project "Classification of Legal Documents". The tools and features developed here will provide the foundation for the classification work in the dissertation, but will not implement classification directly.

## References
[List of NLP-specific references]