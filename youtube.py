import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your actual API key
API_KEY = 'AIzaSyCEJFFS34-9GFNL8C2iTKDVAcdQewRcsHY'
BASE_URL = 'https://www.googleapis.com/youtube/v3/'


def search_youtube(query):
    search_url = f"{BASE_URL}search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'key': API_KEY,
        'maxResults': 50  # Number of results per request (up to 50)
    }
    try:
        response = requests.get(search_url, params=params, timeout=10)
        print(f"API Response Status: {response.status_code}")
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def save_results_to_file(results, filename):
    with open(filename, 'w') as file:
        file.write("YouTube Video Search Results\n")
        file.write("=" * 30 + "\n\n")

        for item in results.get('items', []):
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            file.write(f"Title: {video_title}\n")
            file.write(f"Video ID: {video_id}\n")
            file.write("-" * 30 + "\n")

        file.write("\nEnd of Results")


def send_email(subject, body, to_email, attachment_path):
    from_email = "awanish698@hotmail.com"  # Replace with your Hotmail address
    password = "XXXXXXX"  # Replace with your Hotmail password or app password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach file
    with open(attachment_path, 'r') as file:
        attachment = MIMEText(file.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path)
        msg.attach(attachment)

    try:
        with smtplib.SMTP('smtp-mail.outlook.com', 587, timeout=10) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")


def main():
    # Get user inputs
    artist_name = input("Enter the artist name: ")
    recipient_email = input("Enter the recipient email: ")

    if artist_name and recipient_email:
        print(f"Searching for videos by: {artist_name}")
        results = search_youtube(artist_name)

        if results:
            filename = 'search_results.txt'
            save_results_to_file(results, filename)
            print(f"Results saved to {filename}.")

            # Email the file
            subject = f"YouTube Search Results for {artist_name}"
            body = "Please find the attached file with the search results."
            send_email(subject, body, recipient_email, filename)
        else:
            print(f"No results found for: {artist_name}")
    else:
        print("Both artist name and recipient email must be provided.")


if __name__ == "__main__":
    main()
