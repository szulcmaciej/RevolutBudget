from RevolutBudget.dash_app.app import RevolutBudgetDashApp


revolut_budget_app = RevolutBudgetDashApp()
server = revolut_budget_app.dash_app.server
revolut_budget_app.run()
