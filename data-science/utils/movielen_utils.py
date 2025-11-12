
import urllib
import zipfile
import os






class MoviLenLinkResource:
    ML100K = "http://files.grouplens.org/datasets/movielens/ml-100k.zip"

def download_ml100k(dest_folder_name: str):

    dest_file_path = os.path.join("../datasets/movielen_datasets",dest_folder_name)
    urllib.request.urlretrieve("http://files.grouplens.org/datasets/movielens/ml-100k.zip", dest_file_path)
    zip_ref = zipfile.ZipFile('movielens.zip', "r")
    zip_ref.extractall()

def read_u_base_to_df(ml100k_path: str):
    import pandas as pd
    column_names = ["user_id", "movie_id", "rating", "timestamp"]
    df = pd.read_csv(os.path.join(ml100k_path, "u.base"), names=column_names, sep = "\t", encoding="latin-1")

    return df
