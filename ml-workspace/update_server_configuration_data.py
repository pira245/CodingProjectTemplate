import os
import csv

def set_file_locations():
    """
        This function return a dictionary with custom jupyter configurations data:
    """
    locations = {}
    # Set Conda environment path
    conda_prefix = os.getenv('CONDA_PREFIX', '/opt/conda')
    locations['conda_prefix'] = conda_prefix 
    # Set current working directory
    current_directory = os.path.dirname(__file__)
    # Set server data file locationcon
    server_data_dir = f"{current_directory}/jupyterlab-configurations/jupyter_server_config.d/server_configuration_data.csv"
    locations['server_data_dir'] = server_data_dir
    #Set custom_lab_extensions_path:
    custom_lab_extensions_path = f"{conda_prefix}/share/jupyter/labextensions"
    locations['custom_lab_extensions_path'] = custom_lab_extensions_path
    #Set root_dir:
    root_dir = f"{current_directory}/notebooks"
    locations['root_dir'] = root_dir
    #Set workspaces_dir
    workspaces_dir = f"{current_directory}/notebooks"
    locations['workspaces_dir'] = workspaces_dir
    #Set custom_css
    custom_css = f"{current_directory}/jupyterlab-configurations/statics/assets/css/custom_jupyterlab_ui.css"
    locations['custom_css'] = custom_css
    #Set custom_js
    custom_js = f"{current_directory}/jupyterlab-configurations/statics/assets/js/custom_jupyterlab_script.js"
    locations['custom_js'] = custom_js

    return locations

def update_server_configuration_data(locations):
    """

        Update server_configuration_data csv file:

    """

    file_path = locations['server_data_dir']
    print("\nfile location: {}\n".format(file_path))
    # Read the existing data and apply updates
    updated_data = []

    with open(file_path, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames  # Preserve original headers
        
        for row in reader:
            if row['variable'] in locations:
                row['value'] = locations[row['variable']]
                print(f"Updated {row['variable']} -> {row['value']}")
            updated_data.append(row)

    # Write back the updated data
    with open(file_path, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # Write headers first
        writer.writerows(updated_data)  # Write updated rows

    
if __name__ == '__main__':

    locations = set_file_locations()
    update_server_configuration_data(locations)
