# scripts/utils/viz_utils.py

"""Visualization utilities for legal text analysis project."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from .db_utils import DatabaseUtils

class VisualizationUtils:
    def __init__(self):
        """Initialize visualization utilities."""
        self.db = DatabaseUtils()
        self.setup_style()
        
    def setup_style(self):
        """Configure plotting style."""
        plt.style.use('seaborn-v0_8-darkgrid')  # Updated style name
        sns.set_theme(style="darkgrid")
        plt.rcParams['figure.figsize'] = [12, 6]
        
    def plot_case_distributions(self, save_path=None):
        """Plot distribution of cases by outcome and length category."""
        # Get data
        query = """
        SELECT 
            lc.case_outcome,
            tm.length_category,
            COUNT(*) as count
        FROM legal_cases lc
        JOIN text_metrics tm ON lc.case_id = tm.case_id
        GROUP BY lc.case_outcome, tm.length_category
        """
        df = pd.DataFrame(self.db.query_database(query))
        
        # Create subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Cases by Outcome
        outcome_counts = df.groupby('case_outcome')['count'].sum()
        sns.barplot(x=outcome_counts.values, y=outcome_counts.index, ax=ax1)
        ax1.set_title('Distribution of Case Outcomes')
        ax1.set_xlabel('Number of Cases')
        
        # Plot 2: Cases by Length Category
        length_counts = df.groupby('length_category')['count'].sum()
        sns.barplot(data=length_counts.reset_index(), x='length_category', y='count', ax=ax2)
        ax2.set_title('Distribution of Case Lengths')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            
        return fig
    
    def plot_metrics_heatmap(self, save_path=None):
        """Plot heatmap of metrics correlations."""
        query = """
        SELECT 
            tm.citation_density,
            tm.sentence_complexity,
            LENGTH(lc.case_text) as text_length,
            CAST((LENGTH(lc.case_text) - LENGTH(REPLACE(lc.case_text, ' ', ''))) AS FLOAT) as word_count
        FROM text_metrics tm
        JOIN legal_cases lc ON tm.case_id = lc.case_id
        """
        df = pd.DataFrame(self.db.query_database(query))
        
        # Compute correlation matrix
        corr_matrix = df.corr()
        
        # Plot heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation between Text Metrics')
        
        if save_path:
            plt.savefig(save_path)
            
        return plt.gcf()
    
    def plot_complexity_by_outcome(self, save_path=None):
        """Plot box plots of sentence complexity by case outcome."""
        query = """
        SELECT 
            lc.case_outcome,
            tm.sentence_complexity,
            tm.citation_density
        FROM legal_cases lc
        JOIN text_metrics tm ON lc.case_id = tm.case_id
        """
        df = pd.DataFrame(self.db.query_database(query))
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Sentence Complexity
        sns.boxplot(data=df, x='case_outcome', y='sentence_complexity', ax=ax1)
        ax1.set_title('Sentence Complexity by Case Outcome')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        
        # Plot 2: Citation Density
        sns.boxplot(data=df, x='case_outcome', y='citation_density', ax=ax2)
        ax2.set_title('Citation Density by Case Outcome')
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            
        return fig

# Example usage
if __name__ == "__main__":
    viz = VisualizationUtils()
    
    # Create visualizations
    viz.plot_case_distributions("data/case_distributions.png")
    viz.plot_metrics_heatmap("data/metrics_heatmap.png")
    viz.plot_complexity_by_outcome("data/complexity_by_outcome.png")