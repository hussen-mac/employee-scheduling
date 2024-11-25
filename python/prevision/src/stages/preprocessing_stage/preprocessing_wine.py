import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from data_preparation.needed_imports import *
from stages.preprocessing_stage.main_preprocessing import Preprocessing 
from entities.Global_data import WineData
from common.harcoded import Environment

class PreprocessingWine(Preprocessing):
    """
    Concrete implementation of the Preprocessing class for wine data.

    This class defines specific preprocessing steps for wine data, including 
    cleaning the data and binarizing the target column. It inherits from the 
    Preprocessing class and overrides the run method to apply these preprocessing 
    steps.

    Attributes:
        stage_type (str): The type of stage, set to 'preprocessing'.
        entity (Entity): The entity representing the wine data to be processed, defaults to WineData.

    Methods:
        __init__(entity=WineData()):
            Initializes the PreprocessingWine with the provided entity.
        run(df=None):
            Applies the preprocessing steps to the provided DataFrame.
    """
    
    def __init__(self, entity=WineData()):
        """
        Initializes the PreprocessingWine with the provided entity.

        Args:
            entity (Entity): The entity representing the wine data to be processed. Defaults to WineData.

        Returns:
            None: This method does not return any value. It initializes the class with the provided entity.
        """
        self.stage_type = Environment.preprocessing
        super().__init__(entity)
        
    def run(self,df=None):
        """
        Applies the preprocessing steps to the provided DataFrame.

        This method performs the following steps:
        1. Cleans the data by removing missing values.
        2. Binarizes the target column (e.g., 'quality').

        Args:
            df (pd.DataFrame, optional): The DataFrame to be processed. Defaults to None.

        Returns:
            pd.DataFrame: The DataFrame after applying the preprocessing steps.
        """
        df = df[[WineData.col_datetime]]
        df = self.clean_data(df)
        df_6_14, df_14_23, df_23_5 = Environment.regrouper_commandes_par_date_et_tranche(df, WineData.col_datetime)
        return df_6_14, df_14_23, df_23_5