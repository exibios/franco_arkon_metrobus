#importar bibliotecas
import pandas as pd
import os

def explore_dir(dir=""):
    return os.listdir(dir)
    pass
def dataFromZip(file="",dest="."):
    import zipfile
    fileName="/Metrobus_GTFS_ESTATICO.zip"
    file = file + fileName
    with zipfile.ZipFile(file, 'r') as zip_ref:
    # List all files in the ZIP archive
        file_list = zip_ref.namelist()
    #Returns a list
    return file_list
    pass

def process_zip(zip_path, file_to_process=None):
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as z:
        if file_to_process:  # Process only a specific file
            with z.open(file_to_process) as f:
                df = pd.read_csv(f)
                return df
        else:  # Process all files
            for file_name in z.namelist():
                if file_name.endswith('.txt'):  # Filter for txt files
                    with z.open(file_name) as f:
                        df = pd.read_csv(f)
                        print(f"Processing {file_name}")
                        yield df  # Use a generator for lazy loading

def getDataFromFile(file="",delimeter=","):
    
    df = pd.read_csv(file, delimiter=delimeter)  # Adjust delimiter

    return df
    
    pass

#setup  de directorio de trabajo
actual_dir = os.getcwd()
#actual_dir = os.chdir(actual_dir+"/Metrobus_GTFS_ESTATICO")
#dataFiles = getFileNamesZip(actual_dir)

# Example usage
zip_path = 'Metrobus_GTFS_ESTATICO.zip'
for df in process_zip(zip_path):
    print(df.head())  # Process DataFrame chunk by chunk

#lectura de arhivos fuente
#df = pd.read_csv('trips.txt', delimiter=',')  # Adjust delimiter as needed


