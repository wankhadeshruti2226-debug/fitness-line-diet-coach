from flask import Flask, render_template_string, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "fitness_line"

def init_db():
    conn = sqlite3.connect('fitness.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, 
                  password TEXT, age INTEGER, gender TEXT, 
                  height REAL, weight REAL, activity TEXT, 
                  diet TEXT, goal TEXT)''')
    conn.close()
init_db()

# HOME PAGE - Screenshot 5.1
HOME = "<h1>Fitness Line - Personalized Fitness & Diet Coach</h1><p>AI-Based Personalized Diet Planner</p><a href='/register'><button>Get Started</button></a> <a href='/login'><button>Login</button></a><hr><p>Services: Diet Planning, Workout, Recipe, Expert Talk</p>"

# REGISTER - Screenshot 5.1 (User Registration)
REGISTER = """
<h2>User Registration Module (Ch 5.1.1)</h2>
<form method='post'>
Name: <input name='name' required><br><br>
Email: <input name='email' required><br><br>
Password: <input name='password' type='password' required><br><br>
Age: <input name='age' type='number'><br><br>
Gender: <select name='gender'><option>Male</option><option>Female</option></select><br><br>
<button>Register</button></form>
"""

# LOGIN - Screenshot 5.2 (User Login)
LOGIN = """
<h2>User Login Module (Ch 5.1.2)</h2>
<form method='post'>
Email: <input name='email' required><br><br>
Password: <input name='password' required><br><br>
<button>Login</button></form>
"""

# DASHBOARD - Screenshot 5.2 (User Dashboard)
DASH = """
<h2>User Dashboard - Good Morning {{n}}!</h2>
<p>Today: Greek Yogurt Bowl, Grilled Salmon, Upper Body Power</p>
<a href='/diet-details'><button>Diet Details</button></a>
<a href='/diet-plan'><button>Suggested Diet Plan</button></a>
<a href='/workout'><button>Workout</button></a>
<a href='/recipe'><button>Recipe</button></a>
<a href='/profile'><button>User Profile</button></a>
<a href='/expert'><button>Expert Talk</button></a>
<br><br><a href='/logout'>Logout</a>
"""

# DIET DETAILS - Screenshot 5.3
DIET_DETAILS = """
<h2>Diet Details (Screenshot 5.3 as per Report)</h2>
<form method='post' action='/diet-plan'>
Weight (kg): <input name='weight' value='100'><br><br>
Height (cm): <input name='height' value='80'><br><br>
Age: <input name='age' value='45'><br><br>
Goal: <select name='goal'><option>Weight Loss</option><option>Weight Gain</option><option>Maintenance</option></select><br><br>
Diet: <select name='pref'><option>Vegetarian</option><option>Non-Vegetarian</option><option>Vegan</option></select><br><br>
Activity: <select name='activity'><option>Sedentary</option><option>Moderate</option><option>Active</option></select><br><br>
<button>Generate Diet Plan</button></form>
"""

@app.route("/")
def home(): return render_template_string(HOME)

@app.route("/register", methods=["GET","POST"])
def reg():
    if request.method=="POST":
        session['name']=request.form['name']
        return redirect("/dashboard")
    return render_template_string(REGISTER)

@app.route("/login", methods=["GET","POST"])
def log():
    if request.method=="POST":
        session['name']="User"
        return redirect("/dashboard")
    return render_template_string(LOGIN)

@app.route("/dashboard")
def dash():
    if 'name' not in session: return redirect("/login")
    return render_template_string(DASH, n=session['name'])

@app.route("/diet-details")
def ddetails(): return render_template_string(DIET_DETAILS)

@app.route("/diet-plan", methods=["GET","POST"])
def dplan():
    bmi=0; cal=0
    if request.method=="POST":
        w=float(request.form['weight']); h=float(request.form['height'])/100
        bmi=round(w/(h*h),2)
        cal= 1800 if request.form['goal']=="Weight Loss" else 2500
    
    # BMI and Calorie Module (Ch 5.1.4) + Diet Plan Module (Ch 5.1.5)
    return f"""
    <h2>BMI & Calorie Calculation (Ch 5.1.4)</h2>
    <p><b>BMI:</b> {bmi} | <b>Daily Calories:</b> {cal} kcal</p>
    <h2>Suggested Diet Plan (Ch 5.1.5) - Screenshot 5.1</h2>
    <p><b>Breakfast:</b> Oats, Greek Yogurt Bowl, Poha</p>
    <p><b>Lunch:</b> Dal Rice, Grilled Salmon Salad</p>
    <p><b>Dinner:</b> Roti Sabzi, Soup, Paneer Chilla</p>
    <p><b>Snacks:</b> Fruits, Nuts</p>
    <a href='/dashboard'>Back to Dashboard</a>
    """

@app.route("/profile", methods=["GET","POST"])
def prof():
    return "<h2>User Profile Management (Ch 5.1.3)</h2><p>Update Height, Weight, Activity, Dietary Preference, Health Goals</p><a href='/dashboard'>Back</a>"

@app.route("/workout")
def work(): return "<h2>Workout Module (Screenshot 5.2)</h2><p>Upper Body Power: Bench Press, Shoulder Press</p><a href='/dashboard'>Back</a>"

@app.route("/recipe")
def rec(): return "<h2>Recipe Recommendation Module (Ch 5.1.6) - Screenshot 5.3</h2><p>Paneer Chilla, Rajma Chawal<br>Ingredients, Preparation Steps, Nutrition Info</p><a href='/dashboard'>Back</a>"

@app.route("/expert")
def exp(): return "<h2>Expert Talk Module (Ch 2.3)</h2><p>AI-driven nutrition guidance & tips</p><a href='/dashboard'>Back</a>"

@app.route("/logout")
def out():
    session.clear(); return redirect("/")

if __name__=="__main__":
    app.run(debug=True)