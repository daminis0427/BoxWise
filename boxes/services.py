
from itertools import permutations

from .models import ShippingBox


# Colors used in the 3D visualization and product legend
PRODUCT_COLORS = [
    "#60a5fa",
    "#34d399",
    "#fbbf24",
    "#f472b6",
    "#a78bfa",
    "#fb923c",
]


def get_orientations(product):
    """
    Return all possible orientations of a product.
    This allows products to rotate inside the shipping box.
    """
    dimensions = (
        product.length,
        product.width,
        product.height,
    )

    return set(permutations(dimensions))


def fits_in_space(item_dimensions, space_dimensions):
    """
    Check whether a product fits inside an available space.
    """
    return all(
        item_dimensions[i] <= space_dimensions[i]
        for i in range(3)
    )


def pack_products(order_items, box):
    """
    Pack products using a greedy 3D packing heuristic.

    Returns:
        A list of product placements containing:
        - Product name
        - Product dimensions
        - X, Y, Z positions
        - Product color

        Returns None if all products cannot be packed.
    """

    if not box:
        return None

    items = []

    # Expand quantities into individual products
    for order_item in order_items:
        for _ in range(order_item.quantity):
            items.append(order_item.product)

    if not items:
        return []

    # Sort products by volume (largest first)
    items.sort(
        key=lambda product: (
            product.length
            * product.width
            * product.height
        ),
        reverse=True,
    )

    # Initial available space inside the box
    spaces = [
        {
            "dimensions": (
                box.length,
                box.width,
                box.height,
            ),
            "position": (0, 0, 0),
        }
    ]

    placements = []

    # Place each product inside an available space
    for product in items:

        placed = False

        for index, space in enumerate(spaces):

            space_dimensions = space["dimensions"]

            space_x, space_y, space_z = space["position"]

            # Try every possible product orientation
            for orientation in get_orientations(product):

                if not fits_in_space(
                    orientation,
                    space_dimensions,
                ):
                    continue

                length, width, height = orientation

                old_length, old_width, old_height = space_dimensions

                # Assign a color to this physical product
                product_color = PRODUCT_COLORS[
                    len(placements) % len(PRODUCT_COLORS)
                ]

                # Save product placement information
                placements.append({
                    "name": product.name,
                    "length": length,
                    "width": width,
                    "height": height,
                    "x": space_x,
                    "y": space_y,
                    "z": space_z,
                    "color": product_color,
                })

                # Remove the occupied space
                spaces.pop(index)

                # Divide the remaining space into smaller spaces
                remaining_spaces = [
                    {
                        "dimensions": (
                            old_length - length,
                            old_width,
                            old_height,
                        ),
                        "position": (
                            space_x + length,
                            space_y,
                            space_z,
                        ),
                    },
                    {
                        "dimensions": (
                            length,
                            old_width - width,
                            old_height,
                        ),
                        "position": (
                            space_x,
                            space_y + width,
                            space_z,
                        ),
                    },
                    {
                        "dimensions": (
                            length,
                            width,
                            old_height - height,
                        ),
                        "position": (
                            space_x,
                            space_y,
                            space_z + height,
                        ),
                    },
                ]

                # Keep only valid remaining spaces
                spaces.extend(
                    remaining
                    for remaining in remaining_spaces
                    if all(
                        dimension > 0
                        for dimension in remaining["dimensions"]
                    )
                )

                placed = True
                break

            if placed:
                break

        # If a product cannot fit, packing fails
        if not placed:
            return None

    return placements


def get_suitable_boxes(order):
    """
    Find all shipping boxes that can hold the order
    according to the packing heuristic and weight limit.
    """

    order_items = list(
        order.orderitem_set.select_related("product")
    )

    if not order_items:
        return []

    # Calculate total order weight
    total_weight = sum(
        item.product.weight * item.quantity
        for item in order_items
    )

    # Check boxes that support the total weight
    candidate_boxes = ShippingBox.objects.filter(
        max_weight__gte=total_weight
    ).order_by("cost", "id")

    suitable_boxes = []

    for box in candidate_boxes:

        placements = pack_products(order_items, box)

        if placements is not None:
            suitable_boxes.append(box)

    return suitable_boxes


def recommend_box(order):
    """
    Recommend the cheapest suitable shipping box.
    """

    suitable_boxes = get_suitable_boxes(order)

    if not suitable_boxes:
        return None

    return suitable_boxes[0]


def get_cost_savings(order, recommended_box=None):
    """
    Calculate potential cost savings by comparing
    the cheapest and most expensive suitable boxes.
    """

    suitable_boxes = get_suitable_boxes(order)

    if not suitable_boxes:
        return {
            "suitable_boxes": [],
            "most_expensive_cost": None,
            "potential_savings": None,
            "savings_percentage": None,
        }

    # The first box is the cheapest because boxes
    # are ordered by cost in get_suitable_boxes()
    recommended_box = suitable_boxes[0]

    # Find the most expensive suitable box
    most_expensive_box = max(
        suitable_boxes,
        key=lambda box: (box.cost, box.id),
    )

    recommended_cost = recommended_box.cost

    most_expensive_cost = most_expensive_box.cost

    # Calculate potential savings
    potential_savings = max(
        most_expensive_cost - recommended_cost,
        0,
    )

    # Calculate savings percentage
    savings_percentage = (
        potential_savings / most_expensive_cost * 100
        if most_expensive_cost > 0
        else 0
    )

    return {
        "suitable_boxes": suitable_boxes,
        "most_expensive_cost": most_expensive_cost,
        "potential_savings": round(
            potential_savings, 2
        ),
        "savings_percentage": round(
            savings_percentage, 2
        ),
    }
