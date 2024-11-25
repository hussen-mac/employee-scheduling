import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.write_read_pipeline import RWPipeLine
from stages.preprocessing_stage.preprocessing_wine import PreprocessingWine 
from entities.Global_data import WineData


class FeatureStore: 
    """
    A class to manage and execute feature extraction processes.

    This class is responsible for running the feature extraction pipeline using the RWPipeLine class. 
    It handles the creation and execution of the pipeline stages to obtain the feature DataFrame.

    Attributes:
        features (dict): A dictionary to store features. Currently not used.

    Methods:
        run_feature_extraction():
            Executes the feature extraction pipeline and returns the resulting DataFrame.
    """
    
    def __init__(self):
        """
        Initializes the FeatureStore class.

        Sets up the `features` attribute as an empty dictionary. This attribute is reserved for future use
        to store features if needed.
        """
        self.features = {}
        
    
    def run_feature_extraction(self):
        """
        Executes the feature extraction pipeline.

        Creates an instance of the RWPipeLine class with specified stages and entities, then executes the pipeline.
        The method reads input data, processes it through the defined stages, and returns the resulting DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the extracted features after processing through the pipeline.
        """
        df_feature = RWPipeLine(entity= WineData(), stages=[PreprocessingWine()], read=[True], save=[True]).execute()
        return df_feature


if __name__ == "__main__":

    feature_store = FeatureStore()
    df_feature = feature_store.run_feature_extraction()
    
