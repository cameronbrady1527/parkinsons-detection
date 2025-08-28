# Parkinson's Disease Detection Frontend

This is a modern, responsive web interface for the Parkinson's Disease Detection API.

## Features

- **Beautiful UI**: Modern, medical-grade design with gradient backgrounds and glass-morphism effects
- **Drag & Drop**: Easy file upload with drag and drop support
- **Real-time Status**: Live API health monitoring
- **Model Information**: Display of trained model performance metrics
- **Results Visualization**: Clear presentation of prediction results with confidence scores
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## How to Use

1. **Access the Application**: Navigate to your deployed API URL (e.g., `https://your-app.railway.app/`)

2. **Check API Status**: The top-right corner shows the current API status:
   - 🟢 Green: API is healthy and ready
   - 🟡 Yellow: API is degraded but functional
   - 🔴 Red: API has issues

3. **Upload Data**: 
   - Click the upload area or drag and drop a CSV file
   - The file must contain the required voice measurement columns
   - A sample file (`sample_data.csv`) is provided for testing

4. **Analyze Results**: 
   - Click "Analyze Data" to process your file
   - Results will show predictions from multiple models
   - Each prediction includes confidence scores and risk assessment

## File Format Requirements

Your CSV file must include these columns:
- `name`: Patient/sample identifier
- `MDVP:Fo(Hz)`: Average vocal fundamental frequency
- `MDVP:Fhi(Hz)`: Maximum vocal fundamental frequency
- `MDVP:Flo(Hz)`: Minimum vocal fundamental frequency
- `MDVP:Jitter(%)`: Jitter percentage
- `MDVP:Jitter(Abs)`: Absolute jitter
- `MDVP:RAP`: Relative average perturbation
- `MDVP:PPQ`: Five-point period perturbation quotient
- `Jitter:DDP`: Average absolute difference of differences between jitter cycles
- `MDVP:Shimmer`: Shimmer
- `MDVP:Shimmer(dB)`: Shimmer in dB
- `Shimmer:APQ3`: Three-point amplitude perturbation quotient
- `Shimmer:APQ5`: Five-point amplitude perturbation quotient
- `MDVP:APQ`: Amplitude perturbation quotient
- `Shimmer:DDA`: Average absolute difference between consecutive differences between the amplitudes of consecutive periods
- `NHR`: Noise-to-harmonics ratio
- `HNR`: Harmonics-to-noise ratio
- `status`: Target variable (1 for Parkinson's, 0 for healthy)
- `RPDE`: Recurrence period density entropy
- `DFA`: Detrended fluctuation analysis
- `spread1`: Nonlinear measure of fundamental frequency variation
- `spread2`: Nonlinear measure of fundamental frequency variation
- `D2`: Correlation dimension
- `PPE`: Pitch period entropy

## Understanding Results

### Prediction Badges
- **High Risk (Red)**: Indicates potential Parkinson's disease
- **Low Risk (Green)**: Indicates healthy status

### Confidence Scores
- Displayed as percentages and visual progress bars
- Higher confidence indicates more reliable predictions
- Multiple models provide ensemble predictions for better accuracy

### Model Information
The interface shows:
- **Accuracy**: Cross-validation accuracy for each model
- **Standard Deviation**: Variability in model performance
- **Features Used**: Number of features selected for prediction

## Technical Details

- **Frontend**: Pure HTML, CSS, and JavaScript (no frameworks)
- **API Integration**: RESTful API calls to your FastAPI backend
- **Responsive**: Mobile-first design with CSS Grid and Flexbox
- **Accessibility**: Semantic HTML and keyboard navigation support

## Troubleshooting

### File Upload Issues
- Ensure your CSV file has the correct column headers
- Check that all required columns are present
- Verify the file is not corrupted or empty

### API Connection Issues
- Check if your API is running and accessible
- Verify the API URL is correct
- Check browser console for error messages

### Results Not Displaying
- Ensure your data format matches the expected schema
- Check that the API returned valid predictions
- Try refreshing the page and uploading again

## Sample Data

Use the provided `sample_data.csv` file to test the interface. This file contains sample voice measurements that should work with the trained models.

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Support

If you encounter issues:
1. Check the browser console for error messages
2. Verify your API is running correctly
3. Test with the provided sample data
4. Check the API documentation for endpoint details 