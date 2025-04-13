import pandas as pd
import numpy as np
import multiprocessing as mp

# Load data_ut once outside to avoid multiprocessing issues
data_ut = pd.read_csv("landslide_data.csv")

def process_section(start_idx, end_idx, data_section):
    """Processes a section of rows and updates the given DataFrame."""
    for i in range(start_idx, end_idx):
        try:
            dem = pd.read_csv(f'dem_data/row_{i}.csv')

            y = data_ut.loc[i, 'latitude']
            x = data_ut.loc[i, 'longitude']
            l = int(x)
            b = int(y)
            row = (y - b) / 0.000278
            column = (x - l) / 0.000278

            dem = dem[(dem['Row'] > row - 2) & (dem['Row'] < row + 2) & 
                      (dem['Col'] > column - 2) & (dem['Col'] < column + 2)]

            dem = dem.mean()
            dem.drop(['Row', 'Col'], inplace=True)

            data_section.append(dem.transpose(), ignore_index=True)
        
        except Exception as e:
            print(f"Error processing row {i}: {e}")

    return data_section

if __name__ == "__main__":
    # Define the DataFrame structure
    dem_data_template = {
        'Slope':[], 'Aspect':[], 'Plan Curvature':[], 'Profile Curvature':[], 
        'TPI':[], 'Elevation Relative':[], 'Elevation Percentile':[]
    }

    # Number of rows and processes
    num_rows = 263
    num_processes = 3
    chunk_size = num_rows // num_processes  # Split workload equally

    # Create separate DataFrames for each process
    dem_datas = [pd.DataFrame(dem_data_template) for _ in range(num_processes)]

    # Create and start processes
    processes = []
    with mp.Pool(processes=num_processes) as pool:
        results = [
            pool.apply_async(process_section, args=(i * chunk_size, (i + 1) * chunk_size, dem_datas[i]))
            for i in range(num_processes)
        ]
        dem_datas = [res.get() for res in results]  # Collect results

    # Merge results
    dem_data = pd.concat(dem_datas, ignore_index=True)

    # Save output
    dem_data.to_csv('dem_data.csv', index=False)

    print("Processing complete. Saved as 'dem_data.csv'.")
