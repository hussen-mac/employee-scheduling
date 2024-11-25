from data_preparation.needed_imports import *


class MainVisualisation:
    """
    A class for visualizing model performance using ROC curves and confusion matrices.

    This class provides static methods to generate and display ROC curves and confusion matrices for model evaluation.

    Methods:
        plot_roc(models, ax=None):
            Plots the Receiver Operating Characteristic (ROC) curve for the given models.
        plot_confusion_matrix(cm, classes, reverse=True, ax=None, fig=None, normalize=False, title='Confusion matrix', colorbar=True):
            Plots a confusion matrix with optional normalization and color bar.
        visualize(y_test, y_pred, model=None, show_roc=False, show_cm=True):
            Generates and displays ROC curves and/or confusion matrices based on the provided parameters.
    """
    @staticmethod
    def plot_roc():
        """
        Plots the Receiver Operating Characteristic (ROC) curve for the given models.

        Args:
            models (list of dict): A list of dictionaries where each dictionary contains:
                - 'name': Name of the model.
                - 'fpr': False positive rates.
                - 'tpr': True positive rates.
                - 'roc_auc': Area Under the Curve (AUC) score.
            ax (matplotlib.axes.Axes, optional): The axes on which to plot the ROC curve. If None, a new figure and axes are created.

        Returns:
            None
        """
        pass

    @staticmethod
    def plot_confusion_matrix():
        """
        Plots a confusion matrix with optional normalization and color bar.

        Args:
            cm (np.ndarray): Confusion matrix to plot.
            classes (list of str): List of class names.
            reverse (bool, optional): If True, reverses the confusion matrix and class labels. Defaults to True.
            ax (matplotlib.axes.Axes, optional): The axes on which to plot the confusion matrix. If None, a new figure and axes are created.
            fig (matplotlib.figure.Figure, optional): The figure on which to plot the confusion matrix. If None, a new figure is created.
            normalize (bool, optional): If True, normalizes the confusion matrix. Defaults to False.
            title (str, optional): Title for the plot. Defaults to 'Confusion matrix'.
            colorbar (bool, optional): If True, displays the color bar. Defaults to True.

        Returns:
            None
        """
        pass

    @staticmethod
    def visualize():
        """
        Generates and displays ROC curves and/or confusion matrices based on the provided parameters.

        Args:
            y_test (np.ndarray or pd.Series): True labels.
            y_pred (np.ndarray or pd.Series): Predicted labels.
            model (list of dict, optional): List of model dictionaries with ROC curve data for plotting. Defaults to None.
            show_roc (bool, optional): If True, plots the ROC curve. Defaults to False.
            show_cm (bool, optional): If True, plots the confusion matrix. Defaults to True.

        Returns:
            None
        """
        pass