from stages.training_models.main_training import main_Training_Entity
from entities.Global_data import WineData    
from data_preparation.needed_imports import *
from common.harcoded import Environment

class Training_Entity(main_Training_Entity):
    def __init__(self, model_definitions):
        """
        Initializes the Training_Entity with model definitions and sets up the training stage.
        """
        super().__init__()
        self.stage_type = Environment.training_models
        self.model_definitions = model_definitions

    def process_dataset(self, df):
        """
        Splits the dataset into the required format for Prophet.

        Args:
            df (pd.DataFrame): Dataframe containing date/time and target variable.

        Returns:
            pd.DataFrame: Processed dataframe with 'ds' and 'y' columns for Prophet.
        """
        df = df.rename(columns={WineData.FEATURE_COLUMN: "ds", WineData.TARGET_COLUMN: "y"})
        df["ds"] = pd.to_datetime(df["ds"]) 
        return df

    def split_data(self, df, train_size=0.8):
        """
        Splits the data into training and testing sets.

        Args:
            df (pd.DataFrame): The dataset to split.
            train_size (float): Proportion of the dataset to use for training.

        Returns:
            tuple: Training and testing datasets.
        """
        train_len = int(len(df) * train_size)
        df_train = df[:train_len]
        df_test = df[train_len:]
        return df_train, df_test

    def evaluate_model(self, df_test, forecast):
        """
        Evaluates the Prophet model using RMSE and MAE.

        Args:
            df_test (pd.DataFrame): Testing dataset with actual values.
            forecast (pd.DataFrame): Forecast DataFrame with predicted values.

        Returns:
            dict: Dictionary containing RMSE and MAE scores.
        """
        df_forecast = forecast[['ds', 'yhat']].merge(df_test, on='ds', how='inner')
        rmse = sqrt(mean_squared_error(df_forecast['y'], df_forecast['yhat']))
        mae = mean_absolute_error(df_forecast['y'], df_forecast['yhat'])
        return {'rmse': rmse, 'mae': mae}

    def train_prophet(self, df_train):
        """
        Trains a Prophet model on the provided data.

        Args:
            df_train (pd.DataFrame): Dataframe with 'ds' (datetime) and 'y' (target variable).

        Returns:
            Prophet: A trained Prophet model.
        """
        model = Prophet()
        model.fit(df_train)
        return model

    def make_forecast(self, model, periods, freq):
        """
        Makes a forecast using the trained Prophet model.

        Args:
            model (Prophet): The trained Prophet model.
            periods (int): Number of periods to forecast into the future.
            freq (str): Frequency of the predictions (e.g., 'D' for daily).

        Returns:
            pd.DataFrame: DataFrame containing the forecast.
        """
        future = model.make_future_dataframe(periods=periods, freq=freq)
        forecast = model.predict(future)
        return forecast

    def run(self, df):
        """
        Executes the training, evaluation, and forecasting process.

        Args:
            df (pd.DataFrame): The input dataset.

        Returns:
            dict: Dictionary containing the forecast and evaluation metrics.
        """
        # Prepare the dataset
        df = self.process_dataset(df)

        # Split data into train/test
        df_train, df_test = self.split_data(df)

        # Train the Prophet model
        prophet_model = self.train_prophet(df_train)

        # Forecast future values (6 days after the last date)
        forecast = self.make_forecast(prophet_model, periods=13, freq='D')

        # Evaluate model performance
        metrics = self.evaluate_model(df_test, forecast)
        print(metrics)

        # Save the forecast
        file_path = f"{self.model_definitions.dict_save[Environment.prediction_train]}/"
        forecast_path = os.path.join(file_path, "forecast.csv")
        counter = 1

        while os.path.exists(forecast_path):
            forecast_path = os.path.join(file_path, f"forecast_{counter}.csv")
            counter += 1

        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(forecast_path, index=False)

        return forecast