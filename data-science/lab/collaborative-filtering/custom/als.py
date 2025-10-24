import numpy as np

class AlternativeLeastSquareTrainer:
    def __init__(self, n_user: int, n_items: int, k = 100, _lambda = 1e-7, num_loop=1000, accepted_loss = 1e-7, log_circle= 10):
        self.k = k
        self._lambda = _lambda

        self.n_user = n_user
        self.n_item = n_items

        self.u_latent = np.zeros((self.n_user, self.k))

        self.i_latent = np.zeros((self.n_item, self.k))

        self.num_loop = num_loop

        self.accepted_err = accepted_loss

        self.log_circle = log_circle

    def loss(self, ratings: np.ndarray):
        l = 0.0

        num_rating = ratings.shape[0]

        for u in range(self.n_user):

            u_row_ids = np.where(ratings[:, 0] == u).astype(np.int32)
            i_ids = ratings[u_row_ids, 1]
            r = ratings[u_row_ids, 2]

            l += np.sum(np.square(r-self.i_latent[i_ids] @ self.u_latent[u]))
        l /= num_rating

        l += self._lambda * (np.sum(self.u_latent ** 2) + np.sum(self.i_latent ** 2))

        return l

    def train(self, ratings: np.ndarray):
        def rating_of_user(u_ids: int):

            user_row_ids = np.where(ratings[:, 0] == u_ids).astype(np.int32)

            return user_row_ids, ratings[user_row_ids]

        def rating_of_item(item_ids: int):

            item_row_ids = np.where(ratings[:, 1] == item_ids).astype(np.int32)

            return item_row_ids, ratings[item_row_ids]


        for loop in range(self.num_loop):

            for u in range(self.n_user):
                u_row_ids, rows= rating_of_user(u)

                i_ids = rows[:, 1]
                i_latent = rows[i_ids]
                r =  rows[:, 2]

                len_i = len(i_ids)

                reg_diag = self._lambda * np.diag(np.zeros((len_i, len_i)))

                self.u_latent[u] = np.linalg.inv(i_latent.T @ i_latent + reg_diag) @ np.dot(i_latent.T, r)

            for i in range(self.n_item):
                u_row_ids, rows = rating_of_item(i)

                u_ids = rows[:, 0]
                u_latent = rows[u_ids]
                r = rows[:, 2]

                len_u = len(u_ids)

                reg_diag = self._lambda * np.diag(np.zeros((len_u, len_u)))

                self.i_latent[i] = np.linalg.inv(u_latent.T @ i_latent + reg_diag) @ np.dot(u_latent.T, r)

            l = self.loss(ratings)

            if (loop + 1) % self.log_circle:
                print(f"Loop: {loop} - Error(loss): {l}")

            if l < self.accepted_err:
                break
