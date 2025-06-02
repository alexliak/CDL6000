# Performance Visualization and Prediction System
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class ModelPerformanceAnalyzer:
    """
    A comprehensive system for analyzing, visualizing, and predicting model performance.
    Integrates with our SQLite database and provides detailed insights.
    """
    def __init__(self, db_path='D:/Projects/LegalTextAnalysis/data/legal_text.db'):
        self.db_path = db_path
        # Set up visualization styling
        plt.style.use('seaborn')
        self.colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f']
    
    def load_performance_data(self):
        """Load and prepare performance data from database"""
        query = """
            SELECT 
                timestamp,
                accuracy,
                f1_score,
                EXISTS(
                    SELECT 1 
                    FROM quality_metrics qm 
                    WHERE DATE(qm.metric_date) = DATE(mp.timestamp)
                ) as has_quality_metrics
            FROM model_performance mp
            ORDER BY timestamp
        """
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql(query, conn, parse_dates=['timestamp'])
            df['date'] = df['timestamp'].dt.date
            return df
    
    def create_trend_visualization(self, data=None):
        """
        Create a comprehensive trend visualization with multiple components.
        Includes performance metrics, confidence intervals, and trend indicators.
        """
        if data is None:
            data = self.load_performance_data()
            
        # Create main figure with subplots
        fig = plt.figure(figsize=(15, 10))
        gs = fig.add_gridspec(2, 2, height_ratios=[2, 1])
        
        # Performance Metrics Plot (Top Left)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(data['timestamp'], data['accuracy'], 
                color=self.colors[0], label='Accuracy',
                marker='o', markersize=4)
        ax1.plot(data['timestamp'], data['f1_score'],
                color=self.colors[1], label='F1-Score',
                marker='o', markersize=4, linestyle='--')
        
        # Add trend line
        z = np.polyfit(range(len(data)), data['accuracy'], 1)
        p = np.poly1d(z)
        ax1.plot(data['timestamp'], p(range(len(data))),
                color=self.colors[2], label='Trend',
                linestyle=':')
        
        ax1.set_title('Model Performance Over Time')
        ax1.set_ylabel('Score')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Moving Average Plot (Top Right)
        ax2 = fig.add_subplot(gs[0, 1])
        window = 3
        data['MA_accuracy'] = data['accuracy'].rolling(window=window).mean()
        data['MA_f1'] = data['f1_score'].rolling(window=window).mean()
        
        ax2.plot(data['timestamp'], data['MA_accuracy'],
                color=self.colors[0], label=f'{window}-Day Avg Accuracy')
        ax2.plot(data['timestamp'], data['MA_f1'],
                color=self.colors[1], label=f'{window}-Day Avg F1-Score')
        
        # Add confidence intervals
        std_acc = data['accuracy'].rolling(window=window).std()
        ax2.fill_between(data['timestamp'],
                        data['MA_accuracy'] - std_acc,
                        data['MA_accuracy'] + std_acc,
                        alpha=0.2, color=self.colors[0])
        
        ax2.set_title('Moving Averages with Confidence Intervals')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Performance Distribution (Bottom Left)
        ax3 = fig.add_subplot(gs[1, 0])
        sns.kdeplot(data=data, x='accuracy', ax=ax3, 
                   color=self.colors[0], label='Accuracy Dist.')
        sns.kdeplot(data=data, x='f1_score', ax=ax3,
                   color=self.colors[1], label='F1-Score Dist.')
        
        ax3.set_title('Performance Distribution')
        ax3.grid(True, alpha=0.3)
        
        # Key Metrics Table (Bottom Right)
        ax4 = fig.add_subplot(gs[1, 1])
        metrics_text = [
            f"Latest Accuracy: {data['accuracy'].iloc[-1]:.4f}",
            f"Latest F1-Score: {data['f1_score'].iloc[-1]:.4f}",
            f"Accuracy Trend: {'+' if z[0] > 0 else '-'}{abs(z[0]):.4f}/day",
            f"Measurements: {len(data)}",
            f"Date Range: {data['timestamp'].min().date()} to {data['timestamp'].max().date()}"
        ]
        ax4.text(0.1, 0.5, '\n'.join(metrics_text),
                transform=ax4.transAxes, fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8))
        ax4.axis('off')
        
        plt.tight_layout()
        return fig
    
    def predict_future_performance(self, days_ahead=7):
        """
        Predict future performance using historical data and confidence intervals.
        Uses a combination of trend analysis and statistical modeling.
        """
        data = self.load_performance_data()
        
        # Calculate trend components
        x = np.arange(len(data))
        accuracy_z = np.polyfit(x, data['accuracy'], 1)
        f1_z = np.polyfit(x, data['f1_score'], 1)
        
        # Generate future dates
        last_date = data['timestamp'].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead+1)]
        
        # Make predictions with confidence intervals
        predictions = []
        for i, date in enumerate(future_dates, start=len(data)):
            accuracy_pred = np.poly1d(accuracy_z)(i)
            f1_pred = np.poly1d(f1_z)(i)
            
            # Calculate confidence intervals (using historical variance)
            accuracy_std = data['accuracy'].std()
            f1_std = data['f1_score'].std()
            
            predictions.append({
                'date': date,
                'predicted_accuracy': accuracy_pred,
                'accuracy_lower': max(0, accuracy_pred - 2*accuracy_std),
                'accuracy_upper': min(1, accuracy_pred + 2*accuracy_std),
                'predicted_f1': f1_pred,
                'f1_lower': max(0, f1_pred - 2*f1_std),
                'f1_upper': min(1, f1_pred + 2*f1_std)
            })
        
        return pd.DataFrame(predictions)

# Create and demonstrate the analysis
analyzer = ModelPerformanceAnalyzer()

# Generate visualizations
performance_fig = analyzer.create_trend_visualization()

# Make predictions
predictions = analyzer.predict_future_performance(days_ahead=7)
print("\nPerformance Predictions for Next 7 Days:")
print(predictions[['date', 'predicted_accuracy', 'predicted_f1']].to_string(index=False))