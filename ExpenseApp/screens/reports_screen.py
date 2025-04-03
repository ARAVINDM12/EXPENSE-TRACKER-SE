from Imports.imports import *
from UI.ui_components import *
from database.db import conn, cursor

class ReportsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    
        # Main Vertical Layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title Label (Always on top)
        main_layout.add_widget(Label(text="EXPENSE REPORTS", font_size=24, bold=True, size_hint_y=None, height=75))

        # Charts Box (STRICTLY HALF THE SCREEN)
        self.chart_container = BoxLayout(orientation='horizontal', size_hint_y=0.4, spacing=10)
        main_layout.add_widget(self.chart_container)

        # Summary Layout (Centered, fills remaining space)
        self.summary_layout = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=0.2)
        main_layout.add_widget(self.summary_layout)

        # Lower Section (Filters + Buttons)
        lower_section = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=10)
        

        # Filters Layout (Period Selection & Date Inputs)
        filter_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)

        # Report Type Dropdown (Half Width)
        self.report_type = ModernSpinner(
            text="Daily",
            values=("Daily", "Weekly", "Monthly", "Yearly", "Custom"),
            size_hint=(0.5, None),
            size=(120, 50)
        )
        filter_layout.add_widget(self.report_type)
        self.report_type.bind(text=self.on_report_type_change)

        # Custom Date Inputs (Evenly Split Other Half)
        date_inputs_layout = BoxLayout(size_hint=(0.5, None), height=40, spacing=10)
        self.start_date_input = TextInput(hint_text="Start Date (YYYY-MM-DD)", size_hint=(0.5, None), size=(140, 50))
        self.end_date_input = TextInput(hint_text="End Date (YYYY-MM-DD)", size_hint=(0.5, None), size=(140, 50))
        self.start_date_input.disabled = True
        self.end_date_input.disabled = True
        date_inputs_layout.add_widget(self.start_date_input)
        date_inputs_layout.add_widget(self.end_date_input)
        filter_layout.add_widget(date_inputs_layout)

        lower_section.add_widget(filter_layout)

        # Button Layout (More Evenly Spaced)
        button_layout = GridLayout(cols=3, spacing=10, size_hint_y=None, height=50)

        # Generate Reports Button
        self.generate_button = Button(text="Generate Report", background_color=(0, 0, 0, 1))
        self.generate_button.bind(on_press=self.generate_reports)
        button_layout.add_widget(self.generate_button)

        # Export CSV Button
        csv_button = Button(text="Export CSV", background_color=(0, 0, 0, 1))
        csv_button.bind(on_press=self.export_csv)
        button_layout.add_widget(csv_button)

        # Export PDF Button
        pdf_button = Button(text="Export PDF", background_color=(0, 0, 0, 1))
        pdf_button.bind(on_press=self.export_pdf)
        button_layout.add_widget(pdf_button)

        lower_section.add_widget(button_layout)

        # Back Button (Smaller Height)
        back_button = Button(text="Back", size_hint_x=1, size_hint_y=None, height=50, background_color=(1, 0, 0, 1))
        back_button.bind(on_press=self.go_back)
        lower_section.add_widget(back_button)

        main_layout.add_widget(lower_section)
        self.add_widget(main_layout)

    
        # Generate default daily report
        self.generate_reports(None)

    def on_report_type_change(self, spinner, text):
        if text == "Custom":
            self.start_date_input.disabled = False
            self.end_date_input.disabled = False
        else:
            self.start_date_input.disabled = True
            self.end_date_input.disabled = True

    def generate_reports(self, instance):
        self.chart_container.clear_widgets()
        self.summary_layout.clear_widgets()

        report_type = self.report_type.text
        start_date = self.start_date_input.text
        end_date = self.end_date_input.text
        data = self.fetch_expense_data(report_type, start_date, end_date)

        if data:
            pie_chart, bar_chart = self.create_charts(data)
            self.chart_container.add_widget(FigureCanvasKivyAgg(pie_chart))
            self.chart_container.add_widget(FigureCanvasKivyAgg(bar_chart))

            pie_summary = self.generate_pie_summary(data)
            bar_summary = self.generate_bar_summary(data)

            # Layout for Summary Boxes
            summaries_box = BoxLayout(orientation='horizontal', spacing=00, padding=(10, 00, 10, 0))

            # Pie Chart Summary Grid
            pie_grid = GridLayout(cols=1, spacing=0, size_hint_x=0.5, padding=(10, 0))

            # Bar Chart Summary Grid
            bar_grid = GridLayout(cols=1, spacing=0, size_hint_x=0.5, padding=(10, 0))

            # Pie Chart Summary Title
            pie_label = Label(text="[b][size=20]Pie Chart Summary[/size][/b]", markup=True, halign='center', size_hint_y=None, height=40)
            pie_grid.add_widget(pie_label)

            # Horizontal Divider
            pie_grid.add_widget(Label(text="--------------------------------------", bold=True, size_hint_y=None, height=20))

            for line in pie_summary.split('\n'):
                if line:
                    category, value_percentage = line.split(': ', 1) if ': ' in line else ("", line)
                    label = Label(text=f"[b]{category}:[/b] {value_percentage}", markup=True, halign='left', valign='middle', size_hint_y=None, height=30)
                    pie_grid.add_widget(label)

            # Bar Chart Summary Title
            bar_label = Label(text="[b][size=20]Bar Chart Summary[/size][/b]", markup=True, halign='center', size_hint_y=None, height=40)
            bar_grid.add_widget(bar_label)

            # Horizontal Divider
            bar_grid.add_widget(Label(text="--------------------------------------", bold=True, size_hint_y=None, height=20))

            for line in bar_summary.split('\n'):
                if line.strip():  # Ensure line is not empty
                    if ': ' in line:
                        category, value_percentage = line.split(': ', 1)
                        label_text = f"[b]{category}:[/b] {value_percentage}"
                    else:
                        label_text = f"[b]{line}[/b]"  # Display without extra colon
                    
                    label = Label(text=label_text, markup=True, halign='left', valign='middle', size_hint_y=None, height=30)
                    bar_grid.add_widget(label)


            # Add Grids to the Summary Box
            summaries_box.add_widget(pie_grid)
            summaries_box.add_widget(bar_grid)

            # Add Spacing & Summaries to Layout
            spacer = Label(size_hint_y=None, height=40)
            self.summary_layout.add_widget(spacer)
            self.summary_layout.add_widget(summaries_box)

            # Adjust height based on content
            self.summary_layout.height = self.summary_layout.minimum_height

        else:
            popup = Popup(title="No Data", content=Label(text="No expenses found for the selected period."), size_hint=(0.6, 0.3))
            popup.open()

    def generate_pie_summary(self, data):
        if not data:
            return "No pie chart data available."

        total_expenses = sum(amount for _, amount in data)
        category_summaries = ""

        for category, amount in data:
            percentage = (amount / total_expenses) * 100
            category_summaries += f"{category}: [b]{amount:.2f} ({percentage:.2f}%)[/b]\n"

        return f"{category_summaries}"

    def generate_bar_summary(self, data):
        if not data:
            return "No bar chart data available."

        total_expenses = sum(amount for _, amount in data)
        income = total_expenses * 1.2
        expense = total_expenses

        income_percentage = (income / (income + expense)) * 100
        expense_percentage = (expense / (income + expense)) * 100

        return f"[b]Total Income:[/b] {income:.2f} ({income_percentage:.2f}%)\n[b]Total Expense:[/b] {expense:.2f} ({expense_percentage:.2f}%)"
    
    def fetch_expense_data(self, report_type, start_date, end_date):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        query = """
        SELECT category, SUM(amount)
        FROM expenses
        WHERE date BETWEEN ? AND ?
        GROUP BY category
        ORDER BY category ASC
        """
        if report_type == "Daily":
            start_date = end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Weekly":
            start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Monthly":
            start_date = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Yearly":
            start_date = (datetime.date.today().replace(month=1, day=1)).strftime("%Y-%m-%d")
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Custom":
            if not start_date or not end_date:
                return None

        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()
        conn.close()
        return data

    def create_charts(self, data):
        categories, values = zip(*data) if data else ([], [])

        # Pie Chart with Black Background and White Text
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, textprops={'color': 'white'})  # White text
        ax1.set_title("Category-wise Expense Breakdown", color='white')  # White title
        ax1.set_facecolor('#262626')  # Black background
        fig1.patch.set_facecolor('#262626')  # Black figure background

        # Bar Chart with Black Background and White Text
        fig2, ax2 = plt.subplots()
        ax2.bar(["Total Income", "Total Expense"], [sum(values) * 1.2, sum(values)], color=["green", "red"])
        ax2.set_title("Total Income vs Expense", color='white')  # White title
        ax2.set_facecolor('#262626')  # Black background
        fig2.patch.set_facecolor('#262626')  # Black figure background

        # Set tick and axis label colors to white
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        ax2.xaxis.label.set_color('white')
        ax2.yaxis.label.set_color('white')

        return fig1, fig2

    def export_csv(self, instance):
        report_type = self.report_type.text
        start_date = self.start_date_input.text
        end_date = self.end_date_input.text
        data = self.fetch_expense_data(report_type, start_date, end_date)  # Fetch the data

        if data:
            # 1. Determine the filename
            filename = f"expense_report_{report_type}_{start_date}_{end_date}.csv"  # Example filename

            # 2. Open the CSV file in write mode
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # 3. Write the header row (if needed)
                if report_type == "category":  # Example: Add header for category report
                    writer.writerow(["Category", "Amount", "Percentage"])
                elif report_type == "income_vs_expense":
                    writer.writerow(["Type", "Amount", "Percentage"])

                # 4. Write the data rows
                for row in data:
                    writer.writerow(row)  # Assuming 'data' is a list of lists or tuples

            # (Optional) Display a success message or open the file
            popup = Popup(title="Success", content=Label(text=f"Report exported to {filename}"), size_hint=(0.6, 0.3))
            popup.open()
        else:
            # Show "No Data" popup (you already have this part)
            popup = Popup(title="No Data", content=Label(text="No expenses found for the selected period."), size_hint=(0.6, 0.3))
            popup.open()

    def export_pdf(self, instance):
        report_type = self.report_type.text
        start_date = self.start_date_input.text
        end_date = self.end_date_input.text
        data = self.fetch_expense_data(report_type, start_date, end_date)

        if data:
            # 1. Create a PDF object
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # 2. Add title
            pdf.cell(200, 10, txt=f"Expense Report ({report_type})", ln=True, align="C")
            pdf.cell(200, 10, txt=f"From {start_date} to {end_date}", ln=True, align="C")

            # 3. Add summary data to the PDF
            pie_summary = self.generate_pie_summary(data)
            bar_summary = self.generate_bar_summary(data)

            pdf.ln(10)  # Add some space

            # Add Pie Chart Summary
            pdf.cell(200, 10, txt="Pie Chart Summary", ln=True, align="L")
            for line in pie_summary.split('\n'):
                pdf.cell(200, 10, txt=line, ln=True, align="L")

            pdf.ln(10)

            # Add Bar Chart Summary
            pdf.cell(200, 10, txt="Bar Chart Summary", ln=True, align="L")
            for line in bar_summary.split('\n'):
                pdf.cell(200, 10, txt=line, ln=True, align="L")

            # 4. Add charts to the PDF
            pie_chart, bar_chart = self.create_charts(data)
            pie_chart_path = "pie_chart.png"
            bar_chart_path = "bar_chart.png"
            pie_chart.savefig(pie_chart_path)
            bar_chart.savefig(bar_chart_path)

            pdf.image(pie_chart_path, x=10, y=100, w=100)
            pdf.image(bar_chart_path, x=110, y=100, w=100)

            # 5. Save the PDF
            pdf_filename = f"expense_report_{report_type}_{start_date}_{end_date}.pdf"
            pdf.output(pdf_filename)

            # (Optional) Display a success message or open the file
            popup = Popup(title="Success", content=Label(text=f"Report exported to {pdf_filename}"), size_hint=(0.6, 0.3))
            popup.open()
        else:
            # Show "No Data" popup (you already have this part)
            popup = Popup(title="No Data", content=Label(text="No expenses found for the selected period."), size_hint=(0.6, 0.3))
            popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'
