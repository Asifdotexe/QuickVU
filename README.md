![Logo](https://github.com/Asifdotexe/QuickVU/blob/main/dataset/logo-png.png)

# Quick VU

**Quick VU** (Quick Visual Understanding) is an easy-to-use tool for data preparation, analysis, and visualization. It helps you clean, explore, and visualize your data without coding.
Just upload your data, choose your analysis, and Quick VU will guide you through the process.

## 📌 Project Objective

The goal of **Quick VU** is to simplify data preparation and data exploration by offering a user-friendly platform that allows users to:
* Quickly clean your data and export it, making it ready for analysis.
* Quickly analyse your data and infer from it.

## 📃 Features

* QuickPrep: Data cleaning tool that helps you to perform tasks like column name standarization, missing value treatment, outlier detection and removal, changing data types, filtering rows, data scaling.

* QuickGlance: Data analysis tool that lets you quickly look at the summary statistics, correlation and allows you to make a few quick plots to get a better understanding of the data at hand.

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

