-- First, we create our main table for storing case information
CREATE TABLE legal_cases (
    case_id TEXT PRIMARY KEY,      -- Unique identifier for each case
    case_outcome TEXT,             -- Outcome of the case
    case_title TEXT,               -- Title/name of the case
    case_text TEXT,                -- Full text content of the case
    text_length INTEGER,           -- Number of characters in case_text
    word_count INTEGER,            -- Number of words in case_text
    citation_count INTEGER,        -- Number of citations found
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Record creation time
);

-- Next, we create a table for storing text analysis metrics
CREATE TABLE text_metrics (
    case_id TEXT PRIMARY KEY,
    sentence_count INTEGER,        -- Number of sentences in the text
    citation_density REAL,         -- Citations per text length
    sentence_complexity REAL,      -- Words per sentence ratio
    length_category TEXT,          -- Classification of text length
    FOREIGN KEY (case_id) REFERENCES legal_cases(case_id)
);

-- Finally, we create a table for term frequency-inverse document frequency scores
CREATE TABLE tf_idf_scores (       -- Changed from tfidf_scores to tf_idf_scores
    case_id TEXT,
    term TEXT,                     -- The word or phrase being analyzed
    score REAL,                    -- The TF-IDF score
    term_category TEXT,            -- 'high' or 'low' significance
    PRIMARY KEY (case_id, term),
    FOREIGN KEY (case_id) REFERENCES legal_cases(case_id)
);

-- Create indices for better query performance
CREATE INDEX idx_case_outcome ON legal_cases(case_outcome);
CREATE INDEX idx_text_length ON legal_cases(text_length);
CREATE INDEX idx_term_scores ON tf_idf_scores(score);  -- Changed from tfidf_scores