import pandas as pd
from datetime import datetime
import sys
from Category import Category
class Budget:
  __budget_df = pd.DataFrame({"budget_id":[],"date":[],"category":[],"category_id":[],"monthly_budget":[]}) # Default empty df
  __filepath = './data/budget.xlsx' # Default file path
  __cat_file_path = './data/Categories.xlsx' # Default file path
  @classmethod
  def initialize(cls,excel_file,cat_file_path):
    # Read Excel file and find max id in the given col
    try:
      cls.__filepath = excel_file
      cls.__cat_file_path = cat_file_path
      cls.__budget_df = pd.read_excel(excel_file)
    except FileNotFoundError:
      print(f"{excel_file} does not exist... Creating new file")
      cls.__budget_df.to_excel(excel_file,sheet_name='budget' ,index=False)

    except PermissionError:
      print(f"Permission denied to read {excel_file}, please close the file before proceeding.")
      sys.exit(1)

    except Exception as e:
      print(f"Error reading file: {e}")
    # Return a new instance of the class
    return cls()



  def __init__(self):
    self.__budget_df = Budget.__budget_df
    try:
      self.cat = Category.initialize(self.__cat_file_path)
    except Exception as e:
      print(f"Error reading file: {e}")

  def display_info(self):
    print(f"These are your current budgets for each category: \n\n{self.__budget_df.to_string(index=False)}")


  def create_budget(self,date,category_id,monthly_budget):


    try:
      category_id = int(category_id)
    except ValueError as e:
      raise TypeError(f"Category ID must be an integer or convertible to an integer, got {type(category_id).__name__}.")
      return


    try:
      # Ensure cat_id is an integer
      if not isinstance(category_id, int):
        raise TypeError(f"Category ID must be an integer, got {type(category_id).__name__}.")

        # Check if the budget_id exists in the 'budget_id' column
      if self.cat.get_category(category_id):
        new_row = pd.DataFrame({
        "budget_id": [self.__budget_df['budget_id'].max() + 1 if not self.__budget_df.empty else 1],
        "date":[datetime.strptime(date, "%d-%m-%Y").replace(hour=0, minute=0, second=0)],
        "category": [self.cat.get_category(category_id)],
        "category_id":[category_id],
        "monthly_budget": [monthly_budget]
        })
        self.__budget_df = pd.concat([self.__budget_df, new_row], ignore_index=True)
            # Try saving to an Excel file
        try:
            self.__budget_df.to_excel(self.__filepath, index=False)
            print("File saved successfully.")
        except Exception as e:
            print(f"Error writing to Excel file: {e}")
      else:
          raise ValueError(f"Category ID {category_id} does not exist in the 'Category_ID' column.")
    except Exception as e:
          # Handle any unexpected errors
          raise RuntimeError(f"An error occurred while retrieving the budget: {e}")




  def update_budget(self, budget_id, category_id,new_monthly_budget):
      try:
          # Ensure budget_id is an integer
          if not isinstance(budget_id, int):
              raise TypeError(f"Budget ID must be an integer, got {type(budget_id).__name__}.")

          # Ensure the new monthly budget is a valid number
          if not isinstance(new_monthly_budget, (int, float)) or new_monthly_budget < 0:
              raise ValueError(f"New monthly budget must be a non-negative number, got {new_monthly_budget}.")

          # Check if the budget_id exists in the 'budget_id' column
          if budget_id in self.__budget_df['budget_id'].values:
              # Update the monthly budget for the matching budget_id
              self.__budget_df.loc[self.__budget_df['budget_id'] == budget_id, 'monthly_budget'] = new_monthly_budget
              self.__budget_df.loc[self.__budget_df['budget_id'] == budget_id, 'category'] = self.cat.get_category(category_id)
              self.__budget_df.loc[self.__budget_df['budget_id'] == budget_id, 'category_id'] = category_id
              return True
          else:
              raise ValueError(f"Budget ID {budget_id} does not exist in the 'budget_id' column.")
      except Exception as e:
          # Handle any unexpected errors
          raise RuntimeError(f"An error occurred while updating the budget: {e}")
        
  def update_budget_process(self):
    self.display_info()
    while True:
      try:
        budget_id = int(input("Enter the budget ID to update: "))
        new_monthly_budget = float(input(f"Enter the new monthly budget: "))
        category_id = int(input("Enter the category ID: "))
        updated_status=self.update_budget(budget_id,category_id,new_monthly_budget)
        if updated_status:
          print("Successfully updated budget! 🎉\n")
          self.display_info()
          # Try saving to an Excel file
          try:
              self.__budget_df.to_excel(self.__filepath, index=False)
              print("File saved successfully.")
          except Exception as e:
              print(f"Error writing to Excel file: {e}")
          break
        else:
          print("Please enter a valid budget ID")
      except ValueError:
        print("Invalid input. Please enter a valid budget ID.")
      except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")



  def delete_budget(self, budget_id):
      try:
          # Ensure budget_id is an integer
          if not isinstance(budget_id, int):
              raise TypeError(f"Budget ID must be an integer, got {type(budget_id).__name__}.")
          
          # Check if the 'budget_id' column exists in the DataFrame
          if 'budget_id' not in self.__budget_df.columns:
              raise KeyError("'budget_id' column is missing in the budget DataFrame.")
  
          # Find the index of the row where 'budget_id' matches the given budget_id
          budget_row = self.__budget_df[self.__budget_df['budget_id'] == budget_id]
          
          if budget_row.empty:
              raise ValueError(f"Budget ID {budget_id} does not exist in the 'budget_id' column.")
          
          # Drop the row with the matching 'budget_id'
          self.__budget_df.drop(budget_row.index, inplace=True)          
          return True
  
      except TypeError as e:
          raise RuntimeError(f"Invalid input type: {e}")
      except KeyError as e:
          raise RuntimeError(f"Missing column in DataFrame: {e}")
      except ValueError as e:
          raise RuntimeError(f"Budget ID error: {e}")
      except Exception as e:
          # Catch any other unexpected errors
          raise RuntimeError(f"An error occurred while deleting the budget: {e}")


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

  def delete_budget_process(self):
    self.display_info()
    while True:
      try:
        budget_id = int(input("Enter the budget ID to delete: "))
        deleted_status=self.delete_budget(budget_id)
        if deleted_status:
          print("Successfully deleted budget! 🎉\n")
          self.display_info()
          # Try saving to an Excel file
          try:
              self.__budget_df.to_excel(self.__filepath, index=False)
              print("File saved successfully.")
          except Exception as e:
              print(f"Error writing to Excel file: {e}")
          break
        else:
          print("Please enter a valid budget ID")
      except ValueError:
        print("Invalid input. Please enter a valid budget ID.")
      except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")

  def create_budget_process(self):
    self.display_info()

    try:
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

      while True:
          try:
              monthly_budget = float(input(f"monthly_budget: "))
              if monthly_budget <= 0:
                  print("monthly_budget must be greater than 0. Please enter monthly_budget again")
              elif len(str(monthly_budget).split(".")[1]) > 2:
                    print("monthly_budget can have at most two decimal places. Please enter monthly_budget again")
              else:
                  break
          except ValueError:
              print("invalid input. PLease enter numeric values")

      while True:
          try:
              # Prompt user for category ID input
              category_id = input("Enter new category ID: ")

              # Attempt to convert the input to an integer
              category_id = int(category_id)

              # Initialize the Category class
              cat = Category.initialize(self.__cat_file_path)

              # Check if the category exists
              cat_row = cat.get_category(category_id)
              if cat_row:
                  print("Valid category ID entered.")
                  break  # Exit the loop if a valid category ID is found
              else:
                  print("Invalid category ID. Please enter a valid category ID.")
          except ValueError:
              print("Invalid input. Category ID must be an integer. Please try again.")
          except Exception as e:
              print(f"An unexpected error occurred: {e}")

    except Exception as e:
      print(f"An error occured: {e}")

    self.create_budget(date,category_id,monthly_budget)
    print("Successfully added new budget!!! \n\n")
    self.display_info()
    
    

# Initialize the budget using data from the Excel file
# budget = Budget.initialize('./data/budget.xlsx')
# Create a Category instance
# budget.create_budget_process()
# budget.delete_budget_process()
