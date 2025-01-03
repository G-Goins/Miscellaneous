import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

data = {
    'Year': [2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021,
             2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022,
             2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023],
    'Name': ['Jeff', 'Phil', 'Fenn', 'Connor', 'Solomon', 
             'Grant', 'Cory', 'Matthew', 'Daniel', 'Forrest', 
             'William', 'Will'] * 3,
    'DraftPick': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                  3, 7, 6, 2, 4, 9, 5, 11, 12, 1, 10, 8,
                  12, 2, 1, 10, 5, 8, 7, 6, 11, 3, 4, 3],
    'FinalOutcome': [.28, .42, .57, .42, .57, .42, .50, .64, .28, .57, .71, .57,
                     .57, .42, .50, .57, .64, .50, .35, .50, .14, .78, .42, .57,
                     .57, .35, .50, .57, .57, .64, .35, .50, .14, .78, .50, .50]
}

df = pd.DataFrame(data)

# Perform Linear Regression for Each Year
results = []
images = []

for year in [2021, 2022, 2023]:
    yearly_data = df[df['Year'] == year]
    
    X = yearly_data[['DraftPick']]
    y = yearly_data['FinalOutcome']
    
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    
    results.append({
        'Year': year,
        'Coefficient': model.coef_[0],
        'Intercept': model.intercept_,
        'MSE': mse,
        'R2': r2
    })
    
    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, color='blue')
    plt.plot(X, predictions, color='red')
    plt.xlabel('Draft Pick Position')
    plt.ylabel('Final Outcome')
    plt.title(f'Draft Pick Position vs. Final Outcome (Year {year})')

    # Annotate each data point with the participant's name
    for i in range(len(X)):
        plt.text(X.iloc[i, 0] + 0.1, y.iloc[i] + 0.1, yearly_data['Name'].iloc[i], fontsize=9)

    # Display the metrics on the plot
    plt.text(0.05, 0.95, f'Coefficient: {model.coef_[0]:.2f}', transform=plt.gca().transAxes)
    plt.text(0.05, 0.90, f'Intercept: {model.intercept_:.2f}', transform=plt.gca().transAxes)
    plt.text(0.05, 0.85, f'MSE: {mse:.2f}', transform=plt.gca().transAxes)
    plt.text(0.05, 0.80, f'R-squared: {r2:.2f}', transform=plt.gca().transAxes)

    # Save the plot to an image in memory
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    images.append(ImageReader(img_buffer))
    
    # Close the plot
    plt.close()

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Consolidate the Results into a PDF
pdf_file = "fantasy_football_report_2021_2023.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
width, height = letter

# Title
c.setFont("Helvetica", 16)
c.drawString(150, 770, "Fantasy Football Draft Analysis Report")

# Summary Table
c.setFont("Helvetica", 12)
c.drawString(50, 740, "Yearly Linear Regression Summary")
c.drawString(50, 720, "Year | Coefficient | Intercept | MSE | R2")

# Add each year's result
y_pos = 700
for i, row in results_df.iterrows():
    text = f"{row['Year']} | {row['Coefficient']:.2f} | {row['Intercept']:.2f} | {row['MSE']:.2f} | {row['R2']:.2f}"
    c.drawString(50, y_pos, text)
    y_pos -= 20

# Adjust position for images and add them to the PDF
for i, img in enumerate(images):
    if y_pos < 300:  # If space is insufficient, add a new page
        c.showPage()
        y_pos = 700
    
    c.drawImage(img, 50, y_pos - 200, width=500, height=300)
    y_pos -= 350

c.save()
print(f"Report saved as {pdf_file}")