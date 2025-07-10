ACCOUNT_CREATED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Cinema App</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #42a5f5 0%, #478ed1 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 300;
        }
        .content {
            padding: 40px 30px;
        }
        .welcome-box {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 30px;
            margin: 20px 0;
            text-align: center;
            border-left: 4px solid #42a5f5;
        }
        .btn {
            display: inline-block;
            padding: 15px 35px;
            background-color: #42a5f5;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: 600;
            font-size: 16px;
        }
        .features {
            margin: 30px 0;
        }
        .feature {
            display: flex;
            align-items: center;
            margin: 15px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .feature-icon {
            font-size: 24px;
            margin-right: 15px;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Welcome to Cinema App!</h1>
            <p>Your account has been created successfully</p>
        </div>
        
        <div class="content">
            <div class="welcome-box">
                <h2>Hello {{ user_name }}!</h2>
                <p>Welcome to the ultimate cinema experience. Your account is ready to use!</p>
            </div>
            
            <div class="features">
                <h3>What you can do now:</h3>
                
                <div class="feature">
                    <div class="feature-icon">🎫</div>
                    <div>
                        <strong>Book Tickets</strong><br>
                        Reserve your seats for the latest movies
                    </div>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">⭐</div>
                    <div>
                        <strong>Rate & Review</strong><br>
                        Share your thoughts on movies you've watched
                    </div>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🔔</div>
                    <div>
                        <strong>Get Notifications</strong><br>
                        Stay updated with new releases and special offers
                    </div>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🎁</div>
                    <div>
                        <strong>Exclusive Offers</strong><br>
                        Enjoy member-only discounts and promotions
                    </div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="{{ app_url }}" class="btn">Start Exploring</a>
            </div>
            
            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                <strong>Your account details:</strong><br>
                Email: {{ user_email }}<br>
                Account created: {{ created_date }}
            </p>
        </div>
        
        <div class="footer">
            <p>© 2025 Cinema App. All rights reserved.</p>
            <p>Questions? Contact us at {{ support_email }}</p>
        </div>
    </div>
</body>
</html>
"""

TICKET_PURCHASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Cinema Tickets</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 300;
        }
        .content {
            padding: 40px 30px;
        }
        .ticket-info {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 25px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        .movie-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .detail-label {
            font-weight: 600;
            color: #666;
        }
        .detail-value {
            color: #333;
        }
        .qr-code {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 14px;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background-color: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Your Cinema Tickets</h1>
            <p>Thank you for your purchase!</p>
        </div>
        
        <div class="content">
            <div class="ticket-info">
                <div class="movie-title">{{ movie_title }}</div>
                
                <div class="detail-row">
                    <span class="detail-label">Date & Time:</span>
                    <span class="detail-value">{{ show_date }} at {{ show_time }}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Cinema:</span>
                    <span class="detail-value">{{ cinema_name }}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Hall:</span>
                    <span class="detail-value">{{ hall_name }}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Seats:</span>
                    <span class="detail-value">{{ seats }}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Tickets:</span>
                    <span class="detail-value">{{ ticket_count }} x {{ ticket_price }}</span>
                </div>
                
                <div class="detail-row">
                    <span class="detail-label">Total:</span>
                    <span class="detail-value"><strong>{{ total_price }}</strong></span>
                </div>
            </div>
            
            <div class="qr-code">
                <h3>🎫 Your Ticket Code</h3>
                <div style="font-size: 24px; font-weight: bold; color: #667eea; margin: 15px 0;">
                    {{ ticket_code }}
                </div>
                <p style="color: #666; font-size: 14px;">
                    Show this code at the cinema entrance
                </p>
            </div>
            
            <p>Please arrive at least 15 minutes before the show time. Have a great movie experience!</p>
            
            <div style="text-align: center;">
                <a href="{{ cinema_website }}" class="btn">View Cinema Location</a>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 {{ cinema_name }}. All rights reserved.</p>
            <p>Questions? Contact us at {{ support_email }}</p>
        </div>
    </div>
</body>
</html>
"""


ANNOUNCEMENT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ announcement_title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 300;
        }
        .content {
            padding: 40px 30px;
        }
        .announcement-content {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 30px;
            margin: 20px 0;
            border-left: 4px solid #f5576c;
        }
        .btn {
            display: inline-block;
            padding: 15px 35px;
            background-color: #f5576c;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: 600;
            text-align: center;
        }
        .image-container {
            text-align: center;
            margin: 20px 0;
        }
        .image-container img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 14px;
        }
        .highlight {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📢 {{ announcement_title }}</h1>
            <p>{{ announcement_subtitle }}</p>
        </div>
        
        <div class="content">
            <div class="announcement-content">
                {{ announcement_content }}
            </div>
            
            {% if highlight_text %}
            <div class="highlight">
                <strong>{{ highlight_text }}</strong>
            </div>
            {% endif %}
            
            {% if image_url %}
            <div class="image-container">
                <img src="{{ image_url }}" alt="Announcement Image">
            </div>
            {% endif %}
            
            {% if cta_text and cta_url %}
            <div style="text-align: center;">
                <a href="{{ cta_url }}" class="btn">{{ cta_text }}</a>
            </div>
            {% endif %}
            
            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                This announcement was sent on {{ sent_date }}
            </p>
        </div>
        
        <div class="footer">
            <p>© 2025 Cinema App. All rights reserved.</p>
            <p>Questions? Contact us at {{ support_email }}</p>
        </div>
    </div>
</body>
</html>
"""

AUTH_CODE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Authentication Code</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 300;
        }
        .content {
            padding: 40px 30px;
            text-align: center;
        }
        .auth-code {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 30px;
            margin: 30px 0;
            border: 2px dashed #ff6b6b;
        }
        .code {
            font-size: 36px;
            font-weight: bold;
            color: #ff6b6b;
            letter-spacing: 8px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
        }
        .warning {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Authentication Code</h1>
            <p>Secure access to your account</p>
        </div>
        
        <div class="content">
            <h2>Hello {{ user_name }}!</h2>
            <p>You requested an authentication code for your Cinema App account.</p>
            
            <div class="auth-code">
                <h3>Your verification code:</h3>
                <div class="code">{{ auth_code }}</div>
                <p style="color: #666; font-size: 14px;">
                    Enter this code to complete your verification
                </p>
            </div>
            
            <div class="warning">
                <strong>⚠️ Important:</strong>
                <ul style="text-align: left; margin: 10px 0;">
                    <li>This code expires in {{ expiration_time }} minutes</li>
                    <li>Don't share this code with anyone</li>
                    <li>If you didn't request this code, please ignore this email</li>
                </ul>
            </div>
            
            <p>If you're having trouble, please contact our support team.</p>
        </div>
        
        <div class="footer">
            <p>© 2025 Cinema App. All rights reserved.</p>
            <p>Questions? Contact us at {{ support_email }}</p>
        </div>
    </div>
</body>
</html>
"""
PAYMENT_FAILED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Failed</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 300;
        }
        .content {
            padding: 40px 30px;
        }
        .error-info {
            background-color: #ffeaa7;
            border-radius: 8px;
            padding: 25px;
            margin: 20px 0;
            border-left: 4px solid #e74c3c;
        }
        .btn {
            display: inline-block;
            padding: 15px 35px;
            background-color: #e74c3c;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: 600;
        }
        .help-section {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>❌ Payment Failed</h1>
            <p>We couldn't process your payment</p>
        </div>
        
        <div class="content">
            <p>Hello {{ user_name }},</p>
            
            <p>We encountered an issue while processing your payment for your cinema ticket booking.</p>
            
            <div class="error-info">
                <h3>Order Details:</h3>
                <p><strong>Movie:</strong> {{ movie_title }}</p>
                <p><strong>Date & Time:</strong> {{ show_date }} at {{ show_time }}</p>
                <p><strong>Seats:</strong> {{ seats }}</p>
                <p><strong>Total Amount:</strong> {{ total_price }}</p>
                <p><strong>Error:</strong> {{ error_message }}</p>
            </div>
            
            <div class="help-section">
                <h3>What can you do?</h3>
                <ul>
                    <li>Check your payment method details</li>
                    <li>Ensure sufficient funds are available</li>
                    <li>Try a different payment method</li>
                    <li>Contact your bank if the issue persists</li>
                </ul>
            </div>
            
            <p>Your seats are temporarily reserved for {{ reservation_time }} minutes. Please complete your payment before this time expires.</p>
            
            <div style="text-align: center;">
                <a href="{{ retry_payment_url }}" class="btn">Retry Payment</a>
            </div>
            
            <p>If you continue to experience issues, please contact our support team.</p>
        </div>
        
        <div class="footer">
            <p>© 2025 Cinema App. All rights reserved.</p>
            <p>Questions? Contact us at {{ support_email }}</p>
        </div>
    </div>
</body>
</html>
"""
