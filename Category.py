#category
import pandas as pd
# Generates a dict & df of categories then saves it
category_dict = {'category_name':['Salary','Food','Entertainment','Transport']}
category_df = pd.DataFrame(data=category_dict)

# Add a category_id column
category_df['category_id'] = range(1, len(category_df) + 1)

# Set category_id as the index
category_df.set_index('category_id', inplace=True)
category_df.to_excel('Categories.xlsx')

# Reads excel
category_df = pd.read_excel('Categories.xlsx')
category_df

class Category:
  __category_df = pd.DataFrame({"category_id":[],"category_name":[]}) # Default empty df

  @classmethod
  def initialize(cls,excel_file):
    # Read Excel file and find max id in the given col
    try:
      cls.__category_df = pd.read_excel(excel_file)

    except FileNotFoundError:
      print(f"{excel_file} does not exist... Creating new file")
      cls.__category_df.to_excel(excel_file, index=False)

    except PermissionError:
      print(f"Permission denied to read {excel_file}, please close the file before proceeding.")
      sys.exit(1)

    except Exception as e:
      print(f"Error reading file: {e}")
    # Return a new instance of the class
    return cls()



  def __init__(self):
    self.__category_df = Category.__category_df

  def display_info(self):
    print(f"These are your current categories: \n\n{self.__category_df.to_string(index=False)}")

  def get_category(self, category_id):
      try:
          # Ensure category_id is an integer
          if not isinstance(category_id, int):
              raise TypeError(f"Category ID must be an integer, got {type(category_id).__name__}.")

          # Check if the category_id exists in the 'category_id' column
          if category_id in self.__category_df['category_id'].values:
              # Filter the DataFrame and return the corresponding 'category_name'
              return self.__category_df.loc[self.__category_df['category_id'] == category_id, 'category_name'].iloc[0]
          else:
              raise ValueError(f"Category ID {category_id} does not exist in the 'category_id' column.")
      except Exception as e:
          # Handle any unexpected errors
          raise RuntimeError(f"An error occurred while retrieving the category: {e}")



  def create_category(self,category_name):
    new_row = pd.DataFrame({
    "category_id": [self.__category_df['category_id'].max() + 1 if not self.__category_df.empty else 1],
    "category_name": [category_name]
    })
    self.__category_df = pd.concat([self.__category_df, new_row], ignore_index=True)
    try:
      self.__category_df.to_excel('drive/MyDrive/Colab Notebooks/Categories.xlsx',index=False)
    except Exception as e:
      print(f"Error writing file: {e}")

  def create_category_process(self):
    self.display_info()
    category_name = input("Enter new category name: ")
    self.create_category(category_name)
    print("Successfully added new category!!! \n\n")
    self.display_info()

