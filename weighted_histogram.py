import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def weighted_histogram(
    df,
    observable,
    weight_column,
    bins=None,
    value_range=None,
    plot=True
):
    """
    Compute and optionally plot a weighted histogram of a given observable.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe containing observable and weight columns.
    observable : str
        Name of observable column.
    weight_column : str
        Name of weight column.
    bins : int or array-like, optional
        Number of bins or explicit bin edges.
        If None, a sensible default (sqrt(N)) is used.
    value_range : tuple, optional
        (min, max) range of histogram.
    plot : bool
        If True, produces a matplotlib plot.

    Returns
    -------
    hist : np.ndarray
        Weighted bin counts.
    bin_edges : np.ndarray
        Bin edges.
    """

    # ---------- Validation ----------
    if observable not in df.columns:
        raise ValueError(f"{observable} not found in dataframe.")

    if weight_column not in df.columns:
        raise ValueError(f"{weight_column} not found in dataframe.")

    values = df[observable].to_numpy()
    weights = df[weight_column].to_numpy()

    if len(values) == 0:
        raise ValueError("Observable array is empty.")

    if len(values) != len(weights):
        raise ValueError("Observable and weight arrays must have same length.")

    # Sensible default binning: sqrt(N)
    if bins is None:
        bins = int(np.sqrt(len(values)))

    # Histogram computation
    hist, bin_edges = np.histogram(
        values,
        bins=bins,
        range=value_range,
        weights=weights
    )

    # Plotting 
    if plot:
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

        plt.figure()
        plt.step(bin_centers, hist, where="mid")
        plt.xlabel(observable)
        plt.ylabel("Weighted counts")
        plt.title(f"Weighted Histogram of {observable}")
        plt.show()

    return hist, bin_edges

# Tests using simple assertions

if __name__ == "__main__":

    # Test 1: Basic unweighted case
    # Edge case: ensure histogram integrates to total weight
    
    df1 = pd.DataFrame({
        "x": [1, 2, 3, 4],
        "w": [1, 1, 1, 1]
    })

    hist1, _ = weighted_histogram(df1, "x", "w", bins=4, plot=False)
    assert hist1.sum() == 4, "Basic unweighted test failed."

    # Test 2: Weighted case
    # Edge case: verify weights are actually applied
    
    df2 = pd.DataFrame({
        "x": [1, 2, 3, 4],
        "w": [1, 2, 3, 4]
    })

    hist2, _ = weighted_histogram(df2, "x", "w", bins=4, plot=False)
    assert hist2.sum() == 10, "Weighted sum test failed."
   
    # Test 3: Missing observable column
    # Edge case: robust error handling for wrong input
   
    try:
        weighted_histogram(df1, "y", "w", plot=False)
    except ValueError:
        pass
    else:
        raise AssertionError("Missing observable column test failed.")

    # Test 4: Empty dataframe
    # Edge case: avoid silent failure on empty input
    
    df_empty = pd.DataFrame({"x": [], "w": []})
    try:
        weighted_histogram(df_empty, "x", "w", plot=False)
    except ValueError:
        pass
    else:
        raise AssertionError("Empty dataframe test failed.")


    print("All tests passed successfully.")
