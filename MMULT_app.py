# program to perform complex matrix multiplication

#pip install openpyxl
#pip install xlrd

import streamlit as st
import pandas as pd
import math
import numpy as np
import seaborn as sns
from datetime import date
import base64
sns.set_style("whitegrid")


def download_widget(object_to_download, download_file="download.csv", key=None):
    """Interactive widget to name a CSV file for download."""
    col1, col2 = st.columns(2)
    col1.write("Table shape (rows x columns):")
    col1.write(object_to_download.shape)
    filename = col2.text_input(  "Give a name to the download file", download_file, key=key)
    col2.download_button("Click to Download",object_to_download.to_csv().encode('utf-8'),filename,"text/csv",key='download-csv')


#def download_link(object_to_download, download_filename, download_link_text):
#    """Encodes an object into a downloadable link."""
#    if isinstance(object_to_download, pd.DataFrame):
#        object_to_download = object_to_download.to_csv(index=False)
#    b64 = base64.b64encode(object_to_download.encode()).decode()
#    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

# Get the file
file1 = st.file_uploader("Choose a file", "xlsx", key=1)

def Read_and_Display(key=0):
    # Get the file
    #file1 = st.text_input("File (with path)", "None",key=key+1)
    #file1 = st.file_uploader("Choose a file", "xlsx", key=key+1)
    
    # location of the data in the file
    sheet1 = st.text_input("Excel Sheet", "Sheet1", key=key+2)
    startingrow1 = int(st.text_input("Starting Row", 2,key=key+3))
    matsize1 = int(st.text_input("Matrix Dimension", 25, key=key+4))
    if file1!=None:
        # read in the matrix
        df1 = pd.read_excel(file1, sheet1, skiprows = startingrow1-1, usecols = list(range(0,matsize1)), index_col=None, header=None,nrows=matsize1,engine='openpyxl')
        df1 = df1.applymap(str)
        # numpy uses j for the imaginary variable 
        df1 = df1.replace({'i' : 'j'},regex=True)
        df1_complex = df1.applymap(complex)
        
        # change it from pandas dataframe to numpy array
        mat1 = df1_complex.to_numpy()

        # display it
        dfAB_complex = pd.DataFrame(mat1).applymap(lambda z: "%0.3f + %0.3fi" % (z.real, z.imag))
        st.write(dfAB_complex)
        return mat1
    else:
        st.write("Matrix not yet specified.")


def main():
    matA=None
    matB=None
    matC=None

    # read and display each matrix
    st.header("Specify Matrix A")
    matA = Read_and_Display(10)

    st.header("Specify Matrix B")
    matB = Read_and_Display(20)

    st.header("Specify Matrix C")
    matC = Read_and_Display(30)

    # if they're all available, try to multiply them
    if all([matA is not None,matB is not None,matC is not None]):
        st.header("[A] x [B] x [C]")

        # this line is the matrix mulitplication
        matABC = matA@matB@matC

        # display the result
        dfABC_complex = pd.DataFrame(matABC).applymap(lambda z: "%0.3f + %0.3fi" % (z.real, z.imag))
        st.write(dfABC_complex)

        # download the result
        download_widget(dfABC_complex,key="complex_download",download_file="MMult_%s.csv" % (str(date.today())))


if __name__ == "__main__":
    main()

