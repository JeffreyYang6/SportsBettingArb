from plyer import notification

print("Sending test notification!")
notification.notify(
    title="Plyer Test",
    message="If you see this, plyer notifications work.",
    timeout=10  # Show for 10 seconds (if supported)
)
