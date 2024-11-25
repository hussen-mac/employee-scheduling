from data_preparation.needed_imports import * 
from common.harcoded import Environment
from abc import ABC, abstractmethod
    

class main_Training_Entity(ABC):
    """
    Abstract base class for training models and finding the best parameters.

    This class provides methods to perform hyperparameter tuning using grid search and 
    cross-validation. It also includes functionality to train the best model and assess feature importance.

    Attributes:
        stage (str): The type of stage, set to 'training_models'.

    Methods:
        __init__():
            Initializes the main_Training_Entity with the training models stage.
        best_parameter(X, y, model, param_grid, model_name):
            Performs hyperparameter tuning using grid search and assesses feature importance.
        train(best_model, X, y):
            Trains the best model using cross-validation and returns predictions.
    """
    
    def __init__(self):
        """
        Initializes the main_Training_Entity with the training models stage.

        Args:
            None

        Returns:
            None
        """
        self.stage = Environment.training_models

    
    @abstractmethod
    def run(self, df):
        """
        Abstract method that should be implemented by subclasses to define specific feature extraction logic.

        Args:
            df (pd.DataFrame): The DataFrame to be processed.

        Returns:
            pd.DataFrame: The DataFrame after applying the feature extraction logic.
        """
        pass