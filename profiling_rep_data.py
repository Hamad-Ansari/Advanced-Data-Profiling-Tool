import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import seaborn as sns

# App configuration
st.set_page_config(layout="wide", page_title="Advanced Data Profiler")

# Title and description
st.title("📊 Advanced Data Profiling Tool")
st.markdown("""
Explore and analyze datasets with comprehensive profiling reports.
Select from built-in datasets or upload your own CSV file
            ** with Hammadzahid **.
""")

# Sidebar for dataset selection
with st.sidebar:
    st.header("Data Selection")
    
    dataset_option = st.radio(
        "Choose data source:",
        ("Built-in Datasets", "Upload CSV")
    )
    
    if dataset_option == "Built-in Datasets":
        dataset = st.selectbox(
            "Select dataset:",
            ("Titanic", "Iris", "Tips", "Diamonds", "Penguins", "MPG")
        )
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        st.markdown("""
        **Note:** For large files (>10MB), consider sampling your data first.
        """)

# Load selected dataset
@st.cache_data
def load_data(dataset_name):
    """Load built-in datasets from Seaborn"""
    if dataset_name == "Titanic":
        return sns.load_dataset("titanic")
    elif dataset_name == "Iris":
        return sns.load_dataset("iris")
    elif dataset_name == "Tips":
        return sns.load_dataset("tips")
    elif dataset_name == "Diamonds":
        return sns.load_dataset("diamonds")
    elif dataset_name == "Penguins":
        return sns.load_dataset("penguins")
    elif dataset_name == "MPG":
        return sns.load_dataset("mpg")
    return None

# Main app logic
if dataset_option == "Built-in Datasets":
    df = load_data(dataset)
    st.success(f"Loaded {dataset} dataset with {len(df)} rows")
    
    with st.expander("Dataset Info"):
        if dataset == "Titanic":
            st.write("""
            Titanic passenger data showing survival status and passenger attributes.
            Contains 891 rows with passenger details like age, class, fare, etc.
            """)
        elif dataset == "Iris":
            st.write("""
            Measurements of iris flowers from three species.
            Contains 150 rows with sepal and petal dimensions.
            """)
        elif dataset == "Tips":
            st.write("""
            Restaurant tipping data showing relationships between bills and tips.
            Contains 244 rows with meal information and tipping behavior.
            """)
        # Add descriptions for other datasets...
        
    st.dataframe(df.head())
    
else:
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Uploaded file with {len(df)} rows")
            
            with st.expander("Data Preview"):
                st.dataframe(df.head())
                
            # Add basic statistics
            with st.expander("Quick Stats"):
                st.write("**Data Types:**")
                st.write(df.dtypes)
                st.write("**Missing Values:**")
                st.write(df.isnull().sum())
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.stop()
    else:
        st.info("Please upload a CSV file to begin analysis")
        st.stop()

# Configuration options
with st.sidebar:
    st.header("Report Configuration")
    
    minimal_mode = st.checkbox("Minimal Mode (faster)", False)
    dark_mode = st.checkbox("Dark Mode", False)
    explorative = st.checkbox("Explorative Analysis", True)
    sample_size = st.slider("Sample Size (rows)", 
                           min_value=100, 
                           max_value=len(df), 
                           value=min(1000, len(df)))

# Sample the data if requested
if sample_size < len(df):
    df_sample = df.sample(sample_size, random_state=42)
else:
    df_sample = df.copy()

# Generate and display the profile report
with st.spinner("Generating profile report..."):
    profile = ProfileReport(
        df_sample,
        title=f"{dataset if dataset_option == 'Built-in Datasets' else 'Uploaded Data'} Profiling Report",
        minimal=minimal_mode,
        #dark_mode=dark_mode,
        explorative=explorative
    )

st_profile_report(profile)

# Add download options
with st.sidebar:
    st.header("Export Options")
    
    if st.button("Download Profile Report (HTML)"):
        profile.to_file("profile_report.html")
        with open("profile_report.html", "rb") as f:
            st.download_button(
                label="Click to download",
                data=f,
                file_name="profile_report.html",
                mime="text/html"
            )
    
    if st.button("Download Sampled Data (CSV)"):
        csv = df_sample.to_csv(index=False)
        st.download_button(
            label="Click to download",
            data=csv,
            file_name="sampled_data.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
**Tips:**
- Use the sidebar to configure the report
- For large datasets, use sampling to speed up analysis
- Explore correlations and interactions in the report
""")