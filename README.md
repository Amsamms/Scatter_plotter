
# Simple Scatter Plotter

This is a Streamlit application that allows you to create interactive scatter plots from Excel or CSV data. The application provides features such as outlier removal, multiple chart types, and optional rescaling.

## Features

- **File upload**: The app accepts Excel or CSV files.
- **Outlier removal**: You can choose to remove outliers based on a specified number of standard deviations.
- **Multiple chart types**: You can create various types of charts, including single charts, charts with rescaling, multiple charts for different columns, and a correlation heatmap.
- **Rescaling**: When creating a chart with rescaling, you can manually specify the minimum and maximum numbers for Y rescaling.
- **Date support**: If your data contains a DATE column, the app can handle it properly.

## you can run the app as a web-app here [https://amsamms-scatter-plotter-scatter-plotter-f4ojyj.streamlit.app/]

## How to Run the App locally

1. Install Streamlit using pip:
\```sh
pip install streamlit
\```
2. Run the app:
\```sh
streamlit run scatter_plotter.py
\```
Follow the instructions in the app's sidebar to upload your data and create plots.

## Requirements

- Python 3.6 or higher
- Streamlit
- Pandas
- NumPy
- Plotly
- scikit-learn
- scipy
- openpyxl

For more information on how to use the app, refer to the "How to run the app" section in the app's sidebar, or watch the video tutorial linked in the "Video description of the app" tab.

## License

MIT License

## Contact

For any queries or suggestions, please open an issue on this GitHub repository.
