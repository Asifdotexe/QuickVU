from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso, ElasticNet, SGDClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    AdaBoostClassifier,
    AdaBoostRegressor,
    ExtraTreesClassifier,
    ExtraTreesRegressor,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor
)
from sklearn.svm import SVC, SVR, OneClassSVM
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor, NearestCentroid
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, Birch, MeanShift, OPTICS
from sklearn.mixture import GaussianMixture
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, ComplementNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.experimental import enable_hist_gradient_boosting  # Required for hist gradient boosting
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.covariance import EllipticEnvelope
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.kernel_approximation import Nystroem
from sklearn.ensemble import VotingClassifier, VotingRegressor, StackingClassifier, StackingRegressor
from sklearn.multioutput import MultiOutputClassifier, MultiOutputRegressor

MODEL_DICT = {
    # Linear Models
    "Linear Regression": LinearRegression(),
    "Logistic Regression": LogisticRegression(),
    "Ridge Regression": Ridge(),
    "Lasso Regression": Lasso(),
    "ElasticNet Regression": ElasticNet(),
    "Stochastic Gradient Descent Classifier (SGD)": SGDClassifier(),
    "Isotonic Regression": IsotonicRegression(),

    # Ensemble Models
    "Random Forest Classifier": RandomForestClassifier(),
    "Random Forest Regressor": RandomForestRegressor(),
    "Gradient Boosting Classifier": GradientBoostingClassifier(),
    "Gradient Boosting Regressor": GradientBoostingRegressor(),
    "AdaBoost Classifier": AdaBoostClassifier(),
    "AdaBoost Regressor": AdaBoostRegressor(),
    "Extra Trees Classifier": ExtraTreesClassifier(),
    "Extra Trees Regressor": ExtraTreesRegressor(),
    "Hist Gradient Boosting Classifier": HistGradientBoostingClassifier(),
    "Hist Gradient Boosting Regressor": HistGradientBoostingRegressor(),
    "XGBoost Classifier": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
    "XGBoost Regressor": XGBRegressor(),
    "LightGBM Classifier": LGBMClassifier(),
    "LightGBM Regressor": LGBMRegressor(),
    "CatBoost Classifier": CatBoostClassifier(silent=True),
    "CatBoost Regressor": CatBoostRegressor(silent=True),
    "Voting Classifier": VotingClassifier(estimators=[]),  # Define estimators dynamically as needed
    "Voting Regressor": VotingRegressor(estimators=[]),
    "Stacking Classifier": StackingClassifier(estimators=[]),
    "Stacking Regressor": StackingRegressor(estimators=[]),

    # Support Vector Machines
    "Support Vector Classifier (SVC)": SVC(),
    "Support Vector Regressor (SVR)": SVR(),
    "One-Class SVM": OneClassSVM(),

    # Nearest Neighbors
    "K-Nearest Neighbors Classifier (KNN)": KNeighborsClassifier(),
    "K-Nearest Neighbors Regressor (KNN)": KNeighborsRegressor(),
    "Nearest Centroid Classifier": NearestCentroid(),

    # Decision Trees
    "Decision Tree Classifier": DecisionTreeClassifier(),
    "Decision Tree Regressor": DecisionTreeRegressor(),

    # Naive Bayes
    "Gaussian Naive Bayes": GaussianNB(),
    "Multinomial Naive Bayes": MultinomialNB(),
    "Bernoulli Naive Bayes": BernoulliNB(),
    "Complement Naive Bayes": ComplementNB(),

    # Clustering Models
    "K-Means Clustering": KMeans(),
    "DBSCAN Clustering": DBSCAN(),
    "Agglomerative Clustering": AgglomerativeClustering(),
    "Birch Clustering": Birch(),
    "Mean Shift Clustering": MeanShift(),
    "OPTICS Clustering": OPTICS(),
    "Gaussian Mixture Model (GMM)": GaussianMixture(),

    # Neural Networks
    "Multi-Layer Perceptron Classifier (MLP)": MLPClassifier(),
    "Multi-Layer Perceptron Regressor (MLP)": MLPRegressor(),

    # Discriminant Analysis
    "Linear Discriminant Analysis (LDA)": LinearDiscriminantAnalysis(),
    "Quadratic Discriminant Analysis (QDA)": QuadraticDiscriminantAnalysis(),

    # Outlier Detection
    "Elliptic Envelope": EllipticEnvelope(),

    # Decomposition
    "Principal Component Analysis (PCA)": PCA(),
    "Truncated Singular Value Decomposition (SVD)": TruncatedSVD(),
    "Nystroem Kernel Approximation": Nystroem(),

    # Multi-Output Models
    "Multi-Output Classifier": MultiOutputClassifier(RandomForestClassifier()),
    "Multi-Output Regressor": MultiOutputRegressor(RandomForestRegressor())
}
