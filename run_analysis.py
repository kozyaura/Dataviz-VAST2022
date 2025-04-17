# run_analysis.py

import logging
from pathlib import Path

# Assumes your src directory is importable
from src.data import load_data
from src.features import build_features
from src.visualization import visualize

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
BASE_DIR = Path('.') # Assumes script is run from project root
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
ATTR_DIR = RAW_DATA_DIR / 'Attributes'
LOGS_DIR = RAW_DATA_DIR / 'Activity Logs'
JOURNAL_DIR = RAW_DATA_DIR / 'Journals'

PRIMARY_DATA_DIR = BASE_DIR / 'data' / '03_primary'
REPORTS_DIR = BASE_DIR / 'reports' / 'figures'

LOG_FILE_INDEX_TO_PROCESS = 0 # Which log file to use (0 for first, 1 for second, etc.)
FINANCIAL_THRESHOLD = 50.0 # Threshold for 'Low Balance' group
TIMELINE_SAMPLE_SIZE = 2 # Participants per group for timeline plot
TIMELINE_DAYS = 7 # Number of days for timeline plot

# --- Ensure output directories exist ---
PRIMARY_DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Main Script Logic ---
def main():
    logging.info("Starting analysis pipeline...")

    # 1. Load Data
    logging.info("--- Loading Data ---")
    participants_df = load_data.load_participants(ATTR_DIR)
    # Load only ONE log file for this example script
    logs_df = load_data.load_participant_logs(LOGS_DIR, file_index=LOG_FILE_INDEX_TO_PROCESS)
    financial_journal_df = load_data.load_financial_journal(JOURNAL_DIR)

    if participants_df.empty or logs_df.empty:
        logging.error("Essential data (participants or logs) could not be loaded. Exiting.")
        return

    # 2. Build Features
    logging.info("--- Building Features ---")
    avg_balance_df = build_features.calculate_average_balance(logs_df)
    participants_summary_df = build_features.add_financial_group(
        participants_df, avg_balance_df, threshold=FINANCIAL_THRESHOLD
    )

    # Save primary data
    primary_participants_path = PRIMARY_DATA_DIR / 'participant_summary.csv'
    try:
        participants_summary_df.to_csv(primary_participants_path, index=False)
        logging.info(f"Saved primary participant summary data to {primary_participants_path}")
    except Exception as e:
        logging.error(f"Failed to save primary data: {e}")


    # 3. Generate Visualizations
    logging.info("--- Generating Visualizations ---")

    # Plot balance distribution
    viz_balance_dist_path = REPORTS_DIR / 'initial_avg_balance_histogram.png'
    visualize.plot_balance_distribution(participants_summary_df, viz_balance_dist_path)

    # Plot comparative timeline
    viz_timeline_path = REPORTS_DIR / 'final_balance_timeline_comparison.png'
    visualize.plot_comparative_balance_timeline(
        logs_df, participants_summary_df, financial_journal_df, viz_timeline_path,
        n_samples=TIMELINE_SAMPLE_SIZE, days_window=TIMELINE_DAYS
    )

    # Plot activity heatmap (example for 'AtRestaurant')
    viz_heatmap_path = REPORTS_DIR / 'final_restaurant_heatmap_comparison.png'
    visualize.plot_activity_heatmap(
        logs_df, participants_summary_df, mode_to_plot='AtRestaurant', save_path=viz_heatmap_path
    )
    # Add calls to plot heatmaps for other modes ('AtWork', 'AtRecreation', etc.) if desired

    logging.info("Analysis pipeline finished.")

if __name__ == "__main__":
    main()