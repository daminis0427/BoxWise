
from django.shortcuts import get_object_or_404, render

from .models import Order
from .services import (
    recommend_box,
    get_cost_savings,
    pack_products,
)


def home(request):
    orders = Order.objects.all().order_by("-created_at")

    return render(
        request,
        "boxes/home.html",
        {"orders": orders},
    )


def order_recommendation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Get order products.
    order_items = list(
        order.orderitem_set.select_related("product")
    )

    # Find recommended box.
    recommended_box = recommend_box(order)

    # Calculate cost optimization.
    cost_analysis = get_cost_savings(
        order,
        recommended_box,
    )

    # Calculate actual product placements for 3D visualization.
    placements = (
        pack_products(order_items, recommended_box)
        if recommended_box
        else []
    )

    # Calculate total product weight.
    total_weight = sum(
        item.product.weight * item.quantity
        for item in order_items
    )

    # Calculate total product volume.
    total_product_volume = sum(
        item.product.length
        * item.product.width
        * item.product.height
        * item.quantity
        for item in order_items
    )

    # Calculate selected box volume.
    if recommended_box:
        box_volume = (
            recommended_box.length
            * recommended_box.width
            * recommended_box.height
        )

        unused_volume = max(
            box_volume - total_product_volume,
            0,
        )

        utilization = (
            (total_product_volume / box_volume) * 100
            if box_volume > 0
            else 0
        )

        utilization = round(utilization, 2)

    else:
        box_volume = 0
        unused_volume = 0
        utilization = 0

    context = {
        "order": order,
        "recommended_box": recommended_box,

        # Cost optimization.
        **cost_analysis,

        # Packing analysis.
        "total_weight": total_weight,
        "total_product_volume": total_product_volume,
        "box_volume": box_volume,
        "unused_volume": unused_volume,
        "utilization": utilization,

        # 3D visualization.
        "placements": placements,
    }

    return render(
        request,
        "boxes/recommendation.html",
        context,
    )
