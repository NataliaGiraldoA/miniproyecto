import tempfile
from flask import Flask, redirect, render_template, request, url_for, jsonify
from binarySearch.binary_search import binary_search
from FizzBuzzPy.fizzbuzz import fizzbuzz
from integerToRoman.integer_to_roman import int_to_roman
from reverseString.reverse_string import reverse_string
from moneyToEnglish.money_to_english import money_to_english
from countVowels.vowel_counter import vowel_counter
from palindrome.palindrome import palindrome
from asteriskPyramid.asterisk_pyramid import asterisk_pyramid
from encripter.encripter import encripter
from fibonacci.fibonacci import fibonacci
import subprocess
import random
import os
import ast
import json
import re
import requests


from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  
db = SQLAlchemy(app)




login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
    _instance = None  
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    solutions = db.relationship('Solution', backref='user', lazy=True)
    @staticmethod
    def get_instance():
        """Método estático para implementar Singleton"""
        if User._instance is None:
            User._instance = User()
        return User._instance


class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
    return render_template('login.html')




@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


problems_db = {
    1: {
        "problem_id": 1,
        "title": "Binary Search",
        "difficulty": "Hard",
        "description": "Create a binary search function without using recursion.",
        "template_python": "def binary_search(arr, target):\n    # Your code here\n    return position",
        "template_java": "public class Solution {\n    public static int binarySearch(int[] arr, int target) {\n        // Your code here\n        return -1;\n    }\n} \n\n public static void main(String[] args) {\n     int[] arr = {2, 6, 9, 13, 15, 87, 99};   \n     int target = 13; \n  // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static int binarySearch(int[] arr, int target){\n // Your code here\n    return position;\n }",
        "test_input": "([1, 2, 3, 4, 5], 4)",
        "function_name_python": "binary_search",
        "function_name_java": "binarySearch",
    },
    2: {
        "problem_id": 2,
        "title": "Reverse String",
        "difficulty": "Easy",
        "description": "Write a function that reverses a string.",
        "template_python": "def reverse_string(text):\n    # Your code here\n    return reverse",
        "template_java": "public class Solution {\n    public static String reverseString(String text) {\n        // Your code here\n        return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static String reverseString(String text){\n // Your code here\n return reversed;\n }",
        "test_input": "'hello'",
        "function_name_python": "reverse_string",
        "function_name_java": "reverseString",
    },
    3: {
        "problem_id": 3,
        "title": "Fizzbuzz",
        "difficulty": "Medium",
        "description": "Create the fizzbuzz function that if the number is divisible by 3, return 'Fizz', if it is divisible by 5, return 'Buzz', and if it is divisible by both, return 'FizzBuzz'.",
        "template_python": "def fizzbuzz(numbers):\n    # Your code here\n    return ''",
        "template_java": "public class Solution {\n    public static String fizzbuzz(int[] numbers) {\n        // Your code here\n        return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static String[] fizzbuzz(int[] numbers){\n // Your code here\n return ;\n }",
        "test_input": "[3, 10, 15, 4]",
        "function_name_python": "fizzbuzz",
        "function_name_java": "fizzbuzz",
    },
    4: {
        "problem_id": 4,
        "title": "Integer to Roman",
        "difficulty": "Medium",
        "description": "Converts an integer into its equivalent Roman numeral representation. The function takes a single integer input and returns a string representing the Roman numeral format, using standard conventions for Roman numeral construction.",
        "template_python": "def int_to_roman(number):\n    # Your code here\n    return roman_number",
        "template_java": "public class Solution {\n    public static String integerToRoman(int number) {\n        // Your code here\n        return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static String integerToRoman(int number){\n // Your code here\n return ;\n }",
        "test_input": "5",
        "function_name_python": "int_to_roman",
        "function_name_java": "intToRoman",

    },
    5: {
        "problem_id": 5,
        "title": "Money to english",
        "difficulty": "Medium",
        "description": "Converts a amount of money to english",
        "template_python": "def money_to_english(number):\n    # Your code here\n    return english",
        "template_java": "public class Solution {\n    public static String moneyToEnglish(float number) {\n        // Your code here\n        return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static String moneyToEnglish(float number){\n // Your code here\n return ;\n }",
        "test_input": "25.6",
        "function_name_python": "money_to_english",
        "function_name_java": "moneyToEnglish",

    },
    6:{
        "problem_id": 6,
        "title": "Vowels counter",
        "difficulty": "Medium",
        "description": "Counts the number of vowels in a string",
        "template_python": "def count_vowels(text):\n    # Your code here\n    return count",
        "template_java": "public class Solution {\n    public static int count_vowels(String text) {\n        // Your code here\n        return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static int count_vowels(String text){\n // Your code here\n return ;\n }",
        "test_input": "amarillo",
        "function_name_python": "vowel_counter",
        "function_name_java": "VowelCounter",
    },
    7:{
        "problem_id": 7,
        "title": "Palindrome",
        "difficulty": "Medium",
        "description": "Checks if a word is a palindrome",
        "template_python": "def palindrome(text):\n    # Your code here\n    return ",
        "template_java": "public class Solution {\n    public static bool Palindrome(String text) {\n        // Your code here\n         return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static bool Palindrome(String text){\n // Your code here\n return ;\n }",
        "test_input": "Oso",
        "function_name_python": "palindrome",
        "function_name_java": "Palindrome",
    },
    8: {
        "problem_id": 8,
        "title": "Asterisk Pyramid",
        "difficulty": "Medium",
        "description": "Print a pyramid of asterisks",
        "template_python": "def asterisk_pyramid(n):\n    # Your code here\n    return ",
        "template_java": "public class Solution {\n    public static String AsteriskPyramid(int n) {\n        // Your code here\n         return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static String AsteriskPyramid(int n){\n // Your code here\n return ;\n }",
        "test_input": "10",
        "function_name_python": "asterisk_pyramid",
        "function_name_java": "AsteriskPyramid",
    },
    9: {
        "problem_id": 9,
        "title": "Encripter",
        "difficulty": "Easy",
        "description": "Encript phrases where the a is ai, e is enter, i is imes, o is ober and u is ufat ",
        "template_python": "def encriper(text):\n    # Your code here\n    return ",
        "template_java": "public class Solution {\n    public static String encripter(String text) {\n        // Your code here\n         return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static String encripter(String text){\n // Your code here\n return ;\n }",
        "test_input": "Murcielago",
        "function_name_python": "encripter",
        "function_name_java": "Encripter",

    },
    10: {
        "problem_id": 10,
        "title": "Fibonacci",
        "difficulty": "Hard",
        "description": "Print the first n numbers in the fibonacci sucession",
        "template_python": "def fibonacci(int):\n    # Your code here\n    return ",
        "template_java": "public class Solution {\n    public static int Fibonacci(int n) {\n        // Your code here\n         return \"\";\n    }\n} \n\n public static void main(String[] args) { \n // Your code here\n    }",
        "template_csharp": "using System;\npublic class Solution {\n public static int Fibonacci(int n){\n // Your code here\n return ;\n }",
        "test_input": "50",
        "function_name_python": "fibonacci",
        "function_name_java": "Fibonacci",
    }
}

