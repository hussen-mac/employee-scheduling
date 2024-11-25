import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.Global_data import WineData
from pipeline.write_read_pipeline import RWPipeLine
from entities.models.model_definitions import ModelDefinitions
from stages.training_models.training import Training_Entity
from common.harcoded import Environment
from stages.visualisation.visual_evaluation import ModelVisualisation

class TrainingMultipleModels():
    """
    A class to manage and execute the training and visualization of multiple machine learning models.

    This class handles the process of training multiple models using the specified pipeline stages and
    visualizing the results. It interacts with the RWPipeLine class to execute the training and 
    visualization stages on the provided data.

    Methods:
        main():
            Executes the training and visualization pipeline for multiple models.
    """

    @staticmethod
    def main():
        """
        Executes the training and visualization pipeline for multiple models.

        This method performs the following steps:
        1. Loads the features for model training from the specified stage.
        2. Runs the training pipeline using the `RWPipeLine` class with the specified model.
        3. Runs the visualization pipeline using the `RWPipeLine` class to visualize the results.

        Returns:
            None: This method does not return any value. It executes the pipeline stages and handles the model training and visualization.
        """
        entity = WineData()
        model = ModelDefinitions()
        # RWPipeLine(entity=entity, stages=[Training_Entity(model),
        #                                   ModelVisualisation(entity, model)],
        #            read=[True,False],
        #            save=[True,False]).execute()
        RWPipeLine(entity=entity, stages=[Training_Entity(model)],
                   read=[True],
                   save=[True]).execute()
        

if __name__ == "__main__":

    training_models = TrainingMultipleModels()
    df_model_1 = training_models.main()