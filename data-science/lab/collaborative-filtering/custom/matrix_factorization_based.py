import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class MatrixFactorizationBasedRecommender:
    def __init__(self, Y_data, K, _lambda = 0.1, x_init = None, w_init = None,
                 lr = 0.5, max_iter = 1000, print_every = 100, user_based: bool = True):

        self.Y_raw_data = Y_data
        self.K = K

        self._lambda = _lambda

        self.lr = lr

        self.max_iter = max_iter

        self.user_based = user_based

        self.n_users = int(np.max(Y_data[:, 0])) + 1
        self.n_items = int(np.max(Y_data[:, 1])) + 1

        self.n_ratings = Y_data.shape[0]

        if x_init is None:
            self.X = np.random.randn(self.n_items, K)
        else:
            self.X = x_init

        if w_init is None:
            self.W = np.random.randn(self.n_users, self.K)
        else:
            self.W = w_init
        self.Y_data_n = self.Y_raw_data.copy()
        self.mu = None

        self.print_every = print_every

    def normalize_Y(self):

        if self.user_based:
            pivot_col = 0
            feature_col = 1
            n_objects = self.n_users
        else:
            pivot_col = 1
            feature_col = 0
            n_objects = self.n_items

        users = self.Y_raw_data[:, pivot_col]
        self.mu = np.zeros((n_objects,))

        for n in range(n_objects):
            ids = np.where(users == n)[0].astype(np.int32)

            item_ids = self.Y_data_n[ids, feature_col]

            ratings = self.Y_data_n[ids, 2]

            m = np.mean(ratings)

            if np.isnan(m):
                m = 0

            self.Y_data_n[ids, feature_col] = ratings - self.mu[n]

    def loss(self) -> float:
        L = 0

        for i in range(self.n_ratings):
            n, m, rate = int(self.Y_data_n[i, 0]), int(self.Y_data_n[i, 1]), self.Y_data_n[i, 2]

            L += 0.5 * (rate - self.X[m, L].dot(self.W[:, n])) ** 2

        L /= self.n_ratings
        L += 0.5 * self._lambda * (np.linalg.norm(self.X, "fro") + np.linalg.norm(self.W, "fro"))

        return L

    def get_items_rated_by_user(self, user_id) -> tuple:

        ids = np.where(self.Y_data_n[:, 0] == user_id)[0]
        item_ids = self.Y_data_n[ids, 1].astype(np.int32)
        ratings = self.Y_data_n[ids, 2]

        return item_ids, ratings

    def get_users_who_rate_item(self, item_id):

        ids = np.where(self.Y_data_n[:, 1] == item_id)[0]

        user_ids = self.Y_data_n[ids, 0].astype(np.int32)

        ratings = self.Y_data_n[ids, 2]

        return user_ids, ratings

    def update_X(self):

        for m in range(self.n_items):
            user_ids, ratings = self.get_users_who_rate_item(m)

            W_m = self.W[:, user_ids]

            grad_xm = -(ratings - self.X[m, :] @ W_m) @ W_m.T / self.n_ratings + self._lambda * self.X[m, :]

            self.X[m, :] -= self.lr * grad_xm.reshape((self.K, ))

    def update_W(self):

        for n in range(self.n_users):

            item_ids, ratings = self.get_items_rated_by_user(n)

            X_n = self.X[item_ids, :]

            grad_wn = -X_n.T @ (ratings - X_n @ self.W[:, n]) / self.n_ratings + self._lambda * self.W[:, n]

            self.W[:, n] -= self.lr * grad_wn.reshape((self.K, ))

    def fit(self):

        self.normalize_Y()

        for it in range(self.max_iter):
            self.update_X()
            self.update_W()

            if (it+1) % self.print_every == 0:
                rmse_train = self.evaluate_RMSE(self.Y_raw_data)


    def predict(self, u, i):

        u = int(u)
        i = int(i)

        if self.user_based:
            bias = self.mu[u]
        else:
            bias = self.mu[i]

        pred = self.X[i,:] @ self.W[:, u] + bias

        if pred < 0:
            return 0
        if pred > 5:
            return 5

        return pred

    def predict_for_user(self, user_id):

        ids = np.where(self.Y_data_n[:, 0] == user_id)[0]

        items_rated_by_u = self.Y_data_n[ids, 1].tolist()

        pred_y = self.X.dot(self.W[:, user_id]) + self.mu[user_id]

        predicted_ratings = []

        for i in range(self.n_items):
            if i not in items_rated_by_u:
                predicted_ratings.append(self.predict(i, pred_y[i]))

        return predicted_ratings

    def evaluate_RMSE(self, rate_test):

        n_tests = rate_test.shape[0]

        SE = 0

        for n in range(n_tests):

            pred = self.predict(rate_test[n, 0], rate_test[n, 1])

            SE += (pred - rate_test[n, 2]) ** 2


        RMSE = np.sqrt(SE / n_tests)

        return RMSE




