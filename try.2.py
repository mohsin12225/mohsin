
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Hardcoded app password and receiver email
APP_PASSWORD = "xgut gzuh mmqf iezs"
RECEIVER_EMAIL = "mohsin.alaum10@gmail.com"

class EmailSender(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        
        # Create a layout for fields
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter("height"))

        # Sender email input
        form_layout.add_widget(Label(text="Your Email:", size_hint_y=None, height=40))
        self.sender_email = TextInput(hint_text="Enter your email", multiline=False)
        form_layout.add_widget(self.sender_email)

        # Subject input
        form_layout.add_widget(Label(text="Subject:", size_hint_y=None, height=40))
        self.subject = TextInput(hint_text="Enter email subject", multiline=False)
        form_layout.add_widget(self.subject)

        # Add the form to a scrollable area
        scroll_view = ScrollView(size_hint=(1, 0.4))
        scroll_view.add_widget(form_layout)
        self.add_widget(scroll_view)

        # Message input
        self.add_widget(Label(text="Message:"))
        self.message = TextInput(hint_text="Enter your message here", multiline=True, size_hint=(1, 0.4))
        self.add_widget(self.message)

        # Send button
        self.send_button = Button(text="Send Email", size_hint_y=None, height=50)
        self.send_button.bind(on_press=self.send_email)
        self.add_widget(self.send_button)

    def send_email(self, instance):
        sender_email = self.sender_email.text.strip()
        subject = self.subject.text.strip()
        body = self.message.text.strip()

        if not sender_email or not subject or not body:
            self.show_popup("Error", "All fields are required!")
            return

        try:
            # Create email object
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = RECEIVER_EMAIL
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Connect to SMTP server and send email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, APP_PASSWORD)
                server.send_message(msg)

            self.show_popup("Success", "message sent successfully!")
        except Exception as e:
            self.show_popup("Error", f"Failed to send email: {e}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class EmailSenderApp(App):
    def build(self):
        return EmailSender()

if __name__ == "__main__":
    EmailSenderApp().run()
