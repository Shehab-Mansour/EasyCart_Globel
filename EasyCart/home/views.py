# from django.http import HttpResponse
# from django.shortcuts import render

# from User.views import sinin


# # Create your views here.
# def home (request):
#     return HttpResponse("<h1>Home Page</h1> <dr> <a href=""/user"">user home</a>  <a href=""/user/sinin"">sinin</a> <a href=""/user/login"">login</a> <br> <a href=""/admin"">admin</a>")


# from django.http import HttpResponse
# from django.shortcuts import render
#
# from User.views import sinin
#
#
# # Create your views here.
# def home (request):
#     return HttpResponse("<h1>Home Page</h1> <dr> <a href=""/user/login"">login</a> <br> <a href=""/admin"">admin</a>")
#



from django.http import HttpResponse



def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Cart APIs</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f0fff4 0%, #e6ffec 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #2d3748;
            }
            .container {
                text-align: center;
                background: white;
                padding: 3rem;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
                max-width: 600px;
                width: 90%;
                border: 1px solid #e2e8f0;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 1.5rem;
                background: linear-gradient(to right, #48bb78, #38a169);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p {
                font-size: 1.1rem;
                margin-bottom: 2rem;
                color: #4a5568;
                line-height: 1.6;
            }
            .btn-container {
                display: flex;
                justify-content: center;
                gap: 1.5rem;
                flex-wrap: wrap;
            }
            .btn {
                display: inline-block;
                padding: 12px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            }
            .btn-login {
                background: linear-gradient(to right, #48bb78, #38a169);
                color: white;
                border: 2px solid #48bb78;
            }
            .btn-login:hover {
                background: linear-gradient(to right, #38a169, #2f855a);
                transform: translateY(-3px);
                box-shadow: 0 7px 20px rgba(72, 187, 120, 0.3);
            }
            .btn-admin {
                background: white;
                color: #48bb78;
                border: 2px solid #48bb78;
            }
            .btn-admin:hover {
                background: #f0fff4;
                transform: translateY(-3px);
                box-shadow: 0 7px 20px rgba(72, 187, 120, 0.2);
            }
            .logo {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #48bb78;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .features {
                display: flex;
                justify-content: center;
                gap: 1rem;
                flex-wrap: wrap;
                margin: 2rem 0;
            }
            .feature {
                background: #f0fff4;
                padding: 0.8rem 1.2rem;
                border-radius: 8px;
                font-size: 0.9rem;
                color: #2f855a;
                border: 1px solid #c6f6d5;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <span>🛒</span>
                <span>Easy Cart</span>
            </div>
            <h1>Welcome to Easy Cart APIs</h1>
            <p>
                Manage your e-commerce platform with our powerful and easy-to-use APIs.
                Sign in to access your dashboard or visit the admin panel for full control.
            </p>

            <div class="features">
                <span class="feature">Easy Integration</span>
                <span class="feature">Secure</span>
                <span class="feature">Scalable</span>
            </div>

            <div class="btn-container">
                <a href="/user/login" class="btn btn-login">Login</a>
                <a href="/admin" class="btn btn-admin">Admin Panel</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)