from common.harcoded import Environment
from data_preparation.needed_imports import * 
from abc import ABC, abstractmethod


class Entity(ABC):
    """
    Abstract base class for handling data loading and saving across different stages.

    This class provides a framework for managing data at various stages of the data processing pipeline.
    It defines methods for loading and saving data by stage and provides a structure for handling different
    types of entities in the pipeline.

    Attributes:
        name (str): The name of the entity. This is used to construct file paths for loading and saving data.
        dict_load (dict): A mapping of stages to their corresponding input paths.
        dict_save (dict): A mapping of stages to their corresponding output paths.

    Methods:
        __init__(self, name=None):
            Initializes the Entity with an optional name.
        load_data(self, df):
            Abstract method for loading data. Must be implemented by subclasses.
        save_data(self, data, file_path):
            Abstract method for saving data. Must be implemented by subclasses.
        load_by_stage(self, stage):
            Loads data based on the specified stage.
        save_by_stage(self, data, stage):
            Saves data based on the specified stage.
    """
    name = ''

    dict_load = {
        Environment.raw_data :Environment.raw_data_path,
        Environment.preprocessing:Environment.raw_data_path,
        Environment.postprocessing:Environment.preprocessing_path,
        # Environment.feature_eng:Environment.preprocessing_path,
        Environment.training_models:Environment.preprocessing_path,
        Environment.prediction_train:Environment.training_models,
        Environment.visualisation:Environment.training_models_path
    }
    dict_save = {

        Environment.preprocessing:Environment.preprocessing_path,
        Environment.feature_eng:Environment.feature_eng_path,
        Environment.postprocessing:Environment.postprocessing,
        Environment.training_models:Environment.training_models_path,
        Environment.prediction_train:Environment.prediction_train_path, 
        Environment.visualisation:Environment.visualisation_path
    }

    def __init__(self,name=None):
        """
        Initializes the Entity with an optional name.

        Args:
            name (str, optional): The name of the entity. Default is None.
        """
        self.name = name 

    @abstractmethod
    def load_data(self,df):
        """
        Abstract method for loading data.

        This method must be implemented by subclasses to define how data is loaded.

        Args:
            df (str): The path to the data file.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass
    
    @abstractmethod
    def save_data(self, data, file_path):
        """
        Abstract method for saving data.

        This method must be implemented by subclasses to define how data is saved.

        Args:
            data: The data to be saved.
            file_path (str): The path where the data will be saved.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass
    
    def load_by_stage(self, stage, sep):
        """
        Charge les données pour un stage spécifique.

        Si le stage est `Environment.training_models`, charge tous les fichiers du répertoire et
        les affecte à des DataFrames distincts. Sinon, charge un seul fichier.

        Args:
            stage (str): Le stage pour lequel les données doivent être chargées.

        Returns:
            pd.DataFrame ou tuple: Un DataFrame unique ou un tuple de DataFrames pour `training_models`.

        Raises:
            FileNotFoundError: Si aucun fichier n'est trouvé dans le répertoire.
        """
        input_path = self.dict_load[stage]

        if stage == Environment.training_models:
            dataframes = {}
            for file_name in os.listdir(input_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(input_path, file_name)
                    df = self.load_data(file_path.replace('.csv', ''),sep)
                    key = file_name.replace('.csv', '') 
                    dataframes[key] = df

            if not dataframes:
                raise FileNotFoundError(f"Aucun fichier CSV trouvé dans le répertoire : {input_path}")
            return dataframes.get('train'), dataframes.get('train_1'), dataframes.get('train_2')

        else:
            file_path = os.path.join(input_path, self.name + '.csv')
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Fichier non trouvé : {file_path}")
            return self.load_data(file_path.replace('.csv', ''), sep)
            
    def save_by_stage(self, data, stage):
        """
        Saves data based on the specified stage.

        Constructs the file path using the stage and calls the `save_data` method.

        Args:
            data: The data to be saved.
            stage (str): The stage for which data is to be saved.

        Raises:
            KeyError: If the stage is not found in the `dict_save` dictionary.
        """
        output_path = self.dict_save[stage] + '/'
        self.save_data(data, output_path)
