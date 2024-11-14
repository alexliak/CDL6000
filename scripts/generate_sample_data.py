"""
Δημιουργία sample dataset για development
"""

import pandas as pd
import numpy as np
from pathlib import Path


def create_sample_legal_data(n_samples=100):
    """
    Δημιουργία sample legal dataset
    """
    # Sample legal texts
    legal_texts = [
        f"In the case of Smith v. Johnson ({np.random.randint(1990, 2020)}), "
        + "the court found that pursuant to Section 123 of the Civil Code, "
        + "the defendant was liable for damages. See also Brown v. Williams (2015)."
        for _ in range(n_samples)
    ]

    # Sample outcomes
    outcomes = np.random.choice(
        ["Allowed", "Dismissed", "Settled"], size=n_samples, p=[0.4, 0.35, 0.25]
    )

    # Create DataFrame
    df = pd.DataFrame(
        {
            "case_id": range(1, n_samples + 1),
            "case_text": legal_texts,
            "case_outcome": outcomes,
        }
    )

    return df


if __name__ == "__main__":
    # Create sample data
    sample_df = create_sample_legal_data()

    # Create data directory if it doesn't exist
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Save to CSV
    output_path = data_dir / "legal_cases.csv"
    sample_df.to_csv(output_path, index=False)
    print(f"✅ Created sample dataset with {len(sample_df)} cases at {output_path}")