SOLUTION_PYTHON_FILE = '../solution_python.json'
SOLUTION_JAVA_FILE = '../solution_java.json'
SOLUTION_CSHARP_FILE = '../solution_csharp.json'
PRESUBMIT_RESPONSES_FILE = '../presubmit_responses.json'

def save_presubmit_response(problem_id, code, language):
    if not os.path.exists(PRESUBMIT_RESPONSES_FILE):
        with open(PRESUBMIT_RESPONSES_FILE, 'w') as f:
            json.dump({}, f)

    with open(PRESUBMIT_RESPONSES_FILE, 'r') as f:
        responses = json.load(f)

    responses[str(problem_id)] = {
        'problem_id': problem_id,
        'code': code,
        'language': language,
    }

    with open(PRESUBMIT_RESPONSES_FILE, 'w') as f:
        json.dump(responses, f, indent=4)

#Save and load functions
def save_solution(problem_id, code, language):
    if language == 'python':
        solution_file = SOLUTION_PYTHON_FILE
    elif language == 'java':
        solution_file = SOLUTION_JAVA_FILE
    else:
        solution_file = SOLUTION_CSHARP_FILE

    if not os.path.exists(solution_file):
        with open(solution_file, 'w') as f:
            json.dump({}, f)

    with open(solution_file, 'r') as f:
        solutions = json.load(f)

    solutions[str(problem_id)] = {
        'problem_id': problem_id,
        'code': code
        }

    with open(solution_file, 'w') as f:
        json.dump(solutions, f, indent=4)

    print(f"Solution saved successfully in {solution_file}")


def load_solution(problem_id, language):
    if language == 'python':  #Check the language and saves in the respetive json
        solution_file = SOLUTION_PYTHON_FILE
    elif language == 'java':
        solution_file = SOLUTION_JAVA_FILE
    else:
        solution_file = SOLUTION_CSHARP_FILE

    if not os.path.exists(solution_file):
        return None

    with open(solution_file, 'r') as f:
        solutions = json.load(f)

    return solutions.get(str(problem_id), {}).get('code', None)

def check_no_if(user_code):
    tree = ast.parse(user_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.If): 
            return False  #If finds an if, return false
    return True

def check_no_if_java(user_code):
    if_pattern = r'\bif\s*\('  #Search for an if pattern
    return not re.search(if_pattern, user_code)

