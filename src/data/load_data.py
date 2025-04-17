# src/data/load_data.py

import pandas as pd
from pathlib import Path
import logging
import warnings

# Configure logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

def load_participants(attr_dir: Path) -> pd.DataFrame:
    """
    Loads the Participants.csv file from the attributes directory.

    Args:
        attr_dir: Path object pointing to the 'Attributes' directory.

    Returns:
        A pandas DataFrame containing participant data, or an empty DataFrame on error.
    """
    participants_file = attr_dir / 'Participants.csv'
    logging.info(f"Attempting to load participants file: {participants_file}")
    try:
        df = pd.read_csv(participants_file)
        # Add any *consistent* cleaning needed based on notebook exploration
        # Example: Ensure haveKids is boolean if it sometimes loads differently
        if 'haveKids' in df.columns and df['haveKids'].dtype != 'bool':
             with warnings.catch_warnings(): # Suppress potential future warnings from astype
                warnings.simplefilter("ignore", FutureWarning)
                df['haveKids'] = df['haveKids'].astype(bool)

        if 'participantId' in df.columns and df['participantId'].dtype != 'Int64':
             df['participantId'] = pd.to_numeric(df['participantId'], errors='coerce').astype('Int64')

        logging.info(f"Successfully loaded and performed basic checks on Participants data. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logging.error(f"Participants file not found: {participants_file}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error loading or cleaning {participants_file.name}: {e}")
        return pd.DataFrame()

def load_participant_logs_sample(logs_dir: Path, file_index: int = 0) -> pd.DataFrame:
    """
    Loads a *single* specified participant status log file and performs basic cleaning.
    Designed for loading samples, not the entire dataset at once.

    Args:
        logs_dir: Path object pointing to the 'Activity Logs' directory.
        file_index: The index of the sorted log file to load (default: 0 for the first file).

    Returns:
        A pandas DataFrame containing the sample log data, or an empty DataFrame on error.
    """
    log_files = sorted(logs_dir.glob('ParticipantStatusLogs*.csv'))
    if not log_files or file_index >= len(log_files) or file_index < 0:
        logging.error(f"Log file index {file_index} out of range or no logs found in {logs_dir}")
        return pd.DataFrame()

    file_to_load = log_files[file_index]
    logging.info(f"Attempting to load log file sample: {file_to_load.name}")
    try:
        df = pd.read_csv(file_to_load)

        # --- Consistent Cleaning based on Notebook ---
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        else:
            logging.warning(f"'timestamp' column not found in {file_to_load.name}")

        if 'availableBalance' in df.columns:
             if df['availableBalance'].dtype == 'object':
                 df['availableBalance'] = pd.to_numeric(df['availableBalance'], errors='coerce')
             if pd.api.types.is_integer_dtype(df['availableBalance']):
                 df['availableBalance'] = df['availableBalance'].astype(float)

        if 'participantId' in df.columns:
             if df['participantId'].dtype != 'Int64':
                 df['participantId'] = pd.to_numeric(df['participantId'], errors='coerce').astype('Int64')

        # Add cleaning for other columns (apartmentId, jobId, etc.) if needed

        logging.info(f"Successfully loaded and cleaned log sample {file_to_load.name}. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logging.error(f"Log file sample not found: {file_to_load}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error loading or cleaning log sample {file_to_load.name}: {e}")
        return pd.DataFrame()


def load_financial_journal(journal_dir: Path) -> pd.DataFrame:
    """
    Loads the FinancialJournal.csv file from the journals directory.

    Args:
        journal_dir: Path object pointing to the 'Journals' directory.

    Returns:
        A pandas DataFrame containing financial journal data, or an empty DataFrame on error.
    """
    journal_file = journal_dir / 'FinancialJournal.csv'
    logging.info(f"Attempting to load financial journal file: {journal_file}")
    try:
        df = pd.read_csv(journal_file)

        # --- Consistent Cleaning based on Notebook ---
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        if 'amount' in df.columns:
            if not pd.api.types.is_float_dtype(df['amount']):
                df['amount'] = pd.to_numeric(df['amount'], errors='coerce').astype(float)

        if 'participantId' in df.columns:
            if df['participantId'].dtype != 'Int64':
                 df['participantId'] = pd.to_numeric(df['participantId'], errors='coerce').astype('Int64')

        logging.info(f"Successfully loaded and cleaned Financial Journal data. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logging.error(f"Financial Journal file not found: {journal_file}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error loading or cleaning {journal_file.name}: {e}")
        return pd.DataFrame()

# --- Add functions here to load other files as needed ---
# Example:
# def load_apartments(attr_dir: Path) -> pd.DataFrame:
#     # ... loading logic for Apartments.csv ...
#     pass

# def load_jobs(attr_dir: Path) -> pd.DataFrame:
#     # ... loading logic for Jobs.csv ...
#     pass