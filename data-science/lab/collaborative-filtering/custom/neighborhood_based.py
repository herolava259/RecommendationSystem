import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.metrics.pairwise import cosine_similarity

from scipy import sparse

class NeighborhoodBasedCFRecommender(BaseEstimator):
    def __init__(self, X_data, k_neighbor: int, similarity_function = cosine_similarity, uu_cf = True):
        self.X_data = X_data if uu_cf else X_data[:, [1, 0, 2]]
        self.sim_func = similarity_function
        self.k_neighbor = k_neighbor

        self.n_user = np.max(X_data[:, 0])
        self.n_item = np.max(X_data[:, 1])

        self.uu_cf = uu_cf
        self.mu = None
        self.X_bar_data = None
        self.X_bar = None

        self.S = None

    def add(self, new_data):
        self.X_data = np.hstack((self.X_data, new_data))

    def normalize(self):
        users = self.X_data[:, 0]

        self.X_bar_data = self.X_data.copy()

        self.mu = np.zeros((self.n_user,))

        for n in range(self.n_user):

            ids = np.where(users == n)[0].astype(np.int32)

            #item_ids = self.X_data[ids, 1]

            ratings = self.X_data[ids, 2]

            m = np.mean(ratings)


            if np.isnan(m):
                m = 0
            self.mu[n] = m
            self.X_bar_data[ids, 2] = ratings - self.mu[n]

        self.X_bar = sparse.coo_matrix((self.X_bar_data[:, 2],
                                        (self.X_bar_data[:, 0], self.X_bar_data[:, 1])),(self.n_item, self.n_user))

        self.X_bar = self.X_bar.tocsr()

    def similarity(self):
        self.S = self.sim_func(self.X_bar, self.X_bar)


    def refresh(self):
        self.normalize()
        self.similarity()

    def fit(self):
        self.refresh()


    def __predict(self, u, i, normalized: bool = True):

        ids = np.where(self.X_data[:, 1] == i)[0].astype(np.int32)

        users_rated_i = (self.X_data[ids, 0]).astype(np.int32)

        sim = self.S[u, users_rated_i]

        a = np.argsort(sim)[-self.k_neighbor:]

        nearest_s = sim[a]

        r = self.X_bar[i, users_rated_i[a]]

        if normalized:
            return (r @ nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8)

        return (r @  nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8) + self.mu[u]


    def recommend(self, u, normalized = 1):

        ids = np.where(self.X_data[:, 0] == u)

        items_rated_by_u = self.X_data[ids, 1].tolist()

        recommended_items = []

        for i in range(self.n_item):
            if i not in items_rated_by_u:
                rating  = self.__predict(u, i)
                if rating > 0:
                    recommended_items.append(i)

        return recommended_items








