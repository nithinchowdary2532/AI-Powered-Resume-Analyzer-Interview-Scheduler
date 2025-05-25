import random
import string
from datetime import datetime, timedelta
import requests  # If you want to send the meeting link by email

def generate_random_room_name(length=8):
    """Generate a random room name for the meeting."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def schedule_jitsi_interview(candidate_email):
    # Generate a random room name for the Jitsi meeting
    room_name = generate_random_room_name()

    # Jitsi Meet URL
    jitsi_url = f"https://meet.jit.si/{room_name}"

    # Prepare meeting details (you can add more details as needed)
    interview_details = {
        "candidate_email": candidate_email,
        "meeting_url": jitsi_url,
        "scheduled_time": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    # You could send an email to the candidate here if needed (just an example)
    # For example, using the 'requests' library to send an email (SMTP setup required)
    # You can also use services like SendGrid, Mailgun, etc.

    # Placeholder function to represent email sending
    # send_interview_email(candidate_email, jitsi_url, interview_details['scheduled_time'])

    return interview_details

# Example usage
candidate_email = "candidate@example.com"
meeting_details = schedule_jitsi_interview(candidate_email)
print(f"Jitsi Meeting URL: {meeting_details['meeting_url']}")
print(f"Scheduled Interview Time: {meeting_details['scheduled_time']}")
