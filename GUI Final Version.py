import pickle

import tkinter as tk
from tkinter import messagebox

import pandas as pd

import unicodeit

from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

# Load and preprocess dataset
data = pd.read_excel("Extended Dataset.xls")
# data = pd.read_excel("Dataset.xls")
X = data.iloc[:, :-1].values  # Assuming all other columns are features
X_ = data.iloc[:, :-1]  # Assuming all other columns are features
y = data.iloc[:, -1].values  # Assuming the last column is the target

# Split the dataset into training and testing sets
X_train, y_train = X, y
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)


# Initialize the Gradient Boosting Regressor
xgb_regressor = XGBRegressor()
# #
# # # Use MultiOutputRegressor with the Gradient Boosting Regressor
# dnn_regressor = mlp_regressor
#


# # Fit the model on the training data
xgb_regressor.fit(X_train, y_train)



# # Save the trained model
with open('xgb_regressor.pkl', 'wb') as model_file:
    pickle.dump(xgb_regressor, model_file)

# tkinter GUI
root = tk.Tk()
root.title(f"Prediction of Load Carrying Capacity")

canvas1 = tk.Canvas(root, width=600, height=600)
canvas1.configure(background='#e9ecef')
canvas1.pack()

# label0 = tk.Label(root, text='Compressive Strength Prediction of Concrete', font=('Times New Roman', 15, 'bold'), bg='#e9ecef')
# canvas1.create_window(70, 20, anchor="w", window=label0)
#
# label_phd = tk.Label(root, text='Developed by: Mr. Rupesh Kumar Tipu\n K. R. Mangalam University, India.\n '
#                                 'tipu0003@gmail.com',
#                      font=('Futura Md Bt', 12), bg='#e9ecef')
#
# canvas1.create_window(100, 60, anchor="w", window=label_phd)

label_input = tk.Label(root, text='Input Variables', font=('Times New Roman', 12, 'bold', 'italic', 'underline'),
                       bg='#e9ecef')
canvas1.create_window(20, 90, anchor="w", window=label_input)

# Labels and entry boxes
labels = [
    'Eccentricity (mm)', 'Column Height (mm)', 'Concrete Srength of Standard Cylinder (MPa)', 'Area of Concrete Core '
                                                                                              '(mm\u00b2)',
    'Area of Steel Tube (mm\u00b2)',
    'Yield Strength of Steel Tube (MPa)', 'Total Thickness of FRP Wraps (mm)', 'Width of FRP Wrap × Clear Spacing of '
                                                                               'FRP (mm)', 'Elastic Modulus of FRP ('
                                                                                           'MPa)',

]


entry_boxes = []
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=unicodeit.replace(label_text), font=('Times New Roman', 15, 'italic'), bg='#e9ecef',
                     pady=5)
    canvas1.create_window(20, 120 + i * 30, anchor="w", window=label)

    entry = tk.Entry(root)
    canvas1.create_window(530, 120 + i * 30, window=entry)
    entry_boxes.append(entry)

# label_output = tk.Label(root, text='Flow of Concrete', font=('Times New Roman', 12, 'bold'),
# bg='#e9ecef')
# canvas1.create_window(50, 420, anchor="w", window=label_output)

label_output1 = tk.Label(root, text='Load Carrying Capacity:', font=('Times New Roman', 18, 'bold'),
                         bg='#e9ecef')
canvas1.create_window(20, 560, anchor="w", window=label_output1)

def reset_entries():
    for entry in entry_boxes:
        entry.delete(0, tk.END)
def values():
    # Validate and get the values from the entry boxes
    input_values = []
    for entry_box in entry_boxes:
        value = entry_box.get().strip()
        if value:
            try:
                input_values.append(float(value))
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")
                return
        else:
            messagebox.showerror("Error", "Please fill in all the input fields.")
            return



    # If all input values are valid, proceed with prediction
    input_values_all = [
        input_values[0], input_values[1], input_values[2], input_values[3]/input_values[2], input_values[3],
        input_values[3]/input_values[1], input_values[4], input_values[3]/input_values[4], input_values[5],
        input_values[6], input_values[6]*input_values[4], input_values[7], input_values[8]
    ]
    print(len(input_values_all))
    input_data = pd.DataFrame([input_values_all ],
                        columns=X_.columns)
    input_data = scaler.transform(input_data)
    # Load the trained MultiOutputRegressor model
    with open('xgb_regressor.pkl', 'rb') as model_file:
        xgb_regressor_loaded = pickle.load(model_file)

    # Predict using the loaded XGBRegressor model
    prediction_result = xgb_regressor_loaded.predict(input_data)
    prediction_result1 = round(prediction_result[0], 2)
    # prediction_result2 = round(prediction_result[0, 1], 2)

    # Display the prediction on the GUI
    label_prediction = tk.Label(root, text=f'{str(prediction_result1)} kN', font=('Times New Roman', 20, 'bold'),
                                bg='white')
    canvas1.create_window(280, 560, anchor="w", window=label_prediction)

    # label_prediction1 = tk.Label(root, text=f'{str(prediction_result2)} MPa', font=('Times New Roman', 20, 'bold'),
    #                              bg='white')
    # canvas1.create_window(230, 500, anchor="w", window=label_prediction1)


button1 = tk.Button(root, text='Predict', command=values, bg='#4285f4', fg='white',
                    font=('Times New Roman', 20, 'bold'),
                    bd=3, relief='ridge')
canvas1.create_window(490, 560, anchor="w", window=button1)

# Reset Button
button_reset = tk.Button(root, text="Reset", command=reset_entries, bg="red", fg="white", font=("Times New Roman", 20, "bold"), bd=3, relief="ridge")
canvas1.create_window(550, 500, window=button_reset)

root.mainloop()
