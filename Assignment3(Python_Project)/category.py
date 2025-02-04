# Importing required libraries
import pandas as pd
import sys

# Creating a Class Category
class Category:
    """
    This class is used to manage the categories of expenses in the Expense Tracker.

    Attributes:
    __filepath (str): The file path of the Excel file that contains the categories.
    __category_df (pd.DataFrame): The DataFrame that stores the categories.
    """
    __filepath = './data/Categories.xlsx'  # Default file path
    __category_df = pd.DataFrame({
        "category_id": [],
        "category_name": []
    })  # Default empty df

    @classmethod

    # Function to Intialise the Class
    def initialize(cls, excel_file):
        """
        This class method initializes the Category class by reading the Excel file and creating 
        a new instance of the class.

        Args:
            excel_file (str): The file path of the Excel file that contains the categories.

        Returns:
            Category: A new instance of the Category class.
        """
        cls.__filepath = excel_file

        # Read Excel file and find max id in the given col
        try:
            cls.__category_df = pd.read_excel(excel_file)
        except FileNotFoundError:
            print(f"{excel_file} does not exist... Creating new file")
            cls.__category_df.to_excel(excel_file, index=False)
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
        """The constructor for the Category class."""
        self.__filepath = Category.__filepath
        self.__category_df = Category.__category_df

    # Function to Display Information
    def display_info(self):
        """This method displays the current categories in the Category class."""
        print(
            f"These are your current categories: \n\n{self.__category_df.to_string(index=False)}"
        )

    # Function to Get Category
    def get_category(self, category_id):
        """Retrieve the category_name by category_id"""
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

    # Function to Get Category ID by name
    def get_category_id_by_name(self, category_name):
        """Retrieve the category_id by category_name"""
        try:
            # Ensure category_name is a string
            if not isinstance(category_name, str):
                raise TypeError(
                    f"Category name must be a string, got {type(category_name).__name__}."
                )

            # Check if the category_name exists in the 'category_name' column
            if category_name in self.__category_df['category_name'].values:
                # Filter the DataFrame and return the corresponding 'category_id'
                return self.__category_df.loc[
                    self.__category_df['category_name'] == category_name,
                    'category_id'].iloc[0]
            else:
                raise ValueError(
                    f"Category name '{category_name}' does not exist in the 'category_name' column."
                )
        except Exception as e:
            # Handle any unexpected errors
            raise RuntimeError(
                f"An error occurred while retrieving the category ID: {e}")

    # Function to Create Category
    def create_category(self, category_name):
        """
        This method creates a new category with the given name and adds it to the Category class.

        Args:
            category_name (str): The name of the new category to be created.
        """
        new_row = pd.DataFrame({
            "category_id": [
                self.__category_df['category_id'].max() + 1
                if not self.__category_df.empty else 1
            ],
            "category_name": [category_name]
        })
        self.__category_df = pd.concat([self.__category_df, new_row],
                                       ignore_index=True)
        
        # Try saving to an Excel file
        try:
            self.__category_df.to_excel(self.__filepath, index=False)
            print("File saved successfully.")
        except Exception as e:
            print(f"Error writing to Excel file: {e}")

    def create_category_process(self):
        """This method is used to create a new category and add it to the Category class."""
        self.display_info()

        while True:

            # Prompt the user to enter a new category name
            category_name = input(
                "Enter new category name (3-20 characters, first letter capitalized): "
            )

            # Validate the inputs
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

    # Function to Delete Category
    def delete_category(self):
        """This method is used to delete a category from the Category class."""
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
                        new_df.drop((selected_category_id - 1), inplace=True)
                        new_df.to_excel(self.__filepath, index=False)
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