import sqlite3
import csv
from kivy.uix.image import Image
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle,Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from kivy.uix.popup import Popup
from collections import defaultdict
import datetime
from datetime import  timedelta
import matplotlib.pyplot as plt
from kivy.utils import get_color_from_hex
from fpdf import FPDF
from kivy.uix.dropdown import DropDown
from dateutil.relativedelta import relativedelta
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import os
import matplotlib.ticker as mtick
from matplotlib.table import Table
from kivy.graphics import Color, Rectangle, Line
from matplotlib.gridspec import GridSpec
import smtplib
from email.message import EmailMessage
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


