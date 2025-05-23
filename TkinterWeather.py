import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageDraw, ImageFont, ImageTk


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("5-Day Weather Forecast")
        self.root.geometry("1920x1080")  # Adjusted window size
        self.root.resizable(False, False)

        # API Key
        self.api_key = "https://home.openweathermap.org/ ---> free apikey"

        # Weather icon mapping
        self.icon_mapping = {
            'clear': '☀️',
            'clouds': '☁️',
            'rain': '🌧️',
            'snow': '❄️',
            'thunderstorm': '⚡',
            'drizzle': '🌦️',
            'mist': '🌫️',
            'smoke': '🌫️',
            'haze': '🌫️',
            'fog': '🌫️'
        }

        # Style Configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('Header.TLabel', font=('Arial', 24, 'bold'))
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('Temp.TLabel', font=('Arial', 20, 'bold'))
        self.style.configure('Day.TLabel', font=('Arial', 16, 'bold'))

        # Create UI
        self.create_widgets()

    def create_weather_icon(self, weather_condition):
        """Create a weather icon using emoji characters"""
        condition = weather_condition.lower()
        emoji = '☁️'  # Default cloud icon

        # Find matching emoji
        for key, value in self.icon_mapping.items():
            if key in condition:
                emoji = value
                break

        # Create image with emoji
        image = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        try:
            # Try to load a font that supports emoji
            font = ImageFont.truetype("seguiemj.ttf", 80)  # Windows emoji font
        except:
            try:
                font = ImageFont.truetype("Apple Color Emoji.ttc", 80)  # macOS
            except:
                font = ImageFont.load_default()
                emoji = emoji[0]  # Use first character if emoji font not available

        draw.text((10, 0), emoji, font=font, embedded_color=True)
        return ImageTk.PhotoImage(image)

    def create_widgets(self):
        # Header Frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20, fill='x')

        ttk.Label(header_frame, text="5-Day Weather Forecast", style='Header.TLabel').pack()

        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=15, fill='x')

        ttk.Label(search_frame, text="Enter City:", font=('Arial', 14)).pack(side='left', padx=10)
        self.city_entry = ttk.Entry(search_frame, width=30, font=('Arial', 14))
        self.city_entry.pack(side='left', padx=10)
        self.city_entry.focus()

        search_btn = ttk.Button(search_frame, text="Search", command=self.get_weather)
        search_btn.pack(side='left', padx=10)

        # Weather Display Frame
        self.weather_frame = ttk.Frame(self.root)
        self.weather_frame.pack(pady=30, fill='both', expand=True)

        # Initialize empty forecast frames
        self.forecast_frames = []
        for i in range(5):
            frame = ttk.Frame(self.weather_frame, relief='solid', borderwidth=2)
            frame.grid(row=0, column=i, padx=15, pady=10, sticky='nsew')
            frame.config(width=220, height=400)
            self.weather_frame.grid_columnconfigure(i, weight=1)
            self.forecast_frames.append(frame)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] != "200":
                messagebox.showerror("Error", data['message'])
                return

            self.display_weather(data, city)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")

    def display_weather(self, data, city):
        # Clear previous forecasts
        for frame in self.forecast_frames:
            for widget in frame.winfo_children():
                widget.destroy()

        # Group forecasts by date
        forecasts = {}
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%A\n%d %b %Y')
            if date not in forecasts:
                forecasts[date] = []
            forecasts[date].append(item)

        # Display first 5 days
        for i, (date, items) in enumerate(list(forecasts.items())[:5]):
            frame = self.forecast_frames[i]

            # Date Label
            ttk.Label(frame, text=date, style='Day.TLabel').pack(pady=10)

            # Weather Icon
            weather_condition = items[0]['weather'][0]['main'].lower()
            weather_icon = self.create_weather_icon(weather_condition)

            icon_label = tk.Label(frame, image=weather_icon, bg='#f0f0f0')
            icon_label.image = weather_icon  # Keep reference
            icon_label.pack(pady=10)

            # Temperature
            avg_temp = sum(item['main']['temp'] for item in items) / len(items)
            ttk.Label(frame, text=f"{avg_temp:.1f}°C", style='Temp.TLabel').pack()

            # Weather Description
            weather_desc = items[0]['weather'][0]['description'].capitalize()
            ttk.Label(frame, text=weather_desc, font=('Arial', 14)).pack()

            # Details frame
            details_frame = ttk.Frame(frame)
            details_frame.pack(pady=15)

            # Left column
            left_frame = ttk.Frame(details_frame)
            left_frame.pack(side='left', padx=10)

            ttk.Label(left_frame,
                      text=f"Min: {min(item['main']['temp'] for item in items):.1f}°C",
                      font=('Arial', 12)).pack(anchor='w', pady=3)
            ttk.Label(left_frame,
                      text=f"Max: {max(item['main']['temp'] for item in items):.1f}°C",
                      font=('Arial', 12)).pack(anchor='w', pady=3)


            right_frame = ttk.Frame(details_frame)
            right_frame.pack(side='left', padx=10)

            ttk.Label(right_frame,
                      text=f"Humidity: {items[0]['main']['humidity']}%",
                      font=('Arial', 12)).pack(anchor='w', pady=3)
            ttk.Label(right_frame,
                      text=f"Wind: {items[0]['wind']['speed']} km/h",
                      font=('Arial', 12)).pack(anchor='w', pady=3)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()