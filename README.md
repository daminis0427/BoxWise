# 📦 BoxWise – Smart Packaging & Cost Optimization

**BoxWise** is a Python and Django-based web application designed to recommend suitable shipping boxes for ecommerce orders. It helps warehouse teams select cost-effective packaging based on product dimensions, product weight, box dimensions, maximum weight capacity, and shipping box cost.

The system uses a 3D packing heuristic to check whether products can fit inside available shipping boxes and recommends the cheapest suitable option.

---

## 🚀 Project Overview

In ecommerce businesses, selecting the correct shipping box is important for reducing packaging costs and improving warehouse efficiency.

Choosing an unnecessarily large or expensive box can increase shipping expenses. BoxWise helps solve this problem by analyzing order products and available shipping boxes before recommending a suitable packaging option.

The application also provides cost comparisons, potential savings calculations, packing analysis, and an interactive 3D visualization of product placement.

## ✨ Features

- **Product Management:** Store product names, dimensions, and weights.
- **Shipping Box Management:** Maintain box dimensions, maximum weight capacity, and cost.
- **Order Management:** Manage orders containing multiple products and quantities.
- **Automatic Box Selection:** Find suitable shipping boxes for an order.
- **3D Packing Algorithm:** Check product placement using a greedy 3D packing heuristic.
- **Cost Optimization:** Recommend the cheapest suitable shipping box.
- **Cost Comparison:** Compare suitable boxes and calculate potential savings.
- **Packing Analysis:** Calculate total product weight, product volume, box volume, unused volume, and space utilization.
- **3D Visualization:** Display products inside the recommended shipping box.
- **Product Legend:** Display product names, dimensions, and corresponding colors.
- **Django Admin:** Manage application data through the Django administration interface.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web application framework |
| SQLite | Database |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Interactive functionality |
| Three.js | 3D box and product visualization |
| Git & GitHub | Version control and project hosting |

## 📂 Project Structure

```text
BoxWise/
│
├── boxes/
│   ├── migrations/
│   ├── templates/
│   │   └── boxes/
│   │       ├── home.html
│   │       └── recommendation.html
│   │
│   ├── static/
│   │   └── boxes/
│   │       └── style.css
│   │
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   ├── urls.py
│   └── admin.py
│
├── config/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── AI_USAGE.md
├── TEST_CASES.md
└── TEST_OUTPUT.md
```

*Note: The structure above is illustrative. Adjust it to match your actual repository files.*

## ⚙️ Installation and Setup

Follow these steps to run BoxWise locally.

### 1. Clone the Repository

```bash
git clone https://github.com/daminis0427/BoxWise.git
```

### 2. Navigate to the Project Directory

```bash
cd BoxWise
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the instructions to create your administrator account.

### 8. Run the Development Server

```bash
python manage.py runserver
```

### 9. Open the Application

Visit:

```text
http://127.0.0.1:8000/
```

To access the Django administration panel:

```text
http://127.0.0.1:8000/admin/
```

## 🧠 How Box Selection Works

BoxWise follows these general steps:

1. Retrieve the products and quantities associated with an order.
2. Calculate the total weight of the order.
3. Identify shipping boxes that satisfy the maximum weight requirement.
4. Sort the products by volume, placing larger products first.
5. Try different product orientations to find a suitable placement.
6. Check whether each product fits into an available space inside a candidate box.
7. Divide the remaining space after placing each product.
8. Reject a box if the packing algorithm cannot place every product.
9. Compare the suitable boxes by cost.
10. Recommend the cheapest suitable box.

### Box Recommendation

The application recommends the lowest-cost box among the boxes accepted by the packing algorithm.

### Cost Optimization

The application compares the cheapest and most expensive suitable boxes.

**Potential Savings:**

```text
Potential Savings = Most Expensive Suitable Box Cost
                    - Cheapest Suitable Box Cost
```

**Savings Percentage:**

```text
Savings Percentage = (Potential Savings
                      / Most Expensive Suitable Box Cost) × 100
```

The savings represent a comparison between suitable box options, not necessarily a guaranteed saving on every actual shipment.

## 📊 Packing Analysis

BoxWise calculates the following information:

- Total order weight.
- Total product volume.
- Recommended box volume.
- Unused box volume.
- Space utilization percentage.

**Space Utilization:**

```text
Space Utilization = (Total Product Volume
                     / Box Volume) × 100
```

These calculations provide an overview of how efficiently the recommended box uses its available volume.

## 📦 3D Visualization

BoxWise uses Three.js to display an interactive 3D representation of the recommended shipping box and the products placed inside it.

Visualization features include:

- 3D shipping box representation.
- Individual colored product blocks.
- Product placement based on calculated coordinates.
- Product dimensions and color legend.
- Mouse drag to rotate the view.
- Scroll to zoom in and out.

**Note:** The 3D visualization depends on the Three.js library loaded through a CDN, so an internet connection is required for that resource.

## 🗄️ Database Models

The application uses Django models to organize its data.

### Product

Stores product information:

- Product name.
- Length.
- Width.
- Height.
- Weight.

### ShippingBox

Stores shipping box information:

- Box name.
- Length.
- Width.
- Height.
- Maximum weight capacity.
- Box cost.

### Order

Stores order creation information and maintains its relationship with products through the OrderItem model.

### OrderItem

Connects products with orders and stores the quantity of each product in an order.

## 🧪 Testing

Run Django's system checks:

```bash
python manage.py check
```

Run the project's automated tests:

```bash
python manage.py test
```

Test scenarios should include:

- An order that fits into an available box.
- A product that exceeds the available box dimensions.
- An order that exceeds the box weight capacity.
- An order containing multiple products.
- An order containing multiple quantities of the same product.
- Cost comparison between suitable boxes.
- An order for which no suitable box exists.

Actual test cases and execution results are documented separately in `TEST_CASES.md` and `TEST_OUTPUT.md`.

## ⚠️ Current Limitations

- The packing algorithm uses a greedy heuristic and does not guarantee an optimal packing arrangement.
- The algorithm may reject a box even when a different packing arrangement could fit all products.
- Packing calculations assume consistent units for all product and box dimensions.
- Space utilization is based on volume and does not guarantee that all unused space is physically accessible or usable.
- The current application is intended as a prototype and would need further validation before use in a production warehouse.

## 🔮 Future Enhancements

- Improve the 3D packing algorithm.
- Support more advanced packing strategies.
- Add shipment tracking integration.
- Generate downloadable packaging reports.
- Add order history and analytics.
- Support multiple packaging recommendations.
- Improve automated test coverage.
- Add authentication and role-based access for warehouse users.

## 👩‍💻 Author

**Damini Sonawane**

GitHub: [@daminis0427](https://github.com/daminis0427)

Project Repository: [BoxWise](https://github.com/daminis0427/BoxWise)

## 📄 License

This project was developed as a Python/Django hiring assignment. No open-source license has been specified yet.

---

**BoxWise – Smart Packaging & Cost Optimization**

*Smarter Box Selection. Better Cost Optimization.*