def check_no_recursion(user_code, function_name):
    tree = ast.parse(user_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == function_name:
                return False
    return True

def check_no_recursion_java(user_code, function_name):
    #Search all the calls in the code
    recursion_pattern = rf'\b{function_name}\s*\('
    calls = re.findall(recursion_pattern, user_code)
    
    #if theres more than two calls its recursive
    return len(calls) <=  2

def check_no_if_csharp(user_code):

    if_pattern = r'\bif\s*[\(]'
    return not re.search(if_pattern, user_code)

def check_no_recursion_csharp(user_code, function_name):

    recursion_pattern = rf'\b(this\.)?{function_name}\s*\('
    calls = re.findall(recursion_pattern, user_code)
    
    #if theres more than two calls its recursive
    return len(calls) <= 2

def random_array_and_number() -> list:
    size = random.randint(2, 10)  
    arr = [random.randint(0, 10)]  
    for _ in range(1, size):
        increment = random.randint(1, 5)  
        next_number = arr[-1] + increment
        arr.append(next_number)

    # Choose a random number in an array
    number = random.choice(arr)
    
    return arr, number

def random_number() -> int: #Random number for the integer to roman input
    number = random.randint(0,100)
    return number

def random_number_fibonacci() -> int:
    number = random.randint(2,15)
    return number

def random_float() -> float: #Random float for the money to english input
    return round(random.uniform(0, 100), 2)

def random_string() -> str: #Random string for the vowels counter, reverse string and palindrome input
    words = ['hello', 'world', 'python', 'java', 'programming', 'code', 'flask', 'javascript', 'bob', 'civic','Dewed', 'Kayak', 'Level', 'Madam' ]
    return random.choice(words)

# Validate metadata
def validate_solution(user_code, problem_id, language):
    error_message = "Cool"
    error_class = "none"
    if language == 'python':
        if problem_id == 1 and not check_no_recursion(user_code, 'binary_search'):
            return "Error: Your solution contains recursion."
        elif problem_id == 3 and not check_no_if(user_code):
            return "Error: Your solution contains 'if' statements."
    elif language == 'java':
        if problem_id == 1 and not check_no_recursion_java(user_code, 'binarySearch'):
            return "Error: Your solution contains recursion."
        elif problem_id == 3 and not check_no_if_java(user_code):
            return "Error: Your solution contains 'if' statements."
    elif language == 'csharp':
        if problem_id == 1 and not check_no_recursion_csharp(user_code, 'BinarySearch'):
            return "Error: Your solution contains recursion."
        elif problem_id == 3 and not check_no_if_csharp(user_code):
            return "Error: Your solution contains 'if' statements."
        
    return error_message, error_class


def compile_and_run_java(user_code, input_data):
    user_code = user_code.replace('\u00a0', ' ')  #Clean no valid characters
    
    with tempfile.TemporaryDirectory() as tempdir:
        java_file_path = os.path.join(tempdir, 'Solution.java')
        with open(java_file_path, 'w') as java_file:
            java_file.write(user_code)

        #Compile the file to Java
        compile_process = subprocess.run(['javac', java_file_path], capture_output=True, text=True)

        if compile_process.returncode != 0:
            return f"Compilation error: {compile_process.stderr}"

        #Execute the compile java file
        input_str = ' '.join(map(str, input_data)) #Turn the array to string, so we can pass it as an argument  
        run_process = subprocess.run( 
            ['java', '-cp', tempdir, 'Solution'],
            input=input_str,
            capture_output=True,
            text=True
        )

        if run_process.returncode != 0:
            return f"Runtime error: {run_process.stderr}"

        return run_process.stdout.strip()

#Code tests
def test_solution(user_code, input_data, problem_id, language):
    try:
        if problem_id == 1:  # For binary 
            expected_output = binary_search(*input_data)
        elif problem_id == 2:  # For reverse String
            expected_output = reverse_string(input_data)
        elif problem_id == 3:  # For fizzbuzz
            expected_output = fizzbuzz(input_data)
            expected_output = ', '.join(expected_output)  # turn the list into a string
        elif problem_id == 4: #For integer to roman
            expected_output = int_to_roman(input_data)
        elif problem_id == 5: #For money to english
            expected_output = money_to_english(input_data)
        elif problem_id == 6: #For vowels counter
            expected_output = vowel_counter(input_data)
        elif problem_id == 7: #For palindrome
            expected_output = palindrome(input_data)
        elif problem_id == 8: #For asterisk Pyramid
            expected_output = asterisk_pyramid(input_data)
        elif problem_id == 9: #For encripter
            expected_output = encripter(input_data)
        elif problem_id == 10: #For fibonacci
            expected_output = fibonacci(input_data)

        if language == 'python':
            exec_globals = {}
            exec(user_code, exec_globals)
            user_function = exec_globals.get(problems_db[problem_id]['function_name_python'])
            if problem_id == 1:
                user_output = user_function(*input_data)
            else:
                user_output = user_function(input_data)

            user_output_str = ', '.join(str(item) for item in user_output) if isinstance(user_output, list) else str(user_output)
            expected_output_str = ', '.join(str(item) for item in expected_output) if isinstance(expected_output, list) else str(expected_output)

            if user_output_str == expected_output_str:
                return f"Correct! Output: {user_output_str}, Expected: {expected_output_str}"
            else:
                return f"Incorrect. Output: {user_output_str}, Expected: {expected_output_str}"

        elif language == 'java':
            java_output = compile_and_run_java(user_code, input_data)
            if java_output == str(expected_output):
                return f"Correct! Output: {java_output}, Expected: {expected_output}"
            else:
                return f"Incorrect. Output: {java_output}, Expected: {expected_output}"

        elif language == 'csharp':
            data = {"code": user_code, "id": str(problem_id), "expectedOutput": expected_output, "input": input_data}
            url = "https://localhost:7270/Code/Recieve"
            response = requests.post(url, json=data, verify=False)
            
            if response.status_code == 200:
                result = response.json()
                print(result)
                validate = result["validate"]
                output = result["output_csharp"]
                if validate == True:
                    return f"Correct! Output: {output}, Expected: {expected_output}"
                else:
                    return f"Incorrect. Output: {output}, Expected: {expected_output}"
            else:
                return f"Error de conexion"

    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/problems')
def problem_list():
    return render_template('problem_list.html', problems=problems_db)

@app.route('/problems/<int:problem_id>', methods=['GET', 'POST'])
@login_required
def problem_detail(problem_id):
    problem = problems_db.get(problem_id)
    if not problem:
        return "Problem not found", 404

    if request.method == 'POST':
        code = request.form.get('code')
        language = request.form.get('language')

        #save solution in the data base, asociate with the local user
        solution = Solution(problem_id=problem_id, language=language, code=code, user_id=current_user.id)
        db.session.add(solution)
        db.session.commit()

        save_solution(problem_id, code, language)

        validation_result = validate_solution(code, problem_id, language)
        if "Error" in validation_result:
            return validation_result
        if problem_id == 1:
            test_input = random_array_and_number()
        elif problem_id in [2, 6, 7, 9]:
            test_input = random_string()
        elif problem_id in [4, 8]:
            test_input = random_number()
        elif problem_id == 10:
            print("entro")
            test_input = random_number_fibonacci()
        elif problem_id == 5:
            test_input = random_float()
        else:
            test_input = ast.literal_eval(problem['test_input'])

        result = test_solution(code, test_input, problem_id, language)
        return redirect(url_for('submission_result', problem_id=problem_id, result=result))

    language = request.args.get('language', 'python', 'csharp')
    saved_solution = load_solution(problem_id, language)
    return render_template('problem_detail.html', problem=problem, saved_code=saved_solution)

@app.route('/profile')
@login_required
def profile():
    user_solutions = Solution.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', solutions=user_solutions, username=current_user.username)


@app.route('/problem_detail/<int:problem_id>', methods=['POST'])
def test_code(problem_id):
    problem = problems_db.get(problem_id)
    try:
        
        data = request.get_json()

        code = data.get('code')
        language = data.get('language')

        validation_result = validate_solution(code, problem_id, language)
        if "Error" in validation_result:
            print("Validation error:", validation_result)
            return jsonify({'result': validation_result, 'status': 'error'}), 400

        if problem_id == 1:
            test_input = random_array_and_number()
        elif problem_id in [2, 6, 7, 9]:
            test_input = random_string()
        elif problem_id in [4, 8]:
            test_input = random_number()
        elif problem_id == 10:
            print("entro")
            test_input = random_number_fibonacci()
        elif problem_id == 5:
            test_input = random_float()
        else:
            test_input = ast.literal_eval(problem['test_input'])

        result = test_solution(code, test_input, problem_id, language)

        status = 'success' if "Correct" in result or "Passed" in result else 'error'
        
        save_presubmit_response(problem, code, language)

        return jsonify({'result': result, 'status': status}), 200 if status == 'success' else 400

    except Exception as e:
        error_message = str(e) or "An unknown error occurred"
        print(f"Server error: {error_message}")
        return jsonify({'result': f"Server error: {error_message}", 'status': 'error'}), 500



@app.route('/submission_result/<int:problem_id>')
def submission_result(problem_id):
    problem = problems_db.get(problem_id)
    result = request.args.get('result', 'No result')
    return render_template('submission_result.html', problem=problem, result=result)
    
if __name__ == '__main__':
    with app.app_context(): #app context
        db.create_all() 
    app.run(debug=True)
