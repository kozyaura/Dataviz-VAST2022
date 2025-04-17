# src/features/build_features.py

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_average_balance(logs_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates average availableBalance per participant from log data."""
    if logs_df.empty or 'participantId' not in logs_df or 'availableBalance' not in logs_df:
        logging.warning("Logs DataFrame is empty or missing required columns for balance calculation.")
        return pd.DataFrame(columns=['participantId', 'averageBalance'])

    logging.info("Calculating average balance per participant...")
    avg_balance = logs_df.groupby('participantId')['availableBalance'].mean().reset_index()
    avg_balance = avg_balance.rename(columns={'availableBalance': 'averageBalance'})
    logging.info(f"Calculated average balance for {len(avg_balance)} participants.")
    return avg_balance

def add_financial_group(summary_df: pd.DataFrame, threshold: float = 50.0) -> pd.DataFrame:
    """
    Assigns a financial group based on an existing 'averageBalance' column
    in the input DataFrame.

    Args:
        summary_df: DataFrame containing participant summaries, MUST include
                    an 'averageBalance' column.
        threshold: The threshold below which participants are 'Low Balance'.

    Returns:
        The input DataFrame with an added 'financialGroup' column.
    """
    if summary_df.empty:
        logging.warning("Input DataFrame is empty. Cannot add financial group.")
        return summary_df # Return empty df
    if 'averageBalance' not in summary_df.columns:
        logging.error("Input DataFrame is missing 'averageBalance' column. Cannot assign group.")
        # Optionally add the column with 'Unknown' or return df as is
        summary_df['financialGroup'] = 'Unknown/MissingBalance'
        return summary_df

    logging.info(f"Assigning financial group based on threshold: {threshold}")

    # --- REMOVED THE MERGE CALL ---

    # Assign group based on existing 'averageBalance' column
    summary_df['financialGroup'] = np.where(
        summary_df['averageBalance'].notna() & (summary_df['averageBalance'] < threshold),
        'Low Balance',
        'Other'
    )
    # Handle participants potentially not in the log sample (NaN averageBalance)
    summary_df.loc[summary_df['averageBalance'].isna(), 'financialGroup'] = 'Unknown/Other' # Keep this logic

    logging.info("Financial group counts:\n" + str(summary_df['financialGroup'].value_counts()))
    return summary_df

# Add other feature engineering functions here (e.g., commute time, stability metric)