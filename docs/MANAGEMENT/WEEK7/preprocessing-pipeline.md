# Legal Text Preprocessing Pipeline

_Systematic preprocessing and feature engineering pipeline with database integration_

## 1. Setup and Imports

```Python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3
import logging
from datetime import datetime
import os
# Configure logginglogging.basicConfig(
    filename=f'logs/preprocessing_logs/preprocessing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Database connectiondef get_db_connection():
    """Create database connection with error handling"""    try:
        conn = sqlite3.connect('data/legal_text.db')
        logger.info("Database connection established")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise## 2. Data Loading and Initial Analysisdef load_and_analyze_data():
    """Load data from database and perform initial analysis"""    conn = get_db_connection()
    try:
        # Load data        df = pd.read_sql("SELECT * FROM legal_cases", conn)
        logger.info(f"Loaded {len(df)} records from database")
        # Basic statistics        stats = {
            'total_records': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'text_length_stats': df['case_text'].str.len().describe().to_dict()
        }
        logger.info(f"Initial statistics: {stats}")
        return df, stats
    except Exception as e:
        logger.error(f"Data loading failed: {str(e)}")
        raise    finally:
        conn.close()
## 3. Preprocessing Pipelineclass TextPreprocessingPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.tfidf = TfidfVectorizer(max_features=500)
        logger.info("Initialized preprocessing pipeline")
    def clean_text(self, text):
        """Clean and normalize text"""        # Implementation from your existing notebooks        cleaned = str(text).strip()
        # Add more cleaning steps as needed        return cleaned
    def extract_features(self, df):
        """Extract features from text data"""        features = pd.DataFrame()
        # Basic features        features['char_count'] = df['case_text'].str.len()
        features['word_count'] = df['case_text'].str.split().str.len()
        features['sentence_count'] = df['case_text'].str.count('[.!?]')
        # Citation features        features['citation_count'] = df['case_text'].str.count(r'\[\d{4}\]|\(\d{4}\)')
        features['citation_density'] = features['citation_count'] / features['char_count']
        logger.info("Feature extraction completed")
        return features
    def normalize_features(self, features):
        """Normalize numerical features"""        numeric_cols = features.select_dtypes(include=['float64', 'int64']).columns
        features[numeric_cols] = self.scaler.fit_transform(features[numeric_cols])
        logger.info("Feature normalization completed")
        return features
    def save_to_database(self, features, table_name='text_metrics'):
        """Save processed features to database"""        conn = get_db_connection()
        try:
            features.to_sql(table_name, conn, if_exists='replace', index=False)
            logger.info(f"Saved features to {table_name} table")
        except Exception as e:
            logger.error(f"Database save failed: {str(e)}")
            raise        finally:
            conn.close()
## 4. Pipeline Executiondef main():
    logger.info("Starting preprocessing pipeline")
    try:
        # Load data        df, stats = load_and_analyze_data()
        # Initialize pipeline        pipeline = TextPreprocessingPipeline()
        # Process in batches        batch_size = 1000        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}")
            # Extract and process features            features = pipeline.extract_features(batch)
            normalized_features = pipeline.normalize_features(features)
            # Save to database            pipeline.save_to_database(normalized_features)
        logger.info("Pipeline execution completed successfully")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raiseif __name__ == "__main__":
    main()
```

## 5. Analysis and Validation

```Python
def validate_results():
    """Validate preprocessing results"""    conn = get_db_connection()
    try:
        # Load processed features        features = pd.read_sql("SELECT * FROM text_metrics", conn)
        # Basic validation checks        validation = {
            'total_records': len(features),
            'null_values': features.isnull().sum().to_dict(),
            'feature_ranges': {col: {'min': features[col].min(),
                                   'max': features[col].max()}
                             for col in features.columns}
        }
        logger.info(f"Validation results: {validation}")
        return validation
    finally:
        conn.close()
```

## 6. Usage Example

```Python
# Run the complete pipelinemain()
# Validate resultsvalidation_results = validate_results()
# Display summaryprint("Pipeline execution completed.")
print(f"Processed {validation_results['total_records']} records")
print("Feature ranges:")
for feature, ranges in validation_results['feature_ranges'].items():
    print(f"{feature}: {ranges['min']:.2f} to {ranges['max']:.2f}")
```