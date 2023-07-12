import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(m_path, c_path):
    """
    Loads and merges datasets from 2 filepaths.

    Parameters:
    m_path: messages csv file
    c_path: categories csv file

    Returns:
    dataframe containing m_path and c_path merged
    """
    # load datasets
    messages = pd.read_csv(m_path)
    categories = pd.read_csv(c_path)
    # merge datasets on common id and return the merged dataframe
    return messages.merge(categories, how="outer", on=["id"])


def clean_data(df):
    """
    Cleans the dataframe.

    Parameters:
    df: DataFrame

    Returns:
    df: Cleaned DataFrame
    """
    # create a dataframe of the 36 individual category columns
    categories = df["categories"].str.split(";", expand=True)
    # select first row of the categories dataframe
    row = categories.head(1)
    # apply a lambda function that takes everything
    # up to the second to last character of each string with slicing
    # to create new column names for categories
    category_colnames = row.applymap(lambda x: x[:-2]).iloc[0, :]
    # rename the columns of 'categories'
    categories.columns = category_colnames

    # iterate through the category columns in df to keep only the
    # last character of the string
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].astype(str).str[-1]
        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
    # replace 2s with 1s in related column
    categories["related"] = categories["related"].replace(to_replace=2, value=1)

    # drop the original categories column from `df`
    df.drop("categories", axis=1, inplace=True)
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1)
    # drop duplicates
    df.drop_duplicates(inplace=True)
    return df


def save_data(df, db_path):
    """Stores df in a SQLite database."""
    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql("disaster_messages", engine, index=False, if_exists="replace")


def main():
    """Loads data, cleans data, saves data to database"""
    if len(sys.argv) == 4:
        m_path, c_path, db_path = sys.argv[1:]

        print(
            "Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}".format(
                m_path, c_path
            )
        )
        df = load_data(m_path, c_path)

        print("Cleaning data...")
        df = clean_data(df)

        print("Saving data...\n    DATABASE: {}".format(db_path))
        save_data(df, db_path)

        print("Cleaned data saved to database!")

    else:
        print(
            "Please provide the filepaths of the messages and categories "
            "datasets as the first and second argument respectively, as "
            "well as the filepath of the database to save the cleaned data "
            "to as the third argument. \n\nExample: python process_data.py "
            "disaster_messages.csv disaster_categories.csv "
            "DisasterResponse.db"
        )


if __name__ == "__main__":
    main()
