# src/visualization/visualize.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

# Configure logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

def plot_balance_distribution(participants_summary_df: pd.DataFrame, save_path: Path):
    """
    Generates and saves a histogram showing the distribution of average participant balances.

    Args:
        participants_summary_df: DataFrame containing participant summaries, must include
                                 an 'averageBalance' column.
        save_path: A Path object indicating where to save the generated plot image.
    """
    if participants_summary_df is None or participants_summary_df.empty:
        logging.warning("Participant summary DataFrame is empty. Skipping balance distribution plot.")
        return
    if 'averageBalance' not in participants_summary_df.columns:
        logging.warning("Participant summary DataFrame is missing 'averageBalance' column. Skipping distribution plot.")
        return

    logging.info(f"Plotting average balance distribution and attempting to save to {save_path}")

    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.histplot(data=participants_summary_df, x='averageBalance', bins=50, kde=True)
    plt.title('Distribution of Average Participant Balance (Full Dataset)')
    plt.xlabel('Average Available Balance')
    plt.ylabel('Number of Participants')
    plt.axvline(0, color='red', linestyle='--', label='Zero Balance') # Highlight zero
    plt.legend()
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout() # Adjust layout

    # Save the figure
    try:
        # Ensure the parent directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logging.info(f"Saved balance distribution plot to {save_path}")
    except Exception as e:
        logging.error(f"Failed to save plot to {save_path}: {e}")

    # Close the plot figure to free memory, especially important if calling function multiple times
    plt.close()

# --- Add other visualization functions below as you develop them ---
# Example placeholder:
# def plot_comparative_balance_timeline(...):
#     pass

# def plot_activity_heatmap(...):
#     pass