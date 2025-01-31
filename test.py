from budget import Budget

bud = Budget.initialize("./data/budgets.xlsx","./data/categories.xlsx")

bud.create_budget_process()
bud.delete_budget_process()
bud.update_budget_process()