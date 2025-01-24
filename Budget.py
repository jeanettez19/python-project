#Budget
import pandas as pd
from datetime import datetime

class Budget:
  __budget_df = pd.DataFrame({"budget_id":[],"date":[],"category":[],"monthly_budget":[]}) # Default empty df

  @classmethod
  def initialize(cls,excel_file):
    # Read Excel file and find max id in the given col
    try:
      cls.__budget_df = pd.read_excel(excel_file)

    except FileNotFoundError:
      print(f"{excel_file} does not exist... Creating new file")
      cls.__budget_df.to_excel(excel_file, index=False)

    except PermissionError:
      print(f"Permission denied to read {excel_file}, please close the file before proceeding.")
      sys.exit(1)

    except Exception as e:
      print(f"Error reading file: {e}")
    # Return a new instance of the class
    return cls()



  def __init__(self):
    self.__budget_df = Budget.__budget_df

  def display_info(self):
    print(f"These are your current budgets for each category: \n\n{self.__budget_df.to_string(index=False)}")


  def create_budget(self,date,category_name,monthly_budget):
    new_row = pd.DataFrame({
    "budget_id": [self.__category_df['budget_id'].max() + 1 if not self.__budget_df.empty else 1],
    "date":[date],
    "category":[category_name],
    "monthly_budget": [monthly_budget]
    })
    self.__budget_df = pd.concat([self.__budget_df, new_row], ignore_index=True)
    try:
      self.__budget_df.to_excel('Budget.xlsx',index=False)
    except Exception as e:
      print(f"Error writing file: {e}")

  def get_budget(self, budget_id):
      try:
          # Ensure budget_id is an integer
          if not isinstance(budget_id, int):
              raise TypeError(f"Budget ID must be an integer, got {type(budget_id).__name__}.")

          # Check if the budget_id exists in the 'budget_id' column
          if budget_id in self.__budget_df['budget_id'].values:
              # Filter the DataFrame and return the corresponding 'monthly_budget'
              budget = self.__budget_df.loc[self.__budget_df['budget_id'] == budget_id, 'monthly_budget'].iloc[0]

              # Validate that the budget is a valid number (non-negative)
              if not isinstance(budget, (int, float)) or budget < 0:
                  raise ValueError(f"Invalid budget value for budget ID {budget_id}: {budget}.")

              return budget
          else:
              raise ValueError(f"Budget ID {budget_id} does not exist in the 'budget_id' column.")
      except Exception as e:
          # Handle any unexpected errors
          raise RuntimeError(f"An error occurred while retrieving the budget: {e}")



  def create_budget_process(self):
    self.display_info()
    while True:
      date = input("Budget Date (DD-MM-YYYY) :")
      current_date = datetime.now()
      try:
          datetime.strptime(date, "%d-%m-%Y")
          if datetime.strptime(date, "%d-%m-%Y") < current_date:
            break
          else:
             print("Date entered is in the future. Please enter a valid date")
      except ValueError:
          print("Invalid date format. Please enter the date in DD-MM-YYYY format")
    monthly_budget = input("Enter new monthly budget: ")
    category_name = input("Enter new category name: ")
    self.create_budget(date,category_name,monthly_budget)
    print("Successfully added new budget!!! \n\n")
    self.display_info()

