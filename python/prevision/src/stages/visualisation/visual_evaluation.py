from data_preparation.needed_imports import *
from common.harcoded import Environment
from stages.visualisation.main_visualisation import MainVisualisation


class ModelVisualisation(MainVisualisation):
    """
    A class for visualizing model performance, including actual vs. predicted curves for forecasting models.
    This class extends `MainVisualisation`.
    """
    
    def __init__(self, entity, model_definitions):
        """
        Initializes the ModelVisualisation instance.

        Args:
            entity (Entity): The entity used to load data.
            model_definitions (ModelDefinitions): The definitions and saved models for visualization.
        """
        self.entity = entity
        self.stage_type = Environment.visualisation
        self.model_definitions = model_definitions

    def run(self, df=None):
        """
        Loads data, processes each model, and visualizes their performance.

        Args:
            df (pd.DataFrame, optional): DataFrame to be used. If None, data is loaded from the entity.

        Returns:
            None
        """
        df = self.entity.load_by_stage(Environment.preprocessing)
        y_actual = df[self.model_definitions.TARGET_COLUMN]
        
        for model_name in self.model_definitions.models_dict:
            print(f"Processing model: {model_name}")
            model, y_pred = self.model_definitions.load_data(model_name)
            
            if model_name == "prophet":
                self.plot_actual_vs_predicted(y_actual, y_pred)

    def plot_actual_vs_predicted(self, y_actual, y_pred):
        """
        Visualizes actual vs predicted values for a forecasting model.

        Args:
            y_actual (pd.Series or np.ndarray): The actual target values.
            y_pred (pd.Series or np.ndarray): The predicted target values.

        Returns:
            None: Displays the plot.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(y_actual, label="Actual", color="blue", alpha=0.7, linewidth=2)
        plt.plot(y_pred, label="Predicted", color="orange", linestyle="--", alpha=0.8, linewidth=2)
        plt.title("Actual vs Predicted")
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()