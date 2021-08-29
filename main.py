import os

from RevolutBudget.dash_app.app import RevolutBudgetDashApp

if __name__ == '__main__':
    print(os.getenv('PORT'))
    app = RevolutBudgetDashApp()
    app.run()
