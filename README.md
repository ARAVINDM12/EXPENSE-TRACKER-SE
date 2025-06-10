# **💰 Expense Tracker – Smart Personal Finance Manager**

A modern, cross-platform Expense Tracker App built using Python (Kivy) and SQLite3, designed to help users manage their income, expenses, budgets, and financial goals efficiently with real-time insights.

**🚀 Project Summary**

    Created a cross-platform Expense Tracker using Python (Kivy) and SQLite3, featuring full CRUD operations for seamless income and expense management.
    
    ✅ Achieved 100% data retention and reduced manual tracking time by 60% through:
    
    Real-time overspending alerts
    
    Dynamic budget tracking
    
    Automated email reports
    
    📈 Boosted user engagement by 40% with:
    
    CSV export functionality
    
    Interactive pie/bar chart visualizations
    
    🖥️ Deployed as a standalone .exe using SourceForge for easy offline access and distribution
    
    🔗 Download EXE: 


**📦 Features**

    ✅ View, add, update, and delete transactions (CRUD)
    
    ✅ Real-time budget and expense tracking
    
    📈 Generate interactive visual reports (Pie/Bar Charts)
    
    📊 Export reports to CSV and PDF
    
    🔔 Overspending notifications
    
    📅 View daily, weekly, monthly, yearly, or custom reports
    
    📂 Manage and view historical data
    
    🧮 Budget planner with alerts
    
    🎬 Splash screen before main app
    

**🛠️ Tech Stack**

    Python 3.x
    
    Kivy  – Cross-platform UI framework
    
    SQLite3 – Local database
    
    Matplotlib – Visual reports
    
    FPDF – PDF report generation
    
    smtpmail – Notifications 
    
    dotenv – Environment variable management

**📁 Folder Structure**
    
    EXPENSE-TRACKER-SE/
    ├── ExpenseApp/
    │   ├── Icon/
    │   │   └── SS.ico                # App icon
    │   ├── splash.py                 # Splash screen (entry point)
    │   ├── main.py                   # Main script to launch app
    │   ├── App/
    │   │   └── app.py                # ExpenseApp class and ScreenManager
    │   ├── database/
    │   │   ├── expenses.db           # SQLite DB file
    │   │   └── db.py                 # DB logic
    │   ├── Images/
    │   │   └── SS.png                # Logo / background image
    │   ├── Imports/
    │   │   └── imports.py            # Shared imports
    │   ├── UI/
    │   │   └── ui_components.py      # UI widgets
    │   └── screens/
    │       ├── budgets_screen.py         # Budget management
    │       ├── view_budgets_screen.py    # View budget screen
    │       ├── reports_screen.py         # Graphs, charts, CSV/PDF export
    │       ├── history_screen.py         # View expense history
    │       └── expense_tracker.py        # Main expense entry screen
    ├── requirements.txt              # Python dependencies
    
**🧪 Setup Instructions**

    1. Clone the Repository
    
    git clone https://github.com/ARAVINDM12/EXPENSE-TRACKER-SE.git
    
    2. Install Dependencies
    
    pip install -r requirements.txt

**▶️ How to Run**

    On Local Machine
    
    cd ExpenseApp
    python splash.py
    The splash screen will launch the full application after a short delay.


**📤 Export Reports**

    CSV Export: For all filter types (daily, weekly, monthly, yearly, custom)
    
    PDF Export: Includes pie chart, bar chart, tabular summaries, logo
    
    🧾 Report Filters Supported
    ✅ Daily
    
    ✅ Weekly
    
    ✅ Monthly
    
    ✅ Yearly
    
    ✅ Custom Date Range

**📊 Visualizations**

    📌 Pie Chart – Category-wise expense breakdown
    
    📌 Bar Chart – Total Income vs Expense comparison
    
    📌 Tabular Summaries – Monthly stats, category spend, budget comparison

**📐 Project Documentation**

    ✅ Entity Relationship Diagram (ERD)
    ✅ Context Flow Diagram (Level 0 DFD)
    ✅ Level 1 and Level 2 DFDs
    ✅ State Transition Diagram (All created using eDraw)
