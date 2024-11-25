from entities.entity import Entity
import pandas as pd
import os

class WineData(Entity):
    """
    Handles data related to wine, including loading and saving CSV files.

    This class defines attributes related to wine data, such as target and feature columns,
    and provides methods for loading and saving wine data.

    Attributes:
        TARGET_COLUMN (str): The name of the target column in the dataset.
        FEATURE_COLUMN (list): List of feature column names used in the dataset.

    Methods:
        __init__(self):
            Initializes the WineData with a default name.
        load_data(file_path):
            Loads data from a CSV file into a pandas DataFrame.
        save_data(data, file_path):
            Saves a pandas DataFrame to a CSV file.
        run(df):
            Placeholder method for future implementation.
    """
    column_model = ['model_name', 'best_model', 'y_pred_cv']
    TARGET_COLUMN = 'nb_commandes'
    col_datetime = 'At Pickup time'
    FEATURE_COLUMN = 'date'
    
    def __init__(self):
        """
        Initializes the WineData with a default name 'train'.
        
        Calls the parent class (Entity) constructor with the name 'train'.
        """
        name = 'train'
        super().__init__(name)
        
    @staticmethod 
    def load_data(file_path, sep):
        """
        Loads data from a CSV file into a pandas DataFrame.

        Args:
            file_path (str): The path to the CSV file (without the '.csv' extension).

        Returns:
            pd.DataFrame: DataFrame containing the loaded data.
        """
        return pd.read_csv(file_path + '.csv', sep=sep)
    
    # @staticmethod
    # TODO use self.name or self.file_name or self.dict_file_name
    def save_data(self,data, file_path):
        """
        Saves a pandas DataFrame to a CSV file.

        Args:
            data (pd.DataFrame): The DataFrame to be saved.
            file_path (str): The path where the CSV file will be saved (without the 'train.csv' suffix).

        Returns:
            None: This method does not return any value. It saves the DataFrame to a file.
        """
        
        base_file_path = file_path + 'train.csv'
        final_file_path = base_file_path
        counter = 1

        while os.path.exists(final_file_path):
            final_file_path = f"{file_path}train_{counter}.csv"
            counter += 1

        data.to_csv(final_file_path, index=False)
