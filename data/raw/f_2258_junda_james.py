import logging  # For adding logging to the script
import matplotlib.pyplot as plt

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def f_2258(df, category_col, sales_col):
    """
    Generates a bar chart for sales data from a given DataFrame, with a title 'Sales Report by Category',
    and raises an exception if there are duplicate category entries.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing the sales data. It must not be empty, should contain
                             at least one row with numeric sales data, and must not have duplicate 
                             entries in the category column.
    - category_col (str): Column name for the product categories. This column should not contain duplicates.
    - sales_col (str): Column name for the sales figures.

    Returns:
    - matplotlib.axes.Axes: Axes object of the generated bar chart if df is not empty; None otherwise.

    Raises:
    - ValueError: If the DataFrame is empty, lacks numeric sales data, or contains duplicate entries in the category column.

    Requirements:
    - pandas
    - matplotlib

    Example:
    >>> df_example = pd.DataFrame({'Category': ['Electronics', 'Clothing', 'Home', 'Books', 'Sports'], 'Sales': [1000, 1500, 1200, 800, 1100]})
    >>> ax = f_2258(df_example, 'Category', 'Sales')
    """
    if df.empty or not df[sales_col].dtype.kind in 'biufc':
        logging.error("DataFrame is empty, lacks sales data, or sales data is not numeric.")
        raise ValueError("DataFrame is empty, lacks sales data, or sales data is not numeric.")
    
    if df[category_col].duplicated().any():
        logging.error("DataFrame contains duplicate entries in the category column.")
        raise ValueError("DataFrame contains duplicate entries in the category column.")

    ax = df.set_index(category_col)[sales_col].plot(kind='bar', title="Sales Report by Category")
    plt.ylabel('Sales')
    plt.show()
    return ax


import unittest
import pandas as pd

class TestCases(unittest.TestCase):
    def test_sales_data_input(self):
        df_setup = pd.DataFrame({
            'Category': ['Electronics', 'Clothing', 'Home', 'Books', 'Sports'],
            'Sales': [1000, 1500, 1200, 800, 1100]
        })
        ax_tmp = f_2258(df_setup, 'Category', 'Sales')
        self.assertEqual(len(ax_tmp.patches), 5)  # 5 bars for 5 categories

    def test_single_category_input(self):
        df_setup = pd.DataFrame({
            'Category': ['Electronics', 'Clothing', 'Home', 'Books', 'Sports'],
            'Sales': [1000, 1500, 1200, 800, 1100]
        })
        df_single = df_setup.head(1)  # Only one category
        ax_tmp = f_2258(df_single, 'Category', 'Sales')
        print(ax_tmp.patches)
        self.assertEqual(len(ax_tmp.patches), 1)  # 1 bar for 1 category

    def test_no_data(self):
        df_empty = pd.DataFrame(columns=['Category', 'Sales'])  # Empty DataFrame
        with self.assertRaises(ValueError):
            ax = f_2258(df_empty, 'Category', 'Sales')

    def test_invalid_columns(self):
        df_setup = pd.DataFrame({
            'Category': ['Electronics', 'Clothing', 'Home', 'Books', 'Sports'],
            'Sales': [1000, 1500, 1200, 800, 1100]
        })
        with self.assertRaises(KeyError):
            f_2258(df_setup, 'NonexistentCategory', 'Sales')

    def test_duplicate_category_input(self):
        df_setup = pd.DataFrame({
            'Category': ['Electronics', 'Clothing', 'Home', 'Books', 'Sports'],
            'Sales': [1000, 1500, 1200, 800, 1100]
        })

        df_duplicate = pd.concat([df_setup, df_setup]).reset_index(drop=True)
        with self.assertRaises(ValueError):
            f_2258(df_duplicate, 'Category', 'Sales')

def run_tests():
    """Run all tests for this function."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCases)
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    run_tests()