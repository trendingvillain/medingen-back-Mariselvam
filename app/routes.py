from flask import Blueprint, request, jsonify
from .models import db, Medicine, GenericAlternative, ComparisonProduct, Review, FAQ

api = Blueprint('api', __name__)

# ✅ Get All Medicines (with optional search)
@api.route('/medicines', methods=['GET'])
def get_all_medicines():
    search_query = request.args.get('search')
    if search_query:
        medicines = Medicine.query.filter(Medicine.name.ilike(f'%{search_query}%')).all()
    else:
        medicines = Medicine.query.all()

    result = []
    for med in medicines:
        result.append({
            'id': med.id,
            'name': med.name,
            'strength': med.strength,
            'description': med.description,
            'dosage': med.dosage,
            'uses': med.uses,
            'side_effects': med.side_effects
        })
    return jsonify(result)

# ✅ Get Medicine Details by ID
@api.route('/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine_details(medicine_id):
    med = Medicine.query.get_or_404(medicine_id)
    return jsonify({
        'id': med.id,
        'name': med.name,
        'strength': med.strength,
        'description': med.description,
        'dosage': med.dosage,
        'uses': med.uses,
        'side_effects': med.side_effects,
        'generics': [ {
            'name': g.name,
            'manufacturer': g.manufacturer,
            'price': str(g.price),
            'discount_percent': g.discount_percent,
            'image_url': g.image_url
        } for g in med.generics ],
        'comparisons': [ {
            'name': c.name,
            'manufacturer': c.manufacturer,
            'generic_name': c.generic_name,
            'average_price': str(c.average_price),
            'discounted_price': str(c.discounted_price),
            'chemical_formula': c.chemical_formula,
            'rating': c.rating,
            'image_url': c.image_url
        } for c in med.comparisons ],
        'reviews': [ {
            'rating': r.rating,
            'comment': r.comment
        } for r in med.reviews ],
        'faqs': [ {
            'question': f.question,
            'answer': f.answer
        } for f in med.faqs ]
    })

# ✅ Compare Medicines by IDs
@api.route('/medicines/compare', methods=['POST'])
def compare_medicines():
    data = request.get_json()
    ids = data.get('medicine_ids', [])
    if not ids:
        return jsonify({"error": "No medicine IDs provided"}), 400

    medicines = Medicine.query.filter(Medicine.id.in_(ids)).all()
    result = []
    for med in medicines:
        result.append({
            'id': med.id,
            'name': med.name,
            'strength': med.strength,
            'uses': med.uses,
            'side_effects': med.side_effects
        })
    return jsonify({"comparison": result})

# ✅ Add New Medicine
@api.route('/medicines', methods=['POST'])
def add_medicine():
    data = request.get_json()
    med = Medicine(
        name=data['name'],
        strength=data['strength'],
        description=data['description'],
        dosage=data['dosage'],
        uses=data['uses'],
        side_effects=data['side_effects']
    )
    db.session.add(med)
    db.session.commit()
    return jsonify({"message": "Medicine added successfully", "id": med.id}), 201

# ✅ Update Medicine
@api.route('/medicines/<int:medicine_id>', methods=['PUT'])
def update_medicine(medicine_id):
    med = Medicine.query.get_or_404(medicine_id)
    data = request.get_json()

    med.name = data.get('name', med.name)
    med.strength = data.get('strength', med.strength)
    med.description = data.get('description', med.description)
    med.dosage = data.get('dosage', med.dosage)
    med.uses = data.get('uses', med.uses)
    med.side_effects = data.get('side_effects', med.side_effects)

    db.session.commit()
    return jsonify({"message": "Medicine updated successfully"})

# ✅ Delete Medicine
@api.route('/medicines/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(medicine_id):
    med = Medicine.query.get_or_404(medicine_id)
    db.session.delete(med)
    db.session.commit()
    return jsonify({"message": "Medicine deleted successfully"})

# ✅ Add Generic Alternative
@api.route('/generics', methods=['POST'])
def add_generic():
    data = request.get_json()
    generic = GenericAlternative(
        medicine_id=data['medicine_id'],
        name=data['name'],
        manufacturer=data['manufacturer'],
        price=data['price'],
        discount_percent=data['discount_percent'],
        image_url=data['image_url']
    )
    db.session.add(generic)
    db.session.commit()
    return jsonify({"message": "Generic alternative added successfully", "id": generic.id}), 201

# ✅ Add Comparison Product
@api.route('/comparisons', methods=['POST'])
def add_comparison():
    data = request.get_json()
    comp = ComparisonProduct(
        medicine_id=data['medicine_id'],
        name=data['name'],
        manufacturer=data['manufacturer'],
        generic_name=data['generic_name'],
        average_price=data['average_price'],
        discounted_price=data['discounted_price'],
        chemical_formula=data['chemical_formula'],
        rating=data['rating'],
        image_url=data['image_url']
    )
    db.session.add(comp)
    db.session.commit()
    return jsonify({"message": "Comparison product added successfully", "id": comp.id}), 201

# ✅ Add Review
@api.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    review = Review(
        medicine_id=data['medicine_id'],
        rating=data['rating'],
        comment=data['comment']
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review added successfully", "id": review.id}), 201

# ✅ Add FAQ
@api.route('/faqs', methods=['POST'])
def add_faq():
    data = request.get_json()
    faq = FAQ(
        medicine_id=data['medicine_id'],
        question=data['question'],
        answer=data['answer']
    )
    db.session.add(faq)
    db.session.commit()
    return jsonify({"message": "FAQ added successfully", "id": faq.id}), 201
