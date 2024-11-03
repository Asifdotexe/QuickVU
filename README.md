# Quick VU

**Quick VU** stands for **Quick Visual Understanding**. It is a no-code data visualization and analysis tool designed to help users effortlessly explore and understand their datasets. Built with Streamlit, Quick VU provides an intuitive interface for uploading, preprocessing, and analyzing data, making it accessible to everyone regardless of technical expertise.

## 📌 Project Objective

The goal of **Quick VU** is to simplify data exploration by offering a user-friendly platform that allows users to:
- Upload and preview datasets quickly.
- Select and categorize data columns for analysis.
- Handle missing data with ease.
- Generate summary statistics and visualize correlations.
- Create specific visualizations like sales by product and sales trends over time.

## 🚀 Features

### 1. Data Upload and Preview
- **Upload Your Dataset**: Easily upload your CSV files through the sidebar.
- **Dataset Preview**: View the first few rows of your data to ensure it's loaded correctly.

### 2. Column Selection
- **Categorical Columns**: Select columns that contain categorical data (e.g., Product Type, Category).
- **Numerical Columns**: Choose columns with numerical data (e.g., Sales Amount, Profit).
- **Date/Time Columns**: Identify and select date or time-related columns for time-based analysis.

### 3. Data Preprocessing
- **Handle Missing Values**: Choose how to address missing data by filling with the mean, median, or dropping rows with missing values.
- **Convert Data Types**: Automatically convert integer columns to datetime if specified.

### 4. Exploratory Data Analysis (EDA)
- **Summary Statistics**: Generate and view summary statistics such as mean, median, and standard deviation for numerical columns.
- **Correlation Matrix**: Visualize the relationships between numerical variables using a heatmap. Additionally, get explanations for the correlations to understand the data better.

### 5. Data Visualization
- **Sales by Product**: Create bar charts to compare sales across different product categories. Select specific product and sales amount columns to tailor the visualization.
- **Sales Trends Over Time**: Plot sales trends over selected dates to identify patterns and trends in your data.

### 6. User-Friendly Interface
- **Custom Styling**: Enjoy a modern and consistent look with custom CSS styling applied to the app.
- **Interactive Sidebar**: Access all tools and options through an intuitive sidebar, making navigation straightforward.

### 7. Additional Features
- **Explain Correlation Matrix**: Get detailed explanations of the correlation matrix to better understand the data relationships.
- **Preprocessed Data Display**: View the cleaned and preprocessed dataset after handling missing values.

## 🛠️ Technologies Used

- **Python**
- **Streamlit**: For building the interactive web application.
- **Pandas**: For data manipulation and analysis.
- **Seaborn & Matplotlib**: For creating visualizations.
- **NumPy**: For numerical operations.

## 📦 Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/quick-vu.git
    cd quick-vu
    ```

2. **Create a conda envirioment**
    Assuming you have ananconda installed on your system
    ```bash
    conda create -name quickvu python=3.12
    conda activate quickvu
    ```

2. **Install Dependencies**
    Ensure you have Python installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Google API SDK**
    The Python SDK for the Gemini API is contained in the google-generativeai package. Install the dependency using pip:
    ```bash
    pip install -q -U google-generativeai
    ```

4. **Run the Application**
    Start the Streamlit app:
    ```bash
    streamlit run app.py
    ```

5. **Use Quick VU**
    - Open the provided local URL in your browser.
    - Upload your CSV dataset and start exploring your data!

## 📊 How to Use Quick VU

1. **Upload Your Data**
    - Navigate to the sidebar and use the file uploader to select your CSV file.
    - After uploading, the dataset preview will display the first few rows.

2. **Select Columns for Analysis**
    - Choose which columns are categorical, numerical, and date/time from the sidebar options.

3. **Preprocess Your Data**
    - Decide how to handle missing values by selecting an option (Fill with Mean, Fill with Median, or Drop Missing Rows).
    - The preprocessed dataset will be displayed for your review.

4. **Perform Exploratory Data Analysis**
    - **Summary Statistics**: Check the statistical summary of your numerical data.
    - **Correlation Matrix**: View and understand the correlations between numerical variables.

5. **Visualize Your Data**
    - **Sales by Product**: Generate a bar chart to compare sales across different products.
    - **Sales Trends Over Time**: Plot sales data over selected dates to identify trends.

## 🤝 Contributions

Contributions are welcome! If you have suggestions, bug reports, or want to contribute code, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

For any inquiries or feedback, please contact [Asif Sayyed](mailto:asifdotexe@gmail.com).

---

With **Quick VU**, you can explore and understand your data efficiently without the need for coding. Simplify your data analysis process and gain valuable insights effortlessly.

