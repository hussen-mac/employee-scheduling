from data_preparation.needed_imports import *   
from common.harcoded import Environment
from entities.entity import Entity
from entities.Global_data import WineData
import pickle



class ModelDefinitions(Entity):
    """
    Defines various machine learning models and their hyperparameter grids.

    This class provides a dictionary of machine learning models and their corresponding
    hyperparameter grids for model tuning. It also includes methods for saving and loading
    models and their predictions.

    Attributes:
        RANDOM_SEED (int): Seed for random number generators.
        TARGET_COLUMN (str): Target column name in the dataset.
        models_dict (dict): Dictionary mapping model names to model instances and their versions.
        param_grids_dict (dict): Dictionary mapping model names to their hyperparameter grids.

    Methods:
        __init__(self):
            Initializes the ModelDefinitions with default settings.
        get_model_info(self, model_name):
            Retrieves the model instance, version, and hyperparameter grid for the given model name.
        save_best_model_and_predictions(self, results):
            Saves the best model and predictions based on the results DataFrame.
        load_data(self, model_name):
            Loads a saved model and its predictions from disk.
        save_data(model, output_path):
            Saves a model to disk.
    """
    
    RANDOM_SEED = Environment.RANDOM_SEED
    TARGET_COLUMN = WineData.TARGET_COLUMN

    models_dict = {
        "prophet": (Prophet(), "1.0"),
    }

    param_grids_dict = {
        "prophet": None  
    }
    
    def __init__(self):
        """
        Initializes the ModelDefinitions with default settings.
        
        Calls the parent class (Entity) constructor with an empty name.
        """
        name = ''
        super().__init__(name)
         
         
    def get_model_info(self, model_name):
        """
        Retrieves the model instance, version, and hyperparameter grid for the given model name.

        Args:
            model_name (str): The name of the model.

        Returns:
            tuple: A tuple containing the model instance, version string, and hyperparameter grid dictionary.
                - model (object): The model instance.
                - version (str): The version of the model.
                - param_grid (dict): The hyperparameter grid for the model.
        """
        model, version = self.models_dict.get(model_name, (None, None))
        param_grid = self.param_grids_dict.get(model_name)
        return model, version, param_grid 
    
    def get_models(self ,row):
        
        model_name = row['model_name']
        y_pred_cv = row['y_pred_cv']
        model_path = f"{self.dict_save[Environment.training_models]}/{model_name}.pkl"
        pred_path = f"{self.dict_save[Environment.prediction_train]}/{model_name}.csv"
        
        return model_name, y_pred_cv, model_path, pred_path
    
    @staticmethod
    def save_csv(pred_path, y_pred_cv):
        y_pred_cv = pd.DataFrame(y_pred_cv, columns=[WineData.TARGET_COLUMN])
        y_pred_cv.to_csv(pred_path, index=False)
    
    
    def save_best_model_and_predictions(self, results):
        """
        Saves the best model and its predictions based on the results DataFrame.

        Args:
            results (pd.DataFrame): DataFrame containing model names, best models, and predictions.
                Expected columns: ['model_name', 'best_model', 'y_pred_cv'].

        Returns:
            None: This method does not return any value. It saves models and predictions to disk.
        """
        for _, row in results.iterrows():
            model_name, best_model, y_pred_cv, model_path, pred_path = self.get_models(row)
            self.save_data(best_model, model_path)
            self.save_csv(pred_path, y_pred_cv)
    
    def load_data(self, model_name):
        """
        Loads a saved model and its predictions from disk.

        Args:
            model_name (str): The name of the model to load.

        Returns:
            tuple: A tuple containing the loaded model and its predictions.
                - model (object or None): The loaded model, or None if the model file does not exist.
                - predictions (np.ndarray or None): The predictions from the CSV file, or None if the file does not exist.

        Raises:
            FileNotFoundError: If the model or prediction files do not exist.
        """
        model_path = f"{Environment.training_models_path}/{model_name}.pkl"
        predictions_path = f"{Environment.prediction_train_path}/{model_name}.csv"
        if not os.path.exists(model_path) or not os.path.exists(predictions_path):
            return None, None
        
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        
        predictions = pd.read_csv(predictions_path)
        return model, predictions[WineData.TARGET_COLUMN].values
    
    @staticmethod
    def save_data(model, output_path):
        """
        Saves a model to disk.

        Args:
            model (object): The model to be saved.
            output_path (str): The file path where the model will be saved.

        Returns:
            None: This method does not return any value. It saves the model to disk.
        """
        with open(output_path, 'wb') as file:
            pickle.dump(model, file)