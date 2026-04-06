USER_ACTIVATION_TEMPLATE = """
<html>
<body>
  <h2>Welcome {{ user_name or "Cinema user" }}</h2>
  <p>Your account has been activated.</p>
  <p>Use this link to continue: <a href="{{ activation_url }}">{{ activation_url }}</a></p>
</body>
</html>
"""

AUTH_CODE_TEMPLATE = """
<html>
<body>
  <h2>Authentication code</h2>
  <p>Hello {{ user_name or "Cinema user" }}, your verification code is:</p>
  <h1>{{ auth_code }}</h1>
  <p>This code expires in {{ expiration_time or 10 }} minutes.</p>
</body>
</html>
"""

GENERIC_INFO_TEMPLATE = """
<html>
<body>
  <h2>{{ title or "Cinema notification" }}</h2>
  <p>{{ message or "An update is available." }}</p>
  {% if details %}
  <pre>{{ details }}</pre>
  {% endif %}
</body>
</html>
"""

TICKET_PURCHASE_TEMPLATE = """
<html>
<body>
  <h2>Your cinema ticket receipt</h2>
  <p>Movie: {{ movie_title }}</p>
  <p>Showtime: {{ show_date }} {{ show_time }}</p>
  <p>Seats: {{ seats }}</p>
  <p>Total: {{ total_price }}</p>
  <p>Ticket code: <strong>{{ ticket_code }}</strong></p>
  <p>If provided, your PDF ticket/receipt is attached.</p>
</body>
</html>
"""
