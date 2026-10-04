# fix_templates.py — run with: python fix_templates.py
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'velora_project.settings')

import django
django.setup()

from django.conf import settings

# Use Django's OWN resolved template directory — not a guessed path.
# This is the exact same value the template loader checks internally,
# so there is no possibility of a mismatch.
template_root = str(settings.TEMPLATES[0]['DIRS'][0])
target_dir = os.path.join(template_root, 'dashboard', 'products')
print('Django template root is:', template_root)
print('Writing files to:', target_dir)

os.makedirs(target_dir, exist_ok=True)

FILES = {
    'list.html': '''{% extends "base.html" %}
{% block title %}Products{% endblock %}
{% block content %}
<div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <h1>Products</h1>
        <a class="btn" href="{% url 'dashboard:create_product' %}">+ Add Product</a>
    </div>
</div>

<div class="card">
    {% if products %}
        <table>
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Stock</th>
                    <th>Category</th>
                    <th>Featured</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
            {% for product in products %}
                <tr>
                    <td>{{ product.name }}<br><span class="muted">{{ product.sku }}</span></td>
                    <td>
                        {% if product.discount_price %}
                            <span style="text-decoration:line-through;color:#999;">${{ product.price }}</span>
                            <strong>${{ product.discount_price }}</strong>
                        {% else %}
                            ${{ product.price }}
                        {% endif %}
                    </td>
                    <td>
                        {% if product.stock == 0 %}
                            <span class="badge badge-danger">Out of stock</span>
                        {% elif product.is_low_stock %}
                            <span class="badge badge-warning">{{ product.stock }}</span>
                        {% else %}
                            {{ product.stock }}
                        {% endif %}
                    </td>
                    <td>{{ product.category.name }}</td>
                    <td>{% if product.is_featured %}YES{% else %}-{% endif %}</td>
                    <td>
                        <a href="{% url 'dashboard:edit_product' product.slug %}">Edit</a>
                        &middot;
                        <a href="{% url 'dashboard:delete_product' product.slug %}">Delete</a>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p class="muted">No products yet.</p>
    {% endif %}
</div>
{% endblock %}
''',

    'form.html': '''{% extends "base.html" %}
{% block title %}{{ title }}{% endblock %}
{% block content %}
<div class="card">
    <h1>{{ title }}</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn">
            {% if product %}Update Product{% else %}Add Product{% endif %}
        </button>
        <a class="btn secondary" href="{% url 'dashboard:manage_products' %}">Cancel</a>
    </form>
</div>
{% endblock %}
''',

    'confirm_delete.html': '''{% extends "base.html" %}
{% block title %}Delete Product{% endblock %}
{% block content %}
<div class="card">
    <h1>Delete this product?</h1>
    <p>Are you sure you want to delete <strong>{{ product.name }}</strong> ({{ product.sku }})? This cannot be undone.</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn danger">Yes, Delete</button>
        <a class="btn secondary" href="{% url 'dashboard:manage_products' %}">Cancel</a>
    </form>
</div>
{% endblock %}
''',
}

for filename, content in FILES.items():
    filepath = os.path.join(target_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{filename}: exists={os.path.exists(filepath)}  size={os.path.getsize(filepath)} bytes')

print()
print('--- Now proving Django can actually load it ---')
from django.template.loader import get_template
try:
    tpl = get_template('dashboard/products/form.html')
    print('SUCCESS — Django found and loaded the template from:', tpl.origin.name)
except Exception as e:
    print('STILL FAILING:', e)