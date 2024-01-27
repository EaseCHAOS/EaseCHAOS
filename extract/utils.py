import pandas as pd


def save_to_excel(df: pd.DataFrame, filename: str) -> None:
    """
    Save the dataframe to an excel file.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to save.
    filename : str
        The filename to save the dataframe to.
    """
    df.to_excel(filename, index=True)
