# %%
import pandas as pd
import numpy as np
from pathlib import Path

# Correct path to your CSV file
df = pd.read_csv("data/raw/legal_cases.csv")

# Basic data validation and cleaning
print(f"Total cases: {len(df)}")
print(f"Missing values:\n{df.isnull().sum()}")

# Add length statistics
df["text_length"] = df["case_text"].str.len()
print(f"\nText length statistics:\n{df['text_length'].describe()}")

# Analyze case outcomes distribution
print(f"\nCase outcomes distribution:\n{df['case_outcome'].value_counts()}")

# %%
import os

print(f"Current working directory: {os.getcwd()}")

# %%
# Import required libraries
import re
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


# 1. Create clean citation analysis function
def analyze_citations(df):
    """
    Analyze citations from legal cases
    Returns DataFrame with citation counts
    """
    # Add citation counts column
    citation_pattern = r"\[\d{4}\]\s+[A-Z]+\s+\d+"
    df["citation_count"] = df["case_text"].apply(
        lambda x: len(re.findall(citation_pattern, str(x)))
    )

    # Group by case outcome
    citation_stats = (
        df.groupby("case_outcome")["citation_count"]
        .agg(["mean", "count", "sum"])
        .round(2)
    )

    return citation_stats


# 2. Run the analysis
citation_analysis = analyze_citations(df)
print("\nCitation Analysis by Case Outcome:")
print("-" * 50)
print(citation_analysis.sort_values("mean", ascending=False))


# 3. Extract and analyze specific years
def extract_citation_years(text):
    """Extract years from citation patterns"""
    pattern = r"\[(\d{4})\]"
    years = re.findall(pattern, str(text))
    return [int(year) for year in years]


df["citation_years"] = df["case_text"].apply(extract_citation_years)

# 4. Plot year distribution
all_years = [year for years in df["citation_years"] for year in years]

plt.figure(figsize=(12, 6))
plt.hist(all_years, bins=50, color="skyblue", edgecolor="black")
plt.title("Distribution of Citation Years")
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.grid(True, alpha=0.3)
plt.show()


# 5. Find most common citation patterns
def extract_full_citations(text):
    """Extract complete citation patterns"""
    pattern = r"\[\d{4}\]\s+[A-Z]+\s+\d+"
    return re.findall(pattern, str(text))


df["full_citations"] = df["case_text"].apply(extract_full_citations)
all_citations = [cite for cites in df["full_citations"] for cite in cites]

print("\nTop 10 Most Common Citations:")
print("-" * 50)
for citation, count in Counter(all_citations).most_common(10):
    print(f"{citation}: {count} times")
