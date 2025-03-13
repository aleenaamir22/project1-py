#growth mindset project with python 
import streamlit as st #streamlit
import pandas as pd #pandas
import os #operating system 
from io import BytesIO #python modules

st.set_page_config(page_title="Data sweeper", layout="wide")
#css
st.markdown(
    """
    <style>
    .stApp{
     background-color:gray;
     color:white;
     }
     </style>
     """,
     unsafe_allow_html=True
)

#title & description 
st.title("Datasweeper  by Aleena Amir")
st.write("transform your files btw CSV and Excel formats with built-in data cleaning and visualization Creating this project for Quarter3." )

#file uploader
uploaded_files=st.file_uploader("upload your files (accepts CSV or Excel):",type=["csv","xlsx"],accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext= os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type:{file_ext}")    
            continue

        #file details
        st.write("🔍preview the head of the Dataframe")
        st.dataframe(df.head())

     #data cleaning
    st.subheader("Data cleaning operation")
    if st.checkbox(f"Clean data for {file.name}"):
        col1,col2=st.columns(2)

        with col1:
            if st.button(f"Remove duplicates from the file : {file.name}"):
              df.drop_duplicates(inplace = True)
              st.write("duplicate removed!")

            with col2:
                if st.button(f"Fill the missing values{file.name}"):
                  numeric_cols=df.select_dtypes(include=['number']).columns
                  df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                  st.write(f"missing values has been successfully filled")

        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns] 


        #data visualization  
        st.subheader("Data visualization")
        if st.checkbox(f"show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        #conversion options 

        st.subheader("Conversion Options")
        conversion_type = st.radio(f"convert{file.name} to:",["CSV" , "Excel"],key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type=="CSV":
                df.to.csv(buffer,index=False)
                file_name=file.name.replace(file_ext,".csv")
                mime_type="text/csv"
            elif conversion_type=="Excel":
                df.to.to_excel(buffer,index=False)  
                file_name=file.name.replace(file_ext, ".xlsx")
                mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download file link{file.name}as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )                  
st.success("All files processed successfully")            
