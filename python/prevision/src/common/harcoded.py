import os
import pandas as pd

class Environment:
    """
    A class to manage paths and constants used throughout the project.

    This class contains hardcoded paths and stage variables to manage different stages of the data processing pipeline,
    such as raw data, preprocessing, feature engineering, model training, etc. It also includes a random seed for reproducibility.

    Attributes:
        RANDOM_SEED (int): A constant seed value for ensuring reproducibility across runs.
        raw_data (str): The stage name for raw data.
        preprocessing (str): The stage name for preprocessing.
        postprocessing (str): The stage name for postprocessing.
        feature_eng (str): The stage name for feature engineering.
        training_models (str): The stage name for model training.
        prediction_train (str): The stage name for training predictions.
        visualisation (str): The stage name for visualization.
        project_path (str): The base path for the project directory.
        raw_data_path (str): The full path for raw data.
        preprocessing_path (str): The full path for preprocessing data.
        postprocessing_path (str): The full path for postprocessing data.
        feature_eng_path (str): The full path for feature engineering data.
        training_models_path (str): The full path for model training data.
        prediction_train_path (str): The full path for prediction training data.
        visualisation_path (str): The full path for visualization data.
    """
    
    # Hardcoded var for all
    RANDOM_SEED = 3
    
    # Stage variables
    raw_data = 'raw_data'
    preprocessing = 'preprocessing'
    postprocessing = 'postprocessing'
    feature_eng = 'feature_eng'
    training_models = 'training_models'
    prediction_train = 'prediction_train'
    visualisation = 'visualisation'
    
    # Input paths by stage
    
    project_path = os.path.abspath(os.path.join(os.getcwd(), '../..'))
    raw_data_path = f'{project_path}/{raw_data}'
    preprocessing_path = f'{project_path}/{preprocessing}'
    postprocessing_path = f'{project_path}/{postprocessing}'
    feature_eng_path  = f'{project_path}/{feature_eng}'
    training_models_path = f'{project_path}/{training_models}'
    prediction_train_path = f'{project_path}/{prediction_train}'
    visualisation_path = f'{project_path}/{visualisation}'
    
    
    def regrouper_commandes_par_date_et_tranche(data, col_datetime):
        """
        Regroupe et compte les commandes par date et tranche horaire : [6h-14h[, [14h-23h[, [23h-6h[.

        Parameters:
        -----------
        data : pd.DataFrame
            Le DataFrame contenant les données des commandes.
        col_datetime : str
            Nom de la colonne contenant les dates et heures des commandes.

        Returns:
        --------
        tuple
            Trois DataFrames correspondant aux tranches horaires '6h-14h', '14h-23h', '23h-6h'.
        """
        data[col_datetime] = pd.to_datetime(data[col_datetime])
        data['date'] = data[col_datetime].dt.date

        data['tranche_horaire'] = pd.cut(
            data[col_datetime].dt.hour,
            bins=[0, 5, 14, 23, 24], 
            labels=['23h-6h', '6h-14h', '14h-23h', '23h-6h'],
            right=False,
            ordered=False  
        )

        grouped = data.groupby(['date', 'tranche_horaire']).size().reset_index(name='nb_commandes')

        df_6_14 = grouped[grouped['tranche_horaire'] == '6h-14h']
        df_14_23 = grouped[grouped['tranche_horaire'] == '14h-23h']
        df_23_5 = grouped[grouped['tranche_horaire'] == '23h-6h']

        return df_6_14, df_14_23, df_23_5

