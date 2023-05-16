import os

from src.models import MLConfig
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
import pickle
from dotenv import load_dotenv


load_dotenv()
save_dir = os.getenv('FILENAME')



class MLApps:
    @classmethod
    def fit(cls, X, y, config: MLConfig, process_nums):
        if config.task == "reg":
            if config.model == "Tree":
                model = DecisionTreeRegressor()
            elif config.model == "Boosting":
                model = GradientBoostingRegressor()
            elif config.model == "Linear":
                model = LinearRegression()
        else:
            if config.model == "Tree":
                model = DecisionTreeClassifier()
            elif config.model == "Boosting":
                model = GradientBoostingClassifier()
            elif config.model == "Linear":
                model = LogisticRegression()

        model.fit(X, y)

        filename = save_dir + '/' + config.name + '.sav'

        cls.unload(model, filename) #сохраняем модель в директорию

        with process_nums.get_lock():
            process_nums.value += 1

        return 0

    @classmethod
    def predict(cls, X,  config):
        filename = save_dir + '/' + config.name + '.sav'
        model = cls.load(filename)
        y_predict = model.predict(X)
        return y_predict

    @staticmethod
    def unload(model, filename: str) -> None:
        pickle.dump(model, open(filename, 'wb'))

    @staticmethod
    def load(filename: str):
        try:
            loaded_model = pickle.load(open(filename, 'rb'))
        except (OSError, IOError) as e:
            print("Oops!  That was no valid number.  Try again...")
        return loaded_model

    @classmethod
    def remove(cls, filename) -> None:
        os.remove(filename)