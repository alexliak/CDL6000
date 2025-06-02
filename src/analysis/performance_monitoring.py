from datetime import datetime
import sqlite3
import pandas as pd

class EnhancedPerformanceMonitor:
    """
    Advanced monitoring system that integrates with our database and provides
    comprehensive performance tracking and alerting capabilities.
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.alert_thresholds = {
            'accuracy': {
                'critical': 0.85,
                'warning': 0.87,
                'target': 0.90
            },
            'stability': {
                'high_variance': 0.03,
                'moderate_variance': 0.01
            },
            'measurement_frequency': {
                'min_daily': 3,
                'max_daily': 20
            }
        }
    
    def check_performance_health(self):
        """
        Comprehensive health check of the model's performance metrics.
        Returns a detailed health report with alerts and recommendations.
        """
        query = """
        WITH recent_performance AS (
            SELECT 
                DATE(timestamp) as measurement_date,
                COUNT(*) as daily_measurements,
                AVG(accuracy) as avg_accuracy,
                AVG(f1_score) as avg_f1_score,
                MAX(accuracy) - MIN(accuracy) as accuracy_range
            FROM model_performance
            WHERE timestamp >= DATE('now', '-7 days')
            GROUP BY DATE(timestamp)
        )
        SELECT 
            measurement_date,
            daily_measurements,
            ROUND(avg_accuracy, 4) as avg_accuracy,
            ROUND(avg_f1_score, 4) as avg_f1_score,
            ROUND(accuracy_range, 4) as accuracy_range
        FROM recent_performance
        ORDER BY measurement_date DESC;
        """
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql(query, conn)
            
        health_report = {
            'timestamp': datetime.now(),
            'alerts': [],
            'recommendations': [],
            'status': 'healthy'
        }
        
        # Check accuracy levels
        latest_accuracy = df['avg_accuracy'].iloc[0]
        if latest_accuracy < self.alert_thresholds['accuracy']['critical']:
            health_report['alerts'].append({
                'level': 'CRITICAL',
                'message': f'Accuracy ({latest_accuracy:.4f}) below critical threshold'
            })
            health_report['status'] = 'critical'
        elif latest_accuracy < self.alert_thresholds['accuracy']['warning']:
            health_report['alerts'].append({
                'level': 'WARNING',
                'message': f'Accuracy ({latest_accuracy:.4f}) below warning threshold'
            })
            health_report['status'] = 'warning'
            
        # Check stability
        if df['accuracy_range'].mean() > self.alert_thresholds['stability']['high_variance']:
            health_report['alerts'].append({
                'level': 'WARNING',
                'message': 'High performance variance detected'
            })
            health_report['recommendations'].append(
                'Consider reviewing recent changes that might affect stability'
            )
            
        # Check measurement frequency
        avg_measurements = df['daily_measurements'].mean()
        if avg_measurements < self.alert_thresholds['measurement_frequency']['min_daily']:
            health_report['alerts'].append({
                'level': 'WARNING',
                'message': 'Insufficient daily measurements'
            })
            health_report['recommendations'].append(
                'Increase measurement frequency to at least 3 per day'
            )
            
        # Add trend analysis
        accuracy_trend = df['avg_accuracy'].diff().mean()
        health_report['metrics'] = {
            'current_accuracy': latest_accuracy,
            'weekly_trend': accuracy_trend,
            'stability_score': 1 - (df['accuracy_range'].mean() / latest_accuracy)
        }
        
        return health_report
    
    def generate_weekly_summary(self):
        """
        Creates a detailed weekly summary of performance metrics and trends.
        """
        query = """
        WITH weekly_metrics AS (
            SELECT 
                strftime('%Y-Week %W', timestamp) as week,
                COUNT(*) as measurements,
                ROUND(AVG(accuracy), 4) as avg_accuracy,
                ROUND(AVG(f1_score), 4) as avg_f1_score,
                ROUND(MAX(accuracy) - MIN(accuracy), 4) as accuracy_range
            FROM model_performance
            GROUP BY strftime('%Y-Week %W', timestamp)
        )
        SELECT * FROM weekly_metrics
        ORDER BY week DESC
        LIMIT 4;
        """
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql(query, conn)
            
        summary = {
            'period': f"{df['week'].iloc[-1]} to {df['week'].iloc[0]}",
            'metrics': {
                'accuracy': {
                    'average': df['avg_accuracy'].mean(),
                    'trend': df['avg_accuracy'].diff().mean(),
                    'stability': 1 - df['accuracy_range'].mean()
                },
                'measurements': {
                    'total': df['measurements'].sum(),
                    'average_per_week': df['measurements'].mean()
                }
            },
            'insights': []
        }
        
        # Generate insights
        if summary['metrics']['accuracy']['trend'] > 0:
            summary['insights'].append(
                f"Improving trend: {summary['metrics']['accuracy']['trend']:.4f} per week"
            )
        
        if summary['metrics']['accuracy']['stability'] > 0.95:
            summary['insights'].append("Excellent stability in measurements")
        
        return summary

# Example usage:
monitor = EnhancedPerformanceMonitor('D:/Projects/LegalTextAnalysis/data/legal_text.db')
health_report = monitor.check_performance_health()
weekly_summary = monitor.generate_weekly_summary()

print("\nHealth Report:")
print(f"Status: {health_report['status']}")
if health_report['alerts']:
    print("\nAlerts:")
    for alert in health_report['alerts']:
        print(f"- {alert['level']}: {alert['message']}")

print("\nWeekly Summary:")
print(f"Period: {weekly_summary['period']}")
print(f"Average Accuracy: {weekly_summary['metrics']['accuracy']['average']:.4f}")
print("\nInsights:")
for insight in weekly_summary['insights']:
    print(f"- {insight}")