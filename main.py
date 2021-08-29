import os

from RevolutBudget.dash_app.app import RevolutBudgetDashApp

if __name__ == '__main__':
    revolut_budget_app = RevolutBudgetDashApp()
    server = revolut_budget_app.dash_app.server
    revolut_budget_app.run()
