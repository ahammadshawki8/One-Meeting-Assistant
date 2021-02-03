import mm_backend as mm


print(mm.add_meeting("onetime", 1202404000, "python20", "https://ahammadshawki8.github.io/", "Ahammad Shawki", "Learn to Code with Python", ("2021","03","20","10", "00") ))
print(mm.add_meeting("onetime", 1202404000, "python20", "https://ahammadshawki8.github.io/", "Ahammad Shawki", "Learn to Code with Python", ("2021","03","04","06", "10") ))

print(mm.add_meeting("weekly", 1202404000, "python20", "https://ahammadshawki8.github.io/", "Ahammad Shawki", "Learn to Code with Python", ("Thu","10", "00") ))
print(mm.add_meeting("weekly", 1202404000, "python20", "https://ahammadshawki8.github.io/", "Ahammad Shawki", "Learn to Code with Python", ("Thu","06", "10") ))

print(mm.add_meeting("daily", 1202404000, "python20", "https://ahammadshawki8.github.io/", "Ahammad Shawki", "Learn to Code with Python", ("10", "00") ))
print(mm.add_meeting("daily", 1202404000, "python20", "https://ahammadshawki8.github.io/", "Ahammad Shawki", "Learn to Code with Python", ("06", "10") ))

print(mm.show_upcoming_meetings("30 Day"))

