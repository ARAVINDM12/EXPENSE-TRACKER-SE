from Imports.imports import *
# Set window background color
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark theme

class ModernDropDown(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_width = True
        #self.width = 200  # Set a fixed width

    def add_widget(self, widget, index=0, canvas=None):
        # Apply styling to the buttons in the dropdown
        if isinstance(widget, Button):
            widget.background_normal = ''
            widget.background_color = (0.1, 0.1, 0.1, 1)  # Dark background
            widget.color = (0.9, 0.9, 0.9, 1)  # Light text color
            widget.font_size = 16
            widget.padding = [15, 15]

            with widget.canvas.before:
                Color(0.2, 0.2, 0.2, 1)  # Darker border color
                RoundedRectangle(pos=widget.pos, size=widget.size, radius=[10])

        return super().add_widget(widget, index=index, canvas=canvas)

class ModernSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.1, 0.1, 0.1, 1)  # Dark background
        self.color = (0.9, 0.9, 0.9, 1)  # Light text color
        self.font_size = 18
        self.padding = [15, 15]
        self.size_hint_y = None
        self.height = 50

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Darker border color
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.dropdown_cls = ModernDropDown  # Assign the custom dropdown class

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class StylishLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 42  # Slightly larger font size
        self.bold = True
        self.color = (0.1, 0.1, 0.1, 1)  # Darker gray text
        self.size_hint_y = None
        self.height = 80  # Slightly taller

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Lighter gray background
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])  # Slightly more rounded corners

            # Subtle shadow with a bit more offset
            Color(0, 0, 0, 0.15)  # Lighter shadow
            RoundedRectangle(pos=(self.x + 5, self.y - 5), size=(self.width - 10, self.height - 10), radius=[15])

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50  # Increased height for more space
        self.font_size = 20  # Slightly larger font size
        self.color = (1, 1, 1, 1)  # White text
        self.bold = True
        self.padding = (25, 20)  # More padding for better spacing

        with self.canvas.before:
            # Solid background color
            Color(0.15, 0.15, 0.15, 1)  # Slightly darker gray
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])  # Larger radius for smoother corners

            # Inner shadow
            Color(0, 0, 0, 0.3)  # Semi-transparent black
            self.shadow = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x + 5, self.y - 5)  # Offset the shadow slightly
        self.shadow.size = (self.width, self.height)  # Make the shadow slightly smaller
