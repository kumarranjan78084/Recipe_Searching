from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the recipe data from CSV
data = pd.read_csv('recipes.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    search_type = request.form.get('search_type')
    sort_by = request.form.get('sort_by')
    
    # Perform search based on selected search type
    if search_type == 'recipe_name':
        results = search_by_name(query)
    else:
        results = search_by_ingredients(query)
    
    # Sort results if a sort option is selected
    if sort_by:
        results = results.sort_values(by=sort_by)

    # Count the number of results
    total_results = len(results)

    # Render results page with the found recipes and total count
    return render_template('results.html', search_query=query, results=results.to_dict(orient='records'), total_results=total_results)

def search_by_name(recipe_name):
    # Split query by spaces to search for each keyword independently
    keywords = recipe_name.lower().split()
    return data[data['TranslatedRecipeName'].apply(
        lambda name: all(keyword in name.lower() for keyword in keywords) if isinstance(name, str) else False
    )]

def search_by_ingredients(ingredients):
    ingredients_list = [ingredient.strip().lower() for ingredient in ingredients.split(',')]
    return data[data['Cleaned-Ingredients'].apply(
        lambda ing: all(item in ing.lower() for item in ingredients_list)
    )]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

