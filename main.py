
# import pandas as pd
# import pickle
# from fastapi import FastAPI
# from pydantic import BaseModel
# from datetime import datetime

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# class PriceCalculatorInput(BaseModel):
#     Working_Hours: int
#     Crop_Type: str

# def get_dynamic_values():
#     now = datetime.now()
#     return {
#         "Day_of_Week": now.weekday(),
#         "Month": now.month,
#         "Base_Hourly_Wage": 12.00,
#         "Supply_Demand_Ratio": 1.2,
#         "Dynamic_Pricing_Multiplier": 1.44
#     }

# @app.post("/price-calculator")
# def price_calculator(input_data: PriceCalculatorInput):
#     dynamic_values = get_dynamic_values()
#     new_data = {
#         'Day_of_Week': [dynamic_values["Day_of_Week"]],
#         'Month': [dynamic_values["Month"]],
#         'Working_Hours': [input_data.Working_Hours],  
#         'Crop_Type': [input_data.Crop_Type], 
#         'Base_Hourly_Wage': [dynamic_values["Base_Hourly_Wage"]], 
#         'Supply_Demand_Ratio': [dynamic_values["Supply_Demand_Ratio"]],  
#         'Dynamic_Pricing_Multiplier': [dynamic_values["Dynamic_Pricing_Multiplier"]]
#     }
#     new_input_df = pd.DataFrame(new_data)

#     with open('ann_model.pkl', 'rb') as file:
#         loaded_model = pickle.load(file)
#     predicted_price = loaded_model.predict(new_input_df)

#     return {
#         "Crop_Type": input_data.Crop_Type,
#         "Calculated_Price": predicted_price.tolist(),  # Convert numpy array to list for JSON serialization
#         "Day_of_Week": dynamic_values["Day_of_Week"],
#         "Month": dynamic_values["Month"]
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import pandas as pd
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class PriceCalculatorInput(BaseModel):
    Working_Hours: int
    Crop_Type: str
    Count: int  # How many times to calculate the price

def get_dynamic_values():
    now = datetime.now()
    return {
        "Day_of_Week": now.weekday(),
        "Month": now.month,
        "Base_Hourly_Wage": 12.00,
        "Supply_Demand_Ratio": 1.2,
        "Dynamic_Pricing_Multiplier": 1.44
    }

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/price-calculator/")
def price_calculator(input_data: PriceCalculatorInput):
    dynamic_values = get_dynamic_values()
    total_price = 0  # Initialize total price to sum up all calculations

    for _ in range(input_data.Count):
        new_data = {
            'Day_of_Week': [dynamic_values["Day_of_Week"]],
            'Month': [dynamic_values["Month"]],
            'Working_Hours': [input_data.Working_Hours],  
            'Crop_Type': [input_data.Crop_Type], 
            'Base_Hourly_Wage': [dynamic_values["Base_Hourly_Wage"]], 
            'Supply_Demand_Ratio': [dynamic_values["Supply_Demand_Ratio"]],  
            'Dynamic_Pricing_Multiplier': [dynamic_values["Dynamic_Pricing_Multiplier"]]
        }
        new_input_df = pd.DataFrame(new_data)

        with open('ann_model.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        predicted_price = loaded_model.predict(new_input_df)
        total_price += predicted_price[0]  # Sum the predicted prices

    return {
        "Crop_Type": input_data.Crop_Type,
        "Total_Calculated_Price": 
        
        total_price,
        "Number_of_Calculations": input_data.Count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
