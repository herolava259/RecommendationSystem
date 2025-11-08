import numpy as np
from abc import ABC, abstractmethod
from typing import Self, Any, overload


class BaseLayer(ABC):

    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    @abstractmethod
    def backward(self, dL_dA_nxt: np.ndarray) -> np.ndarray:
        raise NotImplementedError()


class BaseFunction(ABC):

    @abstractmethod
    def call(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    @property
    @abstractmethod
    def gradient(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def calculate_gradient(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()


class TrainingStrategy(ABC):
    pass


class BaseModel(ABC, BaseLayer):

    @abstractmethod
    def calculate_loss(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    @abstractmethod
    def fit(self,x: np.ndarray, y: np.ndarray) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def predict(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    @overload
    @abstractmethod
    def fit(self, x_train: np.ndarray, y_train: np.ndarray,
                    x_val: np.ndarray, y_val: np.ndarray,
                ) -> Any:
        raise NotImplementedError()
    @property
    @abstractmethod
    def loss(self) -> Any:
        raise NotImplementedError()

class BaseTrainer(ABC):
    @abstractmethod
    def setup_training(self, training_strategy: TrainingStrategy | str,
                            num_epochs: int, batch_size) -> Any:

        raise NotImplementedError()

    @abstractmethod
    def train(self, x_train, y_train, x_val = None, y_val = None) -> Any:
        pass



