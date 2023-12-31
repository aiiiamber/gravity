# -*-coding:utf-8 -*-
# @Author: xiaolizhang

import numpy as np

from model.base_model import BaseModel

from sklearn import tree
from sklearn.metrics import classification_report


class DecisionTree(BaseModel):

    def __init__(self, conf, fc, dataset):
        super().__init__(conf=conf, dataset=dataset)
        params = self._conf.model_conf.get('decision_tree', {})
        self.fc = fc
        self.criterion = params.get("criterion", "entropy")
        self.max_depth = params.get("max_depth", 4)
        self.min_samples_split = params.get("min_samples_split", 1000)
        self.x_data = self._dataset[self.fc.fc_columns]
        self.y_data = self._dataset[[self.fc.label_column]]

    def build(self):
        self._model = tree.DecisionTreeClassifier(criterion=self.criterion,
                                                  max_depth=self.max_depth,
                                                  min_samples_split=self.min_samples_split)

    def fit(self):
        self._model.fit(self.x_data, self.y_data)
        # self.print_evaluation_result()

    def predict(self, test_data):
        y_pred = self._model.predict(test_data)
        return y_pred

    def evaluate(self):
        feature_importance = sorted(zip(self.fc.fc_columns, self._model.feature_importances_),
                                    key=lambda x: x[1],
                                    reverse=True)
        print("[Info] Top5 important features >>")
        for fn, fc in feature_importance[:5]:
            if fc > 0:
                print('feature name: {fn}, feature importance: {fc:.4f}'.format(fn=fn, fc=fc))
        print("[Info] Classification report >> \n")
        y_pred = self._model.predict(self.x_data)
        print(classification_report(self.y_data, y_pred))
