from data_preparation.needed_imports import *
from common.harcoded import Environment 
from abc import ABC

class Preprocessing(ABC):
    """
    Abstract base class for preprocessing data.

    This class provides a framework for preprocessing data by defining methods for 
    cleaning data and binarizing the target column. Concrete implementations of this
    class should define specific preprocessing logic.

    Attributes:
        entity (Entity): The entity representing the data to be processed.
        stage (str): The stage of preprocessing, set to 'preprocessing'.

    Methods:
        __init__(entity):
            Initializes the preprocessing with the provided entity.
        clean_data(df):
            Removes missing values from the DataFrame.
        binarize_target(target_column, df):
            Converts target column values to binary (1 or 0).
        run(df):
            Abstract method that should be implemented by subclasses to define specific preprocessing logic.
    """
    def __init__(self, entity):
        """
        Initializes the Preprocessing with the provided entity.

        Args:
            entity (Entity): The entity representing the data to be processed.

        Returns:
            None: This method does not return any value. It initializes the class with the provided entity.
        """
        self.entity = entity
        self.stage = Environment.preprocessing

    @staticmethod
    def clean_data(df):
        """
        Removes missing values from the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to be cleaned.

        Returns:
            pd.DataFrame: The DataFrame with missing values removed.
        """
        df.dropna(inplace=True)
        return df


    
    @staticmethod
    def run(df=None):
        """
        Abstract method that should be implemented by subclasses to define specific preprocessing logic.

        Args:
            df (pd.DataFrame, optional): The DataFrame to be processed. Default is None.

        Returns:
            pd.DataFrame: The DataFrame after applying the preprocessing logic.
        """
        pass