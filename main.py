import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.metrics import cohen_kappa_score
import matplotlib.pyplot as plt
import seaborn as sns

# Function to perform analysis and generate plots
def analyze_data(ai_data, radiologist_data):
    # Extracting relevant columns for comparison
    ai_accuracy = ai_data['accuracy']
    radiologist_accuracy = radiologist_data['accuracy']
    ai_quality = ai_data['quality']
    radiologist_quality = radiologist_data['quality']
    ai_consistency = ai_data['consistency']
    radiologist_consistency = radiologist_data['consistency']
    ai_classification = ai_data['classification']
    radiologist_classification = radiologist_data['classification']
    
    # Perform t-tests
    t_stat_accuracy, p_value_accuracy = stats.ttest_ind(ai_accuracy, radiologist_accuracy)
    t_stat_quality, p_value_quality = stats.ttest_ind(ai_quality, radiologist_quality)
    t_stat_consistency, p_value_consistency = stats.ttest_ind(ai_consistency, radiologist_consistency)

    # Compute Cohen's Kappa for inter-rater reliability
    kappa = cohen_kappa_score(ai_classification, radiologist_classification)

    # Create combined plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot Accuracy Comparison
    sns.barplot(x=['AI', 'Radiologist'], y=[ai_accuracy.mean(), radiologist_accuracy.mean()], ax=axes[0, 0])
    axes[0, 0].set_title('Accuracy Comparison')
    axes[0, 0].set_ylabel('Mean Accuracy')

    # Plot Quality Comparison
    sns.barplot(x=['AI', 'Radiologist'], y=[ai_quality.mean(), radiologist_quality.mean()], ax=axes[0, 1])
    axes[0, 1].set_title('Quality Comparison')
    axes[0, 1].set_ylabel('Mean Quality')

    # Plot Consistency Comparison
    sns.barplot(x=['AI', 'Radiologist'], y=[ai_consistency.mean(), radiologist_consistency.mean()], ax=axes[1, 0])
    axes[1, 0].set_title('Consistency Comparison')
    axes[1, 0].set_ylabel('Mean Consistency')

    # Plot Cohen's Kappa
    sns.heatmap([[kappa]], annot=True, cmap="Blues", fmt=".2f", xticklabels=["Agreement"], yticklabels=["AI vs Radiologist"], ax=axes[1, 1])
    axes[1, 1].set_title("Cohen's Kappa Agreement")

    # Adjust layout
    plt.tight_layout()

    # Save the figure to a file
    report_file = "report.png"
    fig.savefig(report_file)

    # Create a summary of the results
    analysis_results = {
        't_stat_accuracy': t_stat_accuracy,
        'p_value_accuracy': p_value_accuracy,
        't_stat_quality': t_stat_quality,
        'p_value_quality': p_value_quality,
        't_stat_consistency': t_stat_consistency,
        'p_value_consistency': p_value_consistency,
        'kappa': kappa
    }

    # Create a DataFrame for results to be downloaded
    results_df = pd.DataFrame([analysis_results])

    return results_df, report_file

# Streamlit UI
def main():
    st.title("AI vs Radiologist Report Quality Comparison")

    # File upload
    uploaded_ai_file = st.file_uploader("Upload AI Reports CSV", type=["csv"])
    uploaded_radiologist_file = st.file_uploader("Upload Radiologist Reports CSV", type=["csv"])

    if uploaded_ai_file and uploaded_radiologist_file:
        # Load the CSV files into DataFrames
        ai_data = pd.read_csv(uploaded_ai_file)
        radiologist_data = pd.read_csv(uploaded_radiologist_file)

        # Check if the columns match between the two datasets
        if ai_data.shape != radiologist_data.shape:
            st.error("The data shape does not match between AI and Radiologist reports.")
        else:
            st.write("Data successfully loaded!")

            # Perform the analysis
            results_df, report_file = analyze_data(ai_data, radiologist_data)

            # Display analysis results
            st.subheader("Statistical Analysis Results:")
            st.write(results_df)

            # Provide the option to download the CSV report
            st.download_button(
                label="Download CSV Report",
                data=results_df.to_csv(index=False),
                file_name="report_analysis.csv",
                mime="text/csv"
            )

            # Provide the option to download the plot report
            st.download_button(
                label="Download Plot Report",
                data=open(report_file, "rb").read(),
                file_name="report_plots.png",
                mime="image/png"
            )

            # Display the plot on the web interface
            st.subheader("Analysis Plots:")
            st.image(report_file)

if __name__ == "__main__":
    main()
