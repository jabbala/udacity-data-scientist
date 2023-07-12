# import libraries
import sys
import pandas as pd
import pickle
from sqlalchemy import create_engine

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


nltk.download(["punkt", "wordnet"])


def tokenize(text):
    """
    Function to tokenize text.
    """

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def load_data(data_file):
    # load to database
    engine = create_engine(f"sqlite:///../data/{data_file}")
    df = pd.read_sql_table("disaster_messages", con=engine)
    # define features and label arrays
    X, y = df["message"], df.iloc[:, 4:]
    return X, y


def build_model():
    # text processing and model pipeline
    pipeline = Pipeline(
        [
            ("vect", CountVectorizer(tokenizer=tokenize)),
            ("tfidf", TfidfTransformer()),
            ("clf", MultiOutputClassifier(RandomForestClassifier())),
        ]
    )

    # define parameters for GridSearchCV
    parameters = {"clf__estimator__n_estimators": [100]}

    # create gridsearch object and return as final model pipeline
    model_pipeline = GridSearchCV(pipeline, param_grid=parameters)

    return model_pipeline


def train(X, y, model):
    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # fit model
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # output model test results
    for index, column in enumerate(y_test):
        print(column, classification_report(y_test[column], y_pred[:, index]))
    accuracy = (y_pred == y_test).mean()
    print(f"Model Accuracy: {accuracy}")

    return model


def export_model(model):
    # Export model as a pickle file
    filename = "model.pkl"
    pickle.dump(model, open(filename, "wb"))


def run_pipeline(data_file):
    X, y = load_data(data_file)  # run ETL pipeline
    model = build_model()  # build model pipeline
    model = train(X, y, model)  # train model pipeline
    export_model(model)  # save model


if __name__ == "__main__":
    data_file = sys.argv[1]  # get filename of dataset
    run_pipeline(data_file)  # run data pipeline
