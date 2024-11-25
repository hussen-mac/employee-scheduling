import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.pipeline import Pipeline
from common.harcoded import Environment

class RWPipeLine(Pipeline):
    """
    Class representing a data processing pipeline for incremental runs in a real-world use case.

    Attributes:
        - entity (Entity): An instance of the Entity class representing the data entity to be processed.
        - read (list): A list of boolean values indicating whether to load data from the previous stage.
        - init_pip (bool): A boolean value indicating whether to initialize the pipeline.
        - save (list): A list of boolean values indicating whether to save data after each stage.
        **args: Additional keyword arguments to pass to the base Pipeline class.
 
    Methods:
        - __init__(self, entity, read=[], init_pip=False, save=[], **args): Constructor method to initialize the RWPipeLine instance.
        - execute(self, df=None): Method to execute the pipeline on a DataFrame.
 
    Example:
        # Create an Entity instance representing the data entity to be processed
        entity = SomeEntity()
        # Create a RWPipeLine instance with stages
        stage1 = SomeDataProcessingStage()
        stage2 = AnotherDataProcessingStage()
        rw_pipeline = RWPipeLine(entity, stages=[stage1, stage2], read=[True, False], init_pip=True, save=[False, True])
        # Execute the pipeline on a DataFrame
        result_df = rw_pipeline.execute(input_df)
    """
    list_df = None
    def __init__(self, entity, stages=[], read=[], init_pip=False, save=[], **args):
        """
        Constructor method to initialize the RWPipeLine instance.
 
        Args:
            - entity (Entity): An instance of the Entity class representing the data entity to be processed.
            - read (list, optional): A list of boolean values indicating whether to load data from the previous stage. Defaults to an empty list.
            - init_pip (bool, optional): A boolean value indicating whether to initialize the pipeline. Defaults to False.
            - save (list, optional): A list of boolean values indicating whether to save data after each stage. Defaults to an empty list.
            - **args: Additional keyword arguments to pass to the base Pipeline class.
        """
        super().__init__(stages)
        self.entity = entity
        self.init_pip = init_pip
        self.read = read if read else [False for _ in range(len(stages))]
        self.save = save if save else [True for _ in range(len(stages))]

    def execute(self, df=None):
        """
        Method to execute the pipeline on a DataFrame.
 
        Args:
            - df (DataFrame, optional): The input DataFrame to be processed. Defaults to None.
 
        Returns:
            - DataFrame: The output DataFrame after executing all stages in the pipeline.
        """
        for stage, read, save in zip(self.stages, self.read, self.save):
            print(stage.stage_type + '...')
            if read:
                if stage.stage_type == Environment.training_models :
                    df_6_14, df_14_23, df_23_5 = self.entity.load_by_stage(stage.stage_type, ',')
                    self.list_df = [df_6_14, df_14_23, df_23_5]
                else :
                    df = self.entity.load_by_stage(stage.stage_type, ';')

            if stage.stage_type == Environment.preprocessing:
                df_6_14, df_14_23, df_23_5 = stage.run(df)
                if save: 
                    self.entity.save_by_stage(df_6_14, stage.stage_type)
                    self.entity.save_by_stage(df_14_23, stage.stage_type)
                    self.entity.save_by_stage(df_23_5, stage.stage_type)
                    print(f'Finished saving after stage {stage.stage_type}!')
                    return df_6_14, df_14_23, df_23_5
                
            elif stage.stage_type == Environment.training_models:
                for df in [df_6_14, df_14_23, df_23_5]:
                    df = stage.run(df)
                    self.entity.save_by_stage(df, stage.stage_type)
                
            else :
                df = stage.run(df) 
                if save: 
                    self.entity.save_by_stage(df, stage.stage_type)
                    print(f'Finished saving after stage {stage.stage_type}!')
                    return df