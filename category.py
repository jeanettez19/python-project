import pandas as pd
import sys


class Category:
    __filepath = './data/Categories.xlsx'  # Default file path
    __category_df = pd.DataFrame({
        "category_id": [],
        "category_name": []
    })  # Default empty df

    @classmethod
    def initialize(cls, excel_file):
        cls.__filepath = excel_file
        # Read Excel file and find max id in the given col
        try:
            cls.__category_df = pd.read_excel(excel_file)

        except FileNotFoundError:
            print(f"{excel_file} does not exist... Creating new file")
            cls.__category_df.to_excel(excel_file,
                                       index=False)

        except PermissionError:
            print(
                f"Permission denied to read {excel_file}, please close the file before proceeding."
            )
            sys.exit(1)

        except Exception as e:
            print(f"Error reading file: {e}")
        # Return a new instance of the class
        return cls()

    def __init__(self):
        self.__filepath = Category.__filepath
        self.__category_df = pd.DataFrame({
        "category_id": ["1","2","3","4","5","6","7","8"],
        "category_name": ["Salary","Food","Investments","Transportation"
                          ,"Utilities","Freelance","Others","Rent"]
    })  # Default empty df

    def display_info(self):
        print(
            f"These are your current categories: \n\n{self.__category_df.to_string(index=False)}"
        )

    def get_category(self, category_id):
        try:
            # Ensure category_id is an integer
            if not isinstance(category_id, int):
                raise TypeError(
                    f"Category ID must be an integer, got {type(category_id).__name__}."
                )

            # Check if the category_id exists in the 'category_id' column
            if category_id in self.__category_df['category_id'].values:
                # Filter the DataFrame and return the corresponding 'category_name'
                return self.__category_df.loc[
                    self.__category_df['category_id'] == category_id,
                    'category_name'].iloc[0]
            else:
                raise ValueError(
                    f"Category ID {category_id} does not exist in the 'category_id' column."
                )
        except Exception as e:
            # Handle any unexpected errors
            raise RuntimeError(
                f"An error occurred while retrieving the category: {e}")

    def create_category(self, category_name):
        new_row = pd.DataFrame({
            "category_id": [
                self.__category_df['category_id'].max() +
                1 if not self.__category_df.empty else 1
            ],
            "category_name": [category_name]
        })
        self.__category_df = pd.concat([self.__category_df, new_row],
                                       ignore_index=True)
        # Try saving to an Excel file
        try:
            self.__category_df.to_excel(self.__filepath,
                                        index=False)
            # with pd.ExcelWriter(self.__filepath) as writer:
            #     # Write each DataFrame to its respective sheet
            #     for sheet_name, data in self.__category_df.items():
            #         data.to_excel(writer, index=False)
            print("File saved successfully.")
        except Exception as e:
            print(f"Error writing to Excel file: {e}")

    def create_category_process(self):
        self.display_info()

        while True:
            # Prompt the user to enter a new category name
            category_name = input(
                "Enter new category name (3-20 characters, first letter capitalized): "
            )

            # Validate the input
            if len(category_name) < 3 or len(category_name) > 20:
                print(
                    "Error: Category name must be between 3 and 20 characters. Please try again."
                )
                continue
            if not category_name[0].isupper():
                print(
                    "Error: The first letter of the category name must be capitalized. Please try again."
                )
                continue
            if not category_name.isalpha():
                print(
                    "Error: Category name must contain only alphabetic characters. Please try again."
                )
                continue

            # If valid, create the category
            self.create_category(category_name)
            print("Successfully added new category!!! \n\n")
            self.display_info()
            break

    def delete_category(self):
        while True:
            try:
                print("Here are the current Categories: ")
                self.display_info()
                print("")
                # Prompt the user to enter a new category name
                selected_category_id = int(input("Enter the category ID to delete: "))
                if selected_category_id in self.__category_df['category_id'].values:
                    delete_confirmation = input("Are you sure you want to delete this category? (y/n): ")
                    if delete_confirmation.lower() == 'y':
                        new_df = self.__category_df
                        new_df.drop((selected_category_id-1), inplace=True)
                        new_df.to_excel(self.__filepath,index=False)
                        print("Successfully deleted category! 🎉\n")
                        self.display_info()
                        break
                    elif delete_confirmation.lower() == 'n':
                        print("Category deletion cancelled.")
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                        continue
                else:
                    print("Invalid category ID. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid category ID.")
                continue
            
                        

# Initialize the _id_counter using data from the Excel file
# cat = Category()
# cat = Category.initialize('./data/Categories.xlsx')
# cat.display_info()
# Create a Category instance
# cat.create_category_process()
# cat.delete_category()
