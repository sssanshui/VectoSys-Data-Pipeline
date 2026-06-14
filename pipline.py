import numpy as np
import pandas as pd
from typing import Optional

class QuantitativeDataPipeline:
    """
    A production-ready data preprocessing pipeline optimized for 
    quantitative time-series datasets.
    """
    def __init__(self, dataframe: pd.DataFrame):
        if dataframe.empty:
            raise ValueError("Input dataframe cannot be empty.")
        self.df = dataframe.copy()

    def sanitize_columns(self) -> 'QuantitativeDataPipeline':
        """Cleans and standardizes dataframe column headers."""
        self.df.columns = [str(col).lower().strip().replace(" ", "_") for col in self.df.columns]
        return self

    def handle_missing_values(self, method: str = 'ffill') -> 'QuantitativeDataPipeline':
        """Imputes missing data points safely using vectorized operations."""
        if method == 'ffill':
            self.df = self.df.ffill().bfill()
        elif method == 'drop':
            self.df = self.df.dropna()
        else:
            self.df = self.df.fillna(0)
        return self

    def filter_outliers_zscore(self, column: str, threshold: float = 3.0) -> 'QuantitativeDataPipeline':
        """
        Filters anomalies in the dataset based on statistical Z-Score metrics.
        Useful for preventing bad data ticks from distorting analytical models.
        """
        if column not in self.df.columns:
            return self
            
        mean = self.df[column].mean()
        std = self.df[column].std()
        
        if std == 0:
            return self
            
        z_scores = (self.df[column] - mean) / std
        self.df = self.df[abs(z_scores) <= threshold]
        return self

    def get_processed_data(self) -> pd.DataFrame:
        """Returns the fully transformed and optimized dataframe."""
        return self.df

# Operational baseline check
if __name__ == "__main__":
    # Simulate a raw financial tick dataset
    mock_data = pd.DataFrame({
        ' Timestamp ': ['2026-06-01', '2026-06-02', '2026-06-03', '2026-06-04'],
        'Close Price': [150.5, np.nan, 152.3, 300.0]  # Contains missing value and an outlier
    })
    
    print("Initializing VectoSys Pipeline validation...")
    pipeline = QuantitativeDataPipeline(mock_data)
    
    processed_df = (pipeline
                    .sanitize_columns()
                    .handle_missing_values(method='ffill')
                    .filter_outliers_zscore(column='close_price', threshold=2.0)
                    .get_processed_data())
                    
    print("\nData pipeline check complete. Current structure:")
    print(processed_df)
