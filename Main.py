from Transactions import Transaction

def main():
    print("Welcome to the Expense Tracker!")

    print(f"Hello! What would you like to do")

    while True:
        # Menu options
        print("\nMenu:")
        print("1. Manage Budget")
        print("2. Add Transaction")
        print("3. Others")
        print("0. Quit")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            # Manage Budget
            print("Yet to implement manage budget")

        elif choice == "2":
            # Add Transaction
            print("What would you like to do?")
            while True:
                print("1. Manage Income")
                print("2. Manage expenses")
                print("0. Quit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    Transaction.add_transaction("Income")
                    break
                elif choice == "2":
                    Transaction.add_transaction("Expenses")
                    break
                elif choice == "0":
                    break
                else:
                    print("Invalid choice. Please select a valid option.")

        elif choice == "3":
            print("Yet to implement others")

        elif choice == "0":
            print("Thank you for using the Expense Tracker.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

main()