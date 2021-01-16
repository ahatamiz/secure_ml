import numpy as np
import sklearn
import copy

# reference https://arxiv.org/abs/1708.06131


class Attack_sklearn:
    def __init__(self, clf, X_minus_1,
                 dmax, max_iter,
                 gamma, lam, t, h,
                 distance="L1", kde_type="L1"):
        """
        create an adversarial example against sklearn objects

        Attributes:
            clf (sklearn) : sklearn classifier
            X_minus_1 (numpy.array) : datasets that contains
                                    only the class you want to misclasssify
            dmax (float) : max distance between the adversarial example
                           and initial one
            max_iter (int) : maxium number of iterations
            gamma (float) :
            lam (float) :
            t (float) : step_size
            h (float) :
            distance (str) : type of distance such as L2 or L1
            kde_type (str) :

        Methods:

        """

        self.clf = clf
        self.X_minus_1 = X_minus_1
        self.dmax = dmax
        self.max_iter = max_iter
        self.gamma = gamma
        self.lam = lam
        self.t = t
        self.h = h
        self.kde_type = kde_type

        self.n_minus_1 = X_minus_1.shape[0]

        self.delta_g = None
        self.distance = None

        target_type = type(clf)
        if target_type == sklearn.svm._classes.SVC:
            def kernel(xm): return np.exp(-self.gamma *
                                          ((xm - self.clf.support_vectors_)
                                           ** 2))
            self.delta_g = lambda xm:\
                self.clf.dual_coef_.dot((-2 * self.gamma)
                                        * kernel(xm)
                                        * (xm - self.clf.support_vectors_))

        if distance == "L1":
            self.distance = lambda x1, x2: np.sum(np.abs(x1 - x2))

    def _get_delta_p(self, xm):
        """
        Args:
            xm (np.array) : an adversarial example

        Returns:
            delta_p (np.array) : deviation of p

        """
        if self.kde_type == "L1":
            a = (-1 / (self.n_minus_1 * self.h))
            b = np.exp(-(np.sum(np.abs(xm - self.X_minus_1), axis=1)
                         ) / self.h).dot(xm - self.X_minus_1)
            delta_p = a * b
            return delta_p

    def _get_grad_f(self, xm, norm="l1"):
        """
        Args:
            xm (np.array) : an adversarial example
            norm (str) : type of distance for normalization

        Returns:
            delta_f (np.array) : deviation of F
        """

        if norm == "l1":
            delta_f = self.delta_g(xm) - self.lam * self._get_delta_p(xm)
            delta_f /= (np.sum(np.abs(delta_f)) + 1e-5)

        elif norm == "l2":
            pass
            # delta_f /= (np.sqrt(np.sum(delta_f**2, axis=0)) + 1e-5)

        return delta_f

    def attack(self, x0):
        """
        Args:
            x0 (np.array) : initial data point

        Returns:
            xm (np.array) : created adversarial example
            g_list (list) : lof of decision function (only for svm)
                            (need future improvement)
        """

        g_list = []
        xm = copy.copy(x0)
        for i in range(self.max_iter):
            delta_f = self._get_grad_f(xm)
            xm -= self.t * delta_f.reshape(-1)
            d = self.distance(xm, x0)  # + i * (10/255)
            if d > self.dmax:
                xm = x0 + ((xm - x0) / d) * self.dmax

            g_list.append(self.clf.decision_function(xm.reshape(1, -1)))

        return xm, g_list
